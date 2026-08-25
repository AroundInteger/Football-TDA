# EPSRC Small Grant — active sources

The **live** EPSRC Mathematical Sciences Small Grant application. Edit in `live/`. Everything else is evidence, review record, or archive.

Restructured 24 August 2026 to remove cross-contamination: unrelated bids, unrelated literature and the follow-on grant's material now sit outside this directory (see *Moved out* below).

## Start here

**`FOUNDATION.md` is the normative document.** Where any file disagrees with it, it wins and the other file is corrected. It carries the formal definition of the system, the parameter register, the prior-art ledger, the rigour contract, the Month-1 work plan and the standing rulings on contested numbers.

`CANONICAL_NUMBERS.md` holds the headline statistics and is subordinate to `FOUNDATION.md` §2 and §4.

## Layout

```
grant/
├── FOUNDATION.md              Normative: definitions, parameters, tiers, rulings
├── CANONICAL_NUMBERS.md       Headline statistics (subordinate to FOUNDATION §2, §4)
├── README.md                  This file
│
├── live/                      THE SUBMISSION. Edit here, nowhere else
│   ├── 01_Summary.md … 08_Data_Management_Plan.md
│   ├── 02_Vision_and_Approach_REV3.md    Current V&A
│   ├── grant_figure_gantt.png            Figure 1, embedded by REV3
│   ├── LaySummary.docx                   JeS public summary
│   ├── TIMELINE.md                       Locked month table
│   ├── T1_T2_Six_Registers.md            T1/T2 for six audiences
│   ├── REVISION_DISCIPLINE.md            Ten failure modes; pre-commit checklist
│   └── README.md                         Pack-level notes
│
├── evidence/
│   ├── toy_models/            Adversarial TDA toy model (spec, MATLAB, Python, figures)
│   └── figure_sources/        Gantt render scripts and intermediate formats
│
├── review/                    Reviewer artefacts and responses (not submitted)
│
├── archive/                   Superseded. Do not edit; do not cite
│   ├── va_versions/           V&A V7 through V8.9
│   ├── short_form_full/       Pre-REV3 pack versions
│   ├── submission/            Earlier compression history + tex
│   └── full/                  Long-form archive + tex
│
└── shared/references.bib      Shared BibTeX (Vancouver / unsrtnat)
```

## Which file to edit

| Task | Location |
|---|---|
| Anything definitional, or a contested number | `FOUNDATION.md` **first** |
| JeS Vision & Approach | `live/02_Vision_and_Approach_REV3.md` |
| JeS Summary (public) | `live/01_Summary.md`, from `live/LaySummary.docx` |
| R4RI capability, costs, DMP, ethics, partners | `live/03`–`08` |
| Bibliography entries | `shared/references.bib`; numbered list in `live/04_References.md` |
| Headline validation numbers | `FOUNDATION.md` §2/§4, then `CANONICAL_NUMBERS.md` |
| Toy model | `evidence/toy_models/` |

## Moved out (24 Aug 2026)

| Was | Now | Why |
|---|---|---|
| `grant/Previous grants/` | `08_current/reference_bids/` | Four unrelated bids (blood diagnostics, CFS, track record) sitting inside the live application folder |
| `grant/P162.pdf`, `P170.pdf` | `08_current/literature/` | Unrelated papers on neural-network conditioning |
| `grant/short_form_full/NEXT Grant - stepping stone grant - context/` | `08_current/grant_next/` | The **follow-on** grant's material was nested inside the **current** grant's submission pack |

Also removed: six Word lock files (`~$*.docx`), `.DS_Store`, `__pycache__`.

## Conventions

- **LaTeX** is the citation-numbering source of truth (`natbib`, `unsrtnat`, Vancouver order of appearance). Markdown twins use manual `[n]` synced from the compiled PDF. The current order is REV3's 29 entries (Schenck 2022 inserted as [6]); `FOUNDATION.md` §3 is the mapping source.
- **UK English** throughout.
- **Panel legibility.** EPSRC maths panels include adjacent-subfield reviewers who may not be TDA specialists. Vision and Background stay generally readable; Approach and Methodology may be more technical.
- **Language discipline.** The mandatory substitutions are in `FOUNDATION.md` §6, not here, so there is one copy.

## Compile

Archived LaTeX only; the live pack is Markdown pasted into JeS.

```bash
cd 08_current/grant/archive/full/tex && pdflatex main && bibtex main && pdflatex main && pdflatex main
cd 08_current/grant/archive/submission/tex && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Bibliography paths in both were updated to `../../../shared/references` when they moved into `archive/`.

**Figures are not required** by EPSRC for the Vision & Approach text. Figure 1 (Gantt) is optional and is included in REV3; verify the pasted V&A is ≤3 pages before submitting.
