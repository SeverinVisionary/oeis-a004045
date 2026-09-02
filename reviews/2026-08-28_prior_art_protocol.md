# Prior-art search protocol (ChatGPT professor leg, Extra High)

**Date:** 2026-08-28 · **Session:** `07e7e64f` · `chatgpt verify` → VERIFY PASSED, exit 0
**Mode:** Extra High — the depth leg on a fixed question. Requested as methodology,
not as a search: "design the search protocol, so that a second person can execute
it and we can both say afterwards how much of the space was actually covered."

Two name errors in the reply, corrected wherever we acted on it: the Aalto
dissertation author is **Esa A.** Seuranen (not Jukka), and the covering-codes
Honkala is **Iiro** Honkala (Juha Honkala is a different mathematician).

Executed results are the round-2 ledger in `PRIOR_ART.md`.

---

Below is a protocol that distinguishes “searched,” “covered,” and “excluded.” A second person should be able to execute it and produce the same audit trail.

A. Systematic prior-art protocol
0. Freeze the mathematical identity before searching

Create a one-page IDENTITY.md containing:

Universe: V = F_2^8, |V|=256.

B_1(v) = {c : d_H(c,v) <= 1}, size 9.

Code is a set, not a multiset.

Requirement: |C intersect B_1(v)| >= 2 for every v.

Quantity: minimum |C|.

Equivalent IP: min 1^T x, (I+A(Q_8))x >= 2*1, x in {0,1}^256.

Claims being searched separately:

exact K(8,1,2);

lower bound K(8,1,2) >= 61;

nonexistence of size M=60;

existence/nonexistence for each M=59,...,64.

Every possible hit must be compared against this sheet. This prevents false synonym hits.

Also record the exact equivalent graph statement:

K(8,1,2) = gamma_{x2}(Q_8)

where gamma_{x2} denotes 2-tuple/double domination with closed neighborhoods.

And the important complementary formulation:

K(8,1,2) = 256 - L_7(Q_8)

where L_7 is the maximum 7-limited packing number defined by

|N[v] intersect L| <= 7 for every v.

That second equivalence deserves its own search lane.

1. Search the canonical identifier

Resources:

OEIS: https://oeis.org/A004045

OEIS internal record: https://oeis.org/A004045/internal

OEIS history: https://oeis.org/history?seq=A004045

Google/Google Scholar.

Queries:

"A004045"
"A004045" 8
"A004045" 61
"A004045" 60
"2, 3, 4, 8, 12, 20, 32"

Hit: another source states or links an n=8 result.

Miss: only establishes that the result is not attached to the known sequence identifier.

For OEIS, inspect both current page and version history. A value inserted and later removed still counts as prior public knowledge requiring investigation.

2. Search exact coding-theory notation

Run in MathSciNet, zbMATH, Google Scholar, Semantic Scholar, OpenAlex, and ordinary web search:

"K(8,1,2)"
"K(8, 1, 2)"
"K_2(8,1)" covering
"K_2(8, 1)" covering
"K(8,1,mu)" mu=2
"binary multiple covering" "8" "1" "2"
"multiple covering code" "n=8" "mu=2"
"2-fold covering code" "n=8"
"two-fold covering code" "n=8"
"covering multiplicity 2" "n=8"

Then search feasibility notation:

"(8,60,1,2)"
"(8, 60, 1, 2)"
"(8,61,1,2)"
"(8,62,1,2)"
"(8,63,1,2)"
"(8,64,1,2)"
"binary (8,60,1,2) code"
"no (8,60,1,2) code"
"nonexistence" "(8,60,1,2)"

Repeat for M=57,...,64.

Hit: definition must be checked locally; tuple ordering varies between authors.

Miss: closes only the standard coding-notation lane.

3. Search the graph-equivalent problem independently

Resources:

MathSciNet: https://mathscinet.ams.org/mathscinet/

zbMATH: https://zbmath.org/

Google Scholar: https://scholar.google.com/

Semantic Scholar: https://www.semanticscholar.org/

OpenAlex: https://explore.openalex.org/

House of Graphs: https://houseofgraphs.org/

Queries:

"2-tuple domination" hypercube
"2-tuple dominating" hypercube
"2-tuple domination" "Q_8"
"double domination" hypercube
"double domination" "Q_8"
"double domination number" hypercube
"two-fold domination" hypercube
"multiple domination" hypercube
"2-tuple dominating set" "Boolean cube"
"double dominating set" "Boolean cube"

