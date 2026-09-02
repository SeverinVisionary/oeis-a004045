# Prior art for the excess bound: what the published record actually is

Checked at the sources on 2026-09-01, not from recollection.

## The current published lower bound at n=8, mu=2 is 59, and this is its origin

Krotov & Potapov, "On multifold packings of radius-1 balls in Hamming graphs",
IEEE Trans. Inform. Theory **67**(6), 3585-3598, 2021 (arXiv:1902.00023),
Theorem 6, derives lower bounds on `K(n,1,mu)` from their packing Theorem 4.
Writing `mu = tau mod 2`, `tau` in {0,1}, part (a) covers `n = 0 mod 4`:

    K(n,1,mu) >= 2^n (mu*n + 3*mu + tau) / (n(n+4))

and part (c) covers `n = 2 mod 4`:

    K(n,1,mu) >= 2^n (mu*n + mu + tau) / (n(n+2)).

At `n=8, mu=2, tau=0`: `256 * 22 / 96 = 58.67`, so `K(8,1,2) >= 59`. The paper's
own table of updated positions lists `n=8, mu=2` as **59 - 64**. So 59 is the
published lower bound, it comes from this formula, and the paper states it is an
update of the earlier values in Hamalainen-Honkala-Kaikkonen-Litsyn (Des. Codes
Cryptogr. 3, 1993) and Seuranen, "New lower bounds for multiple coverings" (Des.
Codes Cryptogr. 45, 91-94, 2007), Table 1.

## Comparison with the excess bound

`excess_theorem.py` gives, for even n, `K(n,1,2) >= ceil(3 * 2^(n+1) / (3n+2))`.
Against Theorem 6 at `mu=2, tau=0` (computed, not quoted):

| n | excess bound | Krotov-Potapov Thm 6 | known K(n,1,2) |
|---|---|---|---|
| 4 | 7 | 7 | 8 |
| 6 | **20** | 19 | **20 (exact)** |
| 8 | **60** | 59 | 59-64 published |
| 10 | 192 | 188 | |
| 12 | 647 | 640 | |
| 16 | 7865 | 7783 | |
| 20 | 101476 | 100489 | |

The two agree at n=4 and the excess bound is strictly larger at every even
n >= 6 tested. Both are asymptotically `2^(n+1)/n`; the excess bound wins in the
lower-order term.

## The method wins only at mu = 2 -- calibration against overclaiming

The argument generalises to any multiplicity mu, but Step 2 needs the ball sum
`(n+1) + 2*N_2` -- odd for even n -- to round up past `(n+1)*mu`, which happens
only when `mu` is EVEN. And carrying mu through Steps 3-4 gives

    K(n,1,mu) >= (1+mu)*mu*2^n / ((1+mu)(n+1) - 1)     (n even, mu even).

At n=8, against Theorem 6:

| mu | excess bound | KP Thm 6 | |
|---|---|---|---|
| 2 | **60** | 59 | excess wins by 1 |
| 3 | does not apply (mu odd) | 91 | |
| 4 | 117 | **118** | KP wins by 1 |
| 6 | 174 | **176** | KP wins by 2 |
| 8 | 231 | **235** | KP wins by 4 |

At n=6: mu=2 gives 20 vs KP's 19; mu=4 gives 38 for both.

So this is **not** a uniformly better bound. It beats the published one at
mu = 2 and loses at every larger even mu, with the gap widening. Any write-up
must say so: the claim is about `K(n,1,2)`, not about multiple coverings in
general, and specifically about n = 6 and n = 8 where it has been checked
against known or published values.

## What this does and does not establish

**Does:** at `n=8, mu=2` the excess bound gives 60, one above the published 59,
and it agrees with this repository's two independently certified solver
refutations of `M=59`. At `n=6` it gives 20, the exact value, where Theorem 6
gives 19.

**Does not:** it does not establish that the *method* is new. The covering-excess
technique is due to Johnson and to van Wee, and Honkala's "multiexcess"
explicitly generalises it; the fundamental ideas are stated in that literature to
apply to multiple covering codes. The specific mu=2 specialisation done here is
exactly the sort of thing that could sit unremarked in a 1990s paper.

**Still to check, at the sources:**

- Seuranen 2007, Table 1: what value does it list at `n=8, mu=2`? Krotov-Potapov
  say they updated that position to 59, which implies Seuranen's entry was below
  59 -- and therefore that no van Wee-style mu=2 excess bound giving 60 was in
  play as of 2007. That inference is strong but is an argument from a single
  sentence; read the table.
- Hamalainen-Honkala-Kaikkonen-Litsyn 1993, "Bounds for binary multiple covering
  codes": does it contain a general van Wee-type lower bound for `K(n,1,mu)`?
