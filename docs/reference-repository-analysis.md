# 参考仓库结构与 Video MLLM 仓库设计

调研日期：2026-10-08。目标是为 `awesome-video-mllm-architectures` 准备架构目录与论文清单。

## 参考仓库的实际结构

参考：[gokayfem/awesome-vlm-architectures](https://github.com/gokayfem/awesome-vlm-architectures)。分析以最新 raw README、GitHub 文件树、贡献规范和 CI 配置为准；带 `?tab=readme-ov-file` 的网页搜索缓存仍显示旧版目录，不代表当前内容。

```text
awesome-vlm-architectures/
├── README.md
├── CITATION.cff
├── CONTRIBUTING.md
├── CODE-OF-CONDUCT.md
├── LICENSE
├── .markdownlint-cli2.jsonc
├── .gitattributes
├── .gitignore
├── .github/workflows/
│   ├── main.yml
│   └── markdown-links-config.json
├── assets/architectures/
│   ├── <model>-<year>-arch.png
│   ├── manifest.json
│   ├── crop_overrides.json
│   ├── CREDITS.md
│   └── FIGURE_NOTICE.md
└── scripts/
    ├── build_release_timeline.py
    ├── embed_architecture_figures.py
    ├── extract_architecture_figures.py
    ├── prepare_legacy_figure_manifest.py
    └── scan_paper_figures.py
```

它是以 README 为阅读入口的架构目录。图片本地化，图的映射与出处单独维护；Python 脚本负责时间线和架构图处理。代码、权重和 demo 通过链接进入原项目。参考：[文件树](https://github.com/gokayfem/awesome-vlm-architectures)、[图目录](https://github.com/gokayfem/awesome-vlm-architectures/tree/main/assets/architectures)。

## README 的阅读顺序

新版 README 自述收录 155 个架构，标注最后审阅日期为 2026-08-01。它依次提供：标题与封面、范围介绍、Contents、Citation、Models、Release Timeline、Architectures、Important References。Models 是按年份折叠的模型锚点索引；Release Timeline 用日期、架构名和贡献组成表格；正文按发布时间倒序排列。参考：[README 原文](https://raw.githubusercontent.com/gokayfem/awesome-vlm-architectures/main/README.md)。

单个条目有三层：先用短摘要说明机制，再列论文、代码、模型或 demo 链接和作者，最后展示架构图及可展开的详细说明。图注含来源论文、图号或页码；展开区说明架构、训练或对齐方式、数据。这个结构让读者先扫读，再选择深入阅读。

## 收录与维护规则

贡献规范要求有一手技术来源、可解释的架构或训练贡献，并按架构家族合并参数规模和小版本。首个公开日期需注明，时间线由脚本重新生成；描述机制优先于性能，缺少公开架构细节的商业模型不进入技术条目。参考：[CONTRIBUTING.md](https://github.com/gokayfem/awesome-vlm-architectures/blob/main/CONTRIBUTING.md)。

CI 包含 Python lint、awesome lint、Markdown lint、格式检查，以及时间线覆盖和图片映射检查。链接检查在定期任务或手动触发时运行。参考：[main.yml](https://github.com/gokayfem/awesome-vlm-architectures/blob/main/.github/workflows/main.yml)。

## 面向视频架构的组织建议

保留“短摘要—来源—架构图—展开详解”，增加一个按架构机制组织的入口。建议正文按家族倒序排，而索引同时提供下面七类标签；一个条目可拥有多个标签，不必复制正文。

| 类别 | 比较问题 |
| --- | --- |
| Video instruction tuning | 图像模型怎样变成视频模型？ |
| Video encoders and temporal fusion | 时序关系在编码器、连接器还是 LLM 中形成？ |
| Long video and memory | 怎样在有限上下文里保留长时间证据？ |
| Streaming and online interaction | 怎样增量更新，何时回答，如何处理历史记忆？ |
| Temporal grounding and dense outputs | 怎样输出时间区间、事件和像素级对象？ |
| Audio-visual and omni models | 原始音频、帧与语言怎样同步融合？ |
| Efficient video inference | 在哪里选择帧、压缩 token 或压缩 KV cache？ |

应把**完整模型、插拔方法、工具系统、数据与评测**标清。MLVU、Video-MME 等放在评测目录；VideoAgent、VideoTree 等单列系统；压缩方法可以解释架构机制，但不能让读者误以为它们都是新的基础模型。

## 建议的未来正式仓库

以下是设计建议，并非已经创建的全部文件。

```text
awesome-video-mllm-architectures/
├── README.md                   # 英文入口、索引与架构卡片
├── README.zh-CN.md             # 中文同步版本
├── CONTRIBUTING.md
├── CITATION.cff
├── LICENSE
├── data/
│   ├── models.json             # 名称、论文、机制、来源、日期等
│   └── sources.json            # awesome / survey 来源及提取记录
├── assets/architectures/
│   ├── <model>-<year>.png
│   ├── manifest.json
│   └── CREDITS.md
├── docs/
│   ├── taxonomy.md
│   ├── datasets-and-benchmarks.md
│   └── reference-repository-analysis.md
├── scripts/
│   ├── build_readme.py
│   ├── validate_catalog.py
│   └── check_links.py
└── .github/workflows/validate.yml
```

建议让结构化模型数据成为唯一事实来源，从它生成索引、年份列表、对比表和卡片，以减少重复维护。

## 每张架构卡片的字段

| 字段 | 应记录的内容 |
| --- | --- |
| Identity | 模型名、论文完整标题、版本、首次公开日期及日期依据 |
| Sources | 原论文、官方代码、权重、项目页；awesome 发现来源单独记录 |
| Input modalities | 视频帧、原始音频、字幕、文本；区分音频编码与 ASR 转写 |
| Visual path | 编码器 → 连接器 → LLM 的真实路径 |
| Temporal modeling | 时序编码、3D 卷积、位置编码、帧顺序、跨帧注意力等 |
| Token budget | 采样策略、输入帧数、分辨率、每帧 token 和压缩位置 |
| Long video | 长上下文、分段、检索、外部记忆、KV 压缩等具体机制 |
| Streaming | 是否增量输入、是否在线更新、是否主动响应；不能仅凭速度声称实时 |
| Training | 对齐、预训练、SFT、偏好训练或 RL；哪些模块更新、哪些冻结 |
| Data | 核心视频数据与指令数据；规模必须带版本和论文出处 |
| Evaluation | 输入帧、字幕、音频、分辨率、模型规模和具体评测配置 |
| Figure | 论文版本、图号、页码、许可或权利说明；重绘图须标明重绘 |
| Contribution | 架构、训练、数据、推理或系统贡献，允许多选 |

## 推荐卡片模板

```markdown
### Model name — video mechanism in one sentence

A short summary explaining how video becomes language-model input.

**First public date:** YYYY-MM-DD (official release / arXiv v1)
**Type:** Model / Method / System
**Tags:** Long video · Memory · Streaming

[Paper](PRIMARY_SOURCE) · [Code](OFFICIAL_REPO) · [Model](MODEL_CARD)

![Architecture](assets/architectures/model-year.png)
Figure N. Source: paper version, page P; original or redrawn figure.

<details>
<summary>More information</summary>

**Architecture.** Visual encoder → temporal or compression module → LLM.

**Training and alignment.** Stages and trainable modules.

**Data and evaluation.** Dataset mixture and evaluation configuration.

**Distinctive contribution.** What changed relative to its parent family.

</details>
```

首版可先为代表机制制作约 20 张完整卡片，其余以简短介绍表覆盖。这样既保留参考仓库的视觉阅读体验，也能使每张图和每个机制说明有可靠出处。
