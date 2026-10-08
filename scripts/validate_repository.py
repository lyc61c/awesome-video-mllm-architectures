"""Validate catalog, diagram provenance, image coverage and local Markdown links."""

import datetime
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["id", "name", "slug", "record_type", "category", "first_public_date", "date_basis", "authors", "summary", "architecture", "temporal_modeling", "training", "contribution_type", "technical_sources", "official_entries", "primary_sources"]
KINDS = {"paper_crop", "paper_figure", "project_figure", "editorial_schematic"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_path(value):
    path = (ROOT / value).resolve()
    require(path.is_relative_to(ROOT), f"Path escapes repository: {value}")
    require(path.is_file(), f"Missing local file: {value}")
    return path


def source_url(value):
    parsed = urlsplit(value)
    require(parsed.scheme == "https" and bool(parsed.netloc), f"Expected HTTPS source URL: {value}")


def check_image(value):
    path = local_path(value)
    blob = path.read_bytes()
    require(len(blob) > 100, f"Empty image: {value}")
    if path.suffix == ".png":
        require(blob[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG signature: {value}")
        width, height = struct.unpack(">II", blob[16:24])
        require(width >= 300 and height >= 80, f"Image too small to read: {value} {width}x{height}")
        require(blob[-8:] == b"IEND\xaeB`\x82", f"Incomplete PNG: {value}")
    elif path.suffix == ".svg":
        svg = ET.fromstring(blob)
        require(svg.tag.endswith("svg"), f"Invalid SVG root: {value}")
        for element in svg.iter():
            require(not element.tag.endswith("script"), f"Script in SVG: {value}")
            for attribute, target in element.attrib.items():
                require(not attribute.lower().startswith("on"), f"Event handler in SVG: {value}")
                if attribute.endswith("href"):
                    require(target.startswith(("#", "data:")), f"External dependency in SVG: {value}")
    else:
        require(path.suffix.lower() in {".jpg", ".jpeg", ".webp"}, f"Unsupported image extension: {value}")


def heading_slug(text):
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\-\s]", "", text)
    return re.sub(r"\s", "-", text)


def check_markdown():
    files = [path for path in ROOT.rglob("*.md") if not any(part.startswith(".") or part.startswith("source-cache-") or part.startswith("research_cache_") for part in path.relative_to(ROOT).parts)]
    anchors = {}
    for path in files:
        content = path.read_text(encoding="utf-8")
        require("\ufffd" not in content, f"Unicode replacement character: {path}")
        require(content.count("```") % 2 == 0, f"Unclosed code fence: {path}")
        content = re.sub(r"```[^\n]*\n.*?```", "", content, flags=re.S)
        ids = set(re.findall(r'<a\s+id="([^"]+)"', content))
        seen = {}
        for heading in re.findall(r"^#{1,6}\s+(.+)$", content, re.M):
            slug = heading_slug(heading)
            count = seen.get(slug, 0)
            ids.add(slug if count == 0 else f"{slug}-{count}")
            seen[slug] = count + 1
        anchors[path.resolve()] = ids
    count = 0
    for path in files:
        content = path.read_text(encoding="utf-8")
        content = re.sub(r"```[^\n]*\n.*?```", "", content, flags=re.S)
        content = re.sub(r"`[^`\n]*`", "", content)
        targets = re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)\)", content)
        targets += re.findall(r'<(?:img|a)\b[^>]*\b(?:src|href)="([^"]+)"', content)
        for target in targets:
            if target.startswith(("https://", "http://", "mailto:")):
                continue
            target = unquote(target.strip("<>"))
            name, _, fragment = target.partition("#")
            resolved = (path.parent / name).resolve() if name else path.resolve()
            require(resolved.is_relative_to(ROOT), f"Link escapes repository: {path}: {target}")
            require(resolved.is_file(), f"Broken local link: {path.relative_to(ROOT)} -> {target}")
            if fragment and resolved.suffix == ".md":
                require(fragment in anchors.get(resolved, set()), f"Missing anchor: {path.relative_to(ROOT)} -> {target}")
            count += 1
    return count


