# Data Provenance

All data in `08_current/data/` derives from **SkillCorner open broadcast tracking** (10 Hz).

## primary_match/

**Source:** SkillCorner match ID **1996435** (Sydney FC vs Adelaide United, A-League 2024/25)

**Pipeline:** `03_football_analysis/AvailableData/primary_match_skillcorner_analysis.py` (cutoff sweep, temporal windows) and `03_football_analysis/AvailableData/primary_match_uniform_sampling.py` (uniform 150-frame analysis for paper tables).

**Key parameters:**
- Individual cutoff: 2.98 m (Calinski–Harabasz optimum)
- Tactical cutoff: 12.0 m (domain-informed)
- Team cutoff: 30.0 m (information-content optimum from SkillCorner sweep)

**Uniform 150-frame results** (in `uniform_150/`) are the authoritative numbers for Paper Draftv5 Sections 3.1–3.6.

## multi_match/

**Source:** 10 SkillCorner A-League matches (including primary match 1996435), `--skillcorner-only` mode.

**Pipeline:** `03_football_analysis/multi_match_validation.py --skillcorner-only`

**Key parameters:** Same cutoffs as primary match (2.98 m, 12.0 m, 30.0 m). 150 uniformly sampled frames per match (every 100th frame).

**Contents:**
- `aggregate_stats.json` — per-scale grand means, H1 totals, per-match breakdowns
- `per_frame_results.csv` — 4,500 rows (10 matches x 150 frames x 3 scales)

**Headline results (10 matches, 1,500 frames):**
- Individual H0: 19.05 ± 0.39, H1 total: 4,200, presence: 97.0%
- Tactical H0: 4.92 ± 0.36, H1 total: 315, presence: 19.3%
- Team H0: 1.38 ± 0.08, H1 total: 0, presence: 0%

## event_correlation/

**Source:** 10 SkillCorner matches (dynamic_events.csv + phases_of_play.csv per match), individual + tactical scales only.

**Pipeline:** `03_football_analysis/real_event_correlation.py`

**Contents:**
- `event_correlation_summary.json` — per-scale statistical tests (Mann–Whitney U)
- `event_topology_correlation.csv` — 104,722 event–topology pairs

**Headline results (10 matches, 104,722 pairs):**
- On-ball engagement: persistence decrease (p < 0.001 individual, p = 0.014 tactical)
- Build-up: persistence increase (p < 0.001 both scales)
- Passing option: persistence decrease (p < 0.001 both scales)

---

*Updated April 2026 — all results verified with corrected team cutoff (30.0 m); event correlation independently re-run and confirmed.*
