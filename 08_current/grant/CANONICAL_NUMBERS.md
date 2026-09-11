# Canonical grant numbers

Headline validation statistics for the live pack. **Subordinate to `FOUNDATION.md` §2 and §4** — if this file and `FOUNDATION.md` disagree, `FOUNDATION.md` wins.

**Locked:** 2026-09-11 (cardinality-inversion pivot, ruling R15). Previous lock 2026-07-06 was the GPS/SecondSpectrum collage cascade and is not current. **Paths updated:** 2026-08-24 (grant restructure). **Numbering synced to REV3/REV4:** 2026-08-24 (29 entries; methodology paper [23]).

`PAPERS/` abbreviates `08_current/Paper Updated/3-Paper Paradigm/`; bare paths are relative to this directory.

| Quantity | Value | Source |
|---|---|---|
| Validated cutoffs (individual / tactical / team) | **2.75 m / 11.75 m / 23.0 m** | `PAPERS/paper_A_JACT/pipeline/outputs/regime_summary.csv`; protocol `CUTOFF_PROTOCOL.md` |
| Sweep frames (complete, ten Table S1 matches) | 436,648 | same protocol run |
| Per-match inverted $\delta^*$ (mean ± s.d.) | 2.80 ± 0.20 / 11.80 ± 0.35 / 22.98 ± 0.72 m | `regime_summary.csv` |
| Multi-match $H_0$ grand means (cluster counts) | 19.31 ± 0.31 / 5.09 ± 0.38 / 1.98 ± 0.06 | `PAPERS/paper_A_JACT/pipeline/outputs/numbers.json` |
| Primary-match $H_0$ (cluster counts) | 19.32 ± 2.34 / 5.04 ± 1.69 / **1.96 ± 0.36** | Paper results / `uniform_150` cluster counts. Do not quote team 1.87 (finite-bar convention) |
| Multi-match individual $H_1$ presence | 96.5% ± 1.5% (CI [95.6, 97.3]; 4,039 loops) | Paper Table `tab:h1multi` / `numbers.json` |
| Multi-match tactical $H_1$ presence | 18.8% ± 6.5% (CI [15.2, 22.7]; 306 loops) | same |
| Primary-match individual $H_1$ presence | 96.0% (144/150; 378 loops) | Paper Table `tab:h1single` / `uniform_150` |
| Primary-match tactical $H_1$ presence | 15.3% (23/150; 25 loops) | same |
| Spearman $\rho$ (scale complementarity, **total $H_1$ persistence**) | 0.234 | Paper §3.5 / `numbers.json` |
| Spearman $\rho$ (same test on **loop counts**, robustness only) | 0.205 | `numbers.json` key `spearman_rho_counts` |
| Bootstrap CI (Spearman, total persistence) | [0.181, 0.276] | `numbers.json` `bootstrap.spearman_rho_individual_tactical`; median 0.232 |
| Fisher exact odds ratio ($H_1$ presence) | 6.12, $p=0.002$; [[280, 1167], [2, 51]] | `numbers.json` `complementarity` |
| Matched-null $H_1$ excess (individual) | observed 96.5% vs null 91.4%, excess +5.1 pp, CI [+3.9, +6.1] | `PAPERS/paper_A_JACT/pipeline/outputs/cardinality_null/summary.json` |
| Matched-null $H_1$ excess (tactical) | observed 18.8% vs null 9.1%, excess +9.7 pp, CI [+7.3, +12.2] | same file |
| Bottleneck distance between scales | median 1.456 m; **p95 3.556 m**; max 6.737 m | `PAPERS/paper_A_JACT/pipeline/outputs/complementarity/tda_native_distances_summary.json` |
| Landscape $L^2$ distance between scales | median 5.477 | same file |
| Event–topology pairs | 103,856 (10 matches) | Paper §3.8 / `event_correlation_summary.json` |
| Linkage comparison (tactical $H_1$ totals, 600 frames, 4 matches) | single 106 / complete 802 / Ward 822 | `PAPERS/paper_A_JACT/pipeline/outputs/linkage/linkage_headline.json` |
| Pilot tactical $H_1$ presence s.d. (across 10 matches) | 0.065 | `numbers.json` `h1_presence_rate_std`. REV4 keeps $n=32$ for a 0.025 half-width; $1.96\times 0.065/\sqrt{32}=0.0225$ |
| Pilot LMM half-effect $\hat\beta_1$ | −0.081 | `half_level_random_effects.py` — **archive long form only** |
| Pilot LMM $p$ | 0.079 | Archive long form only |
| Stratified permutation $p$ | 0.051 | Cited in REV4 §4 as the replication target |
| O3 method citations | FPCA: Ramsay & Silverman (2005); CUSUM: Page (1954); landscape bootstrap: Chazal et al. (2014) | `shared/references.bib` |

