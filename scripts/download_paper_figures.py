"""Download explicitly selected figures from primary arXiv HTML pages.

Usage: python scripts/download_paper_figures.py --evidence evidence.json
       --selection selection.json --output data/downloaded-figures.json
Evidence records contain id, url, and figures (id, caption, images).
Selection maps catalog IDs to verified figure numbers. No automatic guessing.
"""

import argparse
import concurrent.futures
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    selection = json.loads(args.selection.read_text(encoding="utf-8"))
    directory = ROOT / "assets/architectures"
    directory.mkdir(parents=True, exist_ok=True)

    def download(record):
        figure_number = str(selection[str(record["id"])])
        figure = next((item for item in record["figures"] if re.match(rf"Figure\s+{figure_number}\s*:", item["caption"])), None)
        if figure is None:
            raise ValueError(f"{record['id']}: selected figure {figure_number} not found")
        source_url = record["url"] + "#" + figure["id"]
        image_sources = figure["images"]
        if image_sources:
            images = []
            for index, source in enumerate(image_sources):
                url = urljoin("https://arxiv.org/html/", source)
                response = requests.get(url, timeout=90)
                response.raise_for_status()
                filename = f"{record['id']:02d}-paper" + (f"-{index}" if len(image_sources) > 1 else "")
                if "svg" in response.headers.get("Content-Type", "") or response.content.lstrip().startswith(b"<svg"):
                    path = directory / (filename + ".svg")
                    path.write_bytes(response.content)
                else:
                    path = directory / (filename + ".png")
                    path.write_bytes(response.content)
                    image = Image.open(path)
                    image.verify()
                    if Image.open(path).format != "PNG":
                        Image.open(path).save(path, format="PNG")
                    images.append(path)
            if len(images) > 1:
                opened = [Image.open(path).convert("RGB") for path in images]
                merged = Image.new("RGB", (max(image.width for image in opened), sum(image.height for image in opened)), "white")
                y = 0
                for image in opened:
                    merged.paste(image, (0, y))
                    y += image.height
                path = directory / f"{record['id']:02d}-paper.png"
                merged.save(path)
        else:
            response = requests.get(record["url"], timeout=90)
            response.raise_for_status()
            selected = re.search(r'<figure\b[^>]*\bid="' + re.escape(figure["id"]) + r'"[^>]*>(.*?)</figure>', response.text, re.S)
            svg = re.search(r"<svg\b.*?</svg>", selected.group(1), re.S) if selected else None
            if svg is None:
                raise ValueError(f"{record['id']}: no image or inline SVG; PDF extraction required")
            path = directory / f"{record['id']:02d}-paper.svg"
            markup = svg.group(0)
            if "xmlns=" not in markup.split(">", 1)[0]:
                markup = markup.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
            path.write_text(markup, encoding="utf-8")
        return {
            "id": record["id"], "kind": "paper_figure", "file": path.relative_to(ROOT).as_posix(),
            "source_url": source_url, "image_source_urls": [urljoin("https://arxiv.org/html/", source) for source in image_sources],
            "figure_number": figure_number, "pdf_page": None,
            "caption_excerpt": " ".join(figure["caption"].split()[:25]), "verification": "pending_visual_review",
        }

    records = [record for record in evidence if str(record["id"]) in selection]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for record, future in [(record, pool.submit(download, record)) for record in records]:
            try:
                result = future.result()
                results.append(result)
                print(f"OK {result['id']}: {result['file']}")
            except Exception as error:
                print(f"FAILED {record['id']}: {error}")
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
