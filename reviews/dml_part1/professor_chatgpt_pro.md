Verdict: SEND AFTER FIXES

Do not email the current version.

The good news is decisive: Theorem 1.1 is correct, Theorem 4.1 is correct, and every displayed numerical calculation I checked—including all numbers singled out in the brief—is correct. I found no additional arithmetic typo after the already corrected 384/20 numerator.

The bad news is also decisive: Section 6 contains a false global claim. The bound in Proposition 6.1 is correct, but the statements that it loses to Krotov–Potapov for every even μ≥4 and that “the gain is confined to μ=2” are false. The abstract then advertises a nonexistent “exact range of multiplicities.” Those statements must not reach a referee. The manuscript also overstates its literature dominance at n=6, presents HHKL’s theorem with undefined notation, and under-describes the disclosed AI use.

These are repairable defects. The core note is mathematically real and potentially publishable.

Ranked findings
1. CRITICAL — Section 6’s global comparison with Krotov–Potapov is false

Location: Introduction, LaTeX lines 127–133; Section 6, lines 310–315. The introduction says the argument loses to Krotov–Potapov “at every even μ≥4,” and Section 6 says “The gain is confined to μ=2.” 

dml_submission +1

What is wrong: Proposition 6.1 itself is correct, but its comparison paragraph is not.

Write

P(n,μ)=
(μ+1)(n+1)−1
μ(μ+1)2
n
	​

,D=(μ+1)(n+1)−1.

For even μ, the Krotov–Potapov formulas give the exact differences

P−KP=
Dn(n+4)
μ2
n
(n−3μ)
	​

(n≡0(mod4)),

and

P−KP=
Dn(n+2)
μ2
n
(n−μ)
	​

(n≡2(mod4)).

Therefore, at the level of the real-valued bounds:

n≡0(mod4)
n≡2(mod4)
	​

P>KP⟺μ<n/3,
P>KP⟺μ<n.
	​


So the comparison depends strongly on both n and μ. It is not confined to μ=2.

A concrete counterexample is n=10,μ=4:

P(10,4)=
5⋅11−1
4⋅5⋅1024
	​

=
27
10240
	​

,⌈P(10,4)⌉=380,

whereas

KP(10,4)=
10⋅12
1024(40+4)
	​

=
15
5632
	​

,⌈KP(10,4)⌉=376.

Your bound is four units stronger, not weaker. The Krotov–Potapov formulas used here agree with their published Theorem 6. 
ar5iv

The three n=8 comparisons in the manuscript remain correct; they establish only that the new bound loses at n=8 for μ=4,6,8.

Concrete fix: Replace the false prose by the two displayed difference identities above. State the sign classification explicitly, but qualify it as a comparison of the underlying real bounds. As Section 4 correctly emphasizes, strict comparison of real numbers does not automatically settle comparison after ceilings. For example,

P(6,4)−KP(6,4)=
51
16
	​

>0,

but both ceilings are 38. Either prove the full ceiling classification separately or avoid claiming one.

Delete from the abstract the sentence about recording “the exact range of multiplicities” unless you replace Section 6 with a correct theorem establishing exactly which notion of gain—real-valued or integer-rounded—you mean.

2. CRITICAL — The abstract’s literature-dominance claim is false as written

Location: Abstract, lines 77–82; introduction, lines 127–130; Section 4 title; Table 4.1. 

dml_submission +2

What is wrong: The abstract says:

“The bound strictly improves the best lower bound in the literature at every even length from six onwards.”

That is contradicted by the manuscript’s own table. At n=6, the known exact lower bound is 20, and Theorem 1.1 also gives 20. The gain over the published best value is zero.

More generally, Theorem 4.1 proves strict dominance over the Krotov–Potapov general formula, not over every lower bound that might exist anywhere in the literature for every even n. The latter is a substantially stronger literature claim and is not established by the paper’s four references.

Concrete fix: Replace the claim everywhere with the exact result you prove:

