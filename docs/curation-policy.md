# Curation policy

This collection follows video evidence through the visual encoder, connector, language decoder, and any temporal or memory mechanism. It includes a model only when a primary source establishes video input support. Image-only VLMs, standalone video encoders, generators, datasets and benchmarks are not independent model cards here.

## Record types

The initial collection contains 64 model/version/family records and six method/system records. A record is not a count of distinct backbone architectures. Closely related family versions may share a card; different papers called StreamChat and different Flash-VStream memory designs have separate cards.

The six methods are ReKV, StreamChat (Xiong et al.), TimeRefine, StreamMeCo, FlashVID and SlowFast-LLaVA. Their diagrams explain additions to an existing backbone or a system around it. Dedicated sections keep these mechanisms easy to locate.

## Architecture and contribution

Each card distinguishes the base architecture from its contribution. Contributions can involve encoder/connector design, token compression, position or timestamp representations, cache/memory design, training data, objectives, post-training, or serving. A data-driven advance can be valuable while retaining an existing network.

Nine reading routes organize the collection: early foundations, dedicated video models, general VLMs with video support, long-video context, streaming interaction, temporal grounding, audio-visual/omni interaction, efficient models, and reusable methods/systems. These routes overlap in capabilities; the primary category is an editorial navigation choice.

## Dates and availability

The timeline labels its evidence basis. arXiv entries normally use v1 submission dates in UTC. Official-release entries use the dated project announcement. Where a verified release precedes a report, the release can be the first date with the report date retained in the note. arXiv identifiers alone do not prove a date: VideoChat-Flash `2501.00574` was submitted on 2024-12-31.

Paper, code, checkpoint, project page and hosted API are different kinds of availability. Only author-linked implementation or model pages receive official badges. Flamingo, VideoStreaming, Liu et al.'s StreamChat and Qwen3.5-Omni require explicit availability notes. Qwen3.8-27B's video support does not establish video support for every Qwen3.8 checkpoint.

## Source and diagram policy

Awesome repositories supply discovery candidates; original papers, code and official model cards supply technical claims. The initial audit tracks 15 discovery repositories and 153 name-level candidates. Only 70 curated records received architecture cards in this release.

Prefer an original architecture figure. A representation, memory or training figure can be used when labeled by what it actually shows. If a complete diagram is unavailable, draw a cited editorial schematic and state its simplifications. Never infer a figure number from an image filename. Record arXiv versions because later revisions may change a figure or implementation.

Original captions are paraphrased in cards. Short excerpts in legacy extraction metadata are kept only to identify a selected figure. All prose is newly written from primary evidence. Figure attribution and rights are separate from the repository's text license.

## Reproducibility

`data/architectures.json` is the maintained card source. `assets/architectures/manifest.json` is the maintained figure source. `data/editorial-diagrams.json` stores the original schematic specifications. `scripts/build_readme.py` generates the README and credits deterministically; CI rejects stale outputs. `scripts/build_editorial_diagrams.py` regenerates the schematics. `scripts/validate_repository.py` checks identifiers, dates, record types, primary sources, diagram coverage, safe local paths and Markdown links. Optional network scripts import or extract explicitly selected figures and audit external links.

The research cutoff for the first release is 2026-10-08. Inclusion is curated rather than exhaustive and does not imply a performance ranking.
