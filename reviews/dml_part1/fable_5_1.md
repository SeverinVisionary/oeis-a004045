# Review of "A parity refinement of the covering excess bound for twofold coverings of the hypercube"

Reviewer leg: Fable 5.1. Date: 2026-09-02.
Source reviewed: `dml_submission.tex` (the version with 384/20 already corrected).

## Verdict: SEND AFTER FIXES

The theorem is correct and the proof is complete. Every displayed number
reproduces. The dominance theorem is correct. The paper is not ready to send
because Section 6 (and the sentences in the Abstract and Introduction that
depend on it) asserts something that is false by the manuscript's own
formulas and by Krotov--Potapov's own printed table, and because two
bibliographic statements (OEIS, van Wee) are wrong as written. None of the
fixes touches the main theorem; all of them are a referee's first-pass catches.

---

## What I verified, and how

All computations are in `check_arith.py`, `check_parity.py`, `ilp6.py`,
`ilp8.py` in this directory. Exact rational arithmetic throughout (Python
`fractions`), not floating point.

**Theorem 1.1, Step 1 (parity).** Reconstructed independently.
- Equation (3), the ball-intersection numbers, checked exhaustively for all
  pairs (x, z) in F_2^n for n = 2..9: |B(x) ∩ B(z)| = n+1, 2, 2, 0 for
  d = 0, 1, 2, ≥3. Correct. (For d=1 the two common points are x and z; for
  d=2 the two intermediate words; for d ≥ 3 the triangle inequality kills it.)
- The identity Σ_{y ∈ B(x)} c(y) = (n+1) + 2 N_2(x) for x ∈ C checked on
  53,606 codeword-balls of random subsets C (not necessarily coverings) of
  F_2^n, n = 4..8: zero failures. The exchange of summation uses only
  y ∈ B(z) ⟺ z ∈ B(y), which is fine.
- Diagonal term: z = x contributes n+1, and it is present because x ∈ C. This
  is exactly where "C is a set" is used (Remark 3.2 is accurate). Every
  z ≠ x contributes 0 or 2. Sum is odd when n is even. Each of the n+1 terms
  is ≥ 2 by the covering hypothesis, so the sum is ≥ 2(n+1), which is even;
  an odd integer ≥ an even integer m is ≥ m+1. Hence Σ_{B(x)} g ≥ 1. Valid.
- Confirmed the consequence on real coverings: in the ILP-optimal 8-word
  covering of F_2^4, the ILP-optimal 20-word covering of F_2^6, and the
  OEIS 20-word covering of F_2^6, every codeword ball contains an
  over-covered word. In the OEIS 32-word covering of F_2^7 (n odd, E = 0) it
  fails, as it should.

**Step 2.** Pairs (x, y) with x ∈ C, y ∈ S, y ∈ B(x): each x contributes ≥ 1
(Step 1), each y ∈ S contributes exactly |B(y) ∩ C| = c(y). So
|C| ≤ Σ_S c = Σ_S (g+2) = E + 2s, using g = 0 off S. Correct.

**Step 3.** s ≤ E (g is a non-negative integer, ≥ 1 on S), so |C| ≤ 3E =
3(n+1)|C| − 3·2^{n+1}, giving (3n+2)|C| ≥ 3·2^{n+1}. Correct. Checked
|C| ≤ E + 2s and |C| ≤ 3E numerically on the coverings above.

**Remark 3.1.** C = {000, 001, 110, 111}: c(x) = 2 for all eight x, E = 0,
|C| = 4; no 3-word twofold covering of F_2^3 exists (exhaustive). ⌈48/11⌉ = 5.
All correct.

**Theorem 4.1.**
- Both cross-multiplied identities verified exactly (as rational functions,
  2^n divided out, at n = 1..60, far more points than the degree):
  L − KP = 2^n(2n−12)/(n(n+4)(3n+2)) for n ≡ 0 (mod 4) and
  2^n(2n−4)/(n(n+2)(3n+2)) for n ≡ 2 (mod 4). Correct.
- Gaps: n=6: 8/15 (0.5333); n=8: 16/39 (0.4103); n=10: 64/15 (4.2667).
  All correct. n=4: L = 48/7 ≈ 6.857, KP = 7, both ceilings 7. Correct.
