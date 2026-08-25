# Paper B (JSS) — arXiv / Zenodo pack

- `PaperB_JSS_manuscript.pdf` — compiled manuscript
- `PaperB_JSS_arxiv_source.zip` — TeX sources, figures, `interact.cls`, `tfp.bst`
- `PaperB_JSS_zenodo.zip` — full paper folder for a Zenodo deposit
- `source/` — same manuscript sources (JSS ScholarOne layout)

## Zenodo

Upload `PaperB_JSS_zenodo.zip` to the Swansea University Zenodo community.
After the DOI is assigned, replace `10.5281/zenodo.XXXXXXX` in
`sections/backmatter.tex`.

Tracking data are **not** in the zip. Clone SkillCorner open data as
described in `01_data/README.md`.

## arXiv metadata (suggested)

| Field | Value |
|-------|--------|
| Title | What Persistent Homology Reveals about Football: Event Correlation, Geometric Baselines, and Predictive Utility |
| Authors | Rowan Brown, Gibin Powathil, Liam Kilduff |
| Primary category | stat.AP |
| Cross-list | physics.soc-ph |
| License | CC-BY 4.0 (match Zenodo) |
| Comments | Companion methods paper (Brown, arXiv, in preparation) should be cited by identifier once Paper A is posted. |

Compile the source zip with `tectonic main.tex`. The Taylor \& Francis
`interact.cls` and `tfp.bst` are included.

## Companion citation gate

`references.bib` cites Paper A as in preparation. After Paper A is posted,
replace that entry with the arXiv ID and recompile before posting Paper B.
