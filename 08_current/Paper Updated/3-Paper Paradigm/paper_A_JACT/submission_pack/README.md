# Paper A submission pack

## Journal of Applied and Computational Topology

Upload `PaperA_JACT_sn_source.zip`. It is the December 2024 Springer Nature class (`sn-jnl`) with author-year citations (`sn-mathphys-ay`), which is the style this journal asks for. The zip is one directory of files: `sn-article.tex`, the class, the bibliography style, `references.bib`, `Fig1.pdf` to `Fig4.pdf`, `FigS1.pdf`, `FigS2.pdf`, and `sn-article.pdf`.

Rebuild it from the working manuscript with:

```bash
sh submission_pack/build_jact_source.sh
```

Paste `cover_letter.md` into the cover-letter field, or upload it as a PDF.

On acceptance, choose the subscription route. The open-access charge does not apply to that route.

## arXiv

The preprint source is `../../arXiv_Paper_A.zip`, unpacked at `../../arXiv_Paper_A/`. It uses `arxiv.sty`, not the Springer class. Do not upload that zip to the journal.

## Zenodo

Upload `PaperA_JACT_zenodo.zip` to the Swansea University Zenodo community. After the DOI is assigned, insert it in `sections/declarations.tex` and rebuild both the journal zip and the arXiv zip. Do not ship a placeholder DOI.

Tracking data are not in either zip. Clone SkillCorner open data as described in `01_data/README.md`.
