# Contributing

Contributions should make a video model easier to understand and compare. Read the [scope and taxonomy](docs/curation-policy.md) before adding a record.

1. Confirm video input support using an original paper, author repository, official model card, or technical release. An awesome list is a discovery source.
2. Update `data/architectures.json`. Use a stable, unique ID and slug. Include a short summary, encoder/connector/LLM description, temporal mechanism, training or inference recipe, authors, contribution types, and primary sources.
3. State the version being described. Separate independent papers with identical model names. A new checkpoint or dataset recipe does not automatically create a new architecture.
4. Add a readable local diagram and its record in `assets/architectures/manifest.json`. Give the source URL, figure number, version and PDF page when known. Original figures retain their authors' rights. Label a redrawn schematic `editorial_schematic`; describe its simplifications.
5. Give `first_public_date` and `date_basis`. Use the verified arXiv v1 date or the dated official release, and retain later family milestones separately.
6. Regenerate and validate:

```sh
python scripts/build_readme.py
python scripts/validate_repository.py
python scripts/build_readme.py --check
```

For editorial schematics, edit `data/editorial-diagrams.json`, run `python scripts/build_editorial_diagrams.py`, and confirm `python scripts/build_editorial_diagrams.py --check`. Keep the corresponding figure manifest source and simplification notes consistent.

Open a pull request describing the source evidence and what changed. Avoid performance rankings without comparable evaluation settings. Test remote URLs when adding them; the optional manual link audit reports subsequent failures.

The Chinese research snapshot and its exported discovery data preserve the initial survey. Correct factual errors there when appropriate, but add new curated entries to `data/architectures.json`.
