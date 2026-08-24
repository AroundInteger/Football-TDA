# Adversarial TDA Toy Model

**Mathematical specification, MATLAB implementation guide, and new-chat briefing**

EPSRC Small Grant: Statistical TDA of Competitive Collective Systems | Swansea University | August 2026

---

## 1. Overview

This document specifies the Adversarial TDA Toy Model — a controlled, mathematically honest synthetic system designed to illustrate and computationally test the core concepts of the EPSRC Small Grant on statistical topological data analysis (TDA) of competitive collective systems.

The toy model computes honest versions of the objects it uses: H₀ via the MST, exact Wasserstein distances on diagrams, the W₂ Fréchet mean, and a Page CUSUM. It is a **proof-of-principle analogue** of Theorems T1 and T2, not a substitute for them. The Vision and Approach states T1 and T2 for **persistence landscapes** (Bubenik; Chazal et al.): T1 is convergence of the empirical mean path in landscape space, with the long-run covariance appearing in the limit, and T2 is a Wasserstein-stability bound for landscape-valued CUSUM. Uniqueness of the landscape mean is a routine precondition of T1, not its content. The toy model works with **H₀ persistence diagrams** and **diagram W₁/W₂**, which are related but different statistics. Diagram W₁ is the V&A fallback (R3) if the landscape argument is intractable. The "toy" designation refers to the synthetic, ground-truth setting.

The model has four primary purposes:

1. Proof-of-principle **analogue** of Theorems T1 and T2 (diagram W₁/W₂, not landscape-valued) in a setting where ground truth is known
2. Visualisation of key mathematical concepts (multi-scale hierarchy, scale-specific adversarial coupling, phase transitions) for grant reviewers and academic presentations
3. Domain-generalisation illustration: the same framework operating across football, tumour–immune competition, predator–prey ecology, and autonomous systems
4. Starting point for a MATLAB interactive application and future theoretical extensions

**Implementation files:** `adversarial_tda.m` (figures 1–9); `gtppf_switching.py` (figure 10). This markdown file is the source of truth; `AdversarialTDA_Specification.docx` is generated from it. Relation to Papers A/B/C and Standard Grant transfer of the toy: `TOY_MODEL_PAPERS.md`. Paper C (methods note) lives at `08_current/Paper Updated/3-Paper Paradigm/paper_C_methods/` and is developed after A and B submit.

---

## 2. Mathematical framework

### 2.1 System definition

The system consists of two competing point clouds in a bounded rectangular domain Ω = [0, 120] × [0, 80] (virtual units, matching a standard football pitch).

- **Agent set A (System A):** N_A = 12 agents with positions {x_i^A} ⊂ Ω
- **Agent set B (System B):** N_B = 12 agents with positions {x_i^B} ⊂ Ω

Both sets are organised in a three-level ultrametric hierarchy:

| Level | Structure | Typical death scale |
|-------|-----------|---------------------|
| 1 (Local) | 4 clusters × 3 agents | ≈ 4.0–4.03 |
| 2 (Tactical) | 2 formations × 2 clusters | ≈ 12.7–32.6 (configuration-dependent) |
| 3 (Global) | 1 team | ≈ 12.7–60.0 (configuration-dependent) |

Within-cluster max distance is ≈ 4.03 units for the standard triangle cluster template.

### 2.2 Cluster generation

Each cluster of 3 agents is generated around a centre (c_x, c_y) with radius r = 2.0:

```
agent_1 = (c_x,     c_y - r × 1.1)
agent_2 = (c_x - r, c_y + r × 0.65)
agent_3 = (c_x + r, c_y + r × 0.65)
```

This triangle arrangement gives max within-cluster distance ≈ 4.03 units (two sides of length 4.03, one of length 4.00). Because the triangle is not perfectly symmetric under the MST, the eight local deaths split into four at 4.00 and four at 4.03 — this is expected and reproducible.

### 2.3 H₀ persistent homology

H₀ persistent homology is computed via the minimum spanning tree (MST). This is exact for H₀ on finite metric spaces — the MST edge weights are precisely the Vietoris–Rips H₀ death times (Carlsson–Mémoli correspondence).

