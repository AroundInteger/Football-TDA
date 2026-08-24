# T1-lite and T2-lite (diagram analogues)

UK English. These are the **Tier 2** claims of the methods note: proved under stated hypotheses, not the landscape T1/T2 of the Small Grant. Full competitive dependence is **Tier 3** (conjecture + Monte Carlo).

Notation. A birth-zero $H_0$ diagram of cardinality $K$ is identified with its sorted death vector $d\in\mathbb{R}_+^K$. Ground cost is $L^\infty$ on the birth–death plane: matching $d_k$ to $e_\ell$ costs $|d_k-e_\ell|$; matching $d_k$ to the diagonal costs $d_k/2$. Then
\[
W_p(d,e)^p
=\min_{\text{assignments}}\Bigl(\text{partner costs}^p+\text{diagonal costs}^p\Bigr).
\]
When the optimum uses no diagonal slot, this is $p$-Wasserstein on the line and the monotone (sorted) matching is optimal.

---

## Lemma T1-lite ($W_2$ barycentre)

**Hypothesis (H1).** Diagrams $d^{(1)},\dots,d^{(n)}\in\mathbb{R}_+^K$ have equal cardinality. There is a neighbourhood of $\mu$ in which, for every $i$, the $W_2$-optimal matching between $d^{(i)}$ and $\mu$ does not use the diagonal.

**Claim.** The Fréchet functional
\[
F_2(\mu)=\frac1n\sum_{i=1}^n W_2\bigl(d^{(i)},\mu\bigr)^2
\]
is uniquely minimised at
\[
\mu_{2,k}=\frac1n\sum_{i=1}^n d^{(i)}_{\,(k)},\qquad k=1,\dots,K
\]
(the coordinatewise mean of the order statistics).

**Proof.** Under (H1), $W_2^2(d^{(i)},\mu)=\sum_k\bigl(d^{(i)}_{(k)}-\mu_k\bigr)^2$ by the rearrangement theorem on $\mathbb{R}$. Then $F_2(\mu)=\sum_k\bigl(\tfrac1n\sum_i(d^{(i)}_{(k)}-\mu_k)^2\bigr)$ separates across coordinates. Each summand is ordinary least squares, with unique minimiser the sample mean. Uniqueness of $\mu_2$ follows.

**Remarks.**

1. (H1) fails if some deaths are cheaper to send to the diagonal than to their sorted partner. That is the reason the implementation uses exact assignment, not sort-and-match, for $W_p$ in general. For the ecology and robotics generators the noise-free deaths are bounded away from zero relative to their gaps, and (H1) is checked numerically in the sliding window (no diagonal used at the reported $\mu_2$).
2. This is the one-dimensional special case of Turner et al. (2014), written so we do not import their general geodesic-on-diagram-space machinery.
3. The same vector $\mu_2$ does **not** minimise $F_1(\mu)=\frac1n\sum_i W_1(d^{(i)},\mu)^2$.

---

## Proposition (first-order $W_1$–$W_2$ gap)

**Hypothesis (H2).** In death space, $d^{(i)}=\theta+\varepsilon Z^{(i)}$ with $\mathbb{E}Z=0$, (H1) holding uniformly for $\varepsilon$ small, and $W_1$ likewise using the sorted matching.

**Claim.** Write $\mu=\theta+\varepsilon\nu$. Then $F_1(\mu)=\varepsilon^2\,\mathbb{E}\lVert Z-\nu\rVert_1^2$, so the $W_1$ Fréchet minimiser is $\mu_1=\theta+\varepsilon\nu_1$ with $\nu_1=\mathrm{argmin}_\nu\mathbb{E}\lVert Z-\nu\rVert_1^2$, independent of $\varepsilon$ at leading order. The $W_2$ barycentre is $\mu_2=\theta+o(1)$ in the population limit (or $\theta+\varepsilon\bar Z$ in finite samples). Hence:

- coordinate gap $\lVert\mu_1-\mu_2\rVert_\infty=\Theta(\varepsilon)$;
- relative objective gap $\bigl(F_1(\mu_2)-F_1(\mu_1)\bigr)/F_1(\mu_1)$ is $\Theta(1)$ in $\varepsilon$ (it does not vanish as $\varepsilon\to0$).

