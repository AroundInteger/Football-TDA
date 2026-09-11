# Numerical backing of the three cutoffs

Refresh: `python quantify.py` writes `outputs/dossier.json`.
Source tables: SkillCorner primary-match sweep,
`paper_A_JACT/pipeline/outputs/cutoff_sweep_{agg,results}.csv`.
Paper A locked values are not changed by this note.

## Verdict

None of the three adopted cutoffs is the unrestricted argmax of a
clustering-quality metric on the SkillCorner sweep that Paper A
plots as Figure 2.

| Adopted $\delta$ | What backs it | What does not |
|---|---|---|
| $2.98$ m | Inherited Calinski–Harabasz (CH) cross-epoch mean from the SecondSpectrum GPS 58-window study. On SkillCorner it sits in the prior individual $H_0$ band $15$–$22$. | SkillCorner CH. That peak is $1.39$ m. |
| $12.0$ m | Football-zone heuristic (half a standard zone width), kept after a 50-frame single-frame check against $16.31$ m. | Silhouette, information-content (IC), or CH on either corpus. |
| $30.0$ m | Right endpoint of `np.linspace(0.5, 30.0, 100)`, returned by "minimum IC among rows with team-validation rate $>0.9$". | The earlier team IC optimum $28.11$ m. Silhouette prefers $\approx 22$ m ($k=2$). |

The named tactical disagreement $[6.87, 16.31]$ m is also inherited
from SecondSpectrum. It is not the pair of SkillCorner argmax
points on Figure 2 panel (b).

## Two corpora, two window counts

The 58-window, 30% coverage design belongs to the December 2024
SecondSpectrum GPS investigation
(`02_tda_core/METHODOLOGY_CUTOFF_DISTANCE_SELECTION.md`;
$150{,}214$ frames): 31 + 16 + 7 + 4 windows.

The committed SkillCorner sweep is the same *rule* (30% of
non-overlapping windows, four epoch lengths, 100 cutoffs on
$[0.5, 30.0]$ m) on a shorter match ($43{,}531$ complete frames).
It yields 21 + 10 + 4 + 3 = **38** windows, 3{,}800 rows.
Paper A's Figure 2 caption currently says 58. That is the older
design, not this table.

SkillCorner information-content in the CSV is Shannon entropy of
the cluster-size distribution. The SecondSpectrum "$6.87$" and
"$28.11$" used *goal-specific* IC scores that reward a target
$H_0$ band. Those are different functions.

## Circularity of $H_0$-band validation

`EXPECTED_H0` is hard-coded as $(15,22)$, $(2,12)$, $(1,3)$ before
the sweep. A window is "validated" if its cluster count lands in
that band. A cutoff is then called validated if the mean count
does.

On the SkillCorner aggregate, the prior bands occupy wide
intervals of $\delta$:

| Prior band | $\delta$ interval with mean $H_0$ in band | Width | Grid points |
|---|---|---|---|
| Individual $15$–$22$ | $[0.50, 5.27]$ m | $4.77$ m | 17 |
| Tactical $2$–$12$ | $[7.06, 21.95]$ m | $14.90$ m | 51 |
| Team $1$–$3$ | $[15.40, 30.00]$ m | $14.60$ m | 50 |

Tactical and team overlap on $[15.40, 21.95]$ m. Band membership
therefore does not pick a unique triple. It only says that the
adopted values are *consistent* with the priors. The priors
themselves come from the 22-player roster (individual near the
full set; team one or two sides; tactical the remainder), not
from a clustering metric.

## Individual: $2.98$ m

**Paper A statement.** Carried from an earlier
normalised-coverage calibration. Retained because mean $H_0$ sits
in $15$–$22$. SkillCorner CH optimum $1.39$ m is not adopted.

**What the SkillCorner table actually does at $2.98$ m.**
Nearest grid point $2.88$ m. Mean $H_0 = 19.16 \pm 2.07$.
Stability (fraction of windows with $|H_0 - \mathrm{median}| \le 2$
inside $\pm 0.5$ m) $= 0.875$. Individual validation rate $0.947$.
CH is already well below its peak (mean CH $349$ versus $649$ at
$1.39$ m).

**What produced $2.98$ originally.** SecondSpectrum GPS,
restricted search $[0.5, 3.0]$ m, CH argmax on each epoch, then
the mean: $2.98 \pm 0.37$ m
(`NORMALIZED_SAMPLING_RESULTS_COMPARISON.md`). That is a real
metric calculation. It is not a calculation on the SkillCorner
figure.

**What SkillCorner would pick under the same rules.**

| Rule | $\delta$ (m) | Mean $H_0$ |
|---|---|---|
| Unrestricted CH argmax | $1.39$ | $21.03$ |
| CH argmax restricted to $[0.5, 3.0]$ m | $1.39$ | $21.03$ |
| Mean of per-epoch CH argmax | $1.10$ | (mixed) |

The SkillCorner CH peak is finer than $2.98$ m on every rule we
can run from the committed table. Keeping $2.98$ is an
inheritance-plus-band decision, not a SkillCorner optimum.

## Tactical: $12.0$ m

**Paper A statement.** Automated metrics disagree ($16.31$ versus
$6.87$ m). $12.0$ m is half a football zone width and sits inside
that range. Stability $0.836$.

**What the SkillCorner table actually does at $12.0$ m.**
Nearest grid point $12.12$ m. Mean $H_0 = 4.71 \pm 2.10$.
Stability $0.836$. Tactical validation rate $1.00$. Silhouette
$0.262$, which is a *local dip* between peaks at $7.65$ m
(mean $H_0 \approx 10.7$) and $21.95$ m (mean $H_0 = 2.0$).

**Where $6.87$ and $16.31$ come from.** SecondSpectrum GPS, not
this sweep.