**Algorithm (Prim MST):**

1. Compute all pairwise Euclidean distances D_{ij} between the N agents
2. Find the minimum spanning tree T
3. The N−1 edge weights of T, sorted ascending, are the H₀ death times
4. One component survives to infinity; its death is excluded from finite analysis

For N = 12 agents: 11 finite H₀ death times distributed across three gap scales (8 local, 2 tactical, 1 global).

**H₁ persistent homology (Figure 9 only):** computed by GF(2) reduction of the Vietoris–Rips 1-boundary matrix (`vr_persistence`). Used for the encirclement figure; not required for the main H₀ narrative.

### 2.4 Wasserstein distance

For H₀ diagrams with all births equal to 0, W_p reduces to optimal transport on the real line. Points may be matched to the diagonal at cost |death|/p (half the death value for p = 1).

The implementation solves the **exact** assignment problem via `matchpairs` (MATLAB R2019a+):

- Build a cost matrix between all diagram points and diagonal slots
- Solve minimum-cost perfect matching on the augmented problem
- Handle unequal cardinalities (e.g. after a red card) without approximation

**Do not** use naive sorted matching: for (A_WIDE, A_NARROW) sorted matching gives 87.15, whereas exact W₁ = 76.13.

**Stability:** Cohen–Steiner et al. (2007). A perturbation of agent positions by ε changes death values by at most ε, so W₁(D, D_perturbed) ≤ 11ε for 12 agents.

### 2.5 Fréchet mean (T1 analogue)

Following Turner et al. (2014), the Fréchet mean of persistence diagrams is defined with respect to **W₂**, not W₁. For equal-cardinality H₀ diagrams with all births at 0, and when the optimal matching never uses the diagonal, the W₂ barycentre is the componentwise mean of sorted death times:

```
μ[k] = (1/n) Σ_i sort(D_i)[k]   for k = 1, …, K
```

That formula is **exact for the W₂ Fréchet functional**. It is **not** the minimiser of E[W₁(D_i, μ)²]; an adversarial four-diagram example puts a substantial gap between the two, and even in the toy model's low-noise sliding window the W₁ gap is a few per cent. Dispersion is therefore measured in W₂:

```
σ²_F = (1/n) Σ_i W₂(D_i, μ)²
```

T1 analogue (diagrams, not landscapes): μ is stable in each steady-state phase (low σ²_F), shifts at the transition, and recovers. The bounded domain (diameter ≈ 144 units) makes all deaths finite, converting T1's integrability hypothesis into a geometric fact. The V&A theorem is convergence of the **landscape-valued** empirical mean path; this toy computation is the diagram-valued counterpart.

### 2.6 Adversarial dynamics

The time series model (t = 0 to 100) has three phases:

| Phase | Time | Team A | Team B |
|-------|------|--------|--------|
| Pre-transition | t < 50 | A_WIDE | B_PRESS |
| Transition | 50 ≤ t < 56 | A_WIDE → A_NARROW (smoothstep) | B_PRESS → B_SPREAD |
| Post-transition | t ≥ 56 | A_NARROW | B_SPREAD |

Smoothstep easing: e(t) = ((t−50)/6)² × (3 − 2×(t−50)/6) ensures C² continuity.

**Noise:** Gaussian N(0, σ²) with σ = 1.5, applied per frame via `RandStream('twister','Seed', t×31+7)`.

### 2.7 CUSUM change-point detection (T2 analogue)

Page (1954) CUSUM on the **diagram** W₁ distance between consecutive frames — the V&A fallback statistic (R3), not the landscape-valued CUSUM of T2 as stated:

```
C(t) = max(0, C(t−1) + W₁(t) − κ)
```

**Calibration (revised August 2026):** thresholds are no longer ad hoc. The decision interval h is calibrated by Monte Carlo on **independent in-control realisations** to achieve a target false-alarm rate of 5% over the monitoring horizon (frames 5–100). The drift parameter κ is set from the in-control mean and standard deviation.

```
κ = μ₀ + 0.4 σ₀
h   = calibrated so P(false alarm) ≈ 5%
```

Detection: **T̂ = first t with C(t) ≥ h** (no arbitrary t ≥ 30 guard).

