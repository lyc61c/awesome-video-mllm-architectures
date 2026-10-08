"""Export the research Markdown tables to reusable JSON snapshots."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")


def links(text, label_key):
    return [{label_key: label, "url": url} for label, url in LINK.findall(text)]


def main():
    readme = (ROOT / "RESEARCH.zh-CN.md").read_text(encoding="utf-8")
    entries = []
    category = ""
    for line in readme.splitlines():
        if line.startswith("## "):
            category = line[3:]
        if not re.match(r"^\| \d{2} \|", line):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) != 6:
            raise ValueError(f"Expected six table columns: {line}")
        entry_id, name, year, summary, sources, projects = cells
        entries.append({
            "id": int(entry_id),
            "name": name,
            "first_public_year_or_family_years": year,
            "category": category,
            "record_type": "method_or_system" if int(entry_id) >= 65 else "model_or_version",
            "mechanism_summary": summary,
            "technical_sources": links(sources, "title"),
            "official_entries": links(projects, "label"),
            "official_entry_note": projects,
        })
    if [entry["id"] for entry in entries] != list(range(1, 71)):
        raise ValueError("The research snapshot must contain unique IDs 1–70.")
    if any(not entry["technical_sources"] for entry in entries):
        raise ValueError("Every entry needs a primary technical source.")

    audit = (ROOT / "docs/source-audit.md").read_text(encoding="utf-8")
    repositories = {}
    for line in audit.splitlines():
        if re.match(r"^\| S\d{2} \|", line):
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            repositories[cells[0]] = links(cells[1], "name")[0]
    groups = []
    group_pattern = re.compile(
        r"^### (S\d{2})[^\n]*\n\n提取位置：([^\n]+)\n\n([^\n]+)",
        re.MULTILINE,
    )
    for source_id, section, candidate_line in group_pattern.findall(audit):
        names = [name.strip() for name in candidate_line.rstrip("。").split("；")]
        groups.append({
            "source_id": source_id,
            "repository": repositories[source_id],
            "extraction_section": section,
            "candidate_count": len(names),
            "candidate_names": names,
        })
    if [group["candidate_count"] for group in groups] != [44, 22, 32, 29, 26]:
        raise ValueError("Candidate source group counts do not match the audited snapshot.")
    candidate_count = sum(group["candidate_count"] for group in groups)

    output = ROOT / "data"
    output.mkdir(exist_ok=True)
    catalog = {
        "schema_version": 1,
        "research_cutoff": "2026-10-08",
        "purpose": "Video MLLM architecture introduction research snapshot",
        "year_policy": "arXiv v1 submission year; official release year for project or blog records; later family versions noted separately",
        "count": len(entries),
        "entries": entries,
    }
    candidates = {
        "research_cutoff": "2026-10-08",
        "scope": "Name-level deduplicated discovery pool; not independent architecture count or a fully verified bibliography",
        "count": candidate_count,
        "groups": groups,
    }
    for filename, value in [("catalog.json", catalog), ("candidates.json", candidates)]:
        (output / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"catalog": len(entries), "candidates": candidate_count, "sources": len(repositories)}))


if __name__ == "__main__":
    main()
