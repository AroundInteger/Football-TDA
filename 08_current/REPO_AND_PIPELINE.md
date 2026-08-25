# Repository layout and Paper A pipeline re-run

August 2026. UK English.

This note covers (i) how to run a **full** Paper A pipeline re-run from the
Football monorepo, and (ii) closing out the old **iCloud** copies under
`~/Documents/GitHub/`. It also clarifies the **nested dataset clones** inside
`01_data/` (often confused with conda/anaconda).

---

## 1. Canonical repository location

| Role | Path | Remote |
|------|------|--------|
| **Football (canonical)** | `~/TDA/Football` | `https://github.com/AroundInteger/Football-TDA.git` |
| **Conflict / UKRI work** | `~/TDA/Conflict` | separate repo (check `git remote -v`) |
| **Deprecated (iCloud)** | `~/Documents/GitHub/Football-TDA` | same remote; delete after GitHub sync |

`~/TDA/` is a **plain folder**, not a git repo. It holds independent projects side
by side, outside iCloud Desktop & Documents sync.

**Cursor / IDE:** open `~/TDA/Football`, not the Documents copy.

---

## 2. Full Paper A pipeline re-run

### 2.1 Where to run from

The entry point is always:

```bash
cd ~/TDA/Football/08_current/Paper\ Updated/3-Paper\ Paradigm/paper_A_JACT/pipeline
chmod +x run_all.sh
./run_all.sh
```

`run_all.sh` resolves the **monorepo root** automatically:

- If the paper-local tree has `01_data/opendata/data/matches.json`, it uses the
  paper folder (standalone layout).
- Otherwise it `cd`s to the Football monorepo (`~/TDA/Football`) — required for
  the ten-match index, step 08 linkage (`03_football_analysis/`), and full
  SkillCorner event files.

**Step 08 (linkage)** imports
`03_football_analysis/linkage_method_comparison.py` from the monorepo and
`chdir`s to the monorepo root before loading data. It is not sufficient to run
from a paper-only checkout without `matches.json` at monorepo `01_data/`.

### 2.2 Python environment

Python **3.10+** recommended (manuscript pins 3.11-style stack).

