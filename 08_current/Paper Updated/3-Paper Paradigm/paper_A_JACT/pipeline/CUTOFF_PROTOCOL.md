# Cutoff protocol (Paper A)

Closed estimator. SkillCorner only. Code in `lib/cutoff_protocol.py`
implements this file line for line. Section 2.3 restates it. There is
no second rule in comments.

## Job

The class names three organisational levels by cardinality. The sweep
reads the metres that select those levels from the pooled \(H_0(\delta)\)
curve on this corpus. Clustering-quality metrics are diagnostics. They
do not pick \(\delta\).

## Inputs (a priori)

- Complete-frame roster \(n = 22\).
- Single-linkage hierarchical clustering. Team labels unused.
- Grid: \(\delta \in [0.25, 40.0]\) m at \(0.25\) m steps (160 points).

No SecondSpectrum. No GPS. No 30% random draw. No four mixed epochs.

## Corpus

All ten SkillCorner matches in Supplementary Table S1. Every complete
22-player frame, native 10 Hz.

## Estimator (pooled over every complete frame)

Let \(\overline{H_0}(\delta)\) be the mean cluster count at cutoff
\(\delta\), pooled over all complete frames of all ten matches. Let
\(P(k \ge 4;\delta)\) be the fraction of those frames with at least
four clusters.

- **Individual:** largest \(\delta\) with \(\overline{H_0}(\delta) \ge n-3 = 19\).
- **Tactical:** \(\delta\) minimising \(|\overline{H_0}(\delta) - 5|\), among
  candidates with \(P(k \ge 4;\delta) \ge 0.5\).
- **Team:** smallest \(\delta\) with \(\overline{H_0}(\delta) \le 2\).

Ties: take the smaller \(\delta\). That is the whole selector.

These three targets are roster statements, not SkillCorner-fitted metres.
“Mostly resolved agents” is \(n-3\). “A handful of coordinating groups,
loop-feasible” is 5, with \(k \ge 4\). “At most two envelopes” is 2.

## Acceptance (report; do not override)

At each adopted \(\delta\), every match’s mean \(H_0\) must lie in:

- individual \([15, 22]\)
- tactical \([4, 10]\)
- team \([1, 2.5]\)

Also invert each match separately and report the ten \(\delta^\star\)
values (mean \(\pm\) s.d.). If a match fails a band, record the failure.
Do not hand-edit the pooled triple.

## Diagnostics (not selectors)

On a deterministic 1 Hz subset (every 10th complete frame), record
Calinski–Harabasz, silhouette (omit \(k = 1\); do not code as 0), and
Shannon entropy of cluster sizes. Report silhouette local maxima as
characteristic separations. They are alternatives, not adopted cutoffs.

## Outputs

Step 02 writes `regime_summary.csv` and the `validated_cutoffs` block of
`config.yaml`. Later steps read those values. They are not inputs to
the sweep.