“After taking ceilings, the bound strictly improves the general lower bound of Krotov and Potapov for every even n≥6. At n=6 it matches the known exact value, while at n=8,10,12,14,16 it raises the tabulated lower bounds.”

Rename Section 4 from “Strict dominance for every even n≥6” to something less context-free, such as:

Comparison with the Krotov–Potapov bound

The statement that five tabulated values are sharpened is correct: those are n=8,10,12,14,16.

The abstract should also state the actual theorem instead of relying on promotional comparisons. A defensible replacement is:

A binary code is a twofold covering of radius one if every word lies within Hamming distance one of at least two codewords. For every even n, we prove

K(n,1,2)≥⌈
3n+2
3⋅2
n+1
	​

⌉

by exploiting the parity of the coverage sum over the ball of a codeword. After taking ceilings, this exceeds the general Krotov–Potapov bound for every even n≥6. It raises the tabulated lower bounds at n=8,10,12,14,16 to 60,192,647,2235,7865, and at n=6 gives an elementary lower-bound proof matching the known 20-word construction.

DML says formulas in abstracts are preferably avoided but does not prohibit them; precision is more valuable here than a vague superiority claim. 
Discrete Math Letters

3. HIGH — The HHKL paragraph is not self-contained and contains claims stronger than necessary

Location: Section 7, lines 323–336. 

dml_submission

What is wrong: The displayed version of HHKL’s Theorem 6 contains k and V(n,r), neither of which is defined. Its hypotheses are also absent. A reader cannot verify from the note that cancellation is legitimate or even understand the displayed formula without consulting HHKL.

The sentence

“ε is their entire gain over the sphere covering bound”

is informal and stronger than needed. Likewise,

“which is why their Corollary 2 is stated only…”

imputes an authorial motive. The sentence about no μ=2 table entry being attributed to Theorem 6 is bibliographic evidence you have said you cannot independently reproduce. It contributes nothing to the proof.

Mathematical verdict on the collapse claim: The claimed algebra is correct, assuming the displayed transcription and its omitted hypotheses are accurate. At r=1,

ε=2⌈
2
μ(n+1)
	​

⌉−μ(n+1).

Thus ε=0 exactly when μ(n+1) is even. For even n, n+1 is odd, so this occurs exactly for even μ. Substitution of ε=0 into the displayed HHKL expression cancels the common n+1−k factor and returns the sphere bound. That part is defensible.

Concrete fix: Do not reproduce the general theorem. Specialize it:

“In HHKL’s Theorem 6 the correction parameter at radius one is

ε=2⌈
2
μ(n+1)
	​

⌉−μ(n+1).

Hence, when n and μ are even, ε=0, and their bound reduces to the sphere-covering bound K(n,1,μ)≥μ2
n
/(n+1).”

Give the exact page number. Remove the Corollary 2 motive sentence and remove:

“Consistently, no μ=2 entry in their own table is attributed to Theorem 6.”

The public Springer page confirms the article and its table but exposes only a subscription preview, not enough for me to certify your transcription of the theorem or its complete hypotheses. Check the original PDF before submission. 
Springer

4. HIGH — The Chen–Li paragraph reads like an invitation to reject on originality

Location: Section 7, lines 338–346. 

dml_submission

What is wrong: Scholarly disclosure is appropriate. The present rhetoric is not:

“it may anticipate part or all of the present note”

tells the editor that the author cannot establish originality. The invitation for knowledgeable readers to contact the author belongs in an informal preprint, not a journal submission.

The underlying bibliographic fact is real: HHKL’s reference list includes “W. Chen and D. Li (forthcoming), Lower bounds for multiple covering codes.” 
Springer
 But a 1993 reference to a forthcoming manuscript is not evidence that an accessible publication contains your theorem, and a failed search is not proof that it does not.

Concrete fix: Replace the entire paragraph by one objective sentence, preferably in a footnote:

“HHKL cite an unpublished or forthcoming manuscript of W. Chen and D. Li entitled Lower bounds for multiple covering codes. I have not located a published version; the novelty comparison here is therefore made relative to accessible published literature.”