Headline realisation (seed 7): **T̂ = 54, error = 4** frames (T* = 50).

### 2.8 Dependence structure (Figure 7)

Figure 7 compares two **stationary** generative models with identical marginal distributions:

- **Tug-of-war (coupled):** each team's cluster-centre displacement follows an AR(1) process; Team B tracks Team A with a one-frame lag
- **Coin-flip (independent):** fresh independent displacements every frame

The statistic is **per-frame** W₁(D_t, D_ref) against the undisturbed reference diagram. Consecutive-frame W₁(D_t, D_{t−1}) must not be used: it induces spurious lag-1 correlation even under independence.

Over 200 replicates (T = 400): coupled lag-1 ρ ≈ +0.44; independent lag-1 ρ ≈ 0.00.

### 2.9 H₁ encirclement (Figure 9)

Team B is placed on a ring of radius ρ = 22 about centre (30, 40). A single Team A cluster (3 agents) is either trapped inside the ring or positioned outside it.

| Configuration | H₁ barcode |
|---------------|-------------|
| B ring alone | [27.24, 40.00], persistence 12.76 |
| Ring + trapped A cluster | empty (loop filled) |
| Ring + escaped A cluster | [27.24, 40.00], persistence 12.76 |

This demonstrates H₁ from adversarial embedding geometry (MacPherson–Schweinhart), not from internal hierarchy.

### 2.10 GTPPF switching preview (Figure 10, Python)

Football is a hybrid system: a possession variable $b(t)\in\{0,1\}$ inverts which team is predator and which is prey (Chat 2). This is the Standard Grant conceptual centrepiece; the Small Grant toy model supplies a single telegraph realisation.

| $b$ | Team A | Team B | Encirclement $H_1$ (born $<45$) |
|-----|--------|--------|----------------------------------|
| 1 (A possesses) | prey: A_WIDE | predator: B_RING | A: 0.00, B: 12.76 |
| 0 (B possesses) | predator: A_RING | prey: B_WIDE | A: 12.76, B: 0.00 |

Two deterministic switches at $T^*_1=40$ and $T^*_2=100$. CUSUM on consecutive-frame $W_1$ of Team A detects both (headline seed 11: $\hat T=44, 106$). A two-formation layout also carries a global rectangular $H_1$ hole born at $\delta\approx 60$; that is a hierarchy feature and is excluded from the encirclement readout.

Python entry points:

- `atda_core.py` — shared primitives (the independent verification script, plus exact $W_p$ and the W2 Fréchet mean)
- `verify_atda.py` — Parts 1–3 against the corrected reference values
- `gtppf_switching.py` — Figure 10

---

## 3. Agent configurations

### 3.1 Standard configurations (pitch: 120 × 80 units)

**Team A — Wide (two-formation layout):**

| Cluster | Centre |
|---------|--------|
| 1 | (18, 22) |
| 2 | (18, 58) |
| 3 | (82, 22) |
| 4 | (82, 58) |

**Team A — Narrow (single compressed formation):**

Cluster centres at x = 47 with **uniform 16-unit vertical spacing** (critical for equal tactical deaths):

| Cluster | Centre |
|---------|--------|
| 1 | (47, 16) |
| 2 | (47, 32) |
| 3 | (47, 48) |
| 4 | (47, 64) |

**Team B — Press:**

| Cluster | Centre |
|---------|--------|
| 1 | (5, 22) |
| 2 | (35, 6) |
| 3 | (35, 74) |
| 4 | (96, 40) |

**Team B — Spread:**

| Cluster | Centre |
|---------|--------|
| 1 | (26, 26) |
| 2 | (26, 54) |
| 3 | (66, 22) |
| 4 | (66, 58) |

### 3.2 Single-scale failure (Figure 6)

**A_LINE — linear deployment:**

Clusters at (10, 40), (40, 40), (80, 40), (105, 40).

At δ = 35: **both** A_WIDE and A_LINE have β₀ = 2, β₁ = 0 — identical component counts, but W₁(A_WIDE, A_LINE) = 42.12.

### 3.3 Generalised domain configurations (Figure 5)