Also spelling variants:

hypercube "gamma_x2"
hypercube "gamma_{×2}"
hypercube "tuple domination number"

Hit: exact only if every vertex, including vertices in the dominating set, must see two selected vertices in its closed neighborhood.

Miss: closes the most obvious different-subfield synonym lane.

4. Search the limited-packing complement

This is a particularly important independent route.

Queries:

"limited packing" hypercube
"k-limited packing" hypercube
"limited packing number" "Q_8"
"7-limited packing" "Q_8"
"7-limited packing" hypercube
"L_7(Q_8)"
"L7(Q8)" hypercube

Search possible numerical complements:

"Q_8" "limited packing" 192
"Q_8" "limited packing" 193
"Q_8" "limited packing" 194
"Q_8" "limited packing" 195

because K=64,63,62,61 correspond respectively to L_7=192,193,194,195.

Hit: any proved upper bound L_7(Q_8) <= 195 already implies your K>=61; an exact value completely determines K.

Miss: significant because this literature need never mention covering codes.

5. Search fault-tolerant domination

Deletion of any one selected dominator must leave an ordinary dominating set iff every closed neighborhood originally contains at least two selected vertices.

Queries:

"fault-tolerant domination" hypercube
"fault tolerant domination" hypercube
"fault-tolerant dominating set" "Q_8"
"1-fault-tolerant dominating" hypercube
"one fault tolerant domination" hypercube
"redundant domination" hypercube

Hit: verify what is allowed to fail. Some papers mean faulty graph vertices or edges rather than deletion of a selected dominator.

6. Search the hypergraph/set-multicover formulation

Queries:

"set multicover" hypercube
"set multi-cover" hypercube
"minimum 2-cover" hypercube
"2-cover" "closed neighborhood" hypercube
"2-transversal" "neighborhood hypergraph"
"multiple transversal" hypercube
"b-transversal" hypercube
"neighborhood hypergraph" "Q_8"
"covering integer program" hypercube domination

Also search the matrix formulation:

"(I+A)" hypercube domination integer programming
"adjacency matrix" hypercube "double domination"
"closed neighborhood matrix" hypercube covering

Hit: only equivalent if variables are binary and demand is two for every radius-1 ball.

A multicover model allowing the same center twice is not your problem.

7. Search second-nearest / multiple-covering-radius formulations

A code satisfies your condition iff the distance from every word to its second-nearest distinct codeword is at most 1.

Queries:

"second covering radius" binary code
"second covering radius" Hamming
"2nd covering radius" binary
"multiple covering radius" binary code
"covering radius with multiplicity" binary
"second nearest codeword" covering radius

Hit: inspect carefully. “Generalized covering radius” is overloaded and often means something else.

8. Audit general theorems, not merely stated tables

This is mandatory because the result may never have been printed as 61.

Resources:

Cohen–Honkala–Litsyn–Lobstein, Covering Codes, Chapter 14.

Every multiple-covering survey or book chapter returned above.

Graph-theory surveys on tuple domination and limited packing.

For every lower-bound theorem applicable to binary radius-1 multiplicity-2 coverings:

write its hypotheses;

substitute q=2, n=8, R=1, mu=2;

evaluate with exact integer arithmetic;

record the resulting bound.

Do the analogous substitution for general gamma_{xk}(Q_n) and L_k(Q_n) theorems.

Hit: a theorem implying >=61 is prior art even if K(8,1,2) was never mentioned.

Miss: much stronger than merely finding no table entry.

9. Search theses and grey literature

Resources:

ProQuest Dissertations & Theses: https://www.proquest.com/pqdtglobal

BASE: https://www.base-search.net/

CORE: https://core.ac.uk/

OpenAIRE: https://explore.openaire.eu/

institutional repositories;

Google Scholar with filetype:pdf.

Queries:

"multiple covering codes" thesis
"multiple coverings" Hamming thesis
"double domination" hypercube thesis
"2-tuple domination" hypercube thesis
"limited packing" hypercube thesis
"covering codes" integer programming thesis
"K(n,1,2)" thesis

Then author-specific:

"Östergård" covering thesis
"Honkala" multiple covering thesis
"Lobstein" multiple covering thesis
"Krotov" multiple covering thesis
"Potapov" multiple covering thesis

