# Paper C staging — consistency log

UK English. Single pass, 21 August 2026. Working directory: this folder. No commit. No PR. No edit outside this folder. `numbers.json` was **not** rewritten.

`--verify` prints noise-free H0 / $W_1$ / Betti / $H_1$ only. Monte Carlo, headline CUSUM, T1-lite, and $\rho_1$ are **not** recomputed; they are checked against the stored `numbers.json` from a prior full run.

## Ran

```bash
cd "08_current/Paper Updated/3-Paper Paradigm/paper_C_methods"
python experiments.py --verify
```

- Exit code: **0**.
- Import path: `generators.py` / `experiments.py` insert `08_current/grant/evidence/toy_models/` and import `atda_core`. Import succeeded; `atda_core.py` was not edited.
- Stdout (noise-free) agrees with `numbers.json` at the printed two-decimal rounding. Full Monte Carlo was **not** run (forbidden on this pass). `--quick` was **not** run (it would overwrite `numbers.json` and drop the stored MC tables).
- T2-lite naming in `draft.md` and `lemmas.md` already uses $\xi_t=W_1(D_t,D_{\mathrm{ref}})$; consecutive-frame $W_1$ is labelled operational. No lemma edit.
- No `tex/` skeleton (time spent on the number check).

## Fixed

| Location | Old quote | Source | New quote |
|----------|-----------|--------|-----------|
| `draft.md` §4 robotics Monte Carlo | “at jumps $\gtrsim 70$, power $100\%$ and mean error $\approx 2.2$” | `numbers.json` `robotics.mc` rows $\alpha\in\{0.55,0.75,1.0\}$: jumps $75.96$, $78.51$, $70.64$; mean absolute errors $2.755$, $2.17$, $2.16$ (all power $1.0$) | “at jumps $76.0$, $78.5$, and $70.6$, power $100\%$ and mean errors $2.8$, $2.2$, and $2.2$” (one-decimal, same convention as the ecology table) |

`lemmas.md`: no change. `numbers.json`: no change (`--verify` did not disagree).

## Leftover

