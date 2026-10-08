# Video MLLM awesome 来源与候选条目审计

调研截止：2026-10-08。下表来自逐个读取的 GitHub README。日期是正文可见的覆盖信号，不是最后提交日期，也不是搜索引擎爬取时间。

## 来源目录

| ID | awesome / survey 仓库 | README 组织方式与覆盖 | 用途 |
| --- | --- | --- | --- |
| S01 | [Awesome-LLMs-for-Video-Understanding](https://github.com/yunlong10/Awesome-LLMs-for-Video-Understanding) | 视频 Analyzer / Embedder 与 LLM Summarizer / Manager / Decoder 等交叉分类；训练、任务、数据和评测；主体 2023–2024，零星 2025 | 早期模型、长视频、记忆与系统的核心来源 |
| S02 | [Awesome-Video-MLLMs](https://github.com/pipixin321/Awesome-Video-MLLMs) | General / Streaming / Interesting / Evaluation；日期、会议、代码、Frames/FPS；通用表可见至 2025-08 | 现代通用 Video MLLM 补充；日期和链接需复核 |
| S03 | [Awesome-HumanView-VideoUnderstanding](https://github.com/marinero4972/Awesome-HumanView-VideoUnderstanding) | Watch / Remember / Reason；细粒度、音视频、效率、记忆、流式；对应 2026-06 综述 | 覆盖能力和架构机制的主要补充 |
| S04 | [sotayang/Awesome-Streaming-Video-Understanding](https://github.com/sotayang/Awesome-Streaming-Video-Understanding) | Proactive / Reactive；主动触发、KV、层级记忆、检索、稀疏计算；含 2026 工作 | 流式架构和响应机制主来源 |
| S05 | [Awesome-VLM-Streaming-Video](https://github.com/ydyhello/Awesome-VLM-Streaming-Video) | 主动回应、记忆、实时推理、Thinking、项目、评测和训练数据；有 2026-09/10 标签 | 最新候选发现；十月条目必须核对精确日期 |
| S06 | [Yang011013/Awesome-Streaming-Video-Understanding](https://github.com/Yang011013/Awesome-Streaming-Video-Understanding) | Models 与 Datasets/Benchmarks 表；可见至 2025-10 | 独立流式交叉核对 |
| S07 | [Awesome_Long_Form_Video_Understanding](https://github.com/ttengwang/Awesome_Long_Form_Video_Understanding) | 表征、效率、Long-Term Video LLM、定位、稠密视频描述、预测、数据与工具；含 2025 工作 | 长视频任务背景；传统模型需过滤 |
| S08 | [Comprehensive-Long-Video-Understanding-Survey](https://github.com/Vincent-ZHQ/Comprehensive-Long-Video-Understanding-Survey) | Encoder / LLM / Connector / Frames / Tokens / Training 对比 | 借鉴比较字段；正文元数据有冲突 |
| S09 | [TPAMI26-Awesome-MLLMs-for-Video-Temporal-Grounding](https://github.com/iLearn-Lab/TPAMI26-Awesome-MLLMs-for-Video-Temporal-Grounding) | Facilitator / Executor；预训练、微调、免训练、压缩和显式/隐式时间；含 2025 | 时间定位与时间 token 主来源 |
| S10 | [Audio-Visual-LLMs-Survey](https://github.com/WenyiYao/Audio-Visual-LLMs-Survey) | Model Overview / List / Datasets / Performance / Applications；引用 2026 综述 | 音视频分支；排除纯语音模型与非 MLLM 编码器 |
| S11 | [Awesome-Video-LMM-Post-Training](https://github.com/yunlong10/Awesome-Video-LMM-Post-Training) | RL / SFT Reasoning / Test-Time Scaling / Benchmarks；对应 2025-10 综述 | 后训练补充，不把所有 RL 方法称为新架构 |
| S12 | [Awesome-Multimodal-Reasoning](https://github.com/Video-R1/Awesome-Multimodal-Reasoning) | Image / Video / Audio / Generation；视频表有 SFT、RL 和任务；可见至 2025-04 | 视频推理与定位训练的交叉核对 |
| S13 | [Awesome-Agentic-Video-Understanding](https://github.com/DXY0711/Awesome-Agentic-Video-Understanding) | 上下文、证据稀疏、时间因果、多模态歧义；每篇一次主分类并附标签；含 2026 | 视频 agent 与工具系统支线 |
| S14 | [Awesome-Multimodal-Large-Language-Models](https://github.com/FudanDISC/Awesome-Multimodal-Large-Language-Models) | 输入输出模态；Architecture / Training；Encoder / Connector / LLM 字段；主体 2022–2024 | 通用 MLLM 基础路线与字段设计 |
| S15 | [Awesome-Video-LLMs](https://github.com/zyayoung/Awesome-Video-LLMs) | 模型论文、数据、结果与 VLM-Eval 使用代码；主体 2023–2024 初期 | 早期模型和评测实现核对 |

额外效率来源：[momentslab/awesome-efficient-videollm](https://github.com/momentslab/awesome-efficient-videollm)。适合继续扩展 encoder、LLM token pruning、KV cache 三个压缩位置；本轮 153 条候选统计采用下列五个核心 README，不计此来源。

后续从 S13 补充 15 个视频智能体图文条目，选取范围与机制比较见[视频智能体扩充记录](agentic-expansion.md)。本文件中的 153 条候选与五源分组保留初始调研统计。

## 从五个核心 README 提取的候选池

按首次贡献来源分组，共 **153 条跨来源去重候选名称**。这是发现池，包含模型版本、方法和系统；不等于 153 种独立架构。下面记录名称与提取位置，已入选条目的完整论文题名和一手链接见根目录筛选清单。当前主清单并未逐项收录全部候选。

### S01 的 44 条

提取位置：Taxonomy 1 的 Summarizer / Manager / Text Decoder / Regressor 表。

Video-LLaMA；Video-ChatGPT；Valley；VideoLLM；VideoChat2；Video-LLaVA；Chat-UniVi；LLaMA-VID；Vista-LLaMA；VILA；ST-LLM；PLLaVA；VideoLLaMA 2；VideoGPT+；Video-SALMONN；Tarsier；AuroraCap；LongVA；LongVLM；MA-LMM；MovieChat；MovieChat+；Koala；MiniGPT4-Video；VideoStreaming；Flash-VStream；VideoLLM-online；VideoNarrator；MovieLLM；Slot-VLM；AVicuna；CAT；LLaVA-Hound-DPO；ShareGPT4Video；LLoVi；LangRepo；Video ReCap；VideoTree；DrVideo；OmAgent；MoReVQA；IG-VLM；VideoAgent [2403.10517](https://arxiv.org/abs/2403.10517)；VideoAgent [2403.11481](https://arxiv.org/abs/2403.11481)。

### S02 新增的 22 条

提取位置：General Works；排除 S01 已出现的条目。

VideoChat；InternVL2；InternVL3；InternVL3.5；MiniCPM-V 2.6；MiniCPM-V 4.5；GLM-4.5V；Gemini 2.5；ERNIE 4.5；Seed1.5-VL；Quicksviewer；Long-VITA；Qwen2-VL；Qwen2.5-VL；Apollo；TimeMarker；Aria；LLaVA-Video；LongVU；mPLUG-Owl3；TimeChat；VTimeLLM。

### S03 新增的 32 条

提取位置：1.2 region/object-level、1.3 audio-visual、2.1 offline agent memory、2.2 offline non-agent memory；排除前两组重复。

Elysium；VideoRefer；Omni-RGPT；Describe Anything；CAT-V；PAM；PixelRefer；Strefer；VideoGLaMM；VoCap；CaptionFormer；OmniCaptioner；OmniVinci；Qwen2.5-Omni；Qwen3-Omni；Ming-Omni；Baichuan-Omni；Stream-Omni；InteractiveOmni；ReWind；HEM-LLM；Infinite-Video；VideoLLaMB；HERMES [2408.17443](https://arxiv.org/abs/2408.17443)；HierarQ；MemVid；MARC；M3-Agent；AdaVideoRAG；VideoLucy；GCAgent；EGAgent。

### S04 新增的 29 条

提取位置：Proactive / Reactive 方法表；排除前三组重复。该组 StreamChat 名称仍需在论文层面区分。

ThinkStream；StreamingClaw；Streamo；MMDuet2；VideoLLM-EyeWO；ProAssist；LiveCC；LION-FS；VideoLLM-MoD；STREAM-VLM；STRIDE；Em-Garde；StreamReady；Proact-VL；ROMA；OpenHOUSE；StreamAgent；TimeChat-Online；VST；TaYS；StreamingVLM；StreamMem；InfiniPot-V；StreamForest；ProVideLLM；StreamChat；VideoChat-Online；VideoScan；video-SALMONN S。

### S09 新增的 26 条

提取位置：Executor 表；排除前四组重复。

SeViLA；LLaViLo；GroundingGPT；HawkEye；LITA；VTG-LLM；Mr.BLIP；Momentor；GeLM；SlowFocus；E.T.Chat；Grounded-VideoLLM；TGB；TimeSuite；TRACE；ReVisionLLM；NumPro；LLaVA-MR；Seq2Time；VideoChat-TPO；TemporalVLM；TimeRefine；LLaVA-ST；VideoMind；VideoExpert；VideoChat-R1。

## 原列表错误与名称歧义

| 问题 | 本轮处理与原始证据 |
| --- | --- |
| S02 的 LLaMA-VID 错链到 Chat-UniVi | 正确论文为 [2311.17043](https://arxiv.org/abs/2311.17043)；[2311.08046](https://arxiv.org/abs/2311.08046) 是 Chat-UniVi |
| S02 将 MiniCPM-V 2.6 写作 2023-08 | 官方项目的视频版本属于 2024；[2408.01800](https://arxiv.org/abs/2408.01800) 为 2024 论文，且论文原始重点为 2.5 图像模型，不能直接当成 2.6 视频架构专文 |
| S02 VideoChat URL 有 `httpshttps` | 使用正确的 [2305.06355](https://arxiv.org/abs/2305.06355) |
| S08 LongVLM 年份写成 23.04 | 正确论文 [2404.03384](https://arxiv.org/abs/2404.03384)，为 2024 |
| S08 自述表规模和更新时间与正文不一致 | 不采用其“50+”作为实际读取数量；更新标签不作为模型发布日期 |
| StreamChat 同名 | [2412.08646](https://arxiv.org/abs/2412.08646) 为 cross-attention 模型；[2501.13468](https://arxiv.org/abs/2501.13468) 为记忆编排系统；代码链接不可互配 |
| Flash-VStream 两代 | [2024 STAR Memory](https://arxiv.org/abs/2406.08085) 与 [2025 Flash Memory](https://arxiv.org/abs/2506.23825) 关联同一家族，但机制分别说明 |
| VideoChat-Flash 年份不能由 ID 前缀推出 | [2501.00574](https://arxiv.org/abs/2501.00574) 的 v1 为 2024-12-31；本清单记 2024 |
| VideoAgent 同名 | 候选池保留两个 arXiv ID；正式卡片须按作者或论文题名区分 |
| HERMES 同名 | 2024 episodes/semantics 方法与 2026 hierarchical KV-memory 工作分别记录 |
| HawkEye / TRACE 与其他领域重名 | 使用论文 ID 和官方团队区分；不按名字搜索结果自动关联代码 |
| VideoOnline 别名 | 主清单统一为 VideoLLM-online |
| Streaming Vid2Seq | 属于 [Streaming Dense Video Captioning](https://openaccess.thecvf.com/content/CVPR2024/papers/Zhou_Streaming_Dense_Video_Captioning_CVPR_2024_paper.pdf) 的变体，列为相关字幕方法，不当作独立通用 MLLM |
| 商业模型和 Omni 候选 | 缺少足够公开架构细节者可留在评测对比；纯音频/纯图像模型须从视频架构主列表筛除 |

## 合并与补充原则

名称与别名规范化后，按论文 ID、官方项目及机制核对。只有参数规模变化的小版本合并；连接器、时间建模、输入输出流程有实质变化的版本可以分行，在正式卡片中关联其家族。每个模型只拥有一个正文条目，其他能力通过标签表达。

本轮另从官方论文和项目补充 VideoLLaMA 3、VideoChat-Flash、InternVideo2.5/3、Qwen3-VL/3.5、LLaVA-OneVision-2、MiniCPM-o 4.5、Mobile-VideoGPT、Slow-Fast、ReKV、FlashVID 等。它们的具体机制和题名以根目录清单对应的一手来源为准。

“当前覆盖”表示本次检索和核验的公开资料范围；最新来源里的月度标签不能替代精确日期核验。性能、上下文长度、帧数和实时性均应在正式卡片里附版本及评测配置，不跨论文直接拼出排行榜。
