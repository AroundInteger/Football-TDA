# Multi-Scale Persistent Homology for Competitive Collective Systems

Journal manuscript for the *Journal of Applied and Computational
Topology* (JACT), using the Springer Nature class `sn-jnl` (December
2024) with the author-year mathematics style `sn-mathphys-ay`. The
arXiv preprint is the separate tree `../arXiv_Paper_A/` and stays on
`arxiv.sty`.

## Layout

| Path | Contents |
|------|----------|
| `main.tex`, `sections/`, `references.bib`, `figures/` | Working manuscript (`sn-jnl.cls`) |
| `sn-jnl.cls`, `sn-mathphys-ay.bst` | Springer Nature class and JACT reference style |
| `submission_pack/` | Flat Editorial Manager source |
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

Editorial Manager compiles with TeX Live 2018 and rejects `\input` paths
and figure subfolders. Build the flat upload with:

```bash
sh submission_pack/build_jact_source.sh
```

That writes `submission_pack/PaperA_JACT_sn_source.zip` (one `.tex` file,
`sn-jnl.cls`, `sn-mathphys-ay.bst`, the bibliography, `Fig1.pdf` to
`Fig4.pdf`, `FigS1.pdf`, `FigS2.pdf`, and the compiled PDF). On
acceptance, choose the subscription route. The open-access charge does
not apply to that route.

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