- **Figures.** Regenerated after this log (`python experiments.py --quick`). `--quick` now overlays stored MC from `numbers.json` and does **not** rewrite that file. Panels: `figures/fig1_ecology_territory.png` … `fig5_t2_lite.png`.
- **`--verify` does not recompute** headline $\hat T$, ecology/robotics MC, `mc_ref_xi`, `t1_lite`, or $\rho_1`. Those quotes rest on stored JSON, not this run’s stdout.
- **`experiments.py` print label** `=== Consecutive-frame CUSUM Monte Carlo ===` (renamed after this log; previously `=== T2 Monte Carlo ===`).
- **`rho1_coupled` / `rho1_independent`** in JSON are a single realisation; the draft quotes the 80-replicate means (`rho1_*_mean_80`). Do not swap them.
- **Hard-coded 80-replicate $\rho_1$** in `experiments.py` (`0.296`, `0.139`, `-0.025`, `0.106`) is not recomputed by `--verify`.
- **Noise-free $W_1$ (hunt, ring)** prints as $55.87$ and is not in `numbers.json` or the draft. Harmless extra; do not promote it to a claim on this pass.
- **Integer diameter $187$** in the draft is hypot$(180,50)=186.82$ rounded. Left as display rounding.
- Optional `tex/` skeleton not added.
- Sequence lock unchanged: develop after A/B submit; do not cite C from A; do not copy these generator numbers into JeS or A/B `results.tex`.

---

## Checked numbers (pass / fixed / leftover)

Rounding: two decimals unless the draft already uses a coarser display. MC means: one decimal, matching the ecology table. `--verify` column is stdout vs JSON; draft column is quote vs JSON (and vs stdout where `--verify` prints the quantity).

### Abstract

No numeric results. T2-lite named as $\xi_t$. **Pass.**

### §2 (quoted in draft; not required by the brief’s §§3–5 list)

| Quote | JSON / code | Verdict |
|-------|-------------|---------|
| Relative $W_1$–$W_2$ gap “about $6\%$” at $\sigma=1.2$ | `t1_lite` $\sigma=1.2$: `rel_obj_gap_pct` $6.287$ | Pass (about) |
| Global-feature shift $0.06$ | `global_feature_gap` $0.05544$ | Pass (two-decimal) |
| Encirclement birth max $80$, not $45$ | `ecology.birth_max` $80$; `--verify` | Pass |
| $5\%$ false-alarm calibration | code: $0.95$ quantile of in-control peaks | Pass vs code; not in `--verify` stdout |

`lemmas.md` T1-lite check (“few-percent … $\sigma=1.2$”, gap $\ll 1$) is qualitative and consistent. T2-lite is on $\xi_t$; consecutive-frame is not the theorem. **Pass.**

### §3 Ecology — geometry and noise-free H0 (`--verify` + JSON)

| Quote | Source | Verdict |
|-------|--------|---------|
| $\Omega=[0,240]\times[0,180]$, diameter $300$ | stdout $300.00$; JSON `diameter` $300.0$ | Pass |
| Prey $r=3.5$, $N=15$ | `generators.py` `R_PREY`, stdout $N=15$ | Pass |
| Predators $r=2.8$, $N=12$ | `R_PRED`; stdout | Pass |
| $T^*=55$, smoothstep to $t=64$, $\sigma=1.8$ | `ECO_T_STAR`, `ECO_T_END`, `ECO_NOISE` | Pass vs code |
| Prey dispersed $7.00\times 5$, $7.05\times 5$, $87.49\times 4$ | stdout / JSON `H0_prey_dispersed` | Pass |
| Prey herded $7.00\times 5$, $7.05\times 5$, $17.00\times 2$, $20.18\times 2$ | stdout / JSON | Pass |
| Prey column $7.00\times 5$, $7.05\times 5$, $26.11\times 4$ | stdout / JSON | Pass |
| Predators hunting $5.60\times 4$, $5.64\times 4$, $74.98$, $81.60$, $86.66$ | stdout / JSON | Pass |
| Predator ring $5.60\times 4$, $5.64\times 4$, $62.46\times 3$ | stdout / JSON | Pass |
| $W_1(\mathrm{dispersed},\mathrm{herded})=212.16$ | stdout $212.16$; JSON $212.1638$ | Pass |
| Merge “$\approx 87$” | deaths $87.49$ | Pass |
| $\delta=16$, both $(\beta_0,\beta_1)=(5,0)$, $W_1=227.20$ | stdout / JSON `delta_conflate`, `betti_conflate`, `W1_dispersed_column` | Pass |
| $H_1$ bar $[62.46,90.40]$, persistence $27.94$ | stdout `[[62.46, 90.4]]`, pers. $27.94$; JSON $27.9448$ | Pass |
| Filled $H_1$ persistence $0$ | stdout $0.00$; JSON `H1_filled_pers` $0.0$ | Pass |

### §3 Ecology — CUSUM / MC (JSON only; not in `--verify` stdout)

| Quote | JSON | Verdict |
|-------|------|---------|
| Headline seed $7$, $\hat T=59$, $T^*=55$, error $4$ | `headline_T_hat` $59$, `headline_error` $4$, `T_star` $55$; seed in `HEADLINE_SEED` | Pass vs JSON/code |
| $N=200$ | `N_MC` in `experiments.py` | Pass vs code |
| Jump $112.9$, $\mathbb{E}|\hat T-T^*|$ $15.3$, median $10$, power $58.5\%$ | `mc[0]`: $112.886$, $15.299$, $10.0$, $0.585$ | Pass |
| $171.7$, $6.0$, $5$, $100\%$ | `mc[1]`: $171.661$, $5.98$, $5.0$, $1.0$ | Pass |
| $199.8$, $4.8$, $4$, $100\%$ | `mc[2]`: $199.847$, $4.76$, $4.0$, $1.0$ | Pass |
| $212.2$, $4.1$, $4$, $100\%$ | `mc[3]`: $212.164$, $4.055$, $4.0$, $1.0$ | Pass |
| Trailing window length $12$ | `WIN=12` | Pass vs code |
| Table is consecutive-frame, “not T2-lite” | `lemmas.md` / draft wording | Pass (naming) |
| Figure 5 $\xi_t$ overlay | `mc_ref_xi` stored; `figures/fig5_t2_lite.png` regenerated after this log | Pass (file now present) |

`mc_ref_xi` (T2-lite on $\xi_t$) is **not quoted** as a table in the draft. Do not paste it into A/B or JeS. Not a mismatch.

### §4 Robotics

| Quote | Source | Verdict |
|-------|--------|---------|
| $\Omega=[0,180]\times[0,50]$ | stdout “corridor 180 x 50” | Pass |
| Diameter $187$ | JSON / stdout $186.82$ | Pass (integer rounding); see Leftover |
| Pursuers $N=8$, evaders $N=6$ | stdout / JSON | Pass |
| Internal pair length $4.8$ | `2*R_PAIR` with `R_PAIR=2.4`; local deaths $4.80$ | Pass |
| $T^*=40$ | `ROB_T_STAR` | Pass vs code |
| $W_1(\mathrm{gate},\mathrm{chase})=7.00$ | stdout $7.00$; JSON $7.0$ | Pass |
| Evader $W_1(\mathrm{open},\mathrm{funnel})=70.64$ | stdout $70.64$; JSON $70.643$ | Pass |
| $\delta=12$, both $(\beta_0,\beta_1)=(3,0)$, $W_1=49.69$ | stdout / JSON `W1_open_file` $49.686$ | Pass |
| $N=200$; jump $48.4$, power $60\%$, mean error $4.0$ | `mc[0]`: $48.411$, power $0.6$, mean $3.95$ | Pass (one-decimal) |
| Jumps $\gtrsim 70$, mean error $\approx 2.2$ | `mc[1:4]` errors $2.755$, $2.17$, $2.16$ | **Fixed** (see Fixed) |

Football triangle $4.00$ / $4.03$ appears only as a contrast (“not the football triangle”). Not a Paper C result.

### §5 Dependence

| Quote | JSON | Verdict |
|-------|------|---------|
| $80$ replicates | `N_DEP=80`; keys `*_mean_80` | Pass vs code/JSON |
| Coupled $\rho_1=+0.296$ (s.d. $0.139$) | `rho1_coupled_mean_80`, `rho1_coupled_sd_80` | Pass |
| Independent $\rho_1=-0.025$ (s.d. $0.106$) | `rho1_independent_mean_80`, `rho1_independent_sd_80` | Pass |
| Statistic $W_1(D_t,D_{\mathrm{ref}})$; consecutive-frame excluded | draft + `lemmas.md` | Pass (naming) |

### Count

- Numbers checked: **52** distinct quoted quantities in the abstract and §§2–5 (including the four ecology MC rows as four blocks, and the robotics MC row that was fixed).
- Pass: 51 (after the one robotics MC wording fix).
- Fixed: 1 (`draft.md` §4).
- Leftover after the staging pass: `--verify` coverage gap for MC / $\hat T$ / T1-lite / $\rho_1$; unused hunt–ring $W_1$. Figures and the consecutive-frame print label were closed in a follow-up on the same day.

Stop. No second pass.
