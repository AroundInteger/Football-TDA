# Revision discipline for the Vision & Approach

Record of how REV2 went off piste, and the rules that would have caught it.
Written 24 Aug 2026 after the REV2 → REV3 pass. UK English throughout.

## The budget is three pages, not a word count

The V&A is three pages including Figure 1. The known-good fit is the
23 Aug working master at approximately 1,600 words plus the Gantt figure.
Treat 1,600 words as the hard ceiling and measure it, rather than
inheriting a target from the previous revision.

The consequence is a triage decision on every technical sentence. A grant
is a document under review, not a paper. Correct mathematics is
non-negotiable, but *complete* mathematics is unaffordable, and attempting
it is what pushed REV3 to 1,926 words.

| Print in the body | Cite instead | Defer to another section |
|---|---|---|
| The claim, in one plain sentence | The machinery that makes it true | Proof sketches and technical defences |
| The hypotheses it holds under | Standard results (Bochner, Davis–Kahan, total persistence) | Power-calculation derivations |
| The named failure condition | Prior art establishing the setting | Data governance and ethics |
| The number a reviewer will check | | Team competence arguments |

`T1_T2_Six_Registers.md` exists precisely to hold the deferred technical
material for postal reviewers and introducers. Material that lands there
does not also need to be in §5.

---

## The ten failure modes

### 1. Answering the referee inside the body

REV2 responded to the independent review by writing answers to each
technical objection into the case for support. Five references (Bosq,
Hörmann–Kokoszka, Berkes, Cohen-Steiner 2010, Turner) were added *and*
explained. §5 grew from 249 to 307 words and became the least readable
section in the document.

**Rule.** A referee objection needs an answer *available*, not an answer
*printed*. Add the citation; put the argument in the registers sheet.

### 2. Trading sentences for words

REV2 removed 18 sentences and saved 11 words. Mean sentence length rose
from 16.9 to 20.7, the longest sentence from 42 to 63 words, and
sentences over 35 words from one to seven. The word count looked
unchanged, so the regression was invisible to a word-count check.

**Rule.** Track sentence count and mean length alongside word count. A
revision that holds words constant while cutting sentences has made the
document denser, not shorter.

### 3. Fixing the label rather than the arithmetic

The review noted that phase of play is a within-match factor and cannot
partition matches. REV2 relabelled the cells "fully crossed" and kept the
denominator: `venue × opponent strength × phase of play` gives 18 cells,
so 540 matches yields 30 per cell, not 32, and a CI half-width of 0.0258,
not the stated 0.025.

This is the most dangerous failure mode because the objection looks
addressed.

**Rule.** When an objection concerns a number, recompute the number. Show
the arithmetic in the commit note even if it stays out of the body.

### 4. Defining a metric that does not exist in the evidence base

Asked "0.80 of what?", REV2 answered "intraclass correlation of
interaction lengths". The 0.80 threshold descends from the pilot's
*cross-epoch stability* scores of 0.96 / 0.84 / 1.00 in
`CANONICAL_NUMBERS.md`, which are not ICCs. The new definition severed
the gate from the only evidence that it is passable.

**Rule.** When asked to define a number, retrieve the definition from
`CANONICAL_NUMBERS.md` or the pilot. Never supply a plausible-sounding
substitute.

### 5. Upgrading a hedge in a bold label

The body read "consistent with the summable-mixing condition". The bold
run-in label read "**Mixing verified**". Empirical autocovariance decay is
consistent with α-mixing but does not establish it.

**Rule.** Bold labels, headlines and bullet leads are read as claims.
Carry the hedge into the label or drop it from both.

### 6. Keeping an elegant sentence that conflates two objects

"Block-bootstrap thresholds are that bound in operational form" survived
into REV2 after the review flagged it as a riddle. It is also incorrect:
a detection threshold controls the false-alarm rate, whereas the T2 bound
controls the localisation error. Two different objects.

**Rule.** A sentence that cannot be restated plainly usually contains a
conflation. Restate it or delete it; do not preserve it for its economy.

### 7. Changing a headline claim without updating its dependents

T1 moved from existence to convergence. Three dependents were left
behind: §6's R3 still disclaimed "T1 uniqueness"; `T1_T2_Six_Registers.md`
promised a functional CLT while §5 offered only a rate; and
`AdversarialTDA_Specification.md` line 13 still asserted the retired
uniqueness framing.

**Rule.** A change to the T1 or T2 statement is a change to a system.
Sweep, in order: §1, §5, §6 (R3), `T1_T2_Six_Registers.md`,
`AdversarialTDA_Specification.md`, toy-model figure names, `01_Summary.md`.

### 8. Silent renumbering

References 24–28 were appended to the list but first cited in §1, so the
order of first appearance became 1, 2, 3, 4, 5, 6, 8, 24, 25, 7, … which
`unsrtnat` will not reproduce. `04_References.md` was left at 23 entries
and `CANONICAL_NUMBERS.md` still records the methodology paper as [19].

**Rule.** Adding a reference triggers three actions: renumber to
first-appearance order, sync `04_References.md`, and update the compiled
numbers in `CANONICAL_NUMBERS.md`.

### 9. Deleting a justification along with its sentence

Compression removed the sub-two-second frame timing that makes 1 Hz
feasible, and the Month-2 check that 1 Hz preserves features validated on
10 Hz pilot data. The rate survived; its defence did not. Likewise the
geometric baselines went, leaving §3's "unavailable from conventional
geometry" with no support anywhere in the document.

**Rule.** Before deleting a clause, search the document for the claim it
supports. If a claim elsewhere depends on it, the clause is load-bearing.

### 10. Deferring a decision the reviewer asked you to make

On football's absence from §1 the review said the choice was defensible
either way, but to decide rather than drift. REV2 wrote "a fully tracked
benchmark system (§2)". A cross-reference is not a decision; the noun is
still unresolved on first read.

**Rule.** When a reviewer offers two acceptable options, pick one and
record why. Cross-referencing is the third option and it is the worst.

---

## What REV2 got right, and should be preserved

- Three display lists (success criteria, timeliness, risks). These are the
  most-skimmed elements and the improvement is real.
- Plain-English headlines on T1 and T2 before the technical statement.
- Heading hierarchy repaired, so `## Vision` is a parent rather than a
  sibling of its sections.
- T1 restated as convergence, and T2 stated on the landscape series rather
  than on FPCA scores. Both are substantive mathematical corrections.
- "Single filtration over the full agent set" in place of
  "single-threshold persistent homology".
- The retired-phrase table in `T1_T2_Six_Registers.md`, which REV2
  followed on all seven entries.

---

## Pre-commit checklist

Run before any V&A revision is accepted.

1. Body word count ≤ 1,600. Measure it; do not inherit the target.
2. Mean sentence length ≤ 18 words. Zero sentences over 35.
3. No bold label claims more than its own body text.
4. Every number traceable to `CANONICAL_NUMBERS.md` or recomputed in the
   commit note.
5. Every stratification or power claim divided out and checked.
6. Citations ascending in order of first appearance; all entries cited;
   `04_References.md` count matches.
7. Each section heading noun answered by at least one sentence in that
   section.
8. Every claim of the form "beyond X" has X named somewhere in the
   document.
9. T1/T2 wording swept across the six dependent documents in mode 7.
10. Any reviewer choice offered has been decided, not cross-referenced.