Mention the matter briefly in the cover email. Delete “may anticipate part or all” and the invitation to make contact.

As currently written, the paragraph is honest but editorially self-destructive. In the revised form it becomes appropriate scholarly caution rather than a concession that the central result may not be new.

5. MEDIUM — The AI acknowledgment under-describes the actual use

Location: Acknowledgment, lines 350–354; compare the brief’s description of AI use. The manuscript mentions literature search and drafting, while the brief says AI also proposed arguments. 

dml_submission

 

review_brief

What is wrong: The word “including” makes the current acknowledgment not literally false, but omission of argument generation is material in a mathematics paper. It is precisely the use an editor is most likely to care about.

The placement is correct: DML asks for acknowledgments immediately before the references. 
Discrete Math Letters
 The public author-instructions and ethics pages I checked contain no AI-specific provision, so obtaining a written policy answer before submission is prudent. 
Discrete Math Letters
+1

Concrete fix: Use:

“The author used generative artificial-intelligence tools substantially in developing and preparing this work, including for literature exploration, proposing candidate arguments, and drafting text. The author independently verified every mathematical statement and assumes full responsibility for the content. No funding was received.”

Remove:

“The author thanks the referees in advance for their time.”

That sentence sounds ingratiating and adds nothing.

In the policy query, state explicitly that AI proposed candidate arguments as well as assisting with drafting. Ask whether DML requires tool names, versions, dates, or any additional disclosure.

6. MEDIUM — The OEIS sentence misattributes the 59–64 range

Location: Section 5, lines 288–294. 

dml_submission

What is wrong: The sentence says A004045 is the first unknown term,

“where the recorded range was 59≤K(8,1,2)≤64.”

The first clause is correct, but the attribution of that interval to the current OEIS entry is not. The current entry displays exact values only through n=7, namely

2,3,4,8,12,20,32,

and provides no displayed n=8 interval. 
OEIS
 The 59–64 interval appears in Krotov–Potapov’s table. 
ar5iv

Concrete fix:

“The OEIS entry A004045 currently lists exact values through n=7, making n=8 its first unresolved position. Krotov and Potapov record 59≤K(8,1,2)≤64; Theorem 1.1 raises the lower endpoint to 60.”

Add an OEIS bibliography entry with an access date.

7. MEDIUM — Proposition 6.1 is correct but inadequately proved

Location: Section 6, lines 298–308. 

dml_submission

What is wrong: “The same three steps then give the following” is too compressed, especially because the paragraph immediately after the proposition is false. A referee will now distrust the generalization and demand the missing algebra.

Concrete fix: Add the four-line proof. Put

g
μ
	​

(y)=c(y)−μ,E
μ
	​

=(n+1)∣C∣−μ2
n
,

and let S
μ
	​

={y:g
μ
	​

(y)≥1}, s
μ
	​

=∣S
μ
	​

∣. For even n,μ, Step 1 yields a point of S
μ
	​

 in each codeword ball, and therefore

∣C∣≤
y∈S
μ
	​

∑
	​

c(y)=E
μ
	​

+μs
μ
	​

≤(μ+1)E
μ
	​

.

Consequently,

∣C∣≤(μ+1)((n+1)∣C∣−μ2
n
),

which rearranges to Proposition 6.1.

State that n and μ are positive integers and either restrict to the feasible simple-covering range 1≤μ≤n+1 or state the convention for infeasible parameters. Add the rounded consequence

K(n,1,μ)≥⌈
(μ+1)(n+1)−1
μ(μ+1)2
n
	​

⌉

before quoting integer values such as 117 and 118.

8. MEDIUM — The n=6 rhetoric overstates what is search-free

Location: Abstract lines 79–80; Table 4.1; Section 5 lines 282–286. 

dml_submission +2

What is wrong: Theorem 1.1 supplies a search-free lower-bound proof. Exactness still uses the existence of a 20-word covering, which is imported from previous work. Thus:

“recovers one known exact value with no computer search”

and

“settles it in one line”