Hit: thesis tables count as public prior statements even if never journal-published.

Miss: closes a major grey-literature lane, not unpublished computations.

10. Search source distributions and computational artifacts

Resources:

GitHub code search: https://github.com/search?type=code

GitLab: https://gitlab.com/

SourceForge: https://sourceforge.net/

Zenodo: https://zenodo.org/

OSF: https://osf.io/

Internet Archive: https://archive.org/

Wayback Machine: https://web.archive.org/

Exact strings:

"K(8,1,2)"
"(8,60,1,2)"
"8,60,1,2"
"n=8 r=1 mu=2"
"n = 8" "r = 1" "mu = 2"
"n=8" "radius=1" "multiplicity=2"
"multiple covering" "8 1 2"

File-oriented web queries:

filetype:txt "(8,60,1,2)"
filetype:dat "n=8" "mu=2" covering
filetype:log "n=8" "mu=2"
filetype:zip "covering codes" Ostergard
filetype:gz "covering codes" Ostergard
inurl:ftp "covering codes"

For every historical computational paper, search:

"<paper title>" source
"<author surname>" covering code software
"<author surname>" covering code program
"<author surname>" tabu covering codes

Hit: dated source/log with an identifiable formulation is evidence of prior computation even without prose publication.

11. Audit maintained tables and their historical versions

Do not inspect only today's page.

Targets:

OEIS A004045 and history.

Any binary covering-code tables encountered.

Historical Kéri covering-code material, commonly linked under the SZTAKI author area:
http://www.sztaki.hu/~keri/codes/
— if dead/moved, enter this exact URL into Wayback.

Author-maintained tables found on Östergård/Honkala/Lobstein/Krotov pages.

Any downloadable .txt, .ps, .tex, .html, .dat bound tables.

For every table:

save current version;

Wayback the URL;

sample snapshots around 1995, 2000, 2007, 2011, 2020, present;

diff the n=8,R=1,mu=2 row.

Hit: an older archived version containing 61+ establishes a priority date that the current bibliography may hide.

Miss: current-page absence alone means almost nothing.

12. Search the central authors' complete web footprints

Do not restrict to publication lists.

For each of:

Patric R. J. Östergård

Jukka Seuranen

Denis S. Krotov

Vladimir N. Potapov

Juha Honkala

Antoine Lobstein

use:

site:aalto.fi "Patric Östergård" covering
site:aalto.fi "Jukka Seuranen" covering
site:math.nsc.ru Krotov covering codes
site:math.nsc.ru Potapov covering codes
site:utu.fi Honkala covering codes
"Lobstein" "covering codes" homepage

Then inspect directories labelled:

software, data, codes, tables, download, publications, reports, talks, misc.

Resolve the present author page rather than guessing a permanent personal-page URL, then Wayback that resolved URL.

Hit: software/table entry matters even if absent from the CV.

13. Search conference abstracts and proceedings

Resources:

IEEE Xplore: https://ieeexplore.ieee.org/

DBLP: https://dblp.org/

SpringerLink proceedings.

Google Books.

WorldCat: https://search.worldcat.org/

Queries:

"multiple covering codes" conference
"multiple coverings of the Hamming space" proceedings
"double domination" hypercube conference
"covering codes" "tabu search" proceedings
"covering codes" integer programming abstract

Inspect especially conference programs where only one-page abstracts survive.

Hit: an explicit numerical result is prior public disclosure even if no full paper exists.

14. Sweep pre-1995 literature manually

Database indexing is insufficient here.

Resources:

MathSciNet historical records.

zbMATH.

EuDML: https://eudml.org/

Google Books: https://books.google.com/

HathiTrust: https://catalog.hathitrust.org/

Internet Archive.

bibliography of Covering Codes, Chapter 14.

Procedure:

Extract every pre-1995 reference under multiple coverings.

Inspect each original paper/proceedings item.

Search scans for:
multiple, covering, multiplicity, binary, radius 1, n=8.

Inspect tables manually; OCR often corrupts mathematical notation.

Hit: even a handwritten-looking table row is substantive if its meaning is unambiguous.

15. Non-English sweep

At minimum:

Russian — MathNet

https://www.mathnet.ru/eng/

