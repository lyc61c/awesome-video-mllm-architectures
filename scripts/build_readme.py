"""Generate the illustrated README and figure credits from canonical JSON.

Use --check in CI to detect stale generated outputs. No network or third-party
Python dependencies are needed.
"""

import argparse
import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPE_LABELS = {"model_or_version": "模型／家族", "method_or_system": "方法／系统"}
FIGURE_LABELS = {"paper_crop": "论文原图裁切", "paper_figure": "论文原图", "project_figure": "官方项目图", "editorial_schematic": "本仓库绘制的示意图"}


def link(label, url):
    return f"[{label}]({url})"


def anchor(entry):
    return link(entry["name"], "#" + entry["slug"])


def badges(entry):
    items = []
    seen = set()
    for source in entry["technical_sources"]:
        url = source["url"]
        label = "论文" if "arxiv.org" in url else "技术来源"
        if entry["id"] == 34 and "arxiv.org" in url:
            label = "相关视觉编码论文"
        if url not in seen:
            items.append(link(label, url))
            seen.add(url)
    for source in entry["official_entries"]:
        url = source["url"]
        if url in seen:
            continue
        label = "代码" if "github.com" in url else "模型" if "huggingface.co" in url else "作者论文" if url.endswith(".pdf") else "官方项目"
        if "model-studio" in url:
            label = "托管 API"
        items.append(link(label, url))
        seen.add(url)
    return " · ".join(items)


def figure_caption(figure):
    if figure["kind"] == "editorial_schematic":
        return f"本仓库依据{link('一手资料', figure['source_url'])}绘制的示意图。{figure['simplification']}"
    label = "官方项目图" if figure["kind"] == "project_figure" else f"原文图 {figure['figure_number']}" if figure.get("figure_number") else "作者原图"
    page = f"，PDF 第 {figure['pdf_page']} 页" if figure.get("pdf_page") else ""
    return f"{label}{page}，来源：{link('原始资料', figure['source_url'])}。{figure['display_caption']}"


def card(entry, figure):
    alt = html.escape(f"{entry['name']}: {figure['display_caption']}", quote=True)
    file = html.escape(figure["file"], quote=True)
    lines = [f'<a id="{entry["slug"]}"></a>', "", f'### {entry["name"]}', "", entry["summary"], "",
             badges(entry), "", f"**作者：** {entry['authors']}  ",
             f"**首次公开日期：** {entry['first_public_date']}（{entry['date_basis']}）  ",
             f"**主要贡献：** {'、'.join(entry['contribution_type'])}", "",
             f'<p align="center"><a href="{file}"><img src="{file}" width="820" alt="{alt}" /></a></p>', "",
             "*" + figure_caption(figure) + "*", "",
             "<details>", "<summary>模型结构、时间建模与训练方式</summary>", "",
             "**模型结构：** " + entry["architecture"], "",
             "**时间建模：** " + entry["temporal_modeling"], "",
             "**训练／推理方式：** " + entry["training"], ""]
    if entry.get("datasets"):
        lines.extend(["**资料中提及的数据：** " + "、".join(entry["datasets"]) + "。", ""])
    if entry.get("version_note"):
        lines.extend(["**版本说明：** " + entry["version_note"], ""])
    if entry.get("availability_note"):
        lines.extend(["**公开情况：** " + entry["availability_note"], ""])
    sources = entry.get("primary_sources", [])
    sources = [source["url"] if isinstance(source, dict) else source for source in sources]
    if sources:
        lines.extend(["**一手资料：** " + " · ".join(link(f"来源 {index + 1}", url) for index, url in enumerate(dict.fromkeys(sources))) + "。", ""])
    if figure.get("supplementary"):
        item = figure["supplementary"]
        lines.extend([link(item.get("link_label", "作者补充图"), item["file"]) + " · " + link("原始来源与署名", item["source_url"]) + "。", ""])
    lines.extend(["</details>", "", "---", ""])
    return lines