```bash
cd ~/TDA/Football/08_current/Paper\ Updated/3-Paper\ Paradigm/paper_A_JACT
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Pinned packages (`requirements.txt`):

| Package | Role in pipeline |
|---------|------------------|
| numpy, pandas, scipy | All steps |
| scikit-learn | Cutoff sweep (silhouette / CH), linkage |
| matplotlib | Step 06 figures |
| PyYAML | `config.yaml` |
| ripser | Persistent homology via `tda_utils` |
| **gudhi** | Bottleneck + landscape distances (step 04, optional flag) |
| giotto-tda | Methods cross-check only; not invoked by `run_all.sh` |

`persim` is listed historically but **not imported** by any pipeline script.

### 2.3 Data prerequisites (not pip-installable)

Clone SkillCorner open data into the **monorepo**:

```bash
cd ~/TDA/Football/01_data
git clone https://github.com/SkillCorner/opendata.git
cd opendata && git lfs pull
```

Required file gate:

```
01_data/opendata/data/matches.json
01_data/opendata/data/matches/<match_id>/...
```

Optional:

- **StatsBomb** `01_data/open-data/` — not required for Paper A headline tables.
- **Second Spectrum** — step 08 tries to load one match if present; the
  Discussion linkage counts (153 / 923 / 936) use **4 matches** when it is
  available, **3 SkillCorner matches** otherwise.

**Local-only data:** `01_data/FieldTest/` (~900 MB) is not a public clone; move
it with the repo or back it up before deleting iCloud copies.

### 2.4 Default vs full re-run

**Default** (no extra env vars):

```bash
./run_all.sh
```

Runs steps 01 → 02 → 03 → 05 → 04 → 07 → 08 → 06 → `build_numbers` →
`sync_to_paper`. Step 04 **skips** TDA-native distance recomputation unless
`RUN_TDA_NATIVE=1`; committed `outputs/complementarity/` files remain authoritative.

**Full regeneration** (including bottleneck median 1.511 m, p95 3.416 m,
landscape L² 5.671):

```bash
RUN_TDA_NATIVE=1 ./run_all.sh
```

Requires **gudhi** installed (`pip install gudhi==3.11.0`). Without it, step 04
prints a warning and leaves existing summaries in place.

### 2.5 Step order and runtime notes

| Step | Script | Approx. dependency |
|------|--------|-------------------|
| 01 | `01_primary_uniform.py` | Primary match SkillCorner |
| 02 | `02_cutoff_sweep.py` | Primary match |
| 03 | `03_multi_match.py` | Ten matches, `matches.json` |
| 05 | `05_event_validity.py` | SkillCorner events/phases |
| 04 | `04_complementarity.py` | Step 03 CSV; gudhi if `RUN_TDA_NATIVE=1` |
| 07 | `07_cardinality_null.py` | Step 03; longest step (~200 nulls × 1500 frames) |
| 08 | `08_linkage_comparison.py` | Monorepo path; 4×150 frames |
| 06 | `06_figures.py` | Step 01 outputs |
| — | `lib/build_numbers.py` | Aggregates `outputs/numbers.json` |
| — | `sync_to_paper.py` | Validates LaTeX against `numbers.json` |

Expect **tens of minutes** on a laptop if cardinality null and multi-match run
fresh; linkage alone is ~3–5 minutes.

### 2.6 Success criteria

```bash
python3 sync_to_paper.py
# → PASS: headline patterns found in manuscript.
```

Check `outputs/manifest.json` for SHA-256 hashes and git commit stamp.

---

## 3. Nested dataset clones inside `01_data/` (not conda)

These are **nested git repositories** — separate clones of upstream open datasets,
**gitignored** by the Football repo. They are **not** Anaconda/conda environments.

| Directory | Upstream | Size (typical) | Re-clonable? |
|-----------|----------|----------------|--------------|
| `01_data/open-data/` | statsbomb/open-data | ~19 GB | Yes |
| `01_data/opendata/` | SkillCorner/opendata | ~2 GB | Yes |
| `01_data/FieldTest/` | local capture | ~900 MB | **No** — back up manually |

Local modifications in the two public clones are usually stray `.DS_Store` files
only. After moving to `~/TDA/Football`, you may either:

- **Move** the directories with the repo (fast, preserves LFS objects), or
- **Re-clone** from upstream (slower download, clean tree).

No change to the Football repo’s `origin` remote is required for either option.

**Do not** `git add` these folders to Football-TDA; they stay ignored.

---

## 4. Closing iCloud copies — checklist

Complete **before** deleting `~/Documents/GitHub/Football-TDA` (and any
Conflict-TDA stub still in Documents).

### 4.1 Sync Football to GitHub

The canonical tree is `~/TDA/Football`. As of the last check:

- `main` matches `origin/main` for **committed** history.
- Large local work may still be **uncommitted** (hundreds of untracked/modified
  files from the restructure). **Commit and push** anything you need preserved
  before deleting the iCloud copy.

```bash
cd ~/TDA/Football
git status
git remote -v   # should be AroundInteger/Football-TDA
# when ready:
# git add … ; git commit … ; git push origin main
```

Verify on GitHub that the remote reflects your intended state.

### 4.2 Point tools at the new path

- Cursor: **File → Open Folder → `~/TDA/Football`**
- Close tabs/workspaces still rooted at `~/Documents/GitHub/Football-TDA`
- Terminal aliases / scripts: update any hard-coded Documents paths (the codebase
  itself uses relative `01_data/` discovery, not absolute Documents paths)

### 4.3 Delete the iCloud copy

Only after push verification:

1. Quit apps with open files under `~/Documents/GitHub/Football-TDA`.
2. Delete the folder in **Finder** (moves to Trash; empty Trash when satisfied).
3. If empty grant stubs (`short_form_full/`, `submission/`) **reappear** within
   ~20 s, iCloud `bird` is still replaying an old tree — wait or delete again
   after iCloud sync settles; the real grant tree lives under
   `08_current/grant/live/` in `~/TDA/Football`.

Both copies were ~22 GB because each includes the nested `01_data` clones.
Deleting Documents frees space only if you are not keeping a duplicate 22 GB
tree elsewhere.

### 4.4 Conflict-TDA (separate from TackleTEK)

**TackleTEK** (`github.com/TackleTEK/TackleTEK`) is rugby tackle analysis — a
different project entirely.

**Conflict-TDA** is the UKRI / ACLED conflict-topology strand. Canonical files
are currently at:

```
~/TDA/Conflict/UKRI_AI_Strategy_Alignment/
```

That folder is **not yet its own git repository**. It should be initialised (or
cloned) as a dedicated repo, e.g. `AroundInteger/Conflict-TDA`, not folded into
Football-TDA or TackleTEK.

If a `Conflict-TDA` folder remains under `~/Documents/GitHub/`:

- Confirm `~/TDA/Conflict` holds the content you need.
- Initialise/push the dedicated Conflict repo before deleting any Documents copy.

**Note:** if `git status` run from `~/TDA/Conflict` shows your entire home
directory, a stray `~/.git` exists — fix that before creating Conflict-TDA's
repo (see `~/TDA/README.md`).

---

## 5. Optional next steps (Origin / Cursor cloud)

After GitHub is authoritative and iCloud copies are removed:

- Install Origin CLI if using Cursor-hosted repos (`cursor-guide` / `origin` skill).
- Add a **second remote** (do not replace `origin`):
  `git remote add cursor-origin <cursor-url>`.
- Mirror or push only when deliberately syncing; GitHub remains the citation
  remote for manuscripts until you decide otherwise.

---

## 6. Quick reference

```bash
# Environment
cd ~/TDA/Football/08_current/Paper\ Updated/3-Paper\ Paradigm/paper_A_JACT
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Data (once)
cd ~/TDA/Football/01_data && git clone https://github.com/SkillCorner/opendata.git
cd opendata && git lfs pull

# Full pipeline
cd ~/TDA/Football/08_current/Paper\ Updated/3-Paper\ Paradigm/paper_A_JACT/pipeline
RUN_TDA_NATIVE=1 ./run_all.sh   # omit env var for faster default run
python3 sync_to_paper.py
```

Paper-local pipeline details: `paper_A_JACT/pipeline/README.md`.