- $16.31 \pm 0.52$ m: mean of per-epoch silhouette argmax. The
  same note lists the tactical search band as $8$–$15$ m, so the
  published optimum already sits outside its own search band.
- $6.87$ m: goal-specific *tactical* IC (rewards $H_0$ in
  $0.2$–$0.5$ of $22$ players, i.e. $5$–$11$). That function is
  not the entropy column in `cutoff_sweep_agg.csv`. Unrestricted
  SkillCorner entropy IC is maximised at the left grid edge
  ($0.5$ m) and minimised at the right edge ($30.0$ m).

**What SkillCorner would pick under restricted tactical rules.**

| Rule | $\delta$ (m) | Mean $H_0$ |
|---|---|---|
| Silhouette max in $H_0 \in [2,12]$ | $21.95$ | $2.00$ |
| Entropy IC max in $H_0 \in [2,12]$ | $7.06$ | (band edge) |
| Silhouette max in $\delta \in [8,15]$ m | $14.80$ | $3.16$ |
| Entropy IC max in $\delta \in [8,15]$ m | $8.25$ | $9.61$ |
| First silhouette peak (prominence $0.01$) | $7.65$ | $10.71$ |

None of these is $12.0$, $6.87$, or $16.31$.

**Independent (non-metric) backing for $12.0$.**
`TACTICAL_CUTOFF_OPTIMIZATION_REPORT.md`: on 50 single frames,
$16.31$ m put mean $H_0$ at $2.82$ and only $62\%$ of frames in
the *strict* band $3$–$12$; $12.0$ m put mean $H_0$ at $4.84$ and
$96\%$ in $3$–$12$. The prior band was then widened to $2$–$12$
so that compact $k=2$ frames also count. That is a single-frame
$H_0$-band check, still circular in the same sense, but it is the
only numerical argument that actually compared $12.0$ to $16.31$
on instantaneous frames.

The zone-width sentence is a heuristic, not a derivation.

## Team: $30.0$ m

**Paper A statement.** Automated metrics select directly.
Stability $1.000$. $H_0$ band $1$–$3$.

**What the SkillCorner table actually does at $30.0$ m.**
This *is* a grid point. Mean $H_0 = 1.42 \pm 0.50$. Stability
$1.000$. Team validation rate $1.00$. Mean entropy IC is the
global minimum ($0.112$). Silhouette has already fallen from its
global max ($0.468$ at $21.95$ m to $0.238$).

**How `identify_regimes` picks it.** Keep rows with
`val_team > 0.9`, then take minimum mean IC. Entropy of cluster
sizes falls as the cloud merges, so the rule returns the largest
admissible $\delta$. On this grid that is $30.0$ m.

**What produced $28.11$ originally.** SecondSpectrum GPS,
goal-specific *team* IC, cross-epoch mean $28.11 \pm 0.47$ m.
The same note lists the team search band as $15$–$25$ m, so
$28.11$ also sits outside its own search band. Drafts used
$28.11$ until the H1 pipeline standardised on $30.0$.

**What SkillCorner would pick under alternative team rules.**

| Rule | $\delta$ (m) | Mean $H_0$ |
|---|---|---|
| Global silhouette max | $21.95$ | $2.00$ |
| First $\delta$ with mean $H_0 \le 2$ | $21.95$ | $2.00$ |
| Min entropy IC in $[15,25]$ m | $24.93$ | $1.82$ |
| Mean of per-epoch IC argmin | $29.03$ | (near the edge) |
| `identify_regimes` as coded | $30.00$ | $1.42$ |

$30.0$ m is defensible as "merge until the two sides remain, on a
grid that stops at $30$". It is not an interior critical point of
silhouette or of CH.

## What would have to be true for a mathematical derivation

A cutoff rule that does not lean on a pre-set $H_0$ band needs
one of the following, computed on a declared corpus and windowing
scheme:

1. An interior critical point of a clustering-quality functional
   (CH, silhouette, gap statistic) whose location is stable across
   matches.
2. A change-point in the $H_0(\delta)$ curve that is not inherited
   from the grid endpoints.
3. The persistence-landscape stability criterion already deferred
   in Paper A Section 4.3: minimise path variation under small
   perturbations of $\delta$. Sample size is the number of
   matches.

On the present SkillCorner table, (1) and (2) do not recover
$2.98$, $12.0$, or $30.0$. Item (3) has not been run.

## Implications for Paper A (no edits in this slice)

1. Figure 2 caption: the sweep behind the figure is 38 windows,
   not 58.
2. The disagreement interval $[6.87, 16.31]$ m should be attributed
   to the SecondSpectrum calibration, or replaced by SkillCorner
   numbers if we want Figure 2 to be self-contained.
3. "$30.0$ m is selected by automated metrics" overstates the
   SkillCorner rule. The coded rule returns the grid edge.
4. The individual value is an inherited CH optimum. Saying so
   once, as the draft now does, is accurate. Calling all three
   "validated by the sweep" is not.

Downstream claims (operative $H_1$ range $[6,14]$ m, two $H_1$
regimes, team $H_1$ vanishing for $k\in\{1,2\}$) are conditional
on these cutoffs. They remain internally consistent. They do not
independently justify the cutoffs.

## Next slice (not started)

- Ten-match SkillCorner sweep under the same 30% rule; report
  whether $1.39$, $7.65$, and $21.95$ recur.
- Agreement of adopted $\delta$ on $\tilde{T}$ (150 frames/match)
  versus the 38-window sweep.
- Reconstruct $6.87$ / $16.31$ / $28.11$ from the original
  SecondSpectrum tables if those files are still in the repo.
- Gap statistic and landscape-stability selectors, as alternatives
  that do not use `EXPECTED_H0`.