- 2n−12 ≥ n/2 holds for n ≥ 8 (fails at 7); n(n+4)(3n+2) ≤ 8n^3 holds for
  n ≥ 4 (fails at 3); 2^n > 16n^2 fails at n=10 (1024 < 1600) and holds at
  n=11 (2048 > 1936) and for all n up to 400; 2^n/n^2 is increasing from
  n=3. So the threshold n ≥ 11 is exactly right, and monotonicity is enough.
- ⌈L⌉ ≥ L > KP+1 > ⌈KP⌉ is valid because ⌈x⌉ < x+1 strictly.
- The 98-value claim: even n in [6, 200] is 98 values; ⌈L⌉ > ⌈KP⌉ at all
  of them; L ≤ KP only at n = 2, 4.
- Additive gap ratio (L−KP)/((2/3)2^n/n^2) → 1 (0.95 at n=200, 0.97 at 400).

**Table 4.1.** All twelve numbers reproduce: L-ceilings 20, 60, 192, 647,
2235, 7865 (L(10) = 192 exactly); KP-ceilings 19, 59, 188, 640, 2195, 7783;
gains 1, 4, 7, 40, 82. The manuscript's row for n=6 prints "0" gain against
Seuranen's 20, and "+1" at n=8: correct.

**Krotov--Potapov citation.** I downloaded arXiv:1902.00023 (the IEEE IT
67 (2021) paper) and extracted the text. Their Theorem 6 reads, for
μ ≡ τ (mod 2): (a) 2^n(μn+3μ+τ)/(n(n+4)) if n ≡ 0 mod 4; (c)
2^n(μn+μ+τ)/(n(n+2)) if n ≡ 2 mod 4 — exactly as transcribed in Section 4.
Their table after Theorem 6 prints, at μ=2: 59–64, 188–216, 640–704,
2195–2560, 7783–8192 for n = 8, 10, 12, 14, 16. So "the entries for n ≥ 8
are exactly the μ=2 positions printed in [KP]" and "each printed lower bound
equals the value of their formula" are both verified. The upper bound 64 at
n=8 is also in that table.

**Section 5.** ⌈384/20⌉ = 20 and ⌈1536/26⌉ = 60: correct. K(7,1,2) = 32
(OEIS a(7) = 32; two cosets of the Hamming code) so 2K(7,1,2) = 64: correct.

**Small cases by computer.**
- K(6,1,2) = 20 confirmed independently: HiGHS (scipy.optimize.milp) solves
  the 64-variable ILP to proven optimality in 0.1 s, optimum 20. This is the
  first unconditional confirmation of the theorem's tightness at n=6 in this
  review, and it confirms both halves of "K(6,1,2) = 20". A 20-word covering:
  {000000, 000001, 001110, 001111, 010110, 010111, 011010, 011011, 011100,
  011101, 100010, 100011, 100100, 100101, 101000, 101001, 110000, 110001,
  111110, 111111} (E = 12, s = 4). The OEIS code for n=6 (Tabatabai 2020)
  is also a valid 20-word twofold covering.
- K(4,1,2) = 8 (exhaustive over all 7-subsets of F_2^4; 620 coverings of
  size 8; OEIS agrees). Theorem 1.1 gives only 7 at n=4, the same as the
  sphere bound. Not an error — the note claims nothing at n=4 — but see
  Finding 12.
- n=8: HiGHS, 7-minute limit, 256 binary variables: proved dual bound
  exactly 59.0 and found a 64-word twofold covering of F_2^8 (min c = 2,
  verified), i.e. it reproduced the published range 59 ≤ K(8,1,2) ≤ 64 but
  could not certify 60. The theorem's 60 is beyond what plain ILP gives in
  that time, which supports the "first open case" framing and the value of
  a one-line proof of 60.

**Proposition 6.1.** Re-derived with general even μ: |C| ≤ E + μs ≤ (μ+1)E,
E = (n+1)|C| − μ2^n, giving μ(μ+1)2^n ≤ ((μ+1)(n+1) − 1)|C|. Correct, and
it reduces to Theorem 1.1 at μ=2 (checked for all even n ≤ 100). The three
n=8 comparisons are correct: 117 vs 118, 174 vs 176, 231 vs 235. The general
claim built on them is not — Finding 1.

**HHKL ε.** At r=1, ε = 2⌈μ(n+1)/2⌉ − μ(n+1) ∈ {0,1}, zero iff μ(n+1) even;
for even n iff μ even. With ε = 0 the quoted Theorem 6 collapses to
μ2^n/(n+1) regardless of k. The collapse claim is defensible from the
quoted formula.

