# Independent prior-art review — ChatGPT professor leg

**Date:** 2026-08-28 America/Los_Angeles
**Surface:** `chatgpt` CLI, chatgpt.com Chat (ChatGPT quota, not Codex)
**Thinking mode:** Extra High (`--effort extra-high`, `tierAtSend = Extra High`)
  — the depth leg on a fixed statement, per the standing mode rule; `Pro` is the
  breadth leg for open questions and was not the right call here.
**Session:** `e2712fb9-f68b-4f1e-b82c-eb4998df44c4`
**Verification:** `chatgpt verify` → `VERIFY PASSED`, exit 0, 11697 bytes

The claim submitted for adjudication is reproduced in `prompt.txt`; the reply is
verbatim below. Two of its corrections were folded into `PRIOR_ART.md`
(Hamming-length exact values; two disjoint translates rather than a doubled
multiset). Rendered math arrives with the MathML fallback duplicated, so some
formulas appear as exploded character runs — a known artefact of the capture
path, not of the reply.

---

Verdict

The central claim survives: I found no published exact determination of K(8,1,2), and the best published interval I can verify is still

59≤K(8,1,2)≤64
	​

.

Krotov–Potapov explicitly print the n=8,μ=2 table entry as 59–64, derived from their Theorem 6(a). 
ResearchGate
+1

There is, however, one substantive error in point 1 and two wording qualifications in points 3–4.

Claim	Verdict	Correction / qualification
1. Exact values known only for n≤7; a(8) open	PARTLY REFUTED	a(8) is indeed open, and n=1,…,7 is the known contiguous prefix. But exact values also exist at later Hamming lengths, e.g. K(15,1,2)=4096.
2. 59≤K(8,1,2)≤64	CONFIRMED	This is the best published interval I can verify.
3. 1993 → 1995 → 2007 → Krotov–Potapov is the prior-art chain	ESSENTIALLY CORRECT BUT INCOMPLETE	Good chain for the evolving small-parameter bounds, but not the entire genealogy. In particular, van Wee–Cohen–Litsyn (1991) and Clayton's 1987 thesis belong in a fuller prior-art discussion.
4. No post-2020 closure/improvement; 10,12,14,16 remain open	SUPPORTED, with an absence-of-evidence qualification	I found no later published improvement through August 28, 2026. I would write “no later published improvement located,” not claim logically exhaustive nonexistence.
A. The actual n=8 published record

OEIS A004045 currently says exactly: “Minimal size of binary code of length n such that every vector is within distance 1 of at least 2 codewords,” and lists

2,3,4,8,12,20,32

for n=1,…,7, with a(6),a(7) credited to Paul Tabatabai in March 2020. 
OEIS
+1

Hämäläinen–Honkala–Kaikkonen–Litsyn define K(n,r,μ) as the minimum size of a binary code whose radius-r balls cover every point at least μ times. That is exactly the OEIS definition with r=1,μ=2. 
Tel Aviv University

Krotov–Potapov's Theorem 6(a), for n≡0(mod4), is

K(n,1,μ)≥
n(n+4)
2
n
(μn+3μ+τ)
	​

,μ≡τ(mod2).

At n=8,μ=2,τ=0,

8⋅12
256(16+6)
	​

=
96
5632
	​

=58.666…,

hence

K(8,1,2)≥59.

Their immediately following table explicitly gives n=8,μ=2 as 59–64. It also gives:

n
8
10
12
14
16
	​

K(n,1,2)
59–64
188–216
640–704
2195–2560
7783–8192
	​

	​


ResearchGate

The bibliographic attribution is also slightly date-sensitive: arXiv:1902.00023 appeared in 2019, was accepted/published online by IEEE in December 2020, and appeared in IEEE Transactions on Information Theory 67(6), 3585–3598 in 2021. 
SciAct
+1

I searched the exact notation K(8,1,2), the 59–64 interval, “multiple/double covering,” the equivalent graph-theoretic “double domination / 2-tuple domination of Q
8
	​

,” later citation trails, theses, and non-English variants. I found no published K(8,1,2)=m, no lower bound >59, and no upper bound <64. That supports 59–64 as the current published record, but I cannot prove that no unindexed thesis or obscure report exists.

Important correction to claim 1

“Exact values are known only for n≤7” is false if read literally.

For a Hamming length

