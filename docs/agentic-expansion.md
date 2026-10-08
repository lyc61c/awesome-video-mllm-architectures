# 视频智能体分支扩充记录

资料核验截至 2026-10-08。本轮以 [Awesome-Agentic-Video-Understanding](https://github.com/DXY0711/Awesome-Agentic-Video-Understanding) 为候选发现来源，补充 15 个视频智能体系统与训练方法。架构、训练方式、日期及图片出处均以原论文和作者项目核验。

## 选取原则

优先补充能说明不同机制的代表工作：主动证据搜索、工具调用、结构化长期记忆、记忆回溯，以及多智能体协作。已收录的 VideoStreaming、Flash-VStream（Flash Memory）、ReKV、StreamChat（Xiong 等）和 StreamMeCo 保留原条目。数据集、评测集与综述不计为独立架构，也不直接沿用来源仓库中的会议年份。

新增条目统一归为方法／系统，并单列“视频智能体”阅读路线。免训练编排系统、记忆组织方法和 SFT／RL 工具调用训练各有介绍价值；条目数量不代表新增骨干模型数量，也不代表性能排名。

## 新增条目与阅读重点

| 条目 | 阅读重点 | 原论文 |
| --- | --- | --- |
| VideoAgent（Wang 等） | 由语言模型规划、选择视频证据并逐轮完善回答 | [2403.10517](https://arxiv.org/abs/2403.10517) |
| VideoAgent（Fan 等） | 结合视频内容记忆、对象记忆与工具调用 | [2403.11481](https://arxiv.org/abs/2403.11481) |
| OmAgent | 任务分解、视频索引和按需回看 | [2406.16620](https://arxiv.org/abs/2406.16620) |
| DrVideo | 将长视频转为可检索文档并迭代补充证据 | [2406.12846](https://arxiv.org/abs/2406.12846) |
| GraphVideoAgent | 实体关系图和自适应视频证据检索 | [2501.15953](https://arxiv.org/abs/2501.15953) |
| M3-Agent | 音视频感知、长期记忆与强化学习推理 | [2508.09736](https://arxiv.org/abs/2508.09736) |
| AdaVideoRAG | 面向问题的自适应检索与多粒度证据选择 | [2506.13589](https://arxiv.org/abs/2506.13589) |
| VideoLucy | 从压缩记忆逐层回溯原始视频细节 | [2510.12422](https://arxiv.org/abs/2510.12422) |
| VideoARM | 在层级记忆上执行智能体推理 | [2512.12360](https://arxiv.org/abs/2512.12360) |
| WorldMM | 动态多模态记忆与按需证据获取 | [2512.02425](https://arxiv.org/abs/2512.02425) |
| DVD / Deep Video Discovery | 通过工具主动搜索长视频中的关键证据 | [2505.18079](https://arxiv.org/abs/2505.18079) |
| LongVT | 将视频片段查看作为原生工具调用进行训练 | [2511.20785](https://arxiv.org/abs/2511.20785) |
| FrameThinker | 多轮帧选择与证据驱动推理的强化学习 | [2509.24304](https://arxiv.org/abs/2509.24304) |
| LVAgent | 微调片段检索器与多轮动态协作的视频理解流程 | [2503.10200](https://arxiv.org/abs/2503.10200) |
| VideoMind | 规划、定位、验证与回答角色的协作 | [2503.13444](https://arxiv.org/abs/2503.13444) |

## 维护方式

核验时保留以下差异：LVAgent 的 MLLM 协作流程复用预训练模型，但片段检索器经过微调；LongVT 首次公开于 2025 年，所依据最新技术版本对应 CVPR 2026；VideoMind 的最新版本为 ICLR 2026 定稿；GraphVideoAgent 的 arXiv 题名为 *Understanding Long Videos via LLM-Powered Entity Relation Graphs*，后续出版题名采用 GraphVideoAgent。首次公开日期、论文版本和会议年份分别记录，不相互替代。

两篇 VideoAgent 是独立工作，按作者区分。README 保持模型图、中文结构介绍和条目分割线；图号、论文版本与出处统一记录在[模型图来源与署名](../assets/architectures/CREDITS.md)，不在各条目下重复显示。

新增条目的规范数据保存在 [data/architectures.json](../data/architectures.json)，图源保存在 [manifest.json](../assets/architectures/manifest.json)。初始 153 条候选池保留原始调研范围，本轮新增内容不改写其历史统计。