## Covariate and stratification terminology

Locked for the live pack. **Opponent** and **adversary** are reserved for the class definition of competitive collective systems (at most one use per deliverable). For the fixture unit and power arithmetic, use **opposition** instead.

| Context | Locked form | Do not use |
|---|---|---|
| Unit of analysis | one focal team, **opposition as covariate** | opponent as covariate |
| Stratification crossing | **venue × opposition strength** (6 cells, ~90 matches each) | opponent strength; venue × opponent strength × phase of play |
| Within-match stratum | phase of play (repeated measures, does not partition matches) | phase of play in the crossing |

**Primary match 1996435.** The `uniform_150` run and the ten-match row now use the same stride and agree (144/150, 378 loops; 23/150, 25 loops). Quote either. The older dual-sampling note (143/150 vs 144/150) is historical (FOUNDATION R3, closed 11 Sep 2026).

**Do not quote collage metres as current.** 1.39 / 2.98 / 6.87 / 12.0 / 16.31 / 30.0 m are GPS-era or diagnostic values. Adopted SkillCorner inversions are 2.75 / 11.75 / 23.0 m. See `FOUNDATION.md` ruling R15.

**Always name the statistic when quoting Spearman $\rho$.** It is a correlation on *total $H_1$ persistence* per frame unless the counts robustness check is named. Point estimate as of 11 Sep 2026: 0.234 (counts 0.205). The historical 0.264 / 0.211 pair is the collage cascade. See `FOUNDATION.md` ruling R13.

**Do not restore the 0.80 gate.** Cross-epoch scores 0.875 / 0.836 / 1.000 measured partition reproducibility of the collage sweep. The live Month-2 gate is cardinality inversion plus named $H_0$ bands (FOUNDATION §2.3, REV4 §4).

## Publication track

| Paper | Content | Outlet | In JeS V&A? |
|---|---|---|---|
| **1** | Multi-scale methodology | JACT | Yes (Month 1) |
| **2** | Football analytics (O2 fingerprinting) | *Journal of Sports Sciences* | Yes |
| **3** | Full-season results + persistence landscapes | JACT | Yes (Month 11) |
| **Conflict TDA** | Cross-domain armed-conflict application | TBD | **No** — ethics approval pending; citing it could delay the application |

**Naming in deliverables:** in reviewer-facing documents, refer to these papers **descriptively by content and outlet** ("the methodology paper (JACT)", "the football-analytics paper (JSS)"), **not** by number or letter, which avoids A/B versus 1/2/3 confusion. The `paper_A_JACT` / `paper_B_JSS` names are directory paths only.

**BibTeX keys and V&A citation numbers.** Synced to REV3 plus Schenck (2022) as [6] (29-entry order of first appearance): the methodology paper is `Brown2026`, compiled number **[23]**; the football-analytics paper is `Brown2026b`, compiled number **[29]**. Both keys live in `shared/references.bib`. Re-check after any citation change; `FOUNDATION.md` §3 carries the full mapping.

**Cross-domain framing.** Name adversarial **health and economic** sectors as *future* translation pathways for the follow-on Standard Grant: health as tumour–immune competition with mathematical-oncology collaborators brought in for that programme; economic and security as competitive logistics and autonomous-fleet coordination. Frame these as pathways and Standard-Grant scope, **not** as deliverables of this award. Do **not** list Kilduff or Powathil as Co-Is on this Small Grant (costed team: PI 0.10 + Villamizar 0.05 + RA Months 5–10). This satisfies the breadth reviewers expect without committing page space or in-grant impact that could not be realised in 12 months. Do **not** name the armed-conflict study. Keep the Impact section and the Standard Grant pathway paragraph consistent whenever this framing changes.

## Sync checklist

When a number changes in Paper A:

1. Update `FOUNDATION.md` §2 or §4.
2. Update this file.
3. Update the Month-2 gate in `live/02_Vision_and_Approach_REV4.md` if the gate definition changed. Do not re-insert metres into the V&A body.
4. Update `live/01_Summary.md` if the summary cites it.
5. Run `PAPERS/paper_A_JACT/pipeline/sync_to_paper.py`.

**11 Sep 2026:** do not run `PAPERS/paper_B_JSS/pipeline/sync_to_paper.py`. Papers B and C are deferred (FOUNDATION R15).

Archived twins under `archive/full/` and `archive/submission/` are **not** kept in sync and must not be cited.
