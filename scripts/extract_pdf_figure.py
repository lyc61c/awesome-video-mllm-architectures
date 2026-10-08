"""Inspect a primary PDF, then crop an explicitly reviewed page rectangle.

The page number is one-based; clip coordinates use PDF points. Without --clip,
the script renders a full page for review. Downloads remain in ignored .cache.
"""

import argparse
import hashlib
from pathlib import Path

import fitz
import requests

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--page", type=int)
    parser.add_argument("--clip", type=float, nargs=4)
    parser.add_argument("--find", help="Print pages and bounding boxes containing this text.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cache = ROOT / ".cache/papers"
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / (hashlib.sha256(args.url.encode()).hexdigest()[:16] + ".pdf")
    if not path.exists():
        response = requests.get(args.url, timeout=120)
        response.raise_for_status()
        path.write_bytes(response.content)
    document = fitz.open(path)
    if args.find:
        for index, page in enumerate(document):
            matches = page.search_for(args.find)
            if matches:
                print({"page": index + 1, "matches": [list(rect) for rect in matches], "page_size": list(page.rect)})
    if args.page:
        if not args.output:
            parser.error("--output is required with --page")
        page = document[args.page - 1]
        rectangle = fitz.Rect(args.clip) if args.clip else page.rect
        if not page.rect.contains(rectangle):
            parser.error("Crop rectangle must stay within the selected page.")
        page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rectangle, alpha=False).save(args.output)
        print(f"Rendered page {args.page} to {args.output}")


if __name__ == "__main__":
    main()