n=2
m
−1,

a binary 1-perfect Hamming code H has

∣H∣=
n+1
2
n
	​

.

Take two distinct cosets of H. They are disjoint, and each separately covers every word exactly once. Their union therefore covers every word exactly twice and has size

n+1
2
n+1
	​

,

which is exactly the double sphere bound. Consequently

K(2
m
−1,1,2)=
n+1
2
n+1
	​

.

In particular,

K(15,1,2)=4096
	​

.

Perfect multiple coverings at radius 1 are established prior art; van Wee–Cohen–Litsyn specifically studied their possible parameters and constructions. 
Eindhoven Tech Research Portal
+1
 Recent work also continues to study multifold 1-perfect codes rather than resolving arbitrary minimum multiple coverings such as n=8. 
Wiley Online Library

So the defensible statement is:

A004045 has a known contiguous initial segment through n=7; a(8) is open. There are isolated/general families of exact values at larger n, notably the Hamming lengths.

That distinction matters.

B. Authors of arXiv:1902.00023

Your attribution is correct:

Denis S. Krotov and Vladimir N. Potapov, On multifold packings of radius-1 balls in Hamming graphs. 
arXiv
+1

No missing coauthor.

C. Notation audit: you have the right problem

This is the part most prone to accidental false prior-art matches, but your interpretation is correct.

A004045 = standard binary K(n,1,2). Both OEIS and the 1993 paper have the same quantifier: for every x, at least two members of C lie in its closed radius-1 Hamming ball. 
OEIS
+1
 Equivalently, in graph language,

K(n,1,2)=γ
×2
	​

(Q
n
	​

),

the double-domination number of the n-cube, since N[x] in Q
n
	​

 is exactly the radius-1 Hamming ball. The graph-theory definition of double domination is ∣N[v]∩D∣≥2 for every vertex. 
Combinatorial Press
+1

It is not MCF. The Hämäläinen–Honkala–Litsyn–Östergård 1995 MCF notion only requires multiplicity μ for points at maximum distance r from the code—the “farthest-off points”—while ordinary multiple covering requires the multiplicity condition everywhere. 
SIAM

It is not a 2-fold packing. A λ-fold packing says every radius-1 ball contains at most λ codewords; a μ-covering says at least μ. Krotov–Potapov explicitly distinguish these. 
arXiv
 In fact, because a radius-1 ball in Q
8
	​

 has nine vertices, complementing a simple μ=2 covering gives a 7-fold packing, not a 2-fold packing.

It is also not Klapper's multicovering radius. There the quantifiers are essentially: given an m-tuple v
1
	​

,…,v
m
	​

, find one codeword simultaneously within radius r of all v
i
	​

. 
UK College of Engineering
+1
 And it is unrelated to the recent terminology “nearly perfect covering codes,” meaning ordinary radius-1 covering codes meeting the van Wee bound. 
arXiv

So you are using the right table and the right K(n,r,μ).

D. Sphere-bound arithmetic and the two tight constructions

For μ=2,r=1, counting incidences between codewords and covered vertices gives

∣C∣(n+1)≥2⋅2
n
,

hence

K(n,1,2)≥⌈
n+1
2
n+1
	​

⌉.

For the OEIS terms:

n	sphere LB	A004045
1	2	2
2	3	3
3	4	4
4	7	8
5	11	12
6	19	20
7	32	32
8	57	unknown, published LB 59

The OEIS values agree. 
OEIS

For n=7, yes:

K(7,1,2)=32.

But I would change your phrase “the [7,4] Hamming code doubled.” Standard K(n,r,μ) uses a set, not a multiset containing each Hamming codeword twice. The correct construction is the union of two distinct cosets of the [7,4,3] Hamming code. Each coset is a perfect 1-cover; together they give multiplicity exactly two. Size 16+16=32, matching the sphere bound.

Likewise, K(8,1)=32 is established; modern work explicitly refers to codes attaining K(8,1)=32. 
Aalto University's research portal
 Historically, the exact lower bound K(8,1)≥32 required nontrivial work. 
Pure

A particularly transparent 64 construction for the double-covering problem is:

C
0
	​

=H
7
	​

×F
2
	​

,

which has size 32 and covering radius 1. Pick v∈
/
C
0
	​

; then C
0
	​

+v is a disjoint radius-1 covering. Therefore

