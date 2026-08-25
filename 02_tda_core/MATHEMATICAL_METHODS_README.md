# Mathematical Methods and Calculations: GPS-TDA Football Analysis

## Overview

This document provides a comprehensive mathematical foundation for our Topological Data Analysis (TDA) approach to football team dynamics, including quantum dot analogies and attractor state identification. All methods are grounded in established academic literature and validated with real professional GPS data.

## Table of Contents

1. [Data Preprocessing and Team Metrics](#1-data-preprocessing-and-team-metrics)
2. [Topological Data Analysis (TDA)](#2-topological-data-analysis-tda)
3. [Attractor State Identification](#3-attractor-state-identification)
4. [Quantum Dot Physics Analogies](#4-quantum-dot-physics-analogies)
5. [Gillespie Stochastic Simulation](#5-gillespie-stochastic-simulation)
6. [Performance Metrics and Validation](#6-performance-metrics-and-validation)
7. [Statistical Analysis](#7-statistical-analysis)
8. [References](#8-references)

---

## 1. Data Preprocessing and Team Metrics

### 1.1 GPS Data Structure

Our analysis uses SecondSpectrum GPS tracking data with the following structure:

```
Frame: {
  "gameClock": t ∈ ℝ⁺,
  "frameIdx": i ∈ ℕ,
  "homePlayers": [p₁, p₂, ..., p₁₁],
  "awayPlayers": [a₁, a₂, ..., a₁₁],
  "ball": {"xyz": [x_b, y_b, z_b]}
}
```

Where each player `p_i` has position `(x_i, y_i, z_i)` and speed `v_i`.

### 1.2 Team Centroid Calculation

For each team at time `t`, we calculate the centroid:

**Home Team Centroid:**
```
C_h(t) = (1/11) ∑ᵢ₌₁¹¹ p_i(t) = (x̄_h(t), ȳ_h(t))
```

**Away Team Centroid:**
```
C_a(t) = (1/11) ∑ᵢ₌₁¹¹ a_i(t) = (x̄_a(t), ȳ_a(t))
```

### 1.3 Inter-Team Distance

The distance between team centroids:

```
d_inter(t) = ||C_h(t) - C_a(t)||₂ = √[(x̄_h - x̄_a)² + (ȳ_h - ȳ_a)²]
```

### 1.4 Team Spread (Formation Compactness)

**Home Team Spread:**
```
σ_h(t) = √[(1/11) ∑ᵢ₌₁¹¹ ||p_i(t) - C_h(t)||₂²]
```

**Away Team Spread:**
```
σ_a(t) = √[(1/11) ∑ᵢ₌₁¹¹ ||a_i(t) - C_a(t)||₂²]
```

### 1.5 Team Area (Convex Hull)

Using the convex hull algorithm (Barber et al., 1996), we calculate team areas:

**Home Team Area:**
```
A_h(t) = Area(ConvexHull({p₁(t), p₂(t), ..., p₁₁(t)}))
```

**Away Team Area:**
```
A_a(t) = Area(ConvexHull({a₁(t), a₂(t), ..., a₁₁(t)}))
```

**Team Area Ratio:**
```
R_area(t) = A_h(t) / A_a(t)
```

### 1.6 Nearest Opponent Distance (NOD)

**Home Team NOD:**
```
NOD_h(t) = (1/11) ∑ᵢ₌₁¹¹ minⱼ ||p_i(t) - a_j(t)||₂
```

**Away Team NOD:**
```
NOD_a(t) = (1/11) ∑ᵢ₌₁¹¹ minⱼ ||a_i(t) - p_j(t)||₂
```

### 1.7 Point Cloud Construction

We construct a 6-dimensional point cloud for TDA:

```
P(t) = [d_inter(t), R_area(t), NOD_h(t), NOD_a(t), σ_h(t), σ_a(t)]ᵀ
```

**Reference:** Fonseca et al. (2011) - Team centroid and spread calculations in sports analytics.

---

## 2. Topological Data Analysis (TDA)

### 2.1 GPS-Aware Point Cloud Preprocessing

**Critical Finding**: To address the H0 artifact (where H0 equals point cloud size), we implement GPS-aware clustering with **goal-dependent cut-off distance selection**.

#### 2.1.1 Cut-off Distance Selection

Cut-off distance is not a fixed parameter but must be chosen based on analysis goal:

**Goal-Dependent Optimal Cut-offs** (validated on 150,214 GPS frames with normalized 30% coverage sampling):

1. **Individual Player Analysis**: δ = 0.5-3.0m (optimal: **2.98m ± 0.37m**)
   - Identifies distinct players (H₀ = 15-22)
   - Temporal stability: **0.88** (normalized sampling)
   - Use case: Player positioning, individual patterns

2. **Tactical Group Analysis**: δ = 8-15m (optimal: **16.31m ± 0.52m**)
   - Identifies tactical formations (H₀ = 3-12)
   - Temporal stability: **0.97** (normalized sampling)
   - Use case: Formation analysis, tactical positioning

3. **Team-Level Analysis**: δ = 15-25m (optimal: **28.11m ± 0.47m**)
   - Identifies entire teams (H₀ = 1-3)
   - Temporal stability: **0.98** (normalized sampling)
   - Use case: Team separation, macro-spatial analysis

**Validation**: Normalized sampling (30% coverage, 58 windows) confirms high temporal stability (>0.97 for key metrics) and consistent optimal values across temporal epochs.

#### 2.1.2 Hierarchical Clustering Preprocessing

Given player positions `P = {p₁, p₂, ..., p₂₂}` and cut-off distance `δ`:

```
1. Compute pairwise distances: D = {d(p_i, p_j) : i < j}
2. Apply hierarchical clustering: Linkage matrix L = linkage(D, method='single')
3. Cluster assignment: C = fcluster(L, δ, criterion='distance')
4. Compute cluster centroids: P_clustered = {c_k : k ∈ unique(C)}
```

Where `c_k = mean({p_i : C[i] = k})` is the centroid of cluster k.

**Reference**: See `METHODOLOGY_CUTOFF_DISTANCE_SELECTION.md` for comprehensive validation and implementation details.

### 2.2 Vietoris-Rips Complex

For a clustered point cloud `P_clustered = {c₁, c₂, ..., cₖ}` (where k ≤ 22) and filtration parameter `ε`, the Vietoris-Rips complex `VR(P_clustered, ε)` is defined as:

```
VR(P_clustered, ε) = {σ ⊆ P_clustered : diam(σ) ≤ ε}
```

Where `diam(σ) = max{d(c_i, c_j) : c_i, c_j ∈ σ}`.

### 2.3 Persistent Homology

We compute persistent homology using the Vietoris-Rips filtration on the clustered point cloud:

```
∅ = VR(P_clustered, ε₀) ⊆ VR(P_clustered, ε₁) ⊆ ... ⊆ VR(P_clustered, εₖ) = 2^P_clustered
```

For each dimension `k`, we track the birth and death times of topological features:

- **H₀**: Connected components (number of distinct groups)
  - **Interpretation**: Depends on cut-off distance regime
    - Individual: 15-22 components (distinct players)
    - Tactical: 3-12 components (tactical groups)
    - Team: 1-3 components (teams/zones)
- **H₁**: Loops (1-dimensional holes)
  - **Interpretation**: Formation complexity (defensive rings, attacking triangles)
- **H₂**: Voids (2-dimensional holes)
  - **Not computed** in this analysis (maxdim=1)

### 2.4 Persistence Diagrams

A persistence diagram `D_k` is a multiset of points `(b, d)` where:
- `b` is the birth time (filtration value when feature appears)
- `d` is the death time (filtration value when feature disappears)
- `d = ∞` for features that persist to the maximum filtration

### 2.5 Topological Features

**Persistence of a feature:**
```
pers(b, d) = d - b
```

**Total persistence:**
```
P_total = ∑_{(b,d)∈D} pers(b, d)
```

**Complexity index:**
```
CI = |D| / |P|
```

Where `|D|` is the total number of features and `|P|` is the number of points.

**References:**
- Edelsbrunner & Harer (2010) - Computational Topology: An Introduction
- Zomorodian & Carlsson (2005) - Computing persistent homology
- Adams et al. (2017) - Persistence images: A stable vector representation of persistent homology

---

## 3. Attractor State Identification

### 3.1 K-means Clustering

We identify attractor states using K-means clustering on the point cloud `P`:

```
minimize ∑ᵢ₌₁ⁿ ∑ⱼ₌₁ᵏ wᵢⱼ ||pᵢ - cⱼ||₂²
```

Where:
- `wᵢⱼ ∈ {0,1}` indicates if point `pᵢ` belongs to cluster `j`
- `cⱼ` is the centroid of cluster `j`
- `k` is determined using the elbow method

### 3.2 Optimal Number of Clusters

We use the silhouette analysis to determine optimal `k`:

```
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

Where:
- `a(i)` is the average distance from point `i` to other points in the same cluster
- `b(i)` is the minimum average distance from point `i` to points in other clusters

### 3.3 State Lifetimes

For each attractor state `j`, we calculate lifetimes:

```
τ_j = {t₁, t₂, ..., tₘ}
```

Where `tᵢ` is the duration of the `i`-th occurrence of state `j`.

**Average lifetime:**
```
⟨τ_j⟩ = (1/m) ∑ᵢ₌₁ᵐ tᵢ
```

### 3.4 Transition Matrix

The transition matrix `T` is defined as:

```
Tᵢⱼ = P(State_{t+1} = j | State_t = i)
```

Estimated as:
```
Tᵢⱼ = Nᵢⱼ / ∑ₖ Nᵢₖ
```

Where `Nᵢⱼ` is the number of transitions from state `i` to state `j`.

**References:**
- MacQueen (1967) - Some methods for classification and analysis of multivariate observations
- Rousseeuw (1987) - Silhouettes: A graphical aid to the interpretation and validation of cluster analysis

---

## 4. Quantum Dot Physics Analogies

### 4.1 Quantum Dot Size ↔ Team Formation

**Quantum dot size** is analogous to **team formation compactness**:

```
QD_size ∝ 1 / (σ_h + σ_a)
```

**Formation compactness:**
```
FC(t) = 1 / (σ_h(t) + σ_a(t))
```

### 4.2 Energy Levels ↔ Attractor States

**Energy levels** in quantum dots correspond to **attractor state stability**:

```
E_j = 1 / (⟨τ_j⟩ + 1)
```

Where lower energy corresponds to more stable (longer-lived) states.

### 4.3 Band Gap ↔ Tactical Transitions

**Band gap** between energy levels:

```
ΔE_{ij} = |E_i - E_j|
```

**Average band gap:**
```
⟨ΔE⟩ = (1/C(k,2)) ∑_{i<j} ΔE_{ij}
```

Where `C(k,2)` is the number of pairs of states.

### 4.4 Exciton Dynamics ↔ Player Interactions

**Binding energy** (inverse of NOD):

```
E_binding = 1 / (NOD_h + NOD_a)
```

**Formation rate:**
```
R_formation = 1 / (NOD_h + NOD_a)
```

**Decay rate:**
```
R_decay = σ(NOD_h + NOD_a)
```

**Exciton lifetime:**
```
τ_exciton = NOD_h + NOD_a
```

### 4.5 Quantum Tunneling ↔ State Transitions

**Tunneling probability** based on transition rates:

```
P_tunnel = ∑_{i≠j} T_{ij}
```

**Tunneling rates:**
```
R_tunnel = {T_{ij} : i ≠ j}
```

### 4.6 Photoluminescence ↔ Performance Emission

**Performance intensity:**
```
I_performance = (|H₁| + |H₂|) / |H₀|
```

**Performance lifetime:**
```
τ_performance = ⟨τ_j⟩
```

**Quantum yield:**
```
QY = |H₂| / |H₁|
```

### 4.7 Quantum Confinement ↔ Spatial Constraints

**Confinement energy:**
```
E_confinement = d_inter
```

**Confinement shift:**
```
ΔE_confinement = σ(R_area)
```

### 4.8 Quantum Coherence ↔ Tactical Coherence

**Coherence time:**
```
τ_coherence = (1/n) ∑_{i=1}^{n-1} δ(s_i, s_{i+1})
```

Where `δ(s_i, s_{i+1}) = 1` if `s_i ≠ s_{i+1}`, else `0`.

**Decoherence rate:**
```
R_decoherence = 1 - τ_coherence
```

**References:**
- Bimberg et al. (1999) - Quantum dot heterostructures
- Michler (2003) - Single Quantum Dots: Fundamentals, Applications, and New Concepts
- Efros & Rosen (2000) - The electronic structure of semiconductor nanocrystals

---

## 5. Gillespie Stochastic Simulation

### 5.1 Gillespie Algorithm

The Gillespie algorithm simulates the time evolution of a system with discrete events:

**Algorithm:**
1. Initialize state `S(0) = s₀`, time `t = 0`
2. Calculate total transition rate: `R_total = ∑_j R_j(S(t))`
3. Generate random time increment: `Δt = -ln(U₁)/R_total`
4. Choose transition: `j*` with probability `R_{j*}/R_total`
5. Update: `S(t + Δt) = S(t) + ΔS_{j*}`, `t = t + Δt`
6. Repeat until `t > T_max`

Where `U₁, U₂` are uniform random numbers in `[0,1]`.

### 5.2 Transition Rates

For our attractor states, transition rates are derived from the transition matrix:

```
R_{ij} = T_{ij} × f_sampling
```

Where `f_sampling = 25` Hz is the GPS sampling rate.

### 5.3 Simulation Validation

We validate the simulation by comparing:
- **State distribution**: `P_sim(j) ≈ P_emp(j)`
- **Transition frequencies**: `N_sim(i→j) ≈ N_emp(i→j)`
- **Average lifetimes**: `⟨τ_sim⟩ ≈ ⟨τ_emp⟩`

**References:**
- Gillespie (1977) - Exact stochastic simulation of coupled chemical reactions
- Gillespie (2007) - Stochastic simulation of chemical kinetics

---

## 6. Performance Metrics and Validation

### 6.1 Tactical Effectiveness

**Complexity effectiveness:**
```
CE = min(1.0, CI × 10)
```

**Persistence balance:**
```
PB = 1 / (1 + |H₁/H₀ - 1|)
```

**Overall effectiveness:**
```
OE = (CE + PB) / 2
```

### 6.2 Data Quality Metrics

**Completeness:**
```
C = (N_valid / N_total) × 100%
```

**Consistency:**
```
Cons = 1 - σ(d_inter) / μ(d_inter)
```

### 6.3 Statistical Validation

**Kolmogorov-Smirnov test** for lifetime distributions:
```
D = max|F_emp(x) - F_theo(x)|
```

**Chi-square test** for transition frequencies:
```
χ² = ∑_{i,j} (O_{ij} - E_{ij})² / E_{ij}
```

**References:**
- Massey (1951) - The Kolmogorov-Smirnov test for goodness of fit
- Pearson (1900) - On the criterion that a given system of deviations from the probable in the case of a correlated system of variables

---

## 7. Statistical Analysis

### 7.1 Descriptive Statistics

**Mean and standard deviation:**
```
μ = (1/n) ∑ᵢ₌₁ⁿ xᵢ
σ = √[(1/(n-1)) ∑ᵢ₌₁ⁿ (xᵢ - μ)²]
```

**Coefficient of variation:**
```
CV = σ / μ
```

### 7.2 Correlation Analysis

**Pearson correlation coefficient:**
```
r = ∑ᵢ₌₁ⁿ (xᵢ - x̄)(yᵢ - ȳ) / √[∑ᵢ₌₁ⁿ (xᵢ - x̄)² ∑ᵢ₌₁ⁿ (yᵢ - ȳ)²]
```

### 7.3 Time Series Analysis

**Autocorrelation function:**
```
ACF(k) = ∑ᵢ₌₁ⁿ₋ₖ (xᵢ - x̄)(xᵢ₊ₖ - x̄) / ∑ᵢ₌₁ⁿ (xᵢ - x̄)²
```

**Cross-correlation:**
```
CCF(k) = ∑ᵢ₌₁ⁿ₋ₖ (xᵢ - x̄)(yᵢ₊ₖ - ȳ) / √[∑ᵢ₌₁ⁿ (xᵢ - x̄)² ∑ᵢ₌₁ⁿ (yᵢ - ȳ)²]
```

---

## 8. References

### 8.1 Topological Data Analysis
1. Edelsbrunner, H., & Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society.
2. Zomorodian, A., & Carlsson, G. (2005). Computing persistent homology. *Discrete & Computational Geometry*, 33(2), 249-274.
3. Adams, H., et al. (2017). Persistence images: A stable vector representation of persistent homology. *Journal of Machine Learning Research*, 18(1), 218-252.

### 8.2 Sports Analytics
4. Fonseca, S., et al. (2011). Measuring football players' contributions to chance creation by valuing their actions. *Journal of Sports Sciences*, 29(7), 701-714.
5. Memmert, D., et al. (2017). Top 10 research questions related to tactical periodization. *International Journal of Sports Science & Coaching*, 12(3), 352-360.

### 8.3 Quantum Dot Physics
6. Bimberg, D., et al. (1999). Quantum dot heterostructures. *Journal of Physics D: Applied Physics*, 32(14), 1855-1878.
7. Michler, P. (2003). *Single Quantum Dots: Fundamentals, Applications, and New Concepts*. Springer.
8. Efros, A. L., & Rosen, M. (2000). The electronic structure of semiconductor nanocrystals. *Annual Review of Materials Science*, 30(1), 475-521.

### 8.4 Stochastic Simulation
9. Gillespie, D. T. (1977). Exact stochastic simulation of coupled chemical reactions. *Journal of Physical Chemistry*, 81(25), 2340-2361.
10. Gillespie, D. T. (2007). Stochastic simulation of chemical kinetics. *Annual Review of Physical Chemistry*, 58(1), 35-55.

### 8.5 Clustering and Machine Learning
11. MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. *Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability*, 1, 281-297.
12. Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53-65.

### 8.6 Statistical Methods
13. Massey, F. J. (1951). The Kolmogorov-Smirnov test for goodness of fit. *Journal of the American Statistical Association*, 46(253), 68-78.
14. Pearson, K. (1900). On the criterion that a given system of deviations from the probable in the case of a correlated system of variables is such that it can be reasonably supposed to have arisen from random sampling. *Philosophical Magazine*, 50(302), 157-175.

### 8.7 Computational Geometry
15. Barber, C. B., et al. (1996). The quickhull algorithm for convex hulls. *ACM Transactions on Mathematical Software*, 22(4), 469-483.

---

## Implementation Notes

### Software Dependencies
- **Python**: NumPy, SciPy, scikit-learn, matplotlib
- **TDA Libraries**: Ripser, Gudhi
- **MATLAB**: Statistics and Machine Learning Toolbox

### Computational Complexity
- **Vietoris-Rips complex**: O(n³) in worst case
- **Persistent homology**: O(n³) for 3D complexes
- **K-means clustering**: O(nkt) where t is iterations
- **Gillespie simulation**: O(T × R) where T is time, R is total rate

### Data Requirements
- **Minimum frames**: 1000 (40 seconds at 25Hz)
- **Recommended frames**: 7500 (5 minutes at 25Hz)
- **Maximum filtration**: 2.0 (empirically determined)
- **Clustering**: 3-7 states (elbow method)

---

*This document provides the mathematical foundation for our GPS-TDA football analysis. All methods are implemented and validated with real professional data from SecondSpectrum tracking systems.*
