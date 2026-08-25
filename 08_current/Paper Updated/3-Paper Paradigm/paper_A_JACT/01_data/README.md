# Data (SkillCorner open broadcast tracking)

Tracking data are **not** shipped in this repository. Clone SkillCorner’s
open dataset into this folder before re-running the analysis pipeline:

```bash
cd 01_data
git clone https://github.com/SkillCorner/opendata.git
cd opendata
git lfs pull
```

Expected layout after clone:

```
01_data/opendata/data/matches/<match_id>/
01_data/opendata/data/matches.json
```

Committed `pipeline/outputs/` already contains the result files used for the
manuscript figures and tables, so a full re-run is only needed when regenerating
or extending the analysis.
