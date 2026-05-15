# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

This is a Python + MATLAB research codebase for **GPS-TDA: Quantum Dot-Inspired Topological Data Analysis for Football Team Dynamics**. It consists of standalone analysis scripts (not a web service or deployable application). There are no services to start — scripts are run individually.

### Python environment

- **Python 3.9+** is required. The VM has Python 3.12.
- Dependencies are listed in `requirements.txt`. Install with `pip install -r requirements.txt`.
- MATLAB is not available on the VM; focus on the Python scripts.

### Running scripts

- All 62 `.py` scripts are standalone and run from the repository root: `python3 <script>.py`
- Most scripts generate synthetic data if real GPS data (SecondSpectrum JSONL, StatsBomb, SkillCorner) is not present. The data files are gitignored and not included in the repository.
- Key entry point for demonstrating the pipeline: `python3 standalone_step4_analysis.py`
- Test scripts: `python3 test_corrected_pipeline.py` (has a pre-existing bug at report generation stage when no best method is found) and `python3 corrected_tda_implementation.py`

### Linting

- No linter configuration exists in the repository. Use `ruff check --select E,F,W *.py` for basic lint checks. The existing codebase has many pre-existing lint warnings (whitespace, line length, unused imports).
- `ruff` is installed at `~/.local/bin/ruff`; ensure `$HOME/.local/bin` is on `PATH`.

### Testing

- There is no formal test framework (no pytest, no unittest). The `test_*.py` files are ad-hoc validation scripts that create synthetic data and run analysis pipelines.
- Scripts exit 0 on successful analysis even when domain-level checks show "no improvement" — that is expected behaviour without real GPS data.

### Output directories

- Script outputs (CSV, JSON, PNG, etc.) are written to `*_results/` and `*_output/` directories, which are gitignored.
