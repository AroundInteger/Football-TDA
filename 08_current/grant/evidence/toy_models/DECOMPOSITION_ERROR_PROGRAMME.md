# Decomposition error programme (independent thread)

August 2026. UK English. **Not Paper A or Small Grant scope.**

This note is the handoff stub for investigating what topological information
scale decomposition preserves and whether centroid-projection error can be
characterised. Full allocation and boundaries are in
`08_current/Paper Updated/3-Paper Paradigm/working_foundations.md` §12.

## Question (theory)

Given raw point cloud $P(t)$ and centroid cloud $\tilde P_\delta(t)$ after
single-linkage clustering at interaction length $\delta$, bound or characterise
$\mathrm{W}_\infty(D(P), D(\tilde P_\delta))$ (or $\mathrm{W}_1$) in terms of
cluster radii, inter-scale gaps, and cardinality $k$.

The unconditional Cohen–Steiner bound ($\le 2\times$ max cluster radius) is
documented in §12 as too loose at tactical $\delta$ for football. Content lies in
a **scale-restricted** bound plus a **gap condition** at merge events.

## Relation to grant theorems

| Object | Layer |
|--------|--------|
| Decomposition error (this thread) | Upstream of filtration and temporal inference |
| T1 (landscape mean path) | Temporal, landscape-valued |
| T2 (landscape CUSUM stability) | Temporal; may **compose** with a decomposition bound |

This is **not** “more general than T1 and T2” in the sense of implying them; it
is **logically prior** and could supply a composition factor for diagram or
landscape stability under centroid reduction.

## Toy model extension (proposed)

Current toy (`evidence/toy_models/AdversarialTDA_Specification.md`) computes PH on
the **raw** hierarchical cloud; it does **not** cluster. Proposed independent module:

1. Fix ground-truth ultrametric hierarchy (existing generators).
2. Cluster at $\delta$ with known merge tree; replace with centroids.
3. Compare $D(X)$ vs $D(\pi(X))$ with exact $W_p$ (`atda_core.py`).
4. Sweep $\delta$, gap scales, and $N$; report when bounds are tight vs vacuous.

Do **not** conflate with Fig 6 (scale conflation at fixed point set) or with
Paper C's T1-lite / T2-lite programme.

## Deliverables (when pursued)

- Synthetic figures + optional short methods note section (Paper C appendix or
  Standard Grant WP), **after** Papers A and B submit.
- No new claims in Paper A beyond the existing Limitations sentence.

## Start a new chat with

- This file and `working_foundations.md` §12.
- `TOY_MODEL_PAPERS.md` §2 (cluster-then-PH gap).
- Question: “Extend adversarial toy with centroid projection; test decomposition
  error bounds at known gap scales.”
