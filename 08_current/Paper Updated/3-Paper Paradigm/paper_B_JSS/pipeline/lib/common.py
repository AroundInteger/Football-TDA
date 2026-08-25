"""Shared utilities for Paper B pipeline."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

PIPELINE_DIR = Path(__file__).resolve().parents[1]
PAPER_DIR = PIPELINE_DIR.parent
OUTPUT_DIR = PIPELINE_DIR / "outputs"
FIGURES_DIR = PAPER_DIR / "figures"

# Prefer a self-contained snapshot under this paper folder; fall back to
# the sibling Paper A folder when still working inside the monorepo.
_LOCAL_PAPER_A = PIPELINE_DIR / "inputs" / "from_paper_a"
_SIBLING_PAPER_A = PAPER_DIR.parent / "paper_A_JACT" / "pipeline" / "outputs"
PAPER_A_OUTPUTS = _LOCAL_PAPER_A if (_LOCAL_PAPER_A / "event_correlation").is_dir() else _SIBLING_PAPER_A


def repo_root() -> Path:
    """Resolve analysis root: paper-local layout first, then monorepo."""
    if (PAPER_DIR / "01_data").is_dir() and (PAPER_DIR / "02_tda_core").is_dir():
        return PAPER_DIR
    p = PIPELINE_DIR.resolve()
    for _ in range(12):
        if (p / "01_data").is_dir() and (p / "02_tda_core").is_dir():
            return p
        if p.parent == p:
            break
        p = p.parent
    raise RuntimeError(
        "Could not locate analysis root. Expected either a paper-local "
        "01_data/ + 02_tda_core/ layout, or the Football-TDA monorepo."
    )


def load_config() -> dict:
    with open(PIPELINE_DIR / "config.yaml") as f:
        return yaml.safe_load(f)


def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root(),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def write_manifest(extra: dict | None = None) -> None:
    files = {}
    for p in sorted(OUTPUT_DIR.rglob("*")):
        if p.is_file() and p.name != "manifest.json":
            rel = p.relative_to(OUTPUT_DIR).as_posix()
            files[rel] = file_sha256(p)

    manifest = {
        "paper": "Paper B (JSS)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "output_dir": str(OUTPUT_DIR),
        "files": files,
    }
    if extra:
        manifest.update(extra)

    with open(OUTPUT_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
