# Paper A — arXiv / Zenodo pack

- `../arXiv_Paper_A.zip` — TeX sources, figures, `arxiv.sty`, and compiled `main.pdf`
- Unpacked copy: `../arXiv_Paper_A/`

## Zenodo

Upload `PaperA_JACT_zenodo.zip` to the Swansea University Zenodo community.
After the DOI is assigned, insert it in `sections/declarations.tex` and
rebuild the arXiv zip. Do not ship a placeholder DOI in the preprint.

Tracking data are **not** in the zip. Clone SkillCorner open data as
described in `01_data/README.md`.

## arXiv metadata (suggested)

| Field | Value |
|-------|--------|
| Title | Multi-Scale Persistent Homology for Competitive Collective Systems |
| Author | Rowan Brown |
| Primary category | math.AT |
| Cross-list | stat.AP, cs.CG |
| License | CC-BY 4.0 (match Zenodo) |
| Comments | Preprint. Journal version in preparation for JQAS. Code and pipeline outputs will be archived on Zenodo. |

Compile the source zip with `tectonic main.tex` or pdflatex + bibtex + pdflatex ×2.

## Companion paper

Paper B is in preparation and should be posted after this identifier exists.
Until then, `@unpublished{paperB}` in `references.bib` remains an in-preparation stub.