def main():
    catalog = json.loads((ROOT / "data/architectures.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "assets/architectures/manifest.json").read_text(encoding="utf-8"))
    entries, figures = catalog["entries"], manifest["figures"]
    require(catalog["count"] == len(entries), "Catalog count mismatch")
    require(manifest["count"] == len(figures), "Figure count mismatch")
    require(len({entry["id"] for entry in entries}) == len(entries), "Duplicate catalog IDs")
    require(len({entry["slug"] for entry in entries}) == len(entries), "Duplicate slugs")
    require(len({figure["id"] for figure in figures}) == len(figures), "Duplicate figure IDs")
    require({entry["id"] for entry in entries} == {figure["id"] for figure in figures}, "Every record must have exactly one primary diagram")
    categories = {category["id"] for category in catalog["categories"]}
    specs = json.loads((ROOT / "data/editorial-diagrams.json").read_text(encoding="utf-8"))
    require({spec["id"] for spec in specs} == {figure["id"] for figure in figures if figure["kind"] == "editorial_schematic"}, "Editorial figure specification coverage mismatch")
    require(len({spec["id"] for spec in specs}) == len(specs), "Duplicate editorial specification IDs")
    spec_sources = {spec["id"]: spec["source_url"] for spec in specs}
    cutoff = datetime.date.fromisoformat(catalog["research_cutoff"])
    for entry in entries:
        for field in REQUIRED:
            require(field in entry, f"Missing field {field}: {entry['id']}")
        require(entry["record_type"] in {"model_or_version", "method_or_system"}, f"Unknown record type: {entry['id']}")
        require(entry["category"] in categories, f"Unknown category: {entry['id']}")
        require(datetime.date.fromisoformat(entry["first_public_date"]) <= cutoff, f"Date beyond cutoff: {entry['id']}")
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["slug"]), f"Invalid slug: {entry['id']}")
        for field in ["authors", "date_basis", "summary", "architecture", "temporal_modeling", "training"]:
            require(isinstance(entry[field], str) and bool(entry[field].strip()), f"Empty {field}: {entry['id']}")
        if catalog.get("language") == "zh-CN":
            for field in ["summary", "architecture", "temporal_modeling", "training", "date_basis"]:
                require(re.search(r"[\u4e00-\u9fff]", entry[field]), f"Missing Chinese introduction: {entry['id']} {field}")
        require(bool(entry["contribution_type"]), f"Missing contribution tags: {entry['id']}")
        require(bool(entry["technical_sources"]) and bool(entry["primary_sources"]), f"Missing primary evidence: {entry['id']}")
        for item in entry["technical_sources"] + entry["official_entries"] + entry["primary_sources"]:
            source_url(item["url"] if isinstance(item, dict) else item)
    for figure in figures:
        require(figure["kind"] in KINDS, f"Unknown figure kind: {figure['id']}")
        require(figure.get("verification") == "visually_reviewed", f"Unreviewed figure: {figure['id']}")
        require(bool(figure.get("display_caption")), f"Missing display caption: {figure['id']}")
        source_url(figure["source_url"])
        check_image(figure["file"])
        if figure["kind"] == "editorial_schematic":
            require(bool(figure.get("simplification")), f"Missing redraw explanation: {figure['id']}")
            require(figure["source_url"] == spec_sources[figure["id"]], f"Schematic source mismatch: {figure['id']}")
        elif figure["kind"] in {"paper_crop", "paper_figure"}:
            require(bool(figure.get("figure_number")), f"Missing author figure number: {figure['id']}")
        if figure.get("pdf_page") is not None:
            require(isinstance(figure["pdf_page"], int) and figure["pdf_page"] > 0, f"Invalid PDF page: {figure['id']}")
        if figure.get("supplementary"):
            source_url(figure["supplementary"]["source_url"])
            check_image(figure["supplementary"]["file"])
    links = check_markdown()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require(readme.count('<summary>模型结构、时间建模与训练方式</summary>') == len(entries), "README card coverage mismatch")
    require(readme.count('<p align="center"><a href="assets/architectures/') == len(entries), "README primary figure coverage mismatch")
    print(json.dumps({"records": len(entries), "model_family_cards": sum(e["record_type"] == "model_or_version" for e in entries), "method_system_cards": sum(e["record_type"] == "method_or_system" for e in entries), "primary_diagrams": len(figures), "local_links_checked": links}))


if __name__ == "__main__":
    main()