**What I could not verify.** HHKL 1993 and Seuranen 2007 are paywalled; I
could not check HHKL's Theorem 6 statement (in particular the parameter k),
their Corollary 2, their table attributions, or what Seuranen 2007 proves at
n=6. van Wee 1988 likewise. I could not compile the LaTeX (no pdflatex here).

---

## Findings, ranked by severity

### 1. MAJOR — Section 6, Introduction, Abstract: "the gain is confined to μ=2" is false; Proposition 6.1 beats Krotov--Potapov's printed table at μ=4

Location: Section 6 last two sentences ("The gain is confined to μ=2 ...");
Introduction paragraph after Theorem 1.1 ("by showing that the same argument
*loses* to [KP] at every even μ ≥ 4"); Abstract last sentence ("the exact
range of multiplicities for which the refinement gains anything").

What is wrong: Section 6 checks only n=8 and generalises. By the
manuscript's own Proposition 6.1 and its own transcription of KP Theorem 6
(which I verified against the source), with ceilings taken:

| μ=4 | n=8 | n=10 | n=12 | n=14 | n=16 |
|---|---|---|---|---|---|
| Prop 6.1 | 117 | **380** | 1280 | **4429** | **15604** |
| KP formula = KP printed table | 118 | 376 | 1280 | 4389 | 15565 |

So at μ=4 the refinement loses by 1 at n=8, ties at n=12, and wins by 4, 40
and 39 at n = 10, 14, 16 — against the lower bounds KP actually print. At
μ=6 it wins at n=10 (566 vs 564) and n=14 (6617 vs 6583); at μ=8 at n=10
(753 vs 751) and n=14 (8804 vs 8778). As real numbers the rule is exact:
Prop 6.1 > KP iff n > 3μ when n ≡ 0 (mod 4), and iff n > μ when n ≡ 2
(mod 4) (verified for μ = 4, 6, 8, 10 and n ≤ 200). The deficit does not
"widen with μ" in general; it is a small-n phenomenon.

Why it matters: a referee who plugs n=10, μ=4 into the two displayed
formulas finds the paper contradicting itself in one line. It also means
the note undersells its own result: K(10,1,4) ≥ 380, K(14,1,4) ≥ 4429,
K(16,1,4) ≥ 15604 are new tabulated bounds (relative to KP 2021's table,
which they say updates Seuranen's) and are obtained by the same one-page
argument.

Fix: (a) Rewrite Section 6 to state the crossover rule (n > 3μ resp.
n > μ), keep the n=8 losses as the honest small-n caveat, and add a second
small table with the μ=4 (and optionally μ=6, 8) improvements. (b) Change
the Introduction sentence to "loses to [KP] at n=8 for every even μ ≥ 4
but wins for n > 3μ (n ≡ 0 mod 4) and n > μ (n ≡ 2 mod 4)". (c) Change the
abstract's last sentence; "the exact range of multiplicities for which the
refinement gains anything" is now wrong. (d) Consider whether "twofold" in
the title still describes the paper; it is fine to keep μ=2 as the headline
if the abstract says the refinement applies to every even μ. Before
claiming the μ ≥ 4 improvements as new, check whether anything after KP
2021 improved those table positions.

### 2. MAJOR — Section 5: the OEIS sentence misattributes the range 59–64

Location: Section 5, "The bound K(8,1,2) ≥ 60" paragraph.

What is wrong: I fetched A004045 on 2026-09-02 (revision #32, May 2026). It
reads: 2, 3, 4, 8, 12, 20, 32 (offset 1), keywords `nonn,hard,more`, with
a(6) and a(7) credited to Paul Tabatabai (2020) and explicit optimal codes
for n = 6, 7. There is no comment recording 59 ≤ a(8) ≤ 64. The manuscript
says "where the recorded range was 59 ≤ K(8,1,2) ≤ 64", which attributes
that range to the OEIS entry. The range is in KP's table (verified), not in
OEIS.

Fix: "The length n=8 is the first length not listed in A004045 [OEIS]; the
best published range is 59 ≤ K(8,1,2) ≤ 64 [KP, table after Theorem 6],
the upper bound being the doubling ...". Add the OEIS entry to the
bibliography with the access date.

### 3. MAJOR — Abstract overclaims "strictly improves ... at every even length from six onwards"

Location: Abstract, sentence 3; also Introduction ("strictly stronger ...
than the best published lower bound of Krotov and Potapov at every even
n ≥ 6").

What is wrong: at n=6 the best published lower bound is already 20 (the
manuscript itself says so in Table 4.1 and Section 5). The theorem matches
it; it does not improve it. Theorem 4.1 is correct as stated because it
compares against KP's *formula*, but the abstract compares against "the
best lower bound in the literature", which at n=6 is not KP's formula.

Fix: "strictly improves the best published general lower bound at every
even length from eight onwards, and recovers the known value at length six
without computer search." In the Introduction, "the best published lower
bound of Krotov and Potapov" should be "the general bound of Krotov and
Potapov".

### 4. MODERATE — Section 7: "its even-n consequence at radius one is K(n,1) ≥ 2^n/n" is wrong as stated

Location: Section 7, first paragraph.

What is wrong: van Wee's excess argument at R=1, n even (parity at a
non-codeword) gives K(n,1) ≥ (n+2)2^n/(n^2+2n+2), which is what the quoted
HHKL Theorem 6 reduces to at μ=1, r=1, k=0, ε=1. That quantity is strictly
less than 2^n/n for every n, because n(n+2) < n^2+2n+2. Numerically:
n=10 gives 101 vs 103, n=12 gives 338 vs 342, n=14 gives 1160 vs 1171. So
van Wee does not imply K(n,1) ≥ 2^n/n; it implies something slightly
weaker, asymptotic to 2^n/n. I could not read van Wee 1988 itself; if his
paper states a different formula, quote that one verbatim.

Fix: either quote the actual bound or write "asymptotically 2^n/n". Do not
leave an inequality attributed to a paper that does not prove it.

### 5. MODERATE — Section 7: HHKL Theorem 6 is quoted with an undefined parameter k, and two claims about HHKL's text are unverifiable from the note

Location: Section 7 displayed formula; Introduction ("which is why their
Corollary 2 is stated only for odd μ with n even"); Section 7 ("no μ=2
entry in their own table is attributed to Theorem 6").

What is wrong: k is never defined. A referee will stop at that line. The
two claims about HHKL's Corollary 2 and table are stated as fact; the brief
says the author cannot reproduce their table. A claim about what a table
attributes cannot be made from a formula.

Fix: define k as HHKL do, or specialise the quotation to r=1 and the value
of k actually needed and say so. Keep the Corollary 2 and table-attribution
sentences only if the author has the HHKL paper open and has checked them;
otherwise delete them. The collapse-to-sphere-bound statement itself is
fine (it follows from ε = 0 for any k) and is the only one of the three the
argument needs.

### 6. MODERATE — Section 7, Chen–Li paragraph reads as an invitation to reject

Location: Section 7, second paragraph.

What is wrong: "it may anticipate part or all of the present note" plus
"Readers ... are warmly invited to make contact" tells an editor the
author does not know whether the main result is new. That is a reason to
desk-reject a four-page note. Honesty is right; the framing is not.

What I found: Semantic Scholar and Crossref return no publication titled
"Lower bounds for multiple covering codes" by Chen and Li. What did appear
is D. Li and W. Chen, "New lower bounds for binary covering codes", IEEE
Trans. Inform. Theory 40 (1994) 1122–1129 (ordinary coverings K(n,R), a
"multiexcess" technique). The HHKL-cited manuscript plausibly became part
of that paper or was never published.

Fix: read Li–Chen 1994 (and W. Chen, I. Honkala, "Lower bounds for q-ary
covering codes", IEEE IT 1990) and check whether either contains a
codeword-centred parity for multiple coverings. Then replace the paragraph
with two factual sentences: HHKL cite an unpublished Chen–Li manuscript on
multiple coverings; the author could not locate it, and the Chen–Li results
that did appear concern ordinary coverings. Drop "may anticipate part or
all" and the invitation.

### 7. MODERATE — Theorem 4.1 proof handles only the n ≡ 0 (mod 4) branch explicitly for n ≥ 12

Location: Section 4, proof, last display.

What is wrong: the bound L − KP ≥ 2^n(n/2)/(8n^3) uses the numerator 2n−12
and the denominator n(n+4)(3n+2), which are the n ≡ 0 (mod 4) expressions.
The n ≡ 2 (mod 4) branch is covered because 2n−4 ≥ 2n−12 and
n(n+2)(3n+2) ≤ n(n+4)(3n+2), but the proof does not say so. I checked that
L − KP ≥ 2^n/(16n^2) holds for all even n ≥ 12 in both residue classes, so
the conclusion is right.

Fix: add one sentence: "the n ≡ 2 (mod 4) case has a larger numerator and a
smaller denominator, so the same estimate applies."

### 8. MODERATE — Section 5 and Table 4.1: the existence of a 20-word covering of F_2^6 and the attribution to Seuranen need a citation the reader can check

Location: Section 5, "a twofold covering of F_2^6 with 20 words exists";
Table 4.1 row n=6 "(exact, [Seuranen-2007], by integer programming)";
Section 5 "integer programming together with an exhaustive search".

What is wrong: the existence sentence has no citation and no code. OEIS
credits a(6) = 20 to Tabatabai (2020) and does not cite Seuranen. I could
not open Seuranen 2007 to confirm it establishes K(6,1,2) = 20 by the
method described. If Seuranen's Table 1 lists it as exact, cite that
table; if HHKL already had 20 as an upper bound, cite HHKL for the code.

Fix: print the 20-word code (one line; either the OEIS one or the one
above) or cite OEIS A004045 for it, and make sure the description of
Seuranen's method matches his paper. A referee at DML will know this
literature.

### 9. MINOR — Acknowledgment: the AI disclosure is narrower than the brief says the truth is; one sentence should go

Location: Acknowledgment.

What is wrong: the brief says AI was used "to propose arguments and draft
the text". The acknowledgment says "for literature search and for
drafting". If the parity argument was AI-proposed, the disclosure should
say so; a disclosure that omits the most important use is worse than none
if it comes out later. "The author thanks the referees in advance for
their time" is not something to print. Placement under "Acknowledgment"
is acceptable; a separate unnumbered "Declaration" paragraph would be
cleaner and is what most journals with a policy now ask for.

Fix: "Generative AI was used substantially in preparing this work,
including in proposing the argument, in literature search and in drafting.
All mathematical statements and computations were checked by the author,
who takes full responsibility for the content. No funding was received."
Emailing the editor about policy before submitting is the right step.

### 10. MINOR — Title and framing after Finding 1

Location: title, abstract, keywords.

The title says "twofold". After Finding 1 the honest scope is "even-fold
coverings, with twofold as the case of most interest". Keeping "twofold"
in the title is defensible if the abstract says the refinement applies to
every even μ and improves KP at μ=4 for n ≥ 10 (n ≢ 0 mod 4) or n ≥ 14.
Decide deliberately.

### 11. MINOR — LaTeX: `\titleformat{\section}{...}{\thesection}{1em.}{}`

Location: line 7.

`1em.` is a length followed by a stray period. If this is verbatim from the
DML template, leave it; if not, it will either error or typeset a period
after the section number. I could not compile here (no pdflatex). Compile
and look at a section heading.

### 12. MINOR — Optional honesty item: the bound is not tight at n=4

K(4,1,2) = 8 (OEIS; exhaustive check here) while Theorem 1.1 gives 7, the
same as the sphere bound. One clause in Section 5 ("at n=4 the bound gives
7 against the true value 8") would pre-empt a referee asking why the table
starts at 6.

### Sections with no error found

- Section 2 (Notation): equations (1), (2), (3) all correct; definitions
  adequate.
- Section 3 (Proof): correct in every step; Remarks 3.1 and 3.2 correct
  and accurate about where the hypotheses are used.
- Section 4 (Theorem 4.1 and Table 4.1): correct, subject to Finding 7's
  one missing sentence; every number verified; KP citation verified against
  the source.
- Section 5 arithmetic: correct; the two prose issues are Findings 2 and 8.
- Proposition 6.1: correct; the prose around it is Finding 1.

---

## On desk rejection

Length (4 pages of an 8-page cap), venue scope ("non-trivial progress on
existing problems", short proofs), and content (five improved table
entries, one exact value by hand, a clean half-page proof) fit DML. An
editor's likely objections, in order: the Chen–Li paragraph (Finding 6),
the Section 6 self-contradiction (Finding 1), and the absence of any
statement of what precisely is new in one sentence. Add that sentence to
the end of the Introduction: "Theorem 1.1 is, to the author's knowledge,
the first lower bound for K(n,1,2) at even n that improves on the sphere
bound by the excess method; it improves the general bound of [KP] at every
even n ≥ 8 and every tabulated position, and Proposition 6.1 does the same
at μ=4 for n = 10, 14, 16." Then the paper reads as a contribution, not a
table update.

Once Findings 1–6 are fixed and the AI disclosure is made accurate, send.