def readme(catalog, figures):
    entries = catalog["entries"]
    models = [entry for entry in entries if entry["record_type"] == "model_or_version"]
    methods = [entry for entry in entries if entry["record_type"] == "method_or_system"]
    counts = Counter(figure["kind"] for figure in figures.values())
    original = sum(count for kind, count in counts.items() if kind != "editorial_schematic")
    lines = ["<!-- 由 scripts/build_readme.py 生成；请编辑 data/architectures.json 和图源清单。 -->", "",
             "# Awesome Video MLLM Architectures", "",
             "![Awesome Video MLLM Architectures](assets/banner.svg)", "",
             "本仓库整理视频多模态大语言模型（Video MLLM）的关键架构，以模型图和中文说明介绍视觉编码、视觉语言连接、时间建模，以及长视频与流式视频的压缩、缓存和记忆机制。", "",
             f"**{len(entries)} 个图文条目** · {len(models)} 个模型／版本／家族条目 · {len(methods)} 个方法／系统条目 · 资料核验截至 **{catalog['research_cutoff']}**。", "",
             f"每个条目包含模型图、结构介绍、时间建模机制、训练或推理方式，以及论文、代码和官方项目入口。主图包括 {original} 张作者原图与 {counts['editorial_schematic']} 张明确标注的本仓库示意图。家族版本与训练方案可能沿用同一骨干模型，因此条目数量不等于独立架构数量。", "",
             "仓库的组织方式参考 [Awesome VLM Architectures](https://github.com/gokayfem/awesome-vlm-architectures)。所有介绍依据一手资料重新撰写，模型图均记录出处。初始调研过程见[中文调研稿](RESEARCH.zh-CN.md)。", "",
             "## 目录", "",
             "- [模型索引](#models)", "- [分类阅读](#reading-routes)", "- [发布时间线](#release-timeline)",
             "- [模型架构介绍](#model-architectures)", "- [方法与系统](#methods-and-systems)",
             "- [调研来源](#discovery-sources)", "- [引用与使用](#citation-and-reuse)",
             "- [贡献指南](CONTRIBUTING.md)", "", '<a id="models"></a>', "", "## 模型索引", "",
             "按已核验的首次公开日期分组；同一家族的后续版本在对应条目中说明。方法与系统另列索引。", ""]
    years = sorted({entry["first_public_date"][:4] for entry in models}, reverse=True)
    for year in years:
        group = sorted([entry for entry in models if entry["first_public_date"].startswith(year)], key=lambda entry: entry["first_public_date"], reverse=True)
        lines.extend(["<details open>" if year == years[0] else "<details>", f"<summary>{year} 年（{len(group)} 个条目）</summary>", ""])
        lines.extend("- " + anchor(entry) for entry in group)
        lines.extend(["", "</details>", ""])
    lines.extend(["**方法与系统：** " + " · ".join(anchor(entry) for entry in methods) + "。", "", '<a id="reading-routes"></a>', "", "## 分类阅读", "",
                  "可按下列路线比较模型的关键机制。分类依据主要贡献和阅读重点划分，模型能力可以跨越多个类别。", "",
                  "| 阅读方向 | 重点比较的机制 | 条目 |", "| --- | --- | --- |"])
    for category in catalog["categories"]:
        group = [entry for entry in entries if entry["category"] == category["id"]]
        lines.append(f"| {category['label']} | {category['description']} | " + ", ".join(anchor(entry) for entry in group) + " |")
    lines.extend(["", '<a id="release-timeline"></a>', "", "## 发布时间线", "",
                  "日期采用各条目注明的依据：arXiv 首版提交日期或官方发布日。同一家族的后续里程碑及论文修订不重复计为新条目。", "",
                  "| 首次公开日期 | 条目 | 类型 | 主要贡献 |", "| --- | --- | --- | --- |"])
    ordered = sorted(entries, key=lambda entry: (entry["first_public_date"], entry["id"]), reverse=True)
    for entry in ordered:
        lines.append(f"| {entry['first_public_date']} | {anchor(entry)} | {TYPE_LABELS[entry['record_type']]} | " + "、".join(entry["contribution_type"]) + " |")
    lines.extend(["", '<a id="model-architectures"></a>', "", "## 模型架构介绍", "",
                  "按首次公开日期从新到旧排列。点击模型图可查看完整尺寸；展开详细说明，可阅读编码器、连接器、语言模型、时间机制及训练方式，并区分网络结构、数据和训练方案的贡献。", ""])
    for entry in ordered:
        if entry["record_type"] == "model_or_version":
            lines.extend(card(entry, figures[entry["id"]]))
    lines.extend(['<a id="methods-and-systems"></a>', "", "## 方法与系统", "",
                  "本节介绍作用于既有模型的 KV 缓存检索、token 压缩、时间边界修正，以及智能体与记忆系统。图示说明各方法在整体流程中的作用位置。", ""])
    for entry in ordered:
        if entry["record_type"] == "method_or_system":
            lines.extend(card(entry, figures[entry["id"]]))
    lines.extend(['<a id="discovery-sources"></a>', "", "## 调研来源", "",
                  "初始调研检查了 15 个 awesome 仓库，并从 5 个核心清单中提取 153 个名称级候选。当前 70 个图文条目经过筛选，并以原论文、作者代码及官方模型卡核验技术内容；awesome 清单用于发现候选，具体架构和视频支持情况以一手资料为准。", "",
                  "- [Awesome 仓库审计与候选提取](docs/source-audit.md)",
                  "- [参考仓库的结构与 README 分析](docs/reference-repository-analysis.md)",
                  "- [收录范围、分类、日期与公开情况](docs/curation-policy.md)",
                  "- [初始中文调研稿](RESEARCH.zh-CN.md)",
                  "- [机器可读的架构目录](data/architectures.json)",
                  "- [模型图来源与署名](assets/architectures/CREDITS.md)及[图片权利说明](assets/architectures/FIGURE_NOTICE.md)", "",
                  '<a id="citation-and-reuse"></a>', "", "## 引用与使用", "",
                  "讨论具体模型时，请引用对应的原论文；引用本仓库的整理工作或自绘示意图时，可使用 [CITATION.cff](CITATION.cff)。", "",
                  "本仓库原创文字、脚本和自绘示意图采用 [CC0-1.0](LICENSE)。第三方论文与项目图片的权利仍归原作者或出版方，具体见[图片权利说明](assets/architectures/FIGURE_NOTICE.md)。", "",
                  "更新条目时，请修改源 JSON、重新生成 README，并运行[贡献指南](CONTRIBUTING.md)中的校验命令。"])
    return "\n".join(lines) + "\n"


