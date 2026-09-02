Verdict

The argument is correct for ordinary multiple-covering codes C⊆F
2
n
	​

, where codewords are distinct. I found no published occurrence of the bound

K(n,1,2)≥⌈
3n+2
3⋅2
n+1
	​

⌉(n even),

or of an immediately equivalent statement.

The published chronology I could verify is:

H
a
¨
m
a
¨
l
a
¨
inen et al. / 1996 survey table
post-Seuranen table
Krotov–Potapov
your argument
	​

n=6
19–20
20
20
20
	​

n=8
58–64
58–64
59–64
60–64
	​

	​


The 1996 Honkala–Litsyn survey says explicitly that it is reproducing the radius-one portion of the Hämäläinen–Honkala–Kaikkonen–Litsyn table, and its μ=2 column has 19−20 at n=6 and 58−64 at n=8. Krotov–Potapov later say that their bounds update the Hämäläinen and Seuranen bounds, and print 59−64 at n=8,μ=2. 
Academia
+1

One concrete priority caveat remains: an unpublished and apparently unavailable Chen–Li manuscript, Lower bounds for multiple covering codes, is cited as “forthcoming,” “preprint,” or “in preparation” in sources from 1993–1996. I found no published version or accessible manuscript, so I cannot exclude the possibility that it contains the observation. I also cannot claim that it does. 
Springer
+2
Academia
+2

Proof audit

Put

c(y)=∣B(y)∩C∣,g(y)=c(y)−2.

For x∈C,

y∈B(x)
∑
	​

c(y)
	​

=
z∈C
∑
	​

∣B(x)∩B(z)∣
=(n+1)+2
	​

{z∈C:1≤d(x,z)≤2}
	​

.
	​


The ball-intersection assertion used here is exact in the binary cube:

d(x,z)=1: the intersection is {x,z};

d(x,z)=2: the intersection consists of the two intermediate vertices;

d(x,z)>2: it is empty.

When n is even, n+1 is odd, so the displayed sum is odd. Since it is a sum of n+1 integers each at least 2, it is at least 2(n+1)+1. Hence

y∈B(x)
∑
	​

g(y)≥1.

Thus every x∈C is incident with at least one y∈S={g>0}. Reversing the incidence count gives

M≤
y∈S
∑
	​

c(y)=
y∈S
∑
	​

(g(y)+2)=E+2∣S∣≤3E.

There is no missing contribution in ∑
S
	​

g=E, because g=0 outside S, and ∣S∣≤E follows from integral g(y)≥1 on S. Substitution of

E=(n+1)M−2
n+1

gives exactly

(3n+2)M≥3⋅2
n+1
.

The one important scope condition is that C is a set. For a repeated-word multiple covering, the diagonal contribution need not have the same parity. That does not affect the K(n,R,μ) in your question.

The same proof actually gives, for even n, even μ, and distinct codewords,

K(n,1,μ)≥⌈
(μ+1)(n+1)−1
μ(μ+1)2
n
	​

⌉.

Your bound is the μ=2 case.

1. Is the bound already in the literature?

I did not find a published source for the bound itself.

Van Wee’s 1988 paper is the correct methodological ancestor, but it treats ordinary coverings K(n,R), not μ-fold coverings. Its advertised even-n, radius-one conclusion is the ordinary-code bound K(n,1)≥2
n
/n. 
Eindhoven University Research Portal

Hämäläinen–Honkala–Kaikkonen–Litsyn is the standard paper extending lower-bound methods to binary multiple coverings, and later descriptions explicitly identify it as extending the excess-counting method to that setting. But its recorded small-parameter consequences do not include your inequality: the authors’ subsequent survey reproduces lower bounds 19 and 58, not 20 and 60. 
Springer
+2
ResearchGate
+2

So the placement I can justify is:

Known method family: Johnson–van Wee covering excess/parity, extended to multiple coverings by Hämäläinen et al.
Exact inequality: no published occurrence located.

I would not cite van Wee or Hämäläinen as though either had proved your displayed formula.

The Chen–Li preprint is the unresolved bibliographic hole. Since it remained described as unpublished across several later references and I could not locate its contents, it is a priority risk, not a usable citation. 
Springer
+1

2. Hämäläinen et al. 1993 and Seuranen 2007
Hämäläinen–Honkala–Kaikkonen–Litsyn

It contains general lower-bound theory for multiple coverings in the excess-method lineage, but it does not record or apply a bound that specializes to your 20/60 result.

The contemporaneous Honkala–Litsyn survey states that for lower bounds on K(n,r,μ) it refers to Chen–Li and Hämäläinen et al., and then says it reproduces the r=1 portion of the Hämäläinen table. For μ=2, that table gives:

n=6:19≤K(6,1,2)≤20,
n=8:58≤K(8,1,2)≤64.

Academia

Therefore, whatever general inequalities are proved there, their published specialization gives lower bounds 19 and 58, not 20 and 60.

I did not obtain line-by-line access to the subscription-only primary text. Logically, one cannot exclude an unused lemma in the paper that the authors failed to apply to their own table. But accepting that explanation would require the authors’ own table, the 2007 update, and the 2021 update all to have missed the same immediate specialization.

Seuranen

No. Seuranen’s paper is not a general van-Wee-type analytic bound. Its abstract says that the improvements are obtained using integer programming and exhaustive search, covering 57 parameter cells. 
Springer

For the two cells in question, its resulting lower bounds are:

K(6,1,2)≥20,K(8,1,2)≥58.

Thus it closes n=6 to the known exact value but does not improve the old n=8 lower bound. The consolidated Seuranen table still lists 58−64 in the n=8,μ=2 cell. 
Aaltodoc

In particular, neither cited paper contains a general result which, when correctly specialized, gives your 60.

3. Covering Codes, Chapter 14

There is first a structural correction: Chapter 14 does not have a section entitled “lower bounds.” Its sections are:

definitions;

perfect multiple coverings;

normality;

constructions;

tables for multiple coverings;

multiple coverings of deep holes;

notes.

Chapter 6 is the book’s chapter entitled “Lower bounds,” principally for ordinary covering codes, while Chapter 14 is the separate multiple-covering chapter. 
Cread
+2
Google Books
+2

I could not inspect every displayed formula in the complete Chapter 14 because the available book preview was restricted. I therefore will not claim a literal page-by-page negative.

Nevertheless, I am confident that the book does not record your 20/60 bound as a lower-bound result. The reasons are cumulative:

Two of the book’s authors had just published the 1996 survey table with 19−20 and 58−64.

Seuranen’s later table still had 58−64.

Krotov–Potapov explicitly describe 59 as an update of the Hämäläinen and Seuranen bounds.

If Chapter 14 had stated a theorem immediately yielding 60, that entire later table history would be internally inconsistent.

4. Any later improvement beyond Krotov–Potapov’s 59?

I found none.

Krotov–Potapov define the same simple multiple covering and obtain in Theorem 6(a)

K(n,1,μ)≥
n(n+4)
2
n
(μn+3μ+τ)
	​


for n≡0(mod4), where μ≡τ(mod2). They then say that these inequalities update the previous Hämäläinen and Seuranen lower bounds and print

59≤K(8,1,2)≤64.

arXiv

For n=8,μ=2,τ=0,

8⋅12
2
8
(16+6)
	​

=
96
5632
	​

=58
3
2
	​

,

hence the integer lower bound 59.

As of September 1, 2026, I searched:

both spacings of K(8,1,2);

later papers citing Krotov–Potapov;

the equivalent 2-tuple/double-domination formulation in Q
8
	​

;

the complementary 7-limited-packing formulation;

later radius-one multifold-packing and perfect-code papers.

I found no publication asserting K(8,1,2)≥60, L
7
	​

(Q
8
	​

)≤196, or an equivalent improvement. Crossref currently exposes six citing works for Krotov–Potapov; the listed works concern shortened-perfect-like codes, perfect colorings, orthogonal-array classifications, asymptotic multiple packing, and multifold perfect codes rather than an improved finite K(8,1,2) bound. 
Math-Net

My literature verdict is therefore:

The latest indexed published lower bound I found is 59.

That is a sourced search conclusion, not a proof that no unindexed thesis, private manuscript, or unpublished note contains 60.

5. Blunt judgement

The proposed dichotomy is incomplete.

It is not (b): I find no mathematical error.

I cannot substantiate (a): I cannot give a published reference containing the inequality.

The evidence favors (c): a known-method, apparently unrecorded parity refinement that the standard tables missed.

The strongest evidence is not merely that searches failed. It is the incompatible numerical history:

Hämäläinen’s reproduced table says 19 and 58.

Seuranen computationally reaches 20 but retains 58.

Krotov–Potapov explicitly update those sources to 59.

Your elementary argument validly yields 60.

If the result were already present in one of the three mainstream sources, at least one of those published table statements would be wrong.

The academically defensible way to state priority is therefore:

Proposition. For even n, every binary twofold radius-one covering code with distinct codewords satisfies

∣C∣≥⌈
3n+2
3⋅2
n+1
	​

⌉.

This is an elementary covering-excess/parity argument in the tradition of van Wee and Hämäläinen et al. We have not found this specialization in the published multiple-covering literature.

Then add a footnote disclosing the unlocated Chen–Li preprint. Calling the result unconditionally “new” would be too strong; calling it wrong or already covered by Hämäläinen would be unsupported.
