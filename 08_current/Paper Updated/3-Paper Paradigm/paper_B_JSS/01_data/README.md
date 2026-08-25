# Data (SkillCorner open broadcast tracking)

Tracking data are **not** shipped in this repository. Full re-runs of
pipeline steps 03–05 need SkillCorner open data under this paper folder.

## Recommended: paper-local clone

```bash
cd "08_current/Paper Updated/3-Paper Paradigm/paper_B_JSS/01_data"
git clone https://github.com/SkillCorner/opendata.git
cd opendata
git lfs pull
```

Expected layout after clone:

```
01_data/opendata/data/matches/<match_id>/
01_data/opendata/data/matches.json
```

The pipeline prefers this paper-local path when `01_data/` and
`02_tda_core/` exist under `paper_B_JSS/`.

## Monorepo alternative

If SkillCorner is already cloned at the repository root
(`Football-TDA/01_data/opendata`), you can symlink instead of cloning
again:

```bash
cd "08_current/Paper Updated/3-Paper Paradigm/paper_B_JSS/01_data"
ln -s ../../../../../01_data/opendata opendata
```

## What is already committed

- `pipeline/outputs/` — result files used for manuscript figures and tables.
- `pipeline/inputs/from_paper_a/` — snapshotted event–topology inputs from
  the companion methods paper (no Paper A directory required at run time).

Event correlation (step 01) and the locked window-sensitivity headline
table (step 02) do not require a local opendata clone.
