# Multi-Scale Persistent Homology for Competitive Spatial Systems

Manuscript (target: *Journal of Applied and Computational Topology*) plus a
self-contained analysis pipeline. The `article` class source is suitable for
arXiv as-is.

## Layout

| Path | Contents |
|------|----------|
| `main.tex`, `sections/`, `references.bib`, `figures/` | Manuscript |
| `pipeline/` | Reproducible analysis steps and committed result files |
| `01_data/loaders/` | Vendored tracking-data loaders |
| `01_data/opendata/` | SkillCorner data (clone separately; see `01_data/README.md`) |
| `02_tda_core/` | Vendored TDA utilities |
| `03_football_analysis/` | Vendored analysis modules used by the pipeline |
| `requirements.txt` | Pinned Python dependencies |

Tracking data are **not** redistributed. Clone SkillCorner open data as
described in `01_data/README.md`. Analysis code and committed pipeline
outputs will be archived in the Swansea University Zenodo community at
arXiv posting. The DOI will be inserted once the deposit exists.

## Compile manuscript

```bash
tectonic main.tex
# or: pdflatex + bibtex + pdflatex ×2 with local TeX Live
```

## Reproduce results

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# optional full re-run (requires SkillCorner opendata; see 01_data/README.md):
cd pipeline && ./run_all.sh
```

Committed outputs under `pipeline/outputs/` are sufficient to regenerate
figures via `python3 pipeline/steps/06_figures.py` (needs opendata) and to
validate headline numbers via `python3 pipeline/sync_to_paper.py`.