"кратное покрытие" "булев куб"
"двукратное покрытие" "булев куб"
"коды покрытий" "кратность"
"двойное доминирование" гиперкуб
German — zbMATH / Google Books
"mehrfache Überdeckung" Hamming
"mehrfache Überdeckung" Hyperwürfel
"zweifache Dominierung" Hyperwürfel
French — NUMDAM

https://www.numdam.org/

"recouvrement multiple" Hamming
"recouvrement multiple" hypercube
"double domination" hypercube
Japanese

CiNii Research: https://cir.nii.ac.jp/

multiple covering code hypercube
double domination hypercube

For Russian particularly, search transliterated author names and journal translations separately.

Miss: English-only searching cannot close this lane.

16. Search correspondence and informal public discussion

Resources:

OEIS history/comments.

Google Groups archives.

MathOverflow.

old author mailing-list archives found via web search.

Queries:

"K(8,1,2)" mailing list
"A004045" discussion
"double domination" hypercube mailing
"multiple covering codes" "n=8" discussion

Do not treat absence as strong evidence; archive coverage is poor.

17. Direct expert query

This is the only serious way to attack “computed but never published.”

Send essentially the same question to Östergård, Honkala, Lobstein, Krotov, Potapov, and Seuranen:

Do you know of any published or unpublished computation of the minimum binary radius-1 covering with multiplicity 2 for n=8, equivalently gamma_{x2}(Q_8)? In particular, was infeasibility at M=60 or a lower bound >=61 ever obtained in an unpublished run, table, source distribution, or old computational project?

Also mention:

equivalently 256 - L_7(Q_8).

Record replies verbatim and date them.

Positive reply: investigate the artifact.

Negative reply: unusually valuable evidence, but still not proof of global nonexistence.

18. Produce a search ledger

For every query record:

Field	Required
Resource	exact database/site
Date	UTC date
Query	exact literal string
Filters	years/language/document type
Results examined	e.g. first 100 / all 27
Candidate hits	count
Same quantity?	yes/no/uncertain
Prior claim?	exact/bound/computation
Stable URL	yes
Archived?	Wayback/DOI/hash
Notes	reason rejected

This ledger, not prose like “we searched extensively,” is what lets you state coverage.

B. K(8,1,2): ranked search order

Given the lanes you have already closed, I would execute the remaining work in this order.

Rank	Lane	Probability of a hidden relevant result	Concrete searches
1	2-tuple/double domination of Q_8	High	"2-tuple domination" hypercube, "double domination" hypercube, "2-tuple dominating" "Q_8" in MathSciNet, zbMATH, Scholar
2	7-limited packing of Q_8	High	"limited packing" hypercube, "7-limited packing" "Q_8", "L_7(Q_8)"; this can hide the result completely under a complementary parameter
3	fault-tolerant domination	Medium-high	"fault-tolerant domination" hypercube, "1-fault-tolerant dominating" "Q_8"
4	general theorem instantiation	Medium-high	CHLL Ch.14 + tuple-domination/limited-packing surveys; evaluate every theorem at n=8,k=2 rather than searching for 61
5	author source/software pages + Wayback	Medium-high	Östergård/Honkala/Lobstein/Krotov/Potapov author-site queries above; inspect data, software, tables, reports
6	direct expert correspondence	Medium-high for unpublished computation	Exact question in Step 17
7	theses/technical reports	Medium	ProQuest, BASE, CORE, OpenAIRE with "multiple covering codes", "double domination" hypercube, "limited packing" hypercube
8	GitHub/GitLab/SourceForge/Zenodo/raw artifacts	Medium	"(8,60,1,2)", "n=8 r=1 mu=2", "K(8,1,2)"
9	OEIS historical record	Medium-low but cheap	A004045, /internal, /history?seq=A004045; inspect deleted/old comments and links
10	historical covering-code tables	Medium-low	historical Kéri/SZTAKI material and every table linked by covering-code authors; Wayback all versions
11	pre-1995 proceedings/scans	Low-medium	CHLL bibliography → original papers; IEEE Xplore, HathiTrust, Google Books, IA
12	Russian/Eastern-European literature	Low-medium	MathNet + Russian query strings
13	set-multicover / neighborhood hypergraph literature	Low	"2-transversal" "neighborhood hypergraph", "set multicover" hypercube
14	House of Graphs / generic invariant databases	Low	inspect Q_8 and downloadable invariant records
15	general web/forum/mailing-list residue	Low	exact notation plus synonyms