- Cohen-Honkala-Litsyn-Lobstein, *Covering Codes*, Ch. 14.
- Honkala's multiexcess papers: does the general bound specialise to this at
  `mu=2`, and if so what does it give at n=6 and n=8?
- Anything after 2021. A targeted search found no improvement to `K(8,1,2)`
  published since Krotov-Potapov; that search was not exhaustive.

Until those are done, the correct statement is: *the excess bound reproduces and
exceeds the best lower bound we can find in print at n=6 and n=8, by an argument
short enough that its novelty is doubtful and must be checked.*

## MathSciNet / full-text access

Seuranen 2007 and HHKL 1993 are both paywalled (Springer). Resolving the two
open items above needs library access, which this environment does not have.

## Two-leg prior-art search, 2026-09-01

Two reviewers were given the same prior-art question independently: Codex
`gpt-5.6-terra` (web search, `reviews/2026-09-01_priorart_codex_terra.log`) and
the ChatGPT professor leg at tier `Pro` (session
`ba57b508-d476-401c-97a1-bfdbfa368072`, `chatgpt verify` PASSED, `tierAtSend=Pro`,
`reviews/2026-09-01_priorart_professor_pro.md`).

**Both legs, independently: the proof is correct and no published source for the
inequality was located.** Neither found an error; both audited the ball-intersection
count, the even-n parity step, the `|S| <= E` step, and the final rearrangement.

### Open items now resolved

- **Seuranen 2007, Table 1** -- RESOLVED. Seuranen is not a van Wee-type theorem
  paper at all: it improves 57 individual positions by integer programming and
  exhaustive search. Its consolidated table lists `K(6,1,2) >= 20` and
  `n=8, mu=2` as **58-64**. So Seuranen closed n=6 to the exact value but left
  the n=8 lower bound at 58; no mu=2 excess bound giving 60 was in play in 2007.
  This confirms the inference previously drawn from the single Krotov-Potapov
  sentence.
- **HHKL 1993** -- RESOLVED AT THE TABLE LEVEL. The 1996 Honkala-Litsyn survey
  states it is reproducing the radius-one portion of the HHKL table, and its
  mu=2 column reads **19-20 at n=6** and **58-64 at n=8**. So whatever general
  lower-bound theory HHKL contains, its own published specialisation gives 19
  and 58, not 20 and 60. The paper body remains paywalled, so an unapplied lemma
  in the text cannot be excluded outright -- but that would require HHKL's own
  table, Seuranen's 2007 update, and Krotov-Potapov's 2021 update to have each
  missed the same immediate specialisation.
- **Covering Codes Ch. 14** -- STRUCTURAL CORRECTION. Chapter 14 has no section
  titled "lower bounds"; its sections are definitions, perfect multiple
  coverings, normality, constructions, tables, MCDH, notes. Chapter 6 is the
  book's "Lower bounds" chapter and is principally about *ordinary* covering
  codes. Neither leg could inspect the full chapter (restricted preview), so no
  page-by-page negative is claimed.
- **Anything after 2021** -- no improvement found. The citing works for
  Krotov-Potapov concern shortened-perfect-like codes, perfect colourings,
  orthogonal-array classification, asymptotic multiple packing and multifold
  perfect codes. Equivalent formulations were also searched: 2-tuple/double
  domination in Q_8, and the complementary 7-limited-packing form.

### One new bibliographic hole

**Chen & Li, "Lower bounds for multiple covering codes"** is cited as
"forthcoming" / "preprint" / "in preparation" across sources from 1993-1996.
No published version or accessible manuscript was located. It cannot be excluded
that it contains this observation, and it cannot be claimed that it does. This is
a **priority risk, not a usable citation**, and must be disclosed in any write-up.

### Attribution language that both legs endorse

Do **not** cite van Wee (1988) for this: that paper treats ordinary coverings
`K(n,R)`, and its advertised even-n radius-one consequence is `K(n,1) >= 2^n/n`.
The defensible statement is:

> For even n, every binary twofold radius-one covering code with distinct
> codewords satisfies `|C| >= ceil(3*2^(n+1)/(3n+2))`. This is an elementary
> covering-excess/parity argument in the tradition of van Wee and
> Hamalainen et al. We have not found this specialisation in the published
> multiple-covering literature.

with a footnote disclosing the unlocated Chen-Li preprint. Calling the result
unconditionally "new" is too strong; calling it already covered by HHKL is
unsupported.

### Scope condition made explicit

The professor leg flagged a scope condition worth stating in the paper: `C` must
be a **set**. For a multiple covering with repeated words the diagonal
contribution to the ball sum need not have the same parity, and the argument
breaks. This does not affect `K(n,R,mu)` as defined here, which counts distinct
codewords.

