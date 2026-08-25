# Paper A (JACT) — arXiv / Zenodo pack

- `PaperA_JACT_manuscript.pdf` — compiled manuscript
- `PaperA_JACT_arxiv_source.zip` — TeX sources and figure for arXiv
- `PaperA_JACT_zenodo.zip` — full paper folder for a Zenodo deposit

## Zenodo

Upload `PaperA_JACT_zenodo.zip` to the Swansea University Zenodo community.
After the DOI is assigned, insert it in `sections/declarations.tex` and
rebuild the arXiv zip. Do not ship a placeholder DOI in the preprint.

Tracking data are **not** in the zip. Clone SkillCorner open data as
described in `01_data/README.md`.

## arXiv metadata (suggested)

| Field | Value |
|-------|--------|
| Title | Multi-Scale Persistent Homology for Competitive Spatial Systems |
| Author | Rowan Brown |
| Primary category | math.AT |
| Cross-list | cs.CG |
| License | CC-BY 4.0 (match Zenodo) |
| Comments | 12 pages. Code and pipeline outputs will be archived on Zenodo. |

Compile the source zip with `tectonic main.tex` or pdflatex + bibtex + pdflatex ×2.

## Companion paper

Paper B is in preparation and should be posted after this identifier exists.
Until then, `@unpublished{paperB}` in `references.bib` remains an in-preparation stub.
