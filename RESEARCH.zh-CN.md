# Video MLLM Architectures 调研与介绍清单

调研截止：**2026-10-08**。面向 `awesome-video-mllm-architectures` 的首轮资料库，包含参考仓库分析、awesome 来源、候选池以及经过一手来源核对的模型机制介绍。

本轮阅读 15 个 awesome / survey README，从五个核心来源提取 **153 条去重候选名称**，筛选并补充得到下列 **70 条介绍记录：64 条模型或版本记录，6 条方法或系统记录**。模型记录包含历史基础、通用视频兼容 MLLM、专用视频模型、训练配方和公开技术报告；这个数量不代表 70 种独立架构。

## 导航

- [参考仓库怎样组织](docs/reference-repository-analysis.md)
- [15 个来源与 153 条候选来源映射](docs/source-audit.md)
- [70 条结构化介绍数据](data/catalog.json) · [153 条候选来源数据](data/candidates.json)
- [早期视频对话与图像模型迁移](#早期视频对话与图像模型迁移)
- [视频编码器与通用视频模型](#视频编码器与通用视频模型)
- [支持视频的通用多模态模型](#支持视频的通用多模态模型)
- [长视频压缩与记忆](#长视频压缩与记忆)
- [流式与在线交互](#流式与在线交互)
- [时间定位与细粒度时间推理](#时间定位与细粒度时间推理)
- [音视频与 Omni](#音视频与-omni)
- [轻量模型与融合效率](#轻量模型与融合效率)
- [可插拔方法与系统](#可插拔方法与系统)
- [数据与评测入口](#数据与评测入口)
- [首批完整架构卡片建议](#首批完整架构卡片建议)

## 参考仓库怎样组织

[Awesome VLM Architectures](https://github.com/gokayfem/awesome-vlm-architectures) 的新版入口是“模型索引 → 发布时间线 → 架构卡片”。每个条目先说明机制，再给论文和官方项目、架构图，最后通过 `<details>` 展开架构、训练和数据。配套目录保存架构图、图源 manifest、图的出处和处理脚本，CI 检查格式、时间线覆盖与图片映射。完整目录分析及适合视频的卡片模板见 [结构分析](docs/reference-repository-analysis.md)。

建议沿用这种展示方式，增加视频比较字段：**采样策略、时序关系形成位置、token 压缩位置、长视频记忆、在线更新、主动响应、原始音频和字幕的区别**。正文每个家族一次，类别通过标签提供多个入口。正式版本可同时保留按发布时间倒序和按机制索引两种导航。

## 核心 awesome 来源

| 来源 | 用来收集什么 |
| --- | --- |
| [Awesome-LLMs-for-Video-Understanding](https://github.com/yunlong10/Awesome-LLMs-for-Video-Understanding) | 早期视频对话、长视频、记忆和 LLM 系统路线 |
| [Awesome-Video-MLLMs](https://github.com/pipixin321/Awesome-Video-MLLMs) | 现代通用模型及帧数/FPS 候选信息 |
| [Awesome-HumanView-VideoUnderstanding](https://github.com/marinero4972/Awesome-HumanView-VideoUnderstanding) | Watch / Remember / Reason，细粒度与音视频补充 |
| [Awesome-Streaming-Video-Understanding](https://github.com/sotayang/Awesome-Streaming-Video-Understanding) | 在线记忆、流式处理与主动回应机制 |
| [MLLMs for Video Temporal Grounding](https://github.com/iLearn-Lab/TPAMI26-Awesome-MLLMs-for-Video-Temporal-Grounding) | 时间戳、事件边界、定位与递归 refinement |

其余 10 个来源、提取位置及原列表错链审计见 [来源审计](docs/source-audit.md)。awesome 用于发现文章，以下机制和题名以原论文、官方项目或模型卡为依据。

## 收录口径

- 聚焦视频理解、对话、时序定位、长视频和流式交互；视频生成模型只在确有理解分支时进入。
- 年份采用 **arXiv v1 的首次提交年份**；项目或博客条目采用其公开年份。家族后续版本单独注明，会议年份不替代首次公开年份。
- 名字相同的论文用作者、版本或论文 ID 区分；代码、模型卡、项目页和托管 API 按真实类型标注。
- “视觉输入”并不表示原生音频输入；字幕或 ASR 工具与音频编码器分别说明。实时吞吐与增量流式能力也分别判断。

## 早期视频对话与图像模型迁移

| ID | 模型 | 年份 | 视频机制与收录价值 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 01 | Flamingo | 2022 | 视觉编码器 → Perceiver Resampler → 插入冻结语言模型的 gated cross-attention；原论文支持交错图像、视频与文本，是视频融合的历史基础。 | [Flamingo: a Visual Language Model for Few-Shot Learning](https://arxiv.org/abs/2204.14198) | [作者公开论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf)；原版无公开训练代码 |
| 02 | VideoChat | 2023 | VideoChat-Embed 把视频基础模型通过可学习接口接到 LLM；VideoChat-Text 则把感知结果转成文字。适合介绍显式文本与隐式视觉两条早期路线。 | [VideoChat: Chat-Centric Video Understanding](https://arxiv.org/abs/2305.06355) | [代码](https://github.com/OpenGVLab/Ask-Anything) |
| 03 | Video-ChatGPT | 2023 | CLIP 帧特征通过空间与时间聚合后投影至 Vicuna；简单连接器结合视频指令数据，为视频对话和时空表征提供早期基线。 | [Video-ChatGPT: Towards Detailed Video Understanding via Large Vision and Language Models](https://arxiv.org/abs/2306.05424) | [代码](https://github.com/mbzuai-oryx/Video-ChatGPT) |
| 04 | Video-LLaMA | 2023 | 视觉帧 → Video Q-Former；音频 → ImageBind + Audio Q-Former；两条分支对齐到冻结 LLM 的输入空间，代表早期音视频连接器设计。 | [Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding](https://arxiv.org/abs/2306.02858) | [代码](https://github.com/DAMO-NLP-SG/Video-LLaMA) |
| 05 | Valley | 2023 | 视觉编码器 + 时间建模模块 + 简单投影连接 LLM；通过两阶段对齐和视频指令训练扩展图像对话能力。此处是 RupertLuo 的历史模型。 | [Valley: Video Assistant with Large Language model Enhanced abilitY](https://arxiv.org/abs/2306.07207) | [代码](https://github.com/RupertLuo/Valley) |
| 06 | Video-LLaVA | 2023 | 图像和视频先在 LanguageBind 表征空间对齐，再投影到 LLM；共同视觉表示与混合训练实现图像、视频统一对话。 | [Video-LLaVA: Learning United Visual Representation by Alignment Before Projection](https://arxiv.org/abs/2311.10122) | [代码](https://github.com/PKU-YuanGroup/Video-LLaVA) |
| 07 | Chat-UniVi | 2023 | 动态视觉 tokens 与多尺度表示统一图像和视频，在有限 token 预算内保留空间细节与时间关系；适合解释聚类/压缩型表示。 | [Chat-UniVi: Unified Visual Representation Empowers Large Language Models with Image and Video Understanding](https://arxiv.org/abs/2311.08046) | [代码](https://github.com/PKU-YuanGroup/Chat-UniVi) |
| 08 | MiniGPT4-Video | 2024 | 将帧的视觉 tokens 与对应文本/字幕交错输入语言模型；在 MiniGPT-v2 基础上扩展多帧理解，重点是视觉与文本时间顺序的组织。 | [MiniGPT4-Video: Advancing Multimodal LLMs for Video Understanding with Interleaved Visual-Textual Tokens](https://arxiv.org/abs/2404.03413) | [代码](https://github.com/Vision-CAIR/MiniGPT4-video) |
| 09 | ST-LLM | 2024 | 将时空 tokens 直接送入 LLM 内部建模；动态 masking 和相应训练目标改善成本与稳定性，global-local 输入模块处理长视频。 | [ST-LLM: Large Language Models Are Effective Temporal Learners](https://arxiv.org/abs/2404.00308) | [代码](https://github.com/TencentARC/ST-LLM) |
| 10 | PLLaVA | 2024 | 在图像 LLaVA 到视频的迁移中加入无新增参数的时空 pooling，平滑高范数特征的支配效应；连接模块无新增参数并不等于不做视频训练。 | [PLLaVA: Parameter-free LLaVA Extension from Images to Videos for Video Dense Captioning](https://arxiv.org/abs/2404.16994) | [代码](https://github.com/magic-research/PLLaVA) |

## 视频编码器与通用视频模型

| ID | 模型 | 年份 | 视频机制与收录价值 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 11 | VideoChat2 | 2023 | UMT 视频编码器 → instruction-aware Q-Former → LLM；三阶段训练建立强视频基线。其论文题名为 MVBench，同时贡献模型与 benchmark。 | [MVBench: A Comprehensive Multi-modal Video Understanding Benchmark](https://arxiv.org/abs/2311.17005) | [代码](https://github.com/OpenGVLab/Ask-Anything/tree/main/video_chat2) |
| 12 | VideoLLaMA 2 / 2.1 | 2024 | STC 时空卷积连接器聚合帧的视觉信息，音频分支连接至 LLM；2.1 与 audio_visual 版在家族内注明具体 encoder/backbone 和音频配置。 | [VideoLLaMA 2: Advancing Spatial-Temporal Modeling and Audio Understanding in Video-LLMs](https://arxiv.org/abs/2406.07476) | [代码](https://github.com/DAMO-NLP-SG/VideoLLaMA2) · [AV 分支](https://github.com/DAMO-NLP-SG/VideoLLaMA2/tree/audio_visual) |
| 13 | VideoLLaMA 3 | 2025 | SigLIP-NaViT 动态分辨率视觉编码与视频 token 压缩；四阶段训练研究如何由图像数据迁移到视频，聚焦视觉输入。 | [VideoLLaMA 3: Frontier Multimodal Foundation Models for Image and Video Understanding](https://arxiv.org/abs/2501.13106) | [代码](https://github.com/DAMO-NLP-SG/VideoLLaMA3) |
| 14 | InternVideo2 的 MLLM 分支 | 2024 | 视频基础编码器的阶段式训练与 LLM 集成；此处收录 Stage3/Chat 分支，基础 encoder checkpoint 本身不等于 MLLM。 | [InternVideo2: Scaling Foundation Models for Multimodal Video Understanding](https://arxiv.org/abs/2403.15377) | [代码](https://github.com/OpenGVLab/InternVideo/tree/main/InternVideo2) |
| 15 | InternVideo2.5 | 2025 | 基于 InternVL2.5，用 HiCo 层级时空压缩及丰富视觉监督/TPO 兼顾长上下文和细粒度视频证据；架构、监督和后训练联合改进。 | [InternVideo2.5: Empowering Video MLLMs with Long and Rich Context Modeling](https://arxiv.org/abs/2501.12386) | [代码](https://github.com/OpenGVLab/InternVideo/tree/main/InternVideo2.5) |
| 16 | InternVideo3 | 2026 | M²LA 压缩 KV states，同时保留多模态 token 流；MCR 通过证据、工具、记忆与验证闭环理解长视频。ASR 是工具，不能据此标为原生音频编码器。 | [InternVideo3: Agentify Foundation Models with Multimodal Contextual Reasoning](https://arxiv.org/abs/2606.12195) | [代码](https://github.com/OpenGVLab/InternVideo/tree/main/InternVideo3) |
| 17 | Apollo | 2024 | SigLIP 图像编码器与 InternVideo2 视频编码器互补，特征融合后由 Perceiver resampler 接入 Qwen2.5；系统比较 fps、token 预算和训练选择。 | [Apollo: An Exploration of Video Understanding in Large Multimodal Models](https://arxiv.org/abs/2412.10360) | [作者项目](https://apollo-lmms.github.io/) · [官方模型入口](https://huggingface.co/Apollo-LMMs) |
| 18 | VideoGPT+ | 2024 | 双视觉编码器分别捕获逐帧空间细节与片段时间上下文，分段特征经自适应 pooling 接入 LLM；适合与 Apollo 比较双编码器融合。 | [VideoGPT+: Integrating Image and Video Encoders for Enhanced Video Understanding](https://arxiv.org/abs/2406.09418) | [代码](https://github.com/mbzuai-oryx/VideoGPT-plus) |
| 19 | Tarsier | 2024 | 简单逐帧 CLIP 编码与 LLM 时间建模；主要贡献是视频描述训练配方和细粒度标注/评测，不应包装为全新的时间编码器。 | [Tarsier: Recipes for Training and Evaluating Large Video Description Models](https://arxiv.org/abs/2407.00634) | [代码](https://github.com/bytedance/tarsier) |
| 20 | Tarsier2 | 2025 | 2025 报告从 Qwen2-VL-7B 初始化；扩展视频预训练、细粒度时间对齐与自动偏好训练，从视频详细描述扩展到综合理解。年份按独立论文 v1，非早期项目预告。 | [Tarsier2: Advancing Large Vision-Language Models from Detailed Video Description to Comprehensive Video Understanding](https://arxiv.org/abs/2501.07888) | [代码](https://github.com/bytedance/tarsier) |
| 21 | VideoChat3 | 2026 | I3D-ViT 将二维视觉注意力扩展为分块时空注意力；空间合并与时间池化减少 token，流式自适应帧分辨率支持通用、长视频和在线场景。 | [VideoChat3: Fully Open Video MLLM for Efficient and Generalist Video Understanding](https://arxiv.org/abs/2607.14935) | [代码](https://github.com/MCG-NJU/VideoChat3) |

## 支持视频的通用多模态模型

| ID | 模型 | 年份 | 视频机制与收录价值 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 22 | LLaVA-NeXT-Video | 2024 | 从图像 AnyRes 切块迁移到多帧，配合空间 pooling、上下文扩展、图像视频 SFT 与 DPO；一手技术来源为官方博客，不能虚构同名 arXiv。 | [LLaVA-NeXT: A Strong Zero-shot Video Understanding Model](https://llava-vl.github.io/blog/2024-04-30-llava-next-video/) | [代码](https://github.com/LLaVA-VL/LLaVA-NeXT) |
| 23 | LLaVA-OneVision | 2024 | SigLIP + MLP + Qwen2；统一单图、多图与视频任务，视频帧采用空间下采样控制 token；关注视觉任务迁移及训练配方。 | [LLaVA-OneVision: Easy Visual Task Transfer](https://arxiv.org/abs/2408.03326) | [代码](https://github.com/LLaVA-VL/LLaVA-NeXT) |
| 24 | LLaVA-Video | 2024 | 沿用 LLaVA 家族视觉连接方式，主要贡献为 LLaVA-Video-178K 合成视频指令数据与训练；作为数据驱动路线收录。 | [Video Instruction Tuning With Synthetic Data](https://arxiv.org/abs/2410.02713) | [代码](https://github.com/LLaVA-VL/LLaVA-NeXT) |
| 25 | LLaVA-OneVision-2 | 2026 | OneVision-Encoder、window attention 与 codec-stream tokenization；按视频码流 bit-cost 动态分组，利用运动残差信息选择空间证据并共享 3D RoPE。 | [LLaVA-OneVision-2: Towards Next-Generation Perceptual Intelligence](https://arxiv.org/abs/2605.25979) | [代码](https://github.com/EvolvingLMMs-Lab/LLaVA-OneVision-2) |
| 26 | InternVL2.5 | 2024 | 保持 InternVL2 核心视觉连接架构，通过多帧输入、动态切块、数据训练及 MPO/test-time scaling 升级视频能力；突出训练与数据贡献。 | [Expanding Performance Boundaries of Open-Source Multimodal Models with Model, Data, and Test-Time Scaling](https://arxiv.org/abs/2412.05271) | [代码](https://github.com/OpenGVLab/InternVL) |
| 27 | InternVL3 | 2025 | 原生多模态预训练与文本联合学习，V2PE 支持更长视觉上下文；通用图像视频家族的训练范式变化。 | [InternVL3: Exploring Advanced Training and Test-Time Recipes for Open-Source Multimodal Models](https://arxiv.org/abs/2504.10479) | [代码](https://github.com/OpenGVLab/InternVL) |
| 28 | InternVL3.5 | 2025 | Cascade RL、ViR 动态视觉分辨率路由与 DvD 视觉/语言分离部署；支持视频，但不能把这些效率升级描述成新视频时序 encoder。 | [InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency](https://arxiv.org/abs/2508.18265) | [代码](https://github.com/OpenGVLab/InternVL) |
| 29 | Qwen2-VL | 2024 | 动态分辨率视觉表示统一图像与视频，M-RoPE 分别编码时间和二维空间位置；代表显式时间位置建模。 | [Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution](https://arxiv.org/abs/2409.12191) | [原项目](https://github.com/QwenLM/Qwen2-VL) |
| 30 | Qwen2.5-VL | 2025 | 动态分辨率 ViT、window attention、动态视频采样与绝对时间编码；增加长视频和时间定位能力，须与 Qwen2.5-Omni 区分。 | [Qwen2.5-VL Technical Report](https://arxiv.org/abs/2502.13923) | [原项目](https://github.com/QwenLM/Qwen2.5-VL) |
| 31 | Qwen3-VL | 2025 | Interleaved-MRoPE、DeepStack 多层视觉特征融合与文本时间戳对齐；dense/MoE 家族，增加视频时间对齐的显式结构。 | [Qwen3-VL Technical Report](https://arxiv.org/abs/2511.21631) | [代码](https://github.com/QwenLM/Qwen3-VL) |
| 32 | Qwen3.5 → Qwen3.8-27B | 2026 | 原生视觉语言 early fusion，Gated DeltaNet 与 attention 混合；2026-08-14 的 Qwen3.8-27B 沿用此架构并支持视频，不能推广到所有 Qwen3.8 检查点。 | [Qwen3.5: Towards Native Multimodal Agents（官方发布）](https://qwen.ai/blog?id=qwen3.5) | [3.5 模型卡](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) · [3.8-27B 模型卡](https://huggingface.co/Qwen/Qwen3.8-27B) · [项目](https://github.com/QwenLM/Qwen3.8) |
| 33 | MiniCPM-V 4.5，附 2.6 演进 | 2025 | 统一 3D-Resampler 压缩图像视频，结合端侧部署和混合 RL；2.6 的视频支持属于 2024 项目演进，4.5 有独立架构论文。 | [MiniCPM-V 4.5: Cooking Efficient MLLMs via Architecture, Data, and Training Recipe](https://arxiv.org/abs/2509.18154) | [代码](https://github.com/OpenBMB/MiniCPM-V) |
| 34 | MiniCPM-V 4.6 | 2026 | 官方视频模型采用 SigLIP2 + Qwen3.5-0.8B，视觉编码器内部提前压缩，支持混合压缩率；与 4.5 的 3D-Resampler 有实质差异。 | [LLaVA-UHD v4: What Makes Efficient Visual Encoding in MLLMs?（相关视觉方法论文）](https://arxiv.org/abs/2605.08985) | [官方模型卡](https://huggingface.co/openbmb/MiniCPM-V-4.6) · [代码](https://github.com/OpenBMB/MiniCPM-V) |
| 35 | Oryx / 1.5 | 2024 | OryxViT 任意分辨率输入与可按需改变的动态 token 压缩；统一图像、视频和多视角 3D，适合比较分辨率与压缩预算的关系。 | [Oryx MLLM: On-Demand Spatial-Temporal Understanding at Arbitrary Resolution](https://arxiv.org/abs/2409.12961) | [代码](https://github.com/Oryx-mllm/Oryx) |
| 36 | Eagle 2.5 | 2025 | SigLIP + MLP + Qwen2.5，通过渐进长上下文后训练、Automatic Degrade Sampling 和 Image Area Preservation 控制视频帧与图像面积的预算。 | [Eagle 2.5: Boosting Long-Context Post-Training for Frontier Vision-Language Models](https://arxiv.org/abs/2504.15271) | [代码](https://github.com/NVlabs/Eagle/tree/main/Eagle2_5) |

## 长视频压缩与记忆

| ID | 模型 | 年份 | 视频机制与收录价值 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 37 | MovieChat | 2023 | 稠密视觉 tokens 先进入短期记忆，再合并为稀疏长期记忆，最后对接 LLM；Atkinson–Shiffrin 记忆模型为长视频表示提供组织方式。 | [MovieChat: From Dense Token to Sparse Memory for Long Video Understanding](https://arxiv.org/abs/2307.16449) | [代码](https://github.com/wenhaochai/MovieChat) |
| 38 | LLaMA-VID | 2023 | 每帧压缩为问题条件 context token 与视觉 content token，降低长视频输入成本；“2 tokens”必须结合其具体配置解释。 | [LLaMA-VID: An Image is Worth 2 Tokens in Large Language Models](https://arxiv.org/abs/2311.17043) | [代码](https://github.com/JIA-Lab-research/LLaMA-VID) |
| 39 | MA-LMM | 2024 | 逐帧编码经带视觉和 query memory bank 的 Q-Former 接入 LLM；压缩记忆并保持有限容量，代表循环记忆式长视频理解。 | [MA-LMM: Memory-Augmented Large Multimodal Model for Long-Term Video Understanding](https://arxiv.org/abs/2404.05726) | [代码](https://github.com/boheumd/MA-LMM) |
| 40 | LongVLM | 2024 | 分片视频通过 hierarchical token merging 形成局部特征，再注入全局语义并按时间连接；兼顾局部事件与长视频故事线。 | [LongVLM: Efficient Long Video Understanding via Large Language Models](https://arxiv.org/abs/2404.03384) | [代码](https://github.com/ziplab/LongVLM) |
| 41 | LongVA | 2024 | 延长语言 backbone 上下文，再经 LLaVA 风格视觉对齐迁移长上下文能力；主要路线是语言到视觉的 context transfer。 | [Long Context Transfer from Language to Vision](https://arxiv.org/abs/2406.16852) | [代码](https://github.com/EvolvingLMMs-Lab/LongVA) |
| 42 | LongVU | 2024 | SigLIP + DINOv2 视觉特征经时空自适应压缩进入 LLM；消除时间冗余，并保留文本相关的空间证据。 | [LongVU: Spatiotemporal Adaptive Compression for Long Video-Language Understanding](https://arxiv.org/abs/2410.17434) | [代码](https://github.com/Vision-CAIR/LongVU) |
| 43 | LongVILA | 2024 | VILA 视觉连接架构与语言长上下文扩展、长视频 SFT、Multi-Modal Sequence Parallelism 配合；是模型和分布式系统协同扩展路线。 | [LongVILA: Scaling Long-Context Visual Language Models for Long Videos](https://arxiv.org/abs/2408.10188) | [官方代码目录](https://github.com/NVlabs/VILA/tree/main/longvila) |
| 44 | VideoChat-Flash | 2024 | HiCo 先做片段级 token merging，再在推理阶段于 LLM 层间渐进丢弃视频 tokens，分层控制长视频成本；v1 为 2024-12-31，虽 ID 前缀为 2501。 | [VideoChat-Flash: Hierarchical Compression for Long-Context Video Modeling](https://arxiv.org/abs/2501.00574) | [代码](https://github.com/OpenGVLab/VideoChat-Flash) |

## 流式与在线交互

| ID | 模型 | 年份 | 视频机制与收录价值 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 45 | VideoLLM-online | 2024 | 帧编码、紧凑视觉 tokens 和 projector 接入 LLM；LIVE 学习目标、流式对话数据与在线推理共同支持持续交互。 | [VideoLLM-online: Online Video Large Language Model for Streaming Video](https://arxiv.org/abs/2406.11816) | [代码](https://github.com/showlab/videollm-online) |
| 46 | VideoStreaming | 2024 | 片段之间传播记忆，以 Adaptive Memory Selection 按问题选择固定数量记忆，再送入 LLM；编码过程与多问题回答解耦。 | [Streaming Long Video Understanding with Large Language Models](https://arxiv.org/abs/2405.16009) | 本轮未确认官方独立代码仓库 |
| 47 | Flash-VStream：STAR Memory | 2024 | 连续帧处理与问题响应异步并行，由 STAR Memory 维护历史；这是该家族早期版本，须与 2025 的 Flash Memory 区分。 | [Flash-VStream: Memory-Based Real-Time Understanding for Long Video Streams](https://arxiv.org/abs/2406.08085) | [LLaVA 版本代码](https://github.com/IVGSZ/Flash-VStream/tree/main/Flash-VStream-LLaVA) |
| 48 | Flash-VStream：Flash Memory | 2025 | 两个 handler 分别处理帧与问题；Context Synopsis Memory 聚合长期信息并建模时间信息密度，Detail Augmentation Memory 据此选取关键帧并补充空间细节。 | [Flash-VStream: Efficient Real-Time Understanding for Long Video Streams](https://arxiv.org/abs/2506.23825) | [Qwen 版本代码](https://github.com/IVGSZ/Flash-VStream/tree/main/Flash-VStream-Qwen) |
| 49 | StreamChat：Liu 等 | 2024 | 最新帧 tokens 通过 FIFO 更新，文字解码时通过 cross-attention 读取变化中的视频；parallel 3D-RoPE 对齐时间，每个文字解码步都可读取最新视觉上下文。 | [StreamChat: Chatting with Streaming Video](https://arxiv.org/abs/2412.08646) | [作者项目页](https://jihaonew.github.io/projects/streamchat.html)；代码标为 soon |
| 50 | TimeChat-Online | 2025 | Differential Token Drop 比较相邻帧并去除静态冗余，保留位置索引；视频变化信号还能触发主动响应。 | [TimeChat-Online: 80% Visual Tokens are Naturally Redundant in Streaming Videos](https://arxiv.org/abs/2504.17343) | [代码](https://github.com/yaolinli/TimeChat-Online) |
| 51 | StreamingVLM | 2025 | KV cache 保留 attention sinks、较短视觉窗口和较长文本窗口；通过重叠短片段 SFT 对齐流式推理时的注意力行为。 | [StreamingVLM: Real-Time Understanding for Infinite Video Streams](https://arxiv.org/abs/2510.09608) | [代码](https://github.com/mit-han-lab/streaming-vlm) |

## 时间定位与细粒度时间推理

| ID | 模型 | 年份 | 视频机制与收录价值 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 52 | TimeChat | 2023 | timestamp-aware frame encoder 与 sliding video Q-Former 生成带时间信息、可变长度的视频 tokens；把帧内容和时间戳关联。 | [TimeChat: A Time-sensitive Multimodal Large Language Model for Long Video Understanding](https://arxiv.org/abs/2312.02051) | [代码](https://github.com/RenShuhuai-Andy/TimeChat) |
| 53 | VTimeLLM | 2023 | 通过视觉语言对齐、边界感知多事件训练与指令微调，让 LLM 表达事件时间区间并进行时间推理；主要贡献是训练范式。 | [VTimeLLM: Empower LLM to Grasp Video Moments](https://arxiv.org/abs/2311.18445) | [代码](https://github.com/huangb23/VTimeLLM) |
| 54 | Momentor | 2024 | frame encoder、projector 与 Temporal Perception Module 对接 LLM；配合 Moment-10M 训练细粒度视频片段及时间推理。 | [Momentor: Advancing Video Large Language Model with Fine-Grained Temporal Reasoning](https://arxiv.org/abs/2402.11435) | [代码](https://github.com/DCDmllm/Momentor) |
| 55 | HawkEye | 2024 | 在 VideoChat2 基础上引入时间感知训练与 recursive grounding，通过反复缩小粗定位区间得到视频事件位置。 | [HawkEye: Training Video-Text LLMs for Grounding Text in Videos](https://arxiv.org/abs/2403.10228) | [代码](https://github.com/yellow-binary-tree/HawkEye) |
| 56 | VTG-LLM | 2024 | sequence-time embedding 与 absolute-time tokens 编码时间知识，slot-based token compression 控制视频输入长度，服务 temporal grounding。 | [VTG-LLM: Integrating Timestamp Knowledge into Video LLMs for Enhanced Video Temporal Grounding](https://arxiv.org/abs/2405.13382) | [代码](https://github.com/gyxxyg/VTG-LLM) |
| 57 | TRACE | 2024 | 从 VideoLLaMA2 初始化，交错处理视觉、时间、显著性分数与文本任务；生成包含时间、分数及描述的事件序列来定位视频。 | [TRACE: Temporal Grounding Video LLM via Causal Event Modeling](https://arxiv.org/abs/2410.05643) | [代码](https://github.com/gyxxyg/TRACE) |

## 音视频与 Omni

Video-LLaMA 与 VideoLLaMA 2 的音频分支已在上文收录；此处集中列统一视听输入或语音输出的家族。相同模型不重复计数。

| ID | 模型 | 年份 | 视频机制与收录价值 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 58 | VITA / VITA-1.5 | 2024 / 2025 | 统一图像、视频、音频输入；1.5 通过嵌入驱动的端到端语音生成和渐进训练升级交互。两个版本在同一家族内对照。 | [VITA: Towards Open-Source Interactive Omni Multimodal LLM](https://arxiv.org/abs/2408.05211) · [VITA-1.5: Towards GPT-4o Level Real-Time Vision and Speech Interaction](https://arxiv.org/abs/2501.01957) | [代码](https://github.com/VITA-MLLM/VITA) |
| 59 | MiniCPM-o 4.5，附 o 2.6 | 2026 | Omni-Flow 在共同时间轴对齐输入输出，支持同时看、听、说及主动交互；与 MiniCPM-V 的纯视觉家族分别介绍。 | [MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction](https://arxiv.org/abs/2604.27393) | [代码](https://github.com/OpenBMB/MiniCPM-V) |
| 60 | Qwen2.5-Omni | 2025 | Block-wise 视听编码与 TMRoPE 进行时间对齐；Thinker-Talker 分离文本推理和语音生成，音频端使用流式解码。 | [Qwen2.5-Omni Technical Report](https://arxiv.org/abs/2503.20215) | [代码](https://github.com/QwenLM/Qwen2.5-Omni) |
| 61 | Qwen3-Omni | 2025 | Thinker-Talker MoE 处理视听联合理解，多码本语音 codec 与轻量因果 ConvNet 支持流式语音输出。 | [Qwen3-Omni Technical Report](https://arxiv.org/abs/2509.17765) | [代码](https://github.com/QwenLM/Qwen3-Omni) |
| 62 | Qwen3.5-Omni | 2026 | Hybrid Attention MoE 的 Thinker/Talker 与 ARIA 动态文本语音对齐；公开报告和托管 API 支持音视频，公开权重/训练实现本轮未核验。 | [Qwen3.5-Omni Technical Report](https://arxiv.org/abs/2604.15804) | [官方 API 文档](https://www.alibabacloud.com/help/en/model-studio/qwen-omni)；不是模型实现代码 |

官方 API 文档还列出 2026-09-28 更新的 **Qwen3.8-Omni-Flash**。本轮只核对了 API 的视听输入能力，尚未核验独立架构报告，留作后续关注，不额外计为已核验架构条目。

## 轻量模型与融合效率

| ID | 模型 | 年份 | 视频机制与收录价值 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 63 | Mobile-VideoGPT | 2025 | 轻量双视觉 encoder、紧凑 projector 和小语言模型；Attention-Based Frame Scoring 选择关键帧，减少冗余视觉 tokens，面向移动视频理解。 | [Mobile-VideoGPT: Fast and Accurate Model for Mobile Video Understanding](https://arxiv.org/abs/2503.21782) | [代码](https://github.com/Amshaker/Mobile-VideoGPT) |
| 64 | Slow-Fast Video MLLM | 2025 | 压缩的 fast tokens 与文本一起进入 self-attention；未压缩 slow 特征通过 hybrid decoder cross-attention 按指令读取。与下面免训练 SF-LLaVA 的输入设计不同。 | [Slow-Fast Architecture for Video Multi-Modal Large Language Models](https://arxiv.org/abs/2504.01328) | [代码](https://github.com/SHI-Labs/Slow-Fast-Video-Multimodal-LLM) |

## 可插拔方法与系统

这些记录用于解释视频架构中的推理、压缩和记忆机制。它们不计为独立基础模型。

| ID | 名称 | 年份 | 类型与机制 | 论文或一手技术来源 | 官方项目 |
| --- | --- | --- | --- | --- | --- |
| 65 | ReKV | 2025 | 免训练推理方法：滑动窗口计算视频 KV cache，转存 RAM/磁盘；回答时检索相关 cache，在现有 VideoLLM 上复用视频上下文。 | [Streaming Video Question-Answering with In-context Video KV-Cache Retrieval](https://arxiv.org/abs/2503.00540) | [代码](https://github.com/Becomebright/ReKV) |
| 66 | StreamChat：Xiong 等 | 2025 | 记忆编排系统：Selective Frame Stacking → Memory Formation/retrieval → Contextual Summarization → 既有 MLLM；与 Liu 等的 cross-attention 模型是不同论文。 | [Streaming Video Understanding and Multi-round Interaction with Memory-enhanced Knowledge](https://arxiv.org/abs/2501.13468) | [代码](https://github.com/hmxiong/StreamChat) |
| 67 | TimeRefine | 2024 | 可插拔 grounding 训练/解码方法：粗定位后多轮生成时间偏移来修正边界，辅助预测头监督定位误差。 | [TimeRefine: Temporal Grounding with Time Refining Video LLM](https://arxiv.org/abs/2412.09601) | [代码](https://github.com/SJTUwxz/TimeRefine_code) |
| 68 | StreamMeCo | 2026 | Agent memory 压缩方法：孤立节点 minmax 采样、连通节点权重剪枝及时间衰减检索；作用于记忆层。 | [StreamMeCo: Long-Term Agent Memory Compression for Efficient Streaming Video Understanding](https://arxiv.org/abs/2604.09000) | [代码](https://github.com/Celina-love-sweet/StreamMeCo) |
| 69 | FlashVID | 2026 | 免训练 token 压缩：Attention and Diversity-based Token Selection 选取代表 tokens，再由 Tree-based Spatiotemporal Token Merging 合并跨时空冗余。 | [FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging](https://arxiv.org/abs/2602.08024) | [代码](https://github.com/Fanziyang-v/FlashVID) |
| 70 | SlowFast-LLaVA | 2024 | 免训练输入设计：slow 通路稀疏采帧但保留空间细节，fast 通路密集采帧并强空间 pooling；复用图像 LLaVA-NeXT 权重。 | [SlowFast-LLaVA: A Strong Training-Free Baseline for Video Large Language Models](https://arxiv.org/abs/2407.15841) | [代码](https://github.com/apple-aiml-research/ml-slowfast-llava) |

## 数据与评测入口

下表独立于 70 条介绍记录。正式仓库可拆分为 `docs/datasets-and-benchmarks.md`。

| 资源 | 用途与阅读价值 |
| --- | --- |
| [VideoInstruct100K](https://github.com/mbzuai-oryx/Video-ChatGPT) | 早期视频指令数据与视频对话生成式评测 |
| [LLaVA-Video-178K](https://arxiv.org/abs/2410.02713) | 合成视频指令数据与多任务视频训练 |
| [VideoChat3](https://github.com/MCG-NJU/VideoChat3) | 通用、长视频、在线三个数据分支及训练配方 |
| [MVBench](https://github.com/OpenGVLab/Ask-Anything/tree/main/video_chat2) | 多种视频时间感知与理解任务；也关联 VideoChat2 |
| [Video-MME](https://github.com/MME-Benchmarks/Video-MME) | 短、中、长视频的多模态评测；比较时标明字幕和音频配置 |
| [Video-MME-v2](https://github.com/MME-Benchmarks/Video-MME-v2) | 2026 的下一阶段综合视频理解评测 |
| [MLVU](https://github.com/JUNJIE99/MLVU) | 多任务长视频理解；Dev/Test 与不同任务指标分别记录 |
| [LongVideoBench](https://github.com/longvideobench/LongVideoBench) | 长上下文、交错视频与语言理解 |
| [StreamingBench](https://github.com/THUNLP-MT/StreamingBench) | 流式视频理解，辅助区分离线模型和在线视频能力 |
| [OVO-Bench](https://github.com/JoeLeelyf/OVO-Bench) | 真实在线视频理解与随时间变化的提问 |

## 首批完整架构卡片建议

下面 20 项按“能否解释一种代表机制”选择，不是性能排名。每项扩展为短摘要、论文与代码、原论文架构图、折叠详解；年份、作者、训练数据和图号再进入完整卡片。

| 路线 | 优先制作的卡片 |
| --- | --- |
| 视频连接器起点 | Video-ChatGPT、Video-LLaMA、Video-LLaVA |
| 显式视频表示与融合 | VideoChat2、VideoLLaMA 2、Apollo、VideoChat3 |
| 长视频压缩与记忆 | MovieChat、LLaMA-VID、MA-LMM、LongVA、VideoChat-Flash |
| 通用视频位置建模 | Qwen2.5-VL、Qwen3-VL、LLaVA-OneVision-2 |
| 在线更新与主动交互 | VideoLLM-online、Flash-VStream、MiniCPM-o 4.5 |
| 时间输出与定位 | TimeChat、VTimeLLM |

后续扩展重点：对象/区域视频指代与分割（如 VideoRefer、VideoGLaMM）、视频推理后训练、检索型 agent、更多高效压缩方法。候选池已记录这些路线；补入正文前应核对视频输入、论文版本、具体机制和官方代码。

## 当前资料边界

此稿交付的是仓库设计和带来源的介绍列表。它尚未制作所有模型的完整训练/数据卡片与论文架构图，也不提供跨配置的性能排行榜。源表中的错链、同名模型和会议/预印本年份差异已在 [来源审计](docs/source-audit.md) 中标明；正式发布时可以据此继续完善图源、日期及元数据。

本轮以 Markdown 为编辑源，`data/catalog.json` 和 `data/candidates.json` 为可复用导出快照；运行 `python scripts/export_research.py` 可同步数据并检查记录数量及来源字段。