def credits(catalog, figures):
    names = {entry["id"]: entry["name"] for entry in catalog["entries"]}
    lines = ["<!-- 由 scripts/build_readme.py 生成。 -->", "", "# 模型图来源与署名", "",
             "作者原图的权利归原作者或出版方；本仓库自绘图已明确标注。详见[图片权利说明](FIGURE_NOTICE.md)。图号对应链接中的论文版本；PDF 页码从 1 开始，可能与论文印刷页码不同。", "",
             "| ID | 条目／本地图片 | 图片类型 | 一手来源 | 图号／PDF 页码 | 提取或绘制说明 |",
             "| --- | --- | --- | --- | --- | --- |"]
    for entry_id, figure in sorted(figures.items()):
        filename = Path(figure["file"]).name
        kind = FIGURE_LABELS[figure["kind"]]
        source = link("一手来源", figure["source_url"])
        location = f"图 {figure['figure_number']}" if figure.get("figure_number") else "—"
        if figure.get("pdf_page"):
            location += f"／第 {figure['pdf_page']} 页"
        note = link("原图提取出处", figure["extraction_source"]) if figure.get("extraction_source") else figure.get("simplification", "从作者提供的 HTML 下载，或从原论文 PDF 裁切。")
        lines.append(f"| {entry_id:02d} | {link(names[entry_id], filename)} | {kind} | {source} | {location} | {note} |")
        if figure.get("supplementary"):
            item = figure["supplementary"]
            lines.append(f"| {entry_id:02d}（补充） | {link(names[entry_id] + ' 补充图', Path(item['file']).name)} | {FIGURE_LABELS[item['kind']]} | {link('一手来源', item['source_url'])} | 图 {item.get('figure_number', '—')} | {link('原图提取出处', item['extraction_source']) if item.get('extraction_source') else '作者原图。'} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog = json.loads((ROOT / "data/architectures.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "assets/architectures/manifest.json").read_text(encoding="utf-8"))
    figures = {figure["id"]: figure for figure in manifest["figures"]}
    outputs = {ROOT / "README.md": readme(catalog, figures), ROOT / "assets/architectures/CREDITS.md": credits(catalog, figures)}
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Generated file is stale: {path.relative_to(ROOT)}")
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    print("Generated files are current." if args.check else "Built README.md and figure credits.")


if __name__ == "__main__":
    main()