As in the original specification: tumour–immune, predator–prey, autonomous fleet. Attacking-side barcodes retain the 8–2–1 hierarchy pattern; defending-side barcodes differ.

---

## 4. Reference values (verify any reimplementation)

These values are reproducible with noise = 0 for H₀; time-series results use σ = 1.5 and the stated seed scheme.

```
H₀(A_WIDE)   = [4.00×4, 4.03×4, 32.56, 32.56, 60.00]
H₀(A_NARROW) = [4.00×4, 4.03×4, 12.66, 12.66, 12.66]
H₀(A_LINE)   = [4.00×4, 4.03×4, 21.00, 26.00, 36.00]

W₁(A_WIDE, A_NARROW) = 76.13   [exact OT; naive sorted matching gives 87.15]
W₁(A_WIDE, A_LINE)   = 42.12

H₁(B_RING)                    = [27.24, 40.00], persistence 12.76
H₁(B_RING + trapped A cluster) = empty
H₁(B_RING + escaped A cluster) = [27.24, 40.00], persistence 12.76

Pitch diameter = √(120² + 80²) = 144.22   [T1 integrability bound]

At δ = 35: A_WIDE and A_LINE both have (β₀, β₁) = (2, 0)

CUSUM (5% false-alarm calibration): T̂ = 54, error = 4  (headline seed 7)

Fréchet mean global feature, pre-transition:  ≈ 58.6 δ-units
Fréchet mean global feature, post-transition: ≈ 13.4 δ-units
```

**Display scales for multi-scale figures:** δ₁ = 4.5, δ₂ = **40**, δ₃ = 66.  
(Previous δ₂ = 22 fell below all A_WIDE tactical deaths and duplicated δ₁.)

### Monte Carlo T2 validation (Figure 8)

1000 realisations per condition; E[|T̂ − T*|] decreases as the W₁ jump increases:

| Jump W₁ | E\|T̂ − T*\| | Median | Power |
|---------|-------------|--------|-------|
| 25.3 | 19.0 | 17.0 | 6.2% |
| 50.2 | 11.6 | 6.0 | 15.1% |
| 66.1 | 5.2 | 5.0 | 67.9% |
| 76.1 | 3.8 | 4.0 | 98.7% |

---

## 5. Figure inventory

All figures saved as 300 DPI PNG to `OUTPUT_DIR` (script directory).

| File | Content |
|------|---------|
| fig1_multiscale.png | Multi-scale framework at δ₁, δ₂, δ₃ with barcodes |
| fig2_adversarial_coupling.png | Scale-specific adversarial coupling |
| fig3_phase_transition.png | Phase transition + T2 CUSUM detection |
| fig4_frechet_diagram_mean.png | Diagram $W_2$ Fréchet mean: stability and variance (T1 analogue) |
| fig5_generalised.png | Framework universality across four domains |
| fig6_singlescale.png | Single-scale failure case |
| fig7_dependence.png | Coin-flip vs tug-of-war dependence structure |
| fig8_montecarlo_cusum_delay.png | Monte Carlo localisation delay for diagram-$W_1$ CUSUM (T2 analogue) |
| fig9_h1_encirclement.png | H₁ from adversarial embedding (encirclement) |
| fig10_gtppf_switching.png | Possession switching inverts predator and prey (Python) |

---

## 6. Connections to grant objectives

### 6.1 T1 — Fréchet mean well-posedness

The bounded pitch (diameter ≈ 144 units) makes all H₀ deaths finite. The sliding-window Fréchet mean (W₂, on diagrams) is stable in each steady-state phase, spikes at the transition, and recovers. This is the diagram-valued analogue of T1; the V&A statement is convergence of the empirical mean path in landscape space.

### 6.2 T2 — Wasserstein stability for CUSUM

The phase transition at T* = 50 creates W₁ ≈ 76 between pre- and post-transition A_WIDE/A_NARROW diagrams. CUSUM on that **diagram-W₁** series detects near T* with calibrated 5% false-alarm control. Figure 8 (1000 realisations per jump size) confirms E[|T̂ − T*|] decreases as the W₁ jump increases, which is the qualitative content of T2's localisation bound. The V&A theorem is the same bound for a **landscape-valued** CUSUM; this toy computation is the diagram-valued analogue (and the stated R3 fallback). Do not quote a single-run T̂ as the proof of principle — the Monte Carlo curve is.

