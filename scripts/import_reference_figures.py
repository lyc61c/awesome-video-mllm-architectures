"""Import attributed paper crops from the reference repository.

This is an optional, networked maintenance tool. It never copies README prose.
The repository's original-paper figure notice applies to the downloaded crops.
"""

import concurrent.futures
import json
import re
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raw.githubusercontent.com/gokayfem/awesome-vlm-architectures/main/assets/architectures/"


def arxiv_id(url):
    match = re.search(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})", url)
    return match.group(1) if match else None


def main():
    cache = ROOT / ".cache"
    cache.mkdir(exist_ok=True)
    response = requests.get(BASE + "manifest.json", timeout=60)
    response.raise_for_status()
    reference = response.json()
    (cache / "reference-manifest.json").write_text(json.dumps(reference, indent=2), encoding="utf-8")
    figures = reference["figures"]
    catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))["entries"]
    target = ROOT / "assets/architectures"
    target.mkdir(parents=True, exist_ok=True)
    tasks = []
    for entry in catalog:
        source_ids = {arxiv_id(source["url"]) for source in entry["technical_sources"]}
        source_ids.discard(None)
        matches = [figure for figure in figures if figure.get("arxiv_id") in source_ids and figure.get("file")]
        if not matches:
            continue
        # Prefer the exact model title when multiple cards share one report.
        matches.sort(key=lambda fig: entry["name"].lower() not in fig["title"].lower())
        tasks.append((entry, matches[0]))

    def download(task):
        entry, figure = task
        filename = f"{entry['id']:02d}-paper.png"
        data = requests.get(BASE + figure["file"], timeout=90)
        data.raise_for_status()
        (target / filename).write_bytes(data.content)
        return {
            "id": entry["id"], "kind": "paper_crop", "file": "assets/architectures/" + filename,
            "source_url": figure["source_url"], "figure_number": figure.get("figure"),
            "pdf_page": figure.get("pdf_page"), "caption": figure.get("paper_caption", figure.get("display_caption", "")),
            "alt": figure.get("alt", "Architecture diagram from the original report."),
            "extraction_source": "https://github.com/gokayfem/awesome-vlm-architectures/blob/main/assets/architectures/" + figure["file"],
            "reference_title": figure["title"], "verification": "pending_visual_review",
        }

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(download, task) for task in tasks]
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except requests.RequestException as error:
                print(f"Download failed: {error}")
    results.sort(key=lambda item: item["id"])
    (ROOT / "data/reference-figures.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps([{key: row.get(key) for key in ["id", "reference_title", "figure_number", "pdf_page"]} for row in results], ensure_ascii=False))


if __name__ == "__main__":
    main()