### Independent numerical check of the even-mu generalisation

`mu_generalization.py` brute-forces exact `K(n,1,mu)` for n=2,4 and mu=2,4 and
compares against the formula above. The bound holds in every even-mu case
(tight at (2,2) and (4,4); slack 1 at (4,2)), and the **odd-mu control fires**:
at n=2, mu=3 the formula would give 5 where the true value is 4. That confirms
the even-mu restriction on the parity step is load-bearing rather than
decorative.

## Primary sources read, 2026-09-01 — the gate is now closed on evidence

The three key papers were obtained as PDFs and read directly, not summarised.
This replaces the table-level inference recorded above with primary evidence.

### The Chen-Li citation, found verbatim

HHKL 1993, reference **[2]**:

> Chen, W. and Li, D. (forthcoming). Lower bounds for multiple covering codes.

and their Acknowledgments name them in full:

> ...and Prof. **Wende Chen** and **Dongfeng Li** for sending us preprints of
> their papers.

A **separate** HHKL reference **[29]** is *Li, D. and Chen, W. (forthcoming).
New lower bounds for binary covering codes* — that one WAS published, as
**D. Li and W. Chen, IEEE Trans. Inform. Theory 40(4) (1994) 1122-1129**. It
concerns ORDINARY covering codes `K(n,R)` via "multiexcess", not multiple
coverings, so it is not the missing preprint.

Read for this purpose, the published Li-Chen paper settles a sub-question: its
introduction says "In a forthcoming paper [6], this idea is applied to multiple
covering codes", and its own reference [6] is **HHKL itself**, not a paper of
their own. So the authors, writing in 1994, point at HHKL for the
multiple-covering application and do NOT cite their own multiple-covering
preprint. That is real evidence the preprint never appeared, though it does not
prove it.

**Status:** the preprint remains unlocated and is still a disclosable priority
risk. What changed is that the citation is now confirmed from a primary source
with full author names, so the footnote can be written precisely.

### The novelty argument is now positive, not a failed search

`hhkl_theorem6.py` implements HHKL's Theorem 6 (p.259) from the primary text
and proves the load-bearing point:

    eps := (r+1) ceil(mu(n+1)/(r+1)) - mu(n+1)          [their Lemma 1]

is their entire gain over the sphere bound. At `r=1`, `eps = 0` exactly when
`mu(n+1)` is even — and for EVEN n, `n+1` is odd, so **`eps = 0` exactly when
`mu` is EVEN**. When `eps = 0` Theorem 6 collapses *identically* (not
approximately) to the sphere-covering bound. Verified as exact rational equality
for every even n up to 40 and every even mu < n.

This is why their **Corollary 2** is stated only for "`mu <= n` odd and `n`
even": their parity round-up has nothing to say at even mu. Our argument uses a
*different* parity — the ball sum at a CODEWORD, `(n+1) + 2*N_2(x)`, odd
whenever n is even, for every mu — and therefore fires exactly where theirs
vanishes.

Their own table confirms it. HHKL Table 5 Part I marks each lower bound with the
method that produced it, `c` being Theorem 6. **No mu=2 entry is marked `c`:**

| n | HHKL Thm 6 (= sphere) | HHKL published LB | ours |
|---|---:|---:|---:|
| 6 | 19 | 19 (unmarked = sphere) | **20** |
| 8 | 57 | 58 (marked `a` = ineqs (1),(2)) | **60** |
| 10 | 187 | 187 (unmarked) | **192** |
| 12 | 631 | 631 (unmarked) | **647** |
| 14 | 2185 | 2186 (marked `a`) | **2235** |
| 16 | 7711 | 7711 (unmarked) | **7865** |

So HHKL's excess machinery was never used at mu=2 anywhere in their own table,
because it cannot be.

### Seuranen 2007, Table 1, read directly

`K(n,1,2)`: n=6 is **20** marked `t` (exhaustive search, exact); **n=8 is 58,
UNMARKED**, which his key states means copied from Cohen-Honkala-Litsyn-Lobstein
Tables 14.1-14.4 — i.e. Seuranen did **not** improve n=8. n=10,12,14,16 are
188, 632, 2187, 7713, marked `s` (his IP_sphere method).

This confirms from the primary source what was previously inferred from a single
Krotov-Potapov sentence: no mu=2 excess bound giving 60 was in play in 2007.

### Net effect on the claim

Best published lower bound per n, mu=2 (max over HHKL / Seuranen / KP), against
ours: n=6 20 vs **20** (match, exact value, ours search-free); n=8 59 vs **60**;
n=10 188 vs **192**; n=12 640 vs **647**; n=14 2195 vs **2235**; n=16 7783 vs
**7865**. Five strict improvements and one search-free reproof.