are liable to be read as saying the complete determination, including construction, is obtained without prior computation.

Concrete fix:

“At n=6, the theorem gives an elementary lower-bound proof which, combined with the known 20-word construction, recovers K(6,1,2)=20.”

Cite a source for the construction itself. Also verify the exact description of Seuranen’s computational method before saying “integer programming together with an exhaustive search.” “Previously established computationally” is safer if the methodological attribution has not been checked directly.

At n=10, Krotov–Potapov’s table attributes the value 188 to Seuranen even though it equals the ceiling of their formula, so cite Seuranen as the primary source as well as Krotov–Potapov. 
ar5iv

9. MEDIUM — Johnson is credited but not cited

Location: Introduction lines 102–104 and Section 7 lines 319–323. 

dml_submission

What is wrong: The manuscript twice attributes the excess method to Johnson, but the bibliography contains no Johnson item. DML’s ethics statement expressly requires authors to cite publications that influenced the reported work. 
Discrete Math Letters

Concrete fix: Add the exact Johnson reference that supports the historical attribution, or remove Johnson’s name and attribute only the version you actually cite.

10. LOW — Theorem 4.1’s asymptotic step omits one comparison

Location: Section 4, lines 242–252. 

dml_submission

What is wrong: For n≥12, the proof applies the n≡0(mod4) expression as a common lower bound without saying that the n≡2(mod4) gap is larger.

Concrete fix: Insert

n(n+2)(3n+2)
2n−4
	​

≥
n(n+4)(3n+2)
2n−12
	​

.

Also replace the final monotonicity assertion by the one-line verification

2
11
=2048>1936=16⋅11
2
,

and

2
n
/n
2
2
n+1
/(n+1)
2
	​

=
(n+1)
2
2n
2
	​

>1(n≥3).

The existing argument is correct; these additions merely close an expositional gap.

11. LOW — State a nondegenerate parameter domain

Location: Theorem 1.1 and Proposition 6.1.

What is wrong: “Let n be even” formally includes n=0, while K(0,1,2) is not a finite simple-covering parameter. This does not damage the implication in Theorem 1.1—the antecedent is impossible—but it is cleaner not to leave the convention implicit.

Concrete fix: State “Let n≥2 be even.” In Proposition 6.1, state explicitly that μ is a positive even integer.

12. LOW — Compilation is clean enough, but verify the current template

I compiled the supplied source twice. It produces four A4 pages, with no undefined references or citation errors. The only box warnings are a 15-point overfull box in the journal header and underfull title/author lines, apparently caused by the fixed template layout.

Four pages is comfortably below DML’s eight-page limit. However, DML states that submissions not prepared with its template will not be processed, so compare this source with the current downloadable template before emailing it rather than assuming an older copied header remains acceptable. 
Discrete Math Letters

Mathematical audit
Theorem 1.1: correct

The proof’s load-bearing calculation is

y∈B(x)
∑
	​

c(y)=
z∈C
∑
	​

∣B(x)∩B(z)∣=(n+1)+2N
2
	​

(x).

Every part checks out. 

dml_submission

Diagonal contribution: Since x∈C, the term z=x appears and contributes

∣B(x)∩B(x)∣=n+1.

Every non-diagonal contribution: Because C is a set, any z

=x has positive Hamming distance from x. In the binary cube,

