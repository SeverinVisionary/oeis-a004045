# An elementary lower bound for K(n,1,2), even n

**Status: verified, NOT prior-art-cleared.** This is almost certainly a mu=2
analogue of van Wee's parity/excess method. Do not claim novelty before the
checks in "Prior art" below are done at the sources.

## Theorem

Let n be even and let C be a subset of F_2^n with |B(x) cap C| >= 2 for every x,
where B is the closed radius-1 ball, |B| = n+1. Then

    |C| >= 3 * 2^(n+1) / (3n+2).

For n = 8 this reads **K(8,1,2) >= 60**.

## Proof

Write M = |C|, c(x) = |B(x) cap C|, g(x) = c(x) - 2 >= 0, and
E = sum_x g(x) = (n+1)M - 2^(n+1).

**Step 1 (intersection numbers).** For u != v,

    |B(u) cap B(v)| = 2 if d(u,v) in {1,2},   0 if d(u,v) >= 3.

d=1: the intersection is exactly {u,v} -- a common neighbour of adjacent u,v
would be a triangle, and Q_n is bipartite. d=2: exactly the two midpoints;
neither endpoint lies in the other's ball. d>=3: any common member would put u
and v within distance 2.

**Step 2 (odd ball-excess at codewords).** Fix x in C. Then

    sum_{y in B(x)} c(y) = sum_{c' in C} |B(c') cap B(x)|
                         = (n+1) + 2 * #{c' in C : 1 <= d(c',x) <= 2},

which is **odd** because n+1 is odd. Each of the n+1 terms c(y) is >= 2, so the
sum is >= 2(n+1); being odd it is >= 2(n+1)+1. Hence

    sum_{y in B(x)} g(y) >= 1:  every codeword has an over-covered word in its ball.

**Step 3 (double count).** Let S = {y : c(y) >= 3}, s = |S|. Each y in S has
g(y) >= 1 and g vanishes off S, so s <= E and sum_{y in S} g(y) = E. Count
I = #{(x,y) : x in C, y in B(x) cap S}. Step 2 gives I >= M. Ball symmetry
(y in B(x) iff x in B(y)) gives

    I = sum_{y in S} |C cap B(y)| = sum_{y in S} c(y) = E + 2s <= 3E.

**Step 4.** M <= 3E = 3((n+1)M - 2^(n+1)), i.e. (3n+2)M >= 3*2^(n+1).  QED

## Why the parity step is load-bearing

For odd n the ball has even size and Step 2 collapses. The formula is then not a
theorem, and indeed it is false: it gives 5 at n=3 (K = 4) and 34 at n=7
(K = 32). `excess_theorem.py` prints those two violations and **asserts** that at
least one fires -- if the formula ever held at odd n we would have to suspect the
parity step of being mis-stated rather than merely unused.

There is also an explicit witness (`odd_n_witness.py`), surfaced by the review
below and verified independently here:

    C = {000, 001, 110, 111}  in  F_2^3

is a double covering with `c(x) = 2` for **every** x, so `g == 0` everywhere and
`E = 0`. Step 2 claims each codeword has an over-covered word in its ball; here
there are none at all. The ball sum at `000` is `8 = 4 + 2*2`, even, so no
round-up exists. The example is sharp twice over: it is perfect (every coverage
exactly 2) and optimal (`|C| = 4 = K(3,1,2)`), so the hypothesis fails at the
best possible code rather than at some degenerate one.

## Independent review

An adversarial correctness review by **gpt-5.6-terra** (high reasoning effort,
2026-09-01, prompted to break the proof rather than assess it; transcript in
`reviews/2026-09-01_excess_theorem_codex.log`) returned **VALID**, having
attacked each of Steps 1-4 and the small-n cases:

- Step 1 correct including n=2.
- Step 2 exact: the `c'=x` term contributes `n+1` once **because C is a set**,
  and each codeword at distance 1 or 2 contributes 2; the sum is odd for even n
  while `2(n+1)` is even.
- Step 3 has no overcount -- `I` counts distinct pairs, and a shared surplus
  vertex only increases it. The slack is exactly
  `3E - (E + 2s) = 2(E - s) = 2 * sum_{y in S} (g(y) - 1) >= 0`, plus the
  replacement of each `|B(x) cap S| >= 1` by 1.
- Step 4 rearranges correctly.
- The n=4 value of 7 against a true 8 is **non-tightness, not an error**.

It named Step 2's parity as the most fragile point -- agreeing with the
assessment here -- and held that it survives because `g` is integer-valued and
nonnegative. The odd-n counterexample above is its contribution.

