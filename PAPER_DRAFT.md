# An elementary lower bound for binary 2-fold radius-1 coverings

**Draft. The prior-art gate is narrowed but not closed (see PRIOR_ART_EXCESS.md):
two independent searches found no published source and no error, with the Chen-Li
preprint an unresolved priority risk that must be disclosed.**

## Claim ladder, in order of confidence

1. **`K(n,1,2) >= ceil(3*2^(n+1)/(3n+2))` for even n.** Half a page, verified
   exhaustively at n=4 and on thousands of covers at n=6, 8. Gives 20 at n=6
   (exact) and 60 at n=8.
2. **`K(8,1,2) >= 60`.** Follows from 1. Independently certified in this
   repository by two solver routes with a machine-checkable proof. The published
   lower bound is 59.
3. **`K(6,1,2) >= 20`**, i.e. the exact value, from 1 and from the ladder in 4.
4. **Reduction: any 60-word double covering of F_2^8 is weight-balanced**, with
   exactly 30 even and 30 odd codewords. All four other splits allowed by the
   row sums are killed by hand.
5. **`K(8,1,2) >= 61`** -- NOT ESTABLISHED. Requires killing the balanced case.

## Structure

**1. Introduction.** `K(n,R,mu)`; the n=8, mu=2 entry of the small-parameter
table; state the published 59-64 and its provenance (Krotov-Potapov 2021 Thm 6
for the lower bound, Ostergard 1995 for the upper).

**2. The excess bound.** Steps 1-4 of EXCESS_THEOREM.md. Emphasise that the
parity round-up needs |B| odd, i.e. n even, and show the odd-n failures (n=3, 7)
as evidence the hypothesis is doing work rather than decoration.

**3. The weight split.** The two half-row sums; the per-half excesses; the
zero-excess chain. Worked closure of n=4, M=7 and n=6, M=19.

**4. The half-excess inequality.** `2*M_e - M_o <= 2*E_o + r_o`. The point to
make: the plain argument throws away the *parity* of each codeword's ball
excess, keeping only positivity; retaining it converts the whole even-codeword
count into heavy-adjacency demand. Note the two mirrored forms sum to exactly
the global `M <= 3E`, so nothing is gained globally -- the gain is per case.

**5. The ladder and the reduction.** Table of which M are refuted at n=6 and
n=8. State clearly that at n=6 the first surviving M is 20, which is achieved,
so a surviving balanced split is what a realisable size looks like -- and hence
that the reduction at M=60 is a reduction, not evidence.

**6. Relation to the certified computation.** The repository's VeriPB/VIPR
artifacts refuting M=59. Independent agreement between an elementary proof and a
machine-checked refutation.

**7. Limits.** Section 4's inequality does not touch the balanced case, because
the balanced case is exactly where the global bound is tight. At n=8, M=60 the
global inequality has slack 24 (`M = 60` vs `3E = 84`), so closing M=60 needs a
genuinely different argument, not a refinement. Also: the method wins only at
mu=2 and loses to Krotov-Potapov Thm 6 at every larger even mu.

## What must happen before this is submittable

- **Prior-art gate (narrowed 2026-09-01, no longer fully blocking).** Two
  independent searches -- Codex `gpt-5.6-terra` and the ChatGPT professor leg at
  tier Pro -- each audited the proof and found no error, and neither located a
  published source for the inequality. The table history is now pinned down:
  HHKL's own reproduced table gives 19 and 58, Seuranen 2007 gives 20 and 58
  (by integer programming, not a general theorem), Krotov-Potapov 2021 gives 59.
  See PRIOR_ART_EXCESS.md for the resolution of each item.
  Two residual holes, both disclosable rather than blocking:
  (i) the **Chen-Li preprint** "Lower bounds for multiple covering codes", cited
  as forthcoming across 1993-1996 and never located -- must be named in a
  footnote; (ii) the bodies of HHKL 1993 and *Covering Codes* Ch. 14 remain
  unread, so no page-by-page negative is claimed. The defensible framing is
  "we have not found this specialisation in the published literature", not
  "this is new".
- Decide the balanced case, or state it as the open problem.
- Independent re-derivation of Sections 2 and 4 by a human reader. Every check
  so far is either mine or a machine's.
