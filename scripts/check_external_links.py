"""Read-only URL audit. Reports transient failures; it does not rewrite sources."""

import argparse
import concurrent.futures
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(".cache/link-audit.json"))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    catalog = json.loads((ROOT / "data/architectures.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "assets/architectures/manifest.json").read_text(encoding="utf-8"))
    urls = set()
    for entry in catalog["entries"]:
        for item in entry["technical_sources"] + entry["official_entries"] + entry["primary_sources"]:
            urls.add((item["url"] if isinstance(item, dict) else item).split("#")[0])
    for figure in manifest["figures"]:
        urls.add(figure["source_url"].split("#")[0])

    def check(url):
        for attempt in range(2):
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "AwesomeVideoMLLMArchitectures/0.1 (link audit)"})
                with urllib.request.urlopen(request, timeout=25) as response:
                    response.read(256)
                    return {"url": url, "status": response.status, "resolved_url": response.url, "ok": True}
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                if attempt == 0:
                    time.sleep(1)
                else:
                    return {"url": url, "status": getattr(error, "code", None), "ok": False, "error": str(error)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(check, sorted(urls)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"checked": len(results), "failures": sum(not result["ok"] for result in results), "results": results}, indent=2) + "\n", encoding="utf-8")
    failures = [result for result in results if not result["ok"]]
    print(json.dumps({"checked": len(results), "failures": len(failures), "report": str(args.output)}))
    for item in failures:
        print(json.dumps(item))


if __name__ == "__main__":
    main()