A second leg reviewed the **half-excess inequality** separately:
**deepseek-v4-flash** (2026-09-01; v4-flash rather than v4-pro because the run
fell inside DeepSeek's peak window, per the standing pricing policy; transcript
in `reviews/2026-09-01_half_excess_deepseek.log`). Also **VALID**, with every
step checked as an identity:

- `deg_C(x) = g(x) + 1` is right, and there is no isolated-codeword case, since
  `c(x) >= 2` with `x` in `C` forces `deg_C(x) >= 1`.
- The edge count and the heavy-degree sum are exact identities.
- On the crux, step (3): odd non-heavy mass is `m = 0` so it never enters, the
  only even term in `S(x)` is `x` itself, and the parity split is clean --
  `L` even implies `g` odd implies `g >= 1`; `L` odd implies `S >= L`.

It ran its own arithmetic on the two over-kill controls and confirmed the
inequality **holds** (does not refute) at n=6 with split (10,10) and at n=8 with
the incumbent's split (32,32). It named step (3) as the most fragile, since the
whole chain rests on `S(x)` being odd -- the same judgement as the other leg
made about the corresponding step in the main theorem.

**Neither review addresses novelty**, which remains open; see
`PRIOR_ART_EXCESS.md`. A correctness review is not a prior-art check.

## Values

| n | bound | known K(n,1,2) | |
|---|---|---|---|
| 2 | 3 | 3 | exact |
| 4 | 7 | 8 | one short (closed by the parity split, below) |
| 6 | 20 | 20 | **exact** -- and the split independently kills M=19 |
| 8 | **60** | 59..64 published | one rung past the published lower bound of 59 |

## The weight-parity split (`bipartite_split.py`)

Every neighbour of an even-weight word is odd, so summing coverage over each half
gives two rows that are nonnegative combinations of the original ones:

    M_e + n*M_o >= 2^n,    M_o + n*M_e >= 2^n,
    E_e = M_e + n*M_o - 2^n,   E_o = M_o + n*M_e - 2^n.

**Killed case.** If E_o = 0 then every odd word has c = 2 exactly, so S lies in
the even half. An even codeword's ball is itself plus n odd words, none
over-covered, so Step 2 forces g >= 1 on all of C_e, i.e. C_e is a subset of S.
If moreover |C_e| = E_e then S = C_e with g == 1: coverage is 3 on C_e and 2
everywhere else. Counting C_e-C_o edges from each side,

    x in C_e: c(x) = 1 + deg_o(x) = 3  =>  F = 2*M_e
    y in C_o: c(y) = 1 + deg_e(y) = 2  =>  F =   M_o

so the case dies whenever 2*M_e != M_o (and symmetrically with the halves
swapped).

**Stronger form.** The chain needs only `C_e` contained in `S` and `|S| <= E_e`,
which already forces `M_e <= E_e`. So `E_o = 0` kills the case **outright**
whenever `M_e > E_e`; the edge count is needed only in the boundary case
`M_e = E_e`.

**At n = 6, M = 19 the outright form kills both surviving splits** -- each has a
zero-excess half with `M_e = 9 > 5 = E_e` -- giving `K(6,1,2) >= 20`, the exact
value, with no search. Historically that value needed an IP refutation at M = 19.

**At n = 4, M = 7 the boundary form kills both surviving splits**, giving K(4,1,2) >= 8 -- the
exact value -- with no search. `bipartite_split.py` cross-checks that against a
brute-force enumeration of all C(16,7) subsets, which finds no 7-word double
covering.

**At n = 8** the zero-excess chain does nothing at M = 61, 62, 63 -- no split
there has a zero-excess half, so the chain never starts. **At M = 60** it kills (M_e,M_o) = (28,32) and (32,28). Three cases remained open at that stage: (29,31), (30,30), (31,29). The
half-excess inequality below kills (29,31) and (31,29) as well, leaving **only
the balanced split (30,30)**. Closing that one case gives `K(8,1,2) >= 61`.
That is the live frontier.

## The half-excess inequality (`half_excess.py`)

Keeping the **parity** of the per-codeword ball-excess rather than only its
positivity gives, for even n and every double covering,

    2*M_e - M_o <= 2*E_o + r_o <= 3*E_o        (and its mirror),

where `r_o` is the number of odd words with `g >= 1`. The two mirrored forms sum
to exactly the global `M <= 3E`, so this is a parity refinement of Step 3 and
nothing stronger globally -- but per split it is far sharper.

Run as a ladder over M, requiring both mirrored forms to hold for some split:

| n | refuted outright | first M with a surviving split |
|---|---|---|
| 6 | all M <= 19 | M=20, only the balanced split (10,10) |
| 8 | all M <= 59 | M=60, only the balanced split (30,30) |

At n=6 this reproduces `K(6,1,2) >= 20`, the exact value. At n=8 it reproduces
`K(8,1,2) >= 60` **with no solver at all** -- the same rung this repository
certifies with a 6.5 GB VeriPB/VIPR artifact.

**Do not over-read "only the balanced split survives".** At n=6 the surviving
balanced split sits at M=20, which is *achieved*: a surviving balanced case is
exactly what a realisable size looks like. So (30,30) surviving at n=8, M=60 is
not evidence that 60 is impossible. It is the frontier, not a hint.

## Inside the balanced case: the translate family is dead

`translate_check.py`. A natural way to build a balanced cover is the ansatz
`C = C_e u (C_e + v)` with `v` of odd weight, which determines the whole code
from its even half and reduces the question to `2^(n-1)` variables. Coordinate
permutations act transitively on vectors of a given weight and translation by an
even word fixes `v`, so only one instance per odd weight need be solved.

At n=8, M=60 all four are **infeasible** (0.5s, 1.1s, 1.1s, 4.0s). At n=6,
M=20 the same model is **feasible** at weights 1 and 5 -- the control that makes
the n=8 answer meaningful, since K(6,1,2)=20 is achieved and the realisable
family does contain translate-type codes.

So: in any hypothetical 60-word double covering of `F_2^8`, the odd half is not
a translate of the even half. The n=6-style construction route is closed at n=8.

## Where the balanced case actually resists

The case is self-mirrored, so every parity-split inequality degenerates to its
symmetric form there -- the half-excess inequality contributes only
`r_e, r_o >= 2`. Pushing the counting to the distribution level (over the
induced-edge count, the excess split, and the within-half distance-2 pair
counts) leaves 257 feasible integer tuples, with every value of the excess
parameter surviving.

The quantity that looked like the lever is `e2_e`, the number of distance-2
codeword pairs inside one half. Summing the exact ball identity over the even
codewords gives (`e2_bound.py`, both constituent identities verified on 60
random covers at n=6 and n=8)

    4 * e2_e = Q_o + 238 - 2*gamma,     Q_o = sum over odd words of g^2.

With `sum_{odd} g = 14` and `g` a nonnegative integer, `Q_o >= 14`; and `g <= 7`
since `c <= 9`, so `Q_o <= 98`. With `gamma` in [0,14] this pins

    56 <= e2_e <= 84.

**This closes the counting route negatively.** An upper bound of `e2_e <= 52`
would have killed M=60 by counting alone -- but the identity *forces*
`e2_e >= 56`, so no such bound exists. The target sat below what the case itself
requires. And 56 distance-2 pairs among 30 words is an average degree under 4 in
the distance-2 graph, nowhere near an extremal obstruction.

The balanced case therefore needs a **different method**, not a sharper count.

Calibration against the realisable n=6 balanced code: it sits at the extreme
corner where all excess is on codewords, with induced degrees {1 x16, 4 x4}. So
a realisable analogue would **not** live in the low-degree regime, and any case
analysis must admit codewords of high induced degree.

## Relation to the certified result

The repository separately certifies K(8,1,2) >= 60 by two solver routes with
machine-checkable proofs (a 6.5 GB VeriPB/VIPR artifact). The arguments here
reach the same rung in half a page, and the two agree. That agreement is the
strongest single check either has: an elementary proof and a machine-checked
refutation, arrived at independently, landing on the same value.

The certificates are not superseded -- they remain the independent check -- but
they are no longer needed at this rung.

See `PRIOR_ART_EXCESS.md` for where this sits against the published record
(Krotov-Potapov 2021 Theorem 6 gives 59 at n=8 and 19 at n=6).

## Prior art -- required before any novelty claim

Per the standing prior-art gate, verify at the sources, not from recollection:

- van Wee, "Improved sphere bounds on the covering radius of codes" (1988) and
  van Wee--Cohen--Litsyn on perfect multiple coverings -- the parity/excess method
  this specialises.
- Honkala's early-1990s papers on bounds for binary multiple covering codes.
- Cohen--Honkala--Litsyn--Lobstein, *Covering Codes*, Ch. 14 (multiple coverings),
  lower-bound section for K(n,1,mu).
- OEIS A004045 and its references.

Circumstantial evidence for novelty is weak-to-moderate and cuts both ways: if
the bound were known, published tables would plausibly have carried >= 60 at
n = 8 and >= 20 at n = 6 before the solver-era results. But that is an argument
from absence and does not substitute for the check.