**Check.** Death-space Monte Carlo around the ecology dispersed diagram (see `numbers.json` `t1_lite`) reproduces a few-percent objective gap at $\sigma=1.2$, matching the football-toy verification, and a global-feature coordinate gap $\ll 1$ unit.

This is not a substitute for convergence of the *landscape-valued* empirical mean path (grant T1). It justifies reporting $\mu_2$ as the working mean of diagrams, with a controlled $W_1$ discrepancy in the small-noise window.

---

## Proposition T2-lite (Wald delay, coin-flip increments)

Let $D_{\mathrm{ref}}$ be a fixed pre-change diagram (the noise-free dispersed prey cloud, or its $W_2$ mean). The **persistent** statistic is
\[
\xi_t=W_1(D_t,D_{\mathrm{ref}}).
\]
One-sided Page CUSUM: $C_t=\max(0,C_{t-1}+\xi_t-\kappa)$, alarm $\hat T=\inf\{t\ge t_{\mathrm{mon}}:C_t\ge h\}$.

**Hypothesis (A1) coin-flip.** Within each regime, the increments of $\xi_t$ are uncorrelated. This is the independent-displacement generator. It is **not** claimed for consecutive-frame $W_1(D_t,D_{t-1})$, which shares a diagram between neighbouring terms and is autocorrelated even under coin-flips. It is **not** claimed for the tug-of-war generator.

**Hypothesis (A2) stability.** If every agent moves by at most $\varepsilon$ in Euclidean norm, each MST death moves by at most $2\varepsilon$, hence $W_1(D(X),D(X'))\le 2(N-1)\varepsilon$ (Cohen–Steiner / Lipschitz of $H_0$ deaths). After $T^*$, $\mathbb{E}[\xi_t]=m_1$ satisfies
\[
m_1 \ge J - 2(N-1)\varepsilon,
\]
where $J=W_1(D_{\mathrm{pre}},D_{\mathrm{post}})$ is the noise-free jump.

**Claim.** Let $\delta=m_1-\kappa>0$. Under (A1) and an *instantaneous* post-change mean, the Wald/Siegmund approximation for a one-sided CUSUM is
\[
\mathbb{E}[\hat T-T^*\mid \text{detection}] \;\approx\; \frac{h}{\delta}.
\]
The generators in this note use a smoothstep of several frames, so the mean of $\xi_t$ is not a step. The operational predictor is the noise-free CUSUM evaluated along the interpolant (the first $t$ at which that path hits $h$). Wald $h/\delta$ is the instantaneous special case of that path and is too optimistic when $J\gg\kappa$. Overlay both on Monte Carlo of $\xi_t$ (Figure 5). The plug-in $\delta_{\mathrm{plug}}=\max(J-\kappa,0)$ remains the explicit large-jump formula.

**What this is not.**

- Not grant T2 (landscape CUSUM, Wasserstein stability of the *detection error under dependence*).
- Not a theorem on consecutive-frame $W_1$. That statistic sees a *pulse* during the smoothstep, then returns to a noise floor; delay is then bounded by the transition length when $J$ is large, which is a different calculation. Consecutive-frame CUSUM remains an operational detector (Figure 3); T2-lite is stated for $\xi_t$.
- Under tug-of-war, (A1) fails. Figure 4 and the lag-1 correlations are the computational evidence that the qualitative CUSUM behaviour can survive; that is Tier 3.

---

## How the Standard Grant sits

| Tier | Claim | Status in this note |
|------|--------|---------------------|
| 1 | Cohen–Steiner; Carlsson–Mémoli; Page | Cited |
| 2 | T1-lite; $W_1$–$W_2$ gap; T2-lite on $\xi_t$ under (A1)–(A2) | Proved / approximated here |
| 3 | Fréchet well-posedness and CUSUM localisation under genuine adversarial dependence; landscape T1/T2 | Conjecture; Monte Carlo; Small Grant theorems |
