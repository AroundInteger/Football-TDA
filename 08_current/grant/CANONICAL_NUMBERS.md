# Canonical grant numbers

Headline validation statistics for the live pack. **Subordinate to `FOUNDATION.md` §2 and §4** — if this file and `FOUNDATION.md` disagree, `FOUNDATION.md` wins.

**Locked:** 2026-07-06 (SkillCorner pipeline recompute). **Paths updated:** 2026-08-24 (grant restructure). **Numbering synced to REV3:** 2026-08-24.

`PAPERS/` abbreviates `08_current/Paper Updated/3-Paper Paradigm/`; bare paths are relative to this directory.

| Quantity | Value | Source |
|---|---|---|
| Cross-epoch stability (individual) | 0.96 | `PAPERS/paper_A_JACT/pipeline/outputs/regime_summary.csv` |
| Cross-epoch stability (tactical) | 0.84 | `PAPERS/paper_A_JACT/pipeline/outputs/regime_summary.csv` |
| Cross-epoch stability (team) | 1.00 | `PAPERS/paper_A_JACT/pipeline/outputs/regime_summary.csv` |
| Multi-match individual $H_1$ presence | 97.0% ± 1.5% | Paper Table `tab:h1multi` / `PAPERS/paper_A_JACT/pipeline/outputs/numbers.json` |
| Multi-match tactical $H_1$ presence | 19.3% ± 7.2% | Paper Table `tab:h1multi` / `PAPERS/paper_A_JACT/pipeline/outputs/numbers.json` |
| Primary-match individual $H_1$ presence | 95.3% (143/150) | Paper Table `tab:h1single` / `uniform_150` |
| Primary-match tactical $H_1$ presence | 12.7% (19/150) | Paper Table `tab:h1single` / `uniform_150` |
| Spearman $\rho$ (scale complementarity) | 0.264 | Paper §3.5 / `PAPERS/paper_A_JACT/pipeline/outputs/numbers.json` |
| Bootstrap CI (Spearman) | [0.200, 0.314] | `PAPERS/paper_A_JACT/pipeline/outputs/complementarity/bootstrap_multi_match_ci.json`; bootstrap median 0.262 |
| Event–topology pairs | 104,722 (10 matches) | Paper §3.8 / `PAPERS/paper_A_JACT/pipeline/outputs/event_correlation_summary.json` |
| Validated cutoffs (individual / tactical / team) | 2.98 m / 12.0 m / 30.0 m | Paper methods |
| Pilot LMM half-effect $\hat\beta_1$ | −0.081 | `half_level_random_effects.py` — **archive long form only** |
| Pilot LMM $p$ | 0.079 | Archive long form only |
| Stratified permutation $p$ | 0.051 | Cited in REV3 §4 as the replication target |
| O3 method citations | FPCA: Ramsay & Silverman (2005); CUSUM: Page (1954); landscape bootstrap: Chazal et al. (2014) | `shared/references.bib` |

**Two values that look like errors and are not.** The primary match (1996435) is analysed twice: the `uniform_150` primary-match run gives 143/150 and 19/150, and the ten-match batch row for the same match gives 144/150 and 18/150 under different sampling. The `uniform_150` figures above are canonical whenever "the primary match" is named. See `FOUNDATION.md` ruling R3.

**Do not use 1.39 m.** `regime_summary.csv` records it as the individual-scale Calinski–Harabasz optimum, not the adopted cutoff. The adopted value is 2.98 m. See `FOUNDATION.md` ruling R4.

## Publication track

| Paper | Content | Outlet | In JeS V&A? |
|---|---|---|---|
| **1** | Multi-scale methodology | JACT | Yes (Month 1) |
| **2** | Football analytics (O2 fingerprinting) | *Journal of Sports Sciences* | Yes |
| **3** | Full-season results + persistence landscapes | JACT | Yes (Month 11) |
| **Conflict TDA** | Cross-domain armed-conflict application | TBD | **No** — ethics approval pending; citing it could delay the application |

**Naming in deliverables:** in reviewer-facing documents, refer to these papers **descriptively by content and outlet** ("the methodology paper (JACT)", "the football-analytics paper (JSS)"), **not** by number or letter, which avoids A/B versus 1/2/3 confusion. The `paper_A_JACT` / `paper_B_JSS` names are directory paths only.

**BibTeX keys and V&A citation numbers.** Synced to REV3's 28-entry order of first appearance: the methodology paper is `Brown2026`, compiled number **[22]**; the football-analytics paper is `Brown2026b`, compiled number **[28]**. Both keys live in `shared/references.bib`. Re-check after any citation change; `FOUNDATION.md` §3 carries the full mapping.

**Cross-domain framing.** Name adversarial **health and economic** sectors as *future* translation pathways for the follow-on Standard Grant: health as tumour–immune competition, underpinned by Co-I Powathil's mathematical-oncology expertise; economic and security as competitive logistics and autonomous-fleet coordination. Frame these as pathways and Standard-Grant scope, **not** as deliverables of this award. This satisfies the breadth reviewers expect without committing page space or in-grant impact that could not be realised in 12 months. Do **not** name the armed-conflict study. Keep the Impact section, the Standard Grant pathway paragraph and Powathil's role consistent whenever this framing changes.

## Sync checklist

When a number changes in the paper:

1. Update `FOUNDATION.md` §2 or §4.
2. Update this file.
3. Update `live/02_Vision_and_Approach_REV3.md`.
4. Update `live/01_Summary.md` if the summary cites it.
5. Run `PAPERS/paper_A_JACT/pipeline/sync_to_paper.py` and `PAPERS/paper_B_JSS/pipeline/sync_to_paper.py`.

Archived twins under `archive/full/` and `archive/submission/` are **not** kept in sync and must not be cited.
