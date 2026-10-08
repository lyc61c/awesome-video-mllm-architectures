"""Build original, explicitly labeled SVG schematics from reviewed flow specs."""

import argparse
import html
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def draw(spec):
    colors = ["#e7edf6", "#dceff1", "#ede6fb", "#ffe8d4", "#e6f1df"]
    title = html.escape(spec["title"])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">',
             f"<title id=\"title\">{title}</title>",
             f'<desc id="desc">Editorial schematic. {html.escape(spec["simplification"])}</desc>',
             '<rect width="1200" height="360" rx="18" fill="#f8fafc"/>',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#52677d"/></marker></defs>',
             f'<text x="36" y="55" fill="#142c42" font-family="Arial,sans-serif" font-size="32" font-weight="700">{title}</text>',
             '<text x="36" y="85" fill="#52677d" font-family="Arial,sans-serif" font-size="17">EDITORIAL SCHEMATIC · based on the cited primary source</text>']
    for index, label in enumerate(spec["nodes"]):
        x = 36 + index * 229
        parts.append(f'<rect x="{x}" y="136" width="210" height="108" rx="12" fill="{colors[index]}" stroke="#bdcad8"/>')
        lines = textwrap.wrap(label, width=18, break_long_words=False)
        for line_index, line in enumerate(lines):
            y = 191 - (len(lines) - 1) * 13 + line_index * 26
            parts.append(f'<text x="{x+105}" y="{y}" text-anchor="middle" fill="#142c42" font-family="Arial,sans-serif" font-size="20">{html.escape(line)}</text>')
        if index < 4:
            parts.extend([f'<path d="M {x+211} 190 H {x+224}" stroke="#52677d" stroke-width="2"/>',
                          f'<path d="M {x+220} 186 L {x+227} 190 L {x+220} 194 Z" fill="#52677d"/>'])
    if spec.get("side_input"):
        side = spec["side_input"]
        center = 36 + side["target_index"] * 229 + 105
        parts.extend([f'<rect x="{center-80}" y="94" width="160" height="28" rx="6" fill="#e7edf6" stroke="#bdcad8"/>',
                      f'<text x="{center}" y="114" text-anchor="middle" fill="#142c42" font-family="Arial,sans-serif" font-size="17">{html.escape(side["label"])}</text>',
                      f'<path d="M {center} 122 V 131" stroke="#52677d" stroke-width="2"/>',
                      f'<path d="M {center-4} 128 L {center} 134 L {center+4} 128 Z" fill="#52677d"/>'])
    for index, line in enumerate(textwrap.wrap(spec["note"], width=104)):
        parts.append(f'<text x="36" y="{280+index*25}" fill="#334b60" font-family="Arial,sans-serif" font-size="20">{html.escape(line)}</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    specs = json.loads((ROOT / "data/editorial-diagrams.json").read_text(encoding="utf-8"))
    directory = ROOT / "assets/architectures"
    directory.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        path = directory / f"{spec['id']:02d}-schematic.svg"
        content = draw(spec)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Editorial schematic is stale: {path.relative_to(ROOT)}")
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    print(f"{len(specs)} editorial schematics are current." if args.check else f"Built {len(specs)} editorial schematics.")


if __name__ == "__main__":
    main()