The top two are the most important remaining blind spot. In particular, I would not consider the synonym search finished until L_7(Q_8) has been treated as a first-class target.

C. Synonym and parameterisation map
Community	Name / notation	Same quantity?	Conversion / trap
Coding theory	K(n,R,mu) multiple covering code	Yes under usual set convention	Yours is K(8,1,2)
Coding theory	binary (n,M,R,mu) multiple covering	Yes if every vector has >=mu distinct codewords within R	Search nonexistence at (8,60,1,2)
Coding theory	mu-fold / multiple covering of Hamming space	Usually yes	Check whether repeated codewords are permitted
Coding theory	covering with multiplicity mu	Usually yes	“Multiplicity” can mean multiset centers
Coding theory	second covering radius / second-nearest covering radius	Equivalent feasibility formulation	Requirement is second-nearest distinct codeword distance <=1
Coding theory	generalized covering radius	Ambiguous	Often means a completely different higher-dimensional invariant
Coding theory	multiple covering of farthest-off points / MCF	Generally no	May impose multiplicity only on farthest-off points, not every vector
Coding theory	perfect multiple covering	Stronger/different	Usually exact constant coverage rather than >=2
Coding theory	identifying code	Different	Adds separation of neighborhood traces
Coding theory	redundant/fault-tolerant identifying code	Different/stronger	Has identification constraints
Graph domination	2-tuple domination	Exactly yes	`
Graph domination	double domination	Exactly yes under standard definition	Usually synonym for 2-tuple domination
Graph domination	gamma_{x2}(Q_n) / gamma_{×2}	Exactly yes	K(n,1,2)=gamma_{×2}(Q_n)
Graph domination	2-domination, gamma_2(G)	Usually no	Commonly requires 2 neighbors only for vertices outside D
Graph domination	total 2-domination	No	Uses open N(v), excluding the vertex itself
Graph domination	k-tuple total domination	No	Open-neighborhood variant
Graph domination	multiple domination	Ambiguous	Definitions vary; inspect paper
Graph domination	1-fault-tolerant dominating set	Yes under deletion-of-dominator definition	Equivalent to every closed neighborhood having >=2 selected vertices
Graph domination	secure domination	No	Replacement/security condition, not multiplicity
Graph domination	Roman 2-domination / Roman {2} domination	No	Weighted labels, not a subset multicover
Graph domination	{2}-domination	Usually no	Often integer-valued vertex functions
Graph packing	7-limited packing of Q_8	Complement-equivalent	K(8,1,2)=256-L_7(Q_8)
Graph packing	k-limited packing	Equivalent on regular graphs after changing k	For Q_n, complement threshold is n+1-2=n-1
Graph packing	open packing	No	Uses open neighborhoods and normally upper bound 1
Hypergraph theory	2-transversal of neighborhood hypergraph	Yes if transversal is a set	Hyperedges are N[v]; hit each >=2 times
Hypergraph theory	b-transversal / multiple transversal	Potentially yes	Check whether vertex multiplicities are allowed
Hypergraph theory	2-cover of neighborhood hypergraph	Potentially yes	“cover” may refer to the dual orientation
Optimization	minimum set multicover, demand 2	Exactly yes with binary choice variables	Sets are radius-1 balls
Optimization	binary covering IP Ax>=2	Exactly yes	Here A=I+A(Q_8)
Optimization	integer multicover	Not necessarily	If x_c can exceed 1, repeated centers are allowed
Design theory	2-fold covering by Hamming balls	Yes	Blocks restricted to Hamming balls
Design theory	lambda-fold covering design C_lambda(v,k,t)	No in general	Arbitrary blocks, not structured Hamming balls
Association schemes	2-fold covering in H(n,2)	Yes if radius-1 relation is used	H(n,2) graph is Q_n
OEIS	A004045	Yes	Current canonical sequence
General graph language	minimum closed-neighborhood 2-cover	Yes	Useful search phrase
General graph language	twofold neighborhood cover	Potentially yes	Definition must be checked

The three most dangerous false friends are:

2-domination — usually weaker than your condition.

total double domination — open rather than closed neighborhoods.

multiple covering of farthest-off points — multiplicity may not be global.

D. Stopping criteria

There are three defensible stopping levels.

Level 1 — “No indexed publication found”

Required negatives:

exact coding notation searched;

2-tuple/double-domination terminology searched;

limited-packing complement searched;

MathSciNet + zbMATH + Scholar/OpenAlex/Semantic Scholar searched;

general applicable theorems instantiated at the target parameters.

This supports only:

“We found no indexed publication establishing this bound/value.”

It does not address theses, software, private computations, or old tables.

Level 2 — “No earlier public computation located”

Add all of:

thesis/repository sweep;

author publication/software/data pages;

GitHub/GitLab/SourceForge/Zenodo/artifact search;

current and archived maintained tables;

pre-1995 scan/bibliography sweep;

Russian/German/French search;

conference abstracts/proceedings;

OEIS history/correspondence.

At this point the defensible statement is:

“In a documented search of the indexed literature, grey literature, historical tables, public computational artifacts, and major synonym formulations, we located no earlier public computation establishing K(8,1,2) >= 61.”

That is substantially stronger than “I did not find it.”

Level 3 — “Probably not previously computed at all”

Add:

direct negative responses from the main living researchers/groups associated with multiple covering codes;

explicit question about unpublished solver runs and old source distributions, not merely papers.

Even then I would not write unqualified:

“This was never previously computed.”

An undocumented private run from 1998 is logically impossible to exclude.

Use:

“We found no evidence that this bound had previously been computed, publicly or in the unpublished computations known to the principal researchers we contacted.”

Residual risk after a complete Level-3 sweep:

forgotten private solver run;

lost FTP/source archive;

inaccessible thesis/proceedings;

result embedded in a table with unsearchable notation;

theorem in an unexpected equivalent parameterisation;

non-English/local publication absent from databases.

That residual risk is low but irreducible.

For publication, the strongest useful claim is usually narrower anyway:

“To our knowledge, this is the first publicly documented rigorous proof of K(8,1,2) >= 61.”

That survives discovery of somebody saying “I remember running CPLEX on it in 2003.”

E. Evidence standard: prior art in print vs prior art in substance
Evidence	Prior art in print?	Prior art in substance?	Effect on your novelty	Effect on publishability
Peer-reviewed paper proves K>=61 or exact K	Yes	Yes	Numeric result not new	A paper whose sole result is the same bound is generally not publishable as new mathematics
Conference proceedings / refereed extended abstract	Yes	Yes	Same	Same unless your work supplies materially stronger rigor/method/result
Public thesis proves it	Yes, broadly construed	Yes	Result not new	First journal publication may still be possible, but not as discovery of the result
Technical report / arXiv preprint with proof	Public prior art	Yes	Result not new	Same substantive novelty problem
Thesis/table states the value but gives no proof	Yes	Yes as a prior claim	Cannot claim first statement/computation safely	A first rigorous proof/certificate can still be publishable
Survey quotes the value without proof	Yes	Maybe	Numeric claim already public; trace its source	Rigorous proof may still be new
OEIS entry/comment states exact value	Public record	Yes as a claim	Do not claim first public value	Proof/certification may remain novel
Maintained personal webpage gives exact value	Weak formal publication	Yes	Do not claim first computation without qualification	Rigorous published proof can remain worthwhile
Public source distribution contains solved result	No conventional paper	Yes	“First computed” is false	First documented proof/certificate may still be publishable
Public README/solver log clearly identifies model and result	No	Yes	Same	Same
Raw log gives 60 infeasible but model cannot be identified	No	Not yet	Insufficient to establish prior computation of your quantity	Investigate provenance
Private email saying “we solved it years ago”	No	Weak-to-moderate	Undercuts sweeping first-ever claim	Does not normally block first public rigorous publication
Unpublished solver files supplied privately and verifiable	No	Yes	Result was previously computed	First publication/certification may still be new
Personal recollection with no surviving artifact	No	Weak	Mention cautiously; cannot establish mathematical result	Does not defeat a rigorous publication
Incorrect/unverified claimed value	Yes/public	Claim only	It is prior discussion, not established prior result	Your correction/proof can be new

The key distinction is:

Prior numerical knowledge and prior rigorous mathematical result are different novelty questions.

If an old source tree contains a correct M=60 infeasible solver run, you should not say “we first computed the bound.” But if it has no independently checkable certificate or proof, you can still potentially say “first rigorous/publicly verifiable proof.”

If a prior paper already proves K(8,1,2)>=61, the cheap ILP rediscovery is not a new mathematical result, irrespective of whether your solver was independent.
