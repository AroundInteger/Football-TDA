# Cutoff study: brief

Parallel study to Paper A. It does not change the locked cutoffs
($2.98$, $12.0$, $30.0$ m) unless we later decide to. Everything
downstream of Section 2.3 (filtration, $H_1$ regimes, event
association, ten-match transfer) inherits these three numbers. The
job here is to say what mathematically or numerically backs them.

## Question

For each adopted cutoff, what is the backing: a clustering-quality
optimum on the corpus in the paper, an inherited optimum from an
earlier corpus, a prior $H_0$ band, a football heuristic, or a
grid artefact?

## Locked (Paper A; do not move)

| Level | Adopted $\delta$ | Stated stability |
|---|---|---|
| Individual | $2.98$ m | $0.875$ |
| Tactical | $12.0$ m | $0.836$ |
| Team | $30.0$ m | $1.000$ |

Named marks on Figure 2, also locked for now: Calinski–Harabasz
peak $1.39$ m; tactical disagreement $[6.87, 16.31]$ m.

## Definition of done (this slice)

1. One dossier that states the backing of each adopted $\delta$.
2. Numbers recomputed from the committed SkillCorner sweep tables,
   not re-typed from memory.
3. Provenance of $2.98$, $6.87$, $16.31$, $28.11$, and $30.0$
   named as SecondSpectrum GPS versus SkillCorner broadcast.
4. The circularity of $H_0$-band "validation" quantified as the
   width of $\delta$ that sits in each prior band.

## Out of scope until the next slice

- Moving Paper A numbers or Figure 2 marks.
- Re-running tracking or a ten-match cutoff sweep.
- Persistence-landscape stability of $\delta$ (deferred in Paper A
  Section 4.3).
- Paper C.

## How to refresh the numbers

```bash
cd "08_current/Paper Updated/3-Paper Paradigm/cutoff_study"
python quantify.py
```

Reads `paper_A_JACT/pipeline/outputs/cutoff_sweep_agg.csv` and
`cutoff_sweep_results.csv` only. Writes `outputs/dossier.json`.