C
0
	​

∪(C
0
	​

+v)

is a double covering of size 64. Hence K(8,1,2)≤64.

So point 2's upper-bound reasoning is valid once “two copies” is understood as two disjoint translates, not duplicate codewords.

Prior-art chain

Your four papers form a sensible bound-table chain:

Hämäläinen–Honkala–Kaikkonen–Litsyn (1993) introduced/studied exactly these K(n,r,μ) tables. 
Tel Aviv University
 Östergård (1995) used tabu search to improve many of the upper bounds in those tables. 
Aalto University's research portal
 Seuranen's 2007 paper supplied new lower bounds. 
EBSCO OpenURL
+1
 Krotov–Potapov explicitly say their Theorem 6 updates previous lower bounds in Seuranen's Table 1. 
ResearchGate

I would not call Seuranen's Table 1 a “maintained” table; it is a static published table serving as the prior baseline.

For a fuller genealogy, add at least van Wee–Cohen–Litsyn's 1991 paper on perfect multiple coverings. 
Eindhoven Tech Research Portal
 Clayton's 1987 UCLA thesis, Multiple packings and coverings in algebraic coding theory, is also cited in the MCF literature and predates the 1993 table paper. 
SIAM

E. Is n=8 computationally tractable today?

Yes. This looks like a very plausible exact-computation target today. The hard part is likely certificate-quality symmetry handling, not raw instance size.

The most direct 0–1 formulation has only 256 binary variables, one x
c
	​

 for every word c∈{0,1}
8
, and 256 local constraints

c:d(c,v)≤1
∑
	​

x
c
	​

≥2

for every v. Each constraint contains exactly nine variables. To test a putative size M, add

c
∑
	​

x
c
	​

≤M.

So closing the interval means SAT/PB/ILP feasibility checks for M=59,…,63, stopping as soon as a construction occurs and proving all smaller values infeasible.

The naïve subset space is enormous—for example

(
59
256
	​

)≈6.18×10
58
,

so brute-force subset enumeration is irrelevant. But the automorphism group

Aut(Q
8
	​

)=2
8
⋊S
8
	​


has size 256⋅8!=10,321,920, and much stronger canonical augmentation/stabilizer pruning is possible than merely dividing by that number.

There is also unusually strong near-equality structure. For a size-M double covering, total ball incidence is 9M, versus the mandatory 512. Thus the aggregate coverage excess is only

9M−512.

At M=59, that is just 19. Any hypothetical 59-code is therefore almost a perfect double covering; most vertices must have coverage exactly 2. That is excellent material for branching constraints, integer cuts and exact enumeration.

Historically, Seuranen's dissertation says exactly the relevant toolkit was already being used: exhaustive search to construct or rule out multiple coverings, with integer-programming formulations, bounds on partial-code coverage, and code-isomorphism pruning. 
Aalto University's research portal
 Modern PB/SAT gives substantially better proof infrastructure.

For a publishable attack I would use PB/SAT plus proof logging, not rely on a black-box MILP optimum: symmetry-break aggressively; encode the 256 local constraints plus cardinality; use canonical/isomorph rejection where necessary; and demand a checkable UNSAT certificate (e.g. VeriPB/LRAT-style workflow) plus a trivial independent verifier for any construction.

One encouraging sanity check: I formulated the raw 256-variable MILP during this review, and stock HiGHS reported size ≤59 infeasible in about 8.5 seconds. I am not counting that as a mathematical result or prior art—it is floating-point branch-and-bound with no exported exact certificate, and I have not independently verified its proof—but it strongly suggests that even improving the published lower bound from 59 may be cheap. Size ≤60 did not resolve in a short 35–40 second probe, which is also consistent with symmetry, rather than model size, being the real issue.

Bottom line

If the fixed statement is rewritten as:

“The first unresolved term of A004045 is a(8)=K(8,1,2). The best published bounds we can verify are 59≤a(8)≤64, from Krotov–Potapov's lower bound and a 64-word construction. No later published improvement has been located through August 2026.”

then I endorse it.

I would reject only the phrase “exact values are known only for n≤7,” because later Hamming lengths such as n=15 are exactly determined. I also would not describe the 59–64 non-improvement after 2020 as an absolutely exhaustive theorem about every thesis/non-English publication; it is a strong literature-search conclusion.