∣B(x)∩B(z)∣={
2,
0,
	​

d(x,z)=1 or 2,
d(x,z)≥3.
	​


Thus every non-diagonal codeword contributes exactly 0 or 2.

Parity: If n is even, n+1 is odd, while 2N
2
	​

(x) is even. Hence the entire ball sum is odd.

Rounding: It is also a sum of n+1 coverage values, each at least 2, so it is at least 2(n+1). Since 2(n+1) is even and the sum is odd, the next possible integer is at least

2(n+1)+1.

This step is completely valid.

Incidence count: Therefore

y∈B(x)
∑
	​

g(y)≥1,

so every codeword ball meets S. Counting incidences between C and S,

∣C∣≤
y∈S
∑
	​

c(y)=
y∈S
∑
	​

(g(y)+2)=E+2s.

Since s≤E,

∣C∣≤3E.

Final rearrangement:

∣C∣≤3((n+1)∣C∣−2
n+1
)

is equivalent to

3⋅2
n+1
≤(3n+2)∣C∣.

No inequality is reversed, no integrality condition is missing, and no hidden assumption enters after Step 1.

The set hypothesis

Remark 3.2 identifies the essential use correctly. Since C is a set, there is exactly one distance-zero term, namely z=x. With multiplicity m
x
	​

, the diagonal contribution would be m
x
	​

(n+1), whose parity is not fixed when m
x
	​

 may be even. The later incidence counting can be adapted to multiplicities; it is the unique diagonal parity in Step 1 that fails. 

dml_submission

I would slightly soften “the hypothesis is load bearing” to “the hypothesis is essential for this parity argument” unless you also exhibit a multiset counterexample to the theorem itself.

Odd-n example

The code

{000,001,110,111}⊆F
2
3
	​


indeed covers every word exactly twice. Hence E=0, K(3,1,2)=4, and

⌈
11
48
	​

⌉=5.

The example and all its numbers are correct. 

dml_submission

Theorem 4.1: correct

With

L(n)=
3n+2
6⋅2
n
	​

,

the Krotov–Potapov quantities at μ=2,τ=0 are

KP(n)=
n(n+4)
2
n
(2n+6)
	​

(n≡0(mod4)),

and

KP(n)=
n(n+2)
2
n
(2n+2)
	​

(n≡2(mod4)).

The displayed difference identities are exact:

6n(n+4)−(2n+6)(3n+2)=2n−12,

and

6n(n+2)−(2n+2)(3n+2)=2n−4.

Therefore

L−KP=
n(n+4)(3n+2)
2
n
(2n−12)
	​


in the first residue class, and

L−KP=
n(n+2)(3n+2)
2
n
(2n−4)
	​


in the second. 

dml_submission

The small cases are:

n
4
6
8
10
	​

L
48/7
96/5
768/13
192
	​

KP
7
56/3
176/3
2816/15
	​

L−KP
−1/7
8/15
16/39
64/15
	​

	​


Thus:

⌈L(4)⌉=⌈KP(4)⌉=7,
20>19(n=6),60>59(n=8),192>188(n=10).

For n≥12, the estimates are also correct:

2n−12≥n/2(n≥8),

and

n(n+4)(3n+2)≤8n
3
(n≥4),

because the latter is equivalent to

5n
2
−14n−8≥0.

Hence

L−KP≥
16n
2
2
n
	​

>1.

The claim 2
n
>16n
2
 for every n≥11 is correct: it holds at n=11, and 2
n
/n
2
 is strictly increasing for every integer n≥3. The ceiling argument

⌈L⌉≥L>KP+1>⌈KP⌉

is valid.

The asymptotic difference

L−KP∼
3
2
	​

n
2
2
n
	​


is correct in both residue classes, and there are exactly

2
200−6
	​

+1=98

even integers in [6,200].

Numerical ledger

The values produced by Theorem 1.1 are:

n
6
8
10
12
14
16
	​

3n+2
3⋅2
n+1
	​

384/20=96/5
1536/26=768/13
6144/32
24576/38=12288/19
98304/44=24576/11
393216/50=196608/25
	​

ceiling
20
60
192
647
2235
7865
	​

	​


The four values specifically identified in the brief—192,647,2235,7865—are all correct.

The Krotov–Potapov integer values and table gains are also correct:

n
8
10
12
14
16
	​

⌈KP(n)⌉
59
188
640
2195
7783
	​

⌈L(n)⌉
60
192
647
2235
7865
	​

gain
1
4
7
40
82
	​

	​


At n=6, the gain over Krotov–Potapov’s formula is 20−19=1, but the gain over the best published value is 20−20=0. That distinction is exactly why the abstract must be changed.

For Proposition 6.1 at n=8:

μ
4
6
8
	​

P(8,μ)
1280/11
5376/31
1152/5
	​

⌈P⌉
117
174
231
	​

KP(8,μ)
352/3
176
704/3
	​

⌈KP⌉
118
176
235
	​

	​


Thus 117 versus 118, 174 versus 176, and 231 versus 235 are all correct. The statement that the deficit widens with μ in those three n=8 examples is also correct.

Other displayed numerical claims checked:

⌈48/11⌉=5: correct.

Both n=4 ceilings are 7: correct.

2
11
>16⋅11
2
: 2048>1936, correct.

There are 98 even n in [6,200]: correct.

2K(7,1,2)=2⋅32=64: arithmetically correct.

60≤K(8,1,2)≤64 follows from the theorem and the stated upper bound: correct.

No additional arithmetic typo was found.

Section-by-section disposition

Abstract: Not acceptable yet. It contains the false n=6 dominance claim and advertises a false multiplicity classification.

Section 1, Introduction: Definitions are clear. The preview of Section 6 is false; the “best published bound” language is too broad.

Section 2, Notation: Correct. The excess identity, s≤E, and the ball-intersection numbers are all correct.

Section 3, Theorem 1.1: Correct. No mathematical amendment required beyond stating n≥2 and possibly sharpening Remark 3.2’s wording.

Section 4, Theorem 4.1: Correct. Add the omitted residue-class comparison and one-line monotonicity verification.

Section 5: All arithmetic is correct. Repair the OEIS attribution and moderate the n=6 “without search” rhetoric.

Section 6: Proposition 6.1 is correct. Its comparison with Krotov–Potapov is false and must be replaced.

Section 7: The HHKL collapse algebra is correct conditional on the quoted theorem, but the presentation is not self-contained. The Chen–Li paragraph should be shortened and de-escalated.

Acknowledgment: Correctly placed but should explicitly mention AI-assisted argument generation.

Bibliography: Add Johnson and OEIS; add precise page references for HHKL; cite Seuranen directly at n=10.

I did not treat omission of the separate K(8,1,2)≥61 Lean result as a defect. The brief explicitly says this note intentionally isolates the elementary K(8,1,2)≥60 theorem. 

review_brief

Desk-rejection assessment
Current version

The current file has a meaningful desk-rejection risk for four concrete reasons:

The abstract contains a claim contradicted by the paper’s own table.

Section 6 makes a mathematically false universal assertion.

The related-work section reproduces a theorem with undefined notation and then concedes that an unlocated manuscript may contain “part or all” of the contribution.

The acknowledgment does not disclose the most sensitive part of the AI use—candidate argument generation.

An editor finding either of the first two may reasonably stop reading.

Revised version

After the fixes, this is not merely an incremental table update. The contribution is a uniform theorem with a clean mechanism:

In a simple covering, centering at a codeword creates a unique diagonal contribution n+1, whose parity forces excess when n is even.

That is the paper. The numerical improvements are consequences.

The title is accurate and reasonably strong. Four pages is an excellent length for DML, and the journal expressly welcomes both nontrivial progress on existing problems and short or alternative proofs. 
Discrete Math Letters
 The manuscript’s lack of institutional affiliation and the author’s publication history are not formal defects; DML says editorial decisions are based on scientific content, importance, originality, clarity, and contribution. 
Discrete Math Letters

DML does conduct an initial editorial screening before external review, so accuracy in the abstract and novelty paragraph matters disproportionately. 
Discrete Math Letters

My submission judgment after correction would be:

Mathematical theorem: worthy of submission.

Current manuscript: not ready.

Expected editorial framing after revision: a concise new parity refinement, not “five improved table entries.”

Primary residual risk after revision: prior-art uncertainty, especially the Chen–Li manuscript—not correctness.

Make the Section 6 correction, rewrite the abstract and introduction, repair the HHKL/Chen–Li discussion, correct the OEIS attribution, and obtain the journal’s written AI-policy answer. Then send it.

Final verdict: SEND AFTER FIXES.

MARKER-DML-PROF-2026-09-03.