### 6.3 Multi-scale requirement (Figure 6)

Two configurations with identical β₀ at δ = 35 are separated by W₁ ≈ 42 in the full barcode.

### 6.4 Framework universality (Figure 5)

The same three-level persistence structure appears across football, tumour–immune, predator–prey, and autonomous domains.

### 6.5 H₁ beyond hierarchy (Figure 9)

Encirclement produces a persistent H₁ loop that is destroyed when an opponent cluster penetrates the ring — a feature invisible to H₀ alone.

### 6.6 GTPPF switching (Figure 10)

Possession $b(t)$ inverts predator and prey. Encirclement $H_1$ tracks the pressing team; CUSUM localises both switches. This is the football analogue of telegraph-noise competitive systems (Nguyen–Du–Yin 2014) on which the Standard Grant would rest.

---

## 7. MATLAB implementation notes

### 7.1 Requirements

- **MATLAB R2020b or later** (for `exportgraphics`, `subtitle`, `tiledlayout`)
- Built-in: `matchpairs` (R2019a), `graph` — no Statistics Toolbox required
- Persistent homology computed from first principles (Prim MST for H₀; GF(2) VR for H₁)

### 7.2 Key function signatures

```matlab
pts  = tri_cluster(cx, cy, r)           % 3×2 cluster template
deaths = compute_h0(pts)                % (N−1)×1 sorted deaths
d    = wasserstein_p(d1, d2, p)         % exact W_p (p=1 or 2)
mu   = frechet_mean(diags)              % W2 barycentre (cell array in)
[A,B] = get_config(t, ...)              % agent positions at time t
[C, T_hat] = run_cusum(w_series, kappa, h)
[~, h1] = vr_persistence(pts, max_delta)
[sA, sB] = coupled_series(A0, B0, T, ...)  % dependence experiment
```

### 7.3 Revision history (August 2026)

Corrections since the initial delivery:

1. A_NARROW cluster spacing fixed to uniform 16 units (was 16/20/16)
2. Wasserstein: exact optimal transport via `matchpairs`, not sorted matching
3. Fréchet mean/variance: W₂ throughout (Turner et al.)
4. Noise: Gaussian (`randn`), not uniform
5. CUSUM: Monte Carlo calibration for 5% false-alarm rate
6. Display scale δ₂ = 40 (was 22)
7. Figure 7: stationary coupled vs independent comparison
8. Figures 8 (Monte Carlo T2) and 9 (H₁ encirclement) added

---

## 8. Development directions

### 8.1 Immediate extensions

- **MATLAB App Designer:** δ slider, time slider, live barcode, CUSUM display
- **Ultrametric distance u_GH:** Mémoli–Smith–Wan dendrogram comparison metric

### 8.2 Standard Grant extensions

- Mean-field Fokker–Planck limit for T1
- Topology-conditional switching rate $\lambda(X,b)=\lambda_0+\lambda_1 f(\varphi(X))$ (Chat 2)
- Cross-domain O1 stability gate (threshold 0.80)

---

## 9. Key mathematical references

1. Carlsson & Mémoli (2010) JMLR 11:1425 — ultrametric/dendrogram correspondence
2. Cohen-Steiner et al. (2007) DCG 37:103 — W₁ stability
3. Chazal et al. (2014) SoCG 474 — landscape convergence (T1)
4. Turner et al. (2014) DCG 52:44 — Fréchet means (W₂)
5. Cao & Monod (2025) CG 128:102162 — Fréchet mean uniqueness
6. MacPherson & Schweinhart (2012) JMP 53:073516 — H₁ from embedding
7. Schindler & Barahona (2025) arXiv:2305.04281 — H₁ from cluster conflicts
8. Skraba & Turner (2024) arXiv:2006.16824 — Wasserstein stability (T2)
9. Page (1954) Biometrika 41:100 — CUSUM
10. Nguyen, Du & Yin (2014) JDE 257:2078 — switching competitive systems
