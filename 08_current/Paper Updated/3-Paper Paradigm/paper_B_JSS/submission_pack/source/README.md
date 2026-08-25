# What Persistent Homology Reveals about Football

Manuscript (target: *Journal of Sports Sciences*) plus a self-contained
analysis pipeline.

## Status

See [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md). Compiled PDF:
`main.pdf`. Packaged materials: `submission_pack.zip`.

## Layout

| Path | Contents |
|------|----------|
| `main.tex`, `sections/`, `references.bib`, `figures/` | Manuscript |
| `interact.cls`, `tfp.bst` | Taylor & Francis Interact + Style P |
| `pipeline/` | Reproducible analysis steps and committed result files |
| `pipeline/inputs/from_paper_a/` | Snapshotted companion-paper event outputs |
| `01_data/loaders/` | Vendored tracking-data loaders |
| `01_data/opendata/` | SkillCorner data (clone separately; see `01_data/README.md`) |
| `02_tda_core/` | Vendored TDA utilities |
| `03_football_analysis/` | Vendored analysis modules used by the pipeline |
| `requirements.txt` | Pinned Python dependencies |

Tracking data are **not** redistributed. Clone SkillCorner open data as
described in `01_data/README.md`. Analysis code and committed pipeline
outputs will be archived on Zenodo at arXiv posting
(`https://doi.org/10.5281/zenodo.XXXXXXX`).

## Reproduce results

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# optional full re-run (requires SkillCorner opendata; see 01_data/README.md):
cd pipeline && ./run_all.sh
```

This folder does not require the companion Paper A directory: event-correlation
inputs ship under `pipeline/inputs/from_paper_a/`.

## Compile manuscript

```bash
tectonic main.tex
# or: pdflatex + bibtex + pdflatex ×2 with local TeX Live
```
