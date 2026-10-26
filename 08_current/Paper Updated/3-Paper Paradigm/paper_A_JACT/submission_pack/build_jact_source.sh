#!/bin/sh
# Flatten the JACT manuscript for Editorial Manager.
# Springer Nature asks for one .tex file and no subfolders.
set -eu
cd "$(dirname "$0")/.."
OUT="submission_pack/jact_source"
rm -rf "$OUT"
mkdir -p "$OUT"
python3 - <<'PY'
from pathlib import Path
import re
root = Path(".")
main = (root / "main.tex").read_text()
def repl(match):
    name = match.group(1)
    body = (root / "sections" / f"{name}.tex").read_text().rstrip()
    return body + "\n"
flat = re.sub(r"\\input\{sections/([^}]+)\}", repl, main)
flat = flat.replace(
    "Local compile may use \\input. Editorial Manager does not: build the\n"
    "% flat source with submission_pack/build_jact_source.sh.\n",
    "This file is the Editorial Manager source. It is generated from\n"
    "% main.tex and sections/ by submission_pack/build_jact_source.sh.\n"
    "% Do not edit it by hand.\n",
)
for src, dest in {
    "figures/fig1_pipeline_schematic": "Fig1",
    "figures/fig2_cutoff_sweep": "Fig2",
    "figures/fig3_cycle_geometry": "Fig3",
    "figures/fig4_h1_diagrams": "Fig4",
    "figures/figS1_acf": "FigS1",
    "figures/figS2_cutoff_diagnostics": "FigS2",
}.items():
    flat = flat.replace(src, dest)
(root / "submission_pack/jact_source/sn-article.tex").write_text(flat)
PY
cp sn-jnl.cls sn-mathphys-ay.bst references.bib "$OUT/"
cp figures/fig1_pipeline_schematic.pdf "$OUT/Fig1.pdf"
cp figures/fig2_cutoff_sweep.pdf "$OUT/Fig2.pdf"
cp figures/fig3_cycle_geometry.pdf "$OUT/Fig3.pdf"
cp figures/fig4_h1_diagrams.pdf "$OUT/Fig4.pdf"
cp figures/figS1_acf.pdf "$OUT/FigS1.pdf"
cp figures/figS2_cutoff_diagnostics.pdf "$OUT/FigS2.pdf"
(
  cd "$OUT"
  tectonic sn-article.tex
)
cp "$OUT/sn-article.pdf" submission_pack/PaperA_JACT_sn.pdf
rm -f submission_pack/PaperA_JACT_sn_source.zip
(
  cd "$OUT"
  zip -X ../PaperA_JACT_sn_source.zip \
    sn-article.tex sn-article.pdf sn-jnl.cls sn-mathphys-ay.bst references.bib \
    Fig1.pdf Fig2.pdf Fig3.pdf Fig4.pdf FigS1.pdf FigS2.pdf
)
echo "Wrote submission_pack/PaperA_JACT_sn_source.zip"
