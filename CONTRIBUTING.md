# 贡献指南

本仓库希望帮助读者理解和比较视频模型。新增条目前，请阅读[收录范围与分类原则](docs/curation-policy.md)。模型介绍以中文撰写，模型名、论文题名和必要的技术术语保留原名。

1. 通过原论文、作者仓库、官方模型卡或技术发布资料确认模型支持视频输入。Awesome 清单用于发现候选。
2. 更新 `data/architectures.json`，使用唯一且稳定的 ID 与 slug。补充简要介绍、编码器／连接器／LLM 结构、时间机制、训练或推理方式、作者、贡献类型及一手来源。
3. 明确介绍的版本。同名但独立的论文应分别收录；新增检查点或数据训练方案不自动计为新架构。
4. 添加清晰的本地模型图，并在 `assets/architectures/manifest.json` 记录来源 URL、图号、版本及已知的 PDF 页码。原图权利归原作者；自绘示意图使用 `editorial_schematic` 标记，并说明简化内容。
5. 补充 `first_public_date` 与 `date_basis`，使用已核验的 arXiv 首版日期或官方发布日，后续家族里程碑另行说明。
6. 重新生成并校验：

```sh
python scripts/build_readme.py
python scripts/validate_repository.py
python scripts/build_readme.py --check
```

修改自绘示意图时，请编辑 `data/editorial-diagrams.json`，运行 `python scripts/build_editorial_diagrams.py`，再执行 `python scripts/build_editorial_diagrams.py --check`。图源清单中的来源与简化说明应与示意图保持一致。

提交 Pull Request 时，请说明资料依据和具体改动。只有在评测设置可比较时才给出性能排名。新增外部链接应检查可访问性，手动链接审计工作流可用于后续排查。

中文调研稿及其导出数据保留初始调研过程；其中的事实错误也应相应修正。后续新增图文条目统一维护在 `data/architectures.json`。
