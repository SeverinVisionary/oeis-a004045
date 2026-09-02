# Round-3 sweep — MathSciNet limits and Level-3 traces

**Date:** 2026-08-28 · **Session:** `acfb08b8` · `chatgpt verify` → VERIFY PASSED, exit 0 · Extra High

Briefed to mark every unreachable lane **NOT CHECKED** rather than pass over it,
and explicitly forbidden from producing MR numbers it could not verify — a
fabricated citation would kill this target for no reason.

Its single strongest lead, the Waterson TU/e thesis, was independently verified
to exist (OpenAlex `W7112221050`), obtained, and read. See `PRIOR_ART.md`.

---

I cannot run a subscription MathSciNet historical subject search from this environment. The free AMS tools do not substitute for it.

Task 1 — MathSciNet, honestly

AMS describes MR Lookup/MRef as tools for verifying and constructing references, while its freely accessible search facilities are MSC search, collaboration distance, journals from the last six weeks, and publications from the last six months. The full Publications Search can search Title, Review Text, MSC, Anywhere, and References, but that historical corpus search is the subscription product. AMS also advertises a 30-day trial and exposes shortened public author profiles; I found no standing free window giving unrestricted historical subject search. 
MathSciNet
+1

Requested query	Answerable exhaustively free?	What a subscriber should run
"double domination" AND hypercube	No — MathSciNet corpus NOT CHECKED	Publications Search: Anywhere = "double domination" AND Anywhere = hypercube; repeat with Review Text and with References. Also try hypercube*, "binary cube", "n-cube".
"tuple domination" AND hypercube	No — NOT CHECKED	Same pattern with "tuple domination"; additionally "2-tuple domination" and "k-tuple domination". Closed-neighbourhood versus total-domination terminology matters.
"limited packing" AND hypercube	No — NOT CHECKED	Anywhere = "limited packing" AND Anywhere = hypercube; repeat in Review Text/References and with "k-limited packing", "7-limited packing", L_7.
"multiple covering" AND (hypercube OR "Hamming space")	No — NOT CHECKED	Prefer two searches if the UI makes nested Boolean awkward: "multiple covering" + hypercube, and "multiple covering" + "Hamming space". Repeat in Review Text and References. Add "multiple covering code*", "multifold covering*".
"K(n,1,2)" OR "K(8,1,2)"	No — NOT CHECKED	Run both literal strings separately in Anywhere, Review Text and References. Formula indexing is fragile, so also search "binary multiple covering" + "radius 1" + 2, and "double covering" + 8.

That recommendation is based on AMS's own search-field documentation: MathSciNet treats References as a separately searchable field, and Review Text is also explicit. 
MathSciNet

What I could confirm through public MR traces

I did not manufacture MR identifiers. Two relevant Russian-lane records publicly expose their MathSciNet links through MathNet:

Krotov–Potapov, On Multifold MDS and Perfect Codes That Are Not Splittable into Onefold Codes (2004): MR2099015. It concerns exact multifold MDS/perfect codes, not minimizing an at-least-two radius-one covering. 
Math-Net

Vorob'ev, Perfect multiple coverings of hypercube (2012): MR3013543. Its definition requires every ball to contain exactly k code vertices, again a different problem. 
Math-Net

So public MR fragments do exist in exactly the Russian journals relevant to this search. They simply don't let me run your five subject queries.

MathSciNet versus zbMATH: residual coverage risk

There is a real nonzero residual risk here. zbMATH currently reports about 5.1 million document entries, coverage complete from 1868 through the present via the Jahrbuch integration, over 5,000 journals plus nearly 3,000 book series, and substantial conference-proceedings coverage. MathSciNet reports over 3.6 million items; Mathematical Reviews itself begins in 1940, although retrodigitized bibliographic metadata reaches the early 1800s. 
ZbMath
+1

More importantly, this is not merely theoretical for your author set: MathNet's current Vladimir Potapov profile reports 89 total publications, 60 in MathSciNet, 55 in zbMATH. Thus a zero-result zbMATH search does not imply a zero-result MathSciNet search even for this precise research group. 
Math-Net

By category:

Journals: exact current MathSciNet-minus-zbMATH journal set: NOT CHECKED. I did not perform a journal-by-journal serial-list diff. A library comparison says Zentralblatt historically had broader applied-math/engineering coverage; another historical comparison characterizes MathSciNet as relatively stronger on American and Zentralblatt on European literature. Treat those as historical tendencies, not a current inclusion theorem. 
CWI
+1

Russian-language material: material risk. AMS explicitly warns that it changed Cyrillic transliteration in January 1983 and that searches may require both old and new transliterations. An older database comparison also found differences in handling Russian originals versus translations. 
MathSciNet
+1

Decades: the large formal difference is pre-1940, which is irrelevant to K(8,1,2). For this problem the more meaningful risk is 1980s–2000s proceedings, local reports, translations and grey literature, not ordinary mainstream journal articles.

Specific Russian journals in this lane: Diskretnyi Analiz i Issledovanie Operatsii and Problems of Information Transmission demonstrably have MR-linked records, so those journals are not a wholesale blind spot. 
Math-Net
+1

Bottom line for Task 1: your five actual MathSciNet searches remain NOT CHECKED. A subscriber run is still worthwhile; the Potapov 60-vs-55 discrepancy is enough that I would not treat the zbMATH sweep as a proxy.

Task 2 — Level 3: computed but never published
Lane A — Wayback snapshots of tables and author pages

Status: NOT CHECKED.

I could reach the Internet Archive front end, but I could not reliably enumerate CDX captures or open arbitrary archived snapshot URLs from this environment. Search-engine indexing of web.archive.org was not sufficient to reconstruct the requested time series.

Therefore I did not actually verify 1996 / 2000 / 2007 / 2011 / 2020 snapshots for Östergård, Iiro Honkala, Lobstein, Krotov, Potapov, Litsyn, Kaikkonen, or the historical covering-code table pages.

Consequently the specific question

Did any archived page ever show the n=8,μ=2 row stronger than 59−64?

is NOT CHECKED, not “no.”

This is the largest explicit hole in this round.

Lane B — old FTP/software/report directories

Status: PARTIALLY CHECKED; archive-only/dead FTP is NOT CHECKED.

I searched live remnants of the old Helsinki/HUT infrastructure for covering-code programs, reports, source, data, FTP directories, “tabu search,” and “multiple covering.” Old report indexes survive, and some legacy reports/program descriptions are still indexed. What I did not find was a live source/data directory identifiable as the output of the 1995 multiple-covering tabu computations.

Some tempting hits were false positives: for example, surviving descriptions of a program called cover concern covering designs, not the word-by-word radius-one multiple-covering problem.

Any dead FTP link that only survives inside an archived author page is part of the Wayback failure above: NOT CHECKED.

So this lane does not exclude an old results.dat, solver log, email-era table, or source distribution on a vanished HUT server.

Lane C — conference talks, abstracts and proceedings

Status: targeted search CHECKED; exhaustive conference-archive sweep NOT CHECKED.

A concrete older dissemination trail surfaced. Cohen–Honkala–Litsyn–Mattson's weighted-covering work appeared as a one-page ISIT 1994 contribution and as a February 1995 Syracuse technical report. The eventual paper records that some of its results had previously been presented at SEQUENCES '91, the 1991 French-Soviet Workshop on Algebraic Coding, EUROCODE '92, and ISIT '94. EUROCODE '92 contained a paper titled On Weighted Coverings and Packings with Diameter One. 
Tel Aviv University
+3
SURFACE
+3
Tel Aviv University
+3

The accessible abstracts describe weighted/perfect constructions and a framework encompassing multiple coverings. They do not expose a computational K(8,1,2) value.

The Syracuse technical-report landing page is accessible, but its downloadable report body was blocked to me. Therefore:

SU-CIS-95-01 full report: NOT CHECKED. 
SURFACE

I also targeted ACCT/WCC/ISIT and general combinatorics searches around “multiple covering,” “double domination,” “limited packing,” and the named researchers. I found no indexed abstract stating K(8,1,2)≥61, K(8,1,2)=⋯, or infeasibility of 60.

However:

systematic WCC-by-year program inspection: NOT CHECKED;

every ACCT proceedings volume: NOT CHECKED;

Finnish workshop programs/slides not indexed by search engines: NOT CHECKED;

Russian local workshop slide archives: NOT CHECKED.

So this is a meaningful targeted negative, not an exhaustive negative.

Lane D — Russian / MathNet / DAIRO

Status: targeted CHECKED; issue-by-issue exhaustive archive sweep NOT CHECKED.

I searched English and Russian variants around кратное покрытие, кратные покрытия, двукратное покрытие, двойное доминирование, булев куб, plus Krotov/Potapov/Vorob'ev.

The main apparent hit is Vorob'ev's 2012 Perfect multiple coverings of hypercube. MathNet's abstract makes the distinction decisive: every vertex must be within radius r of exactly k vertices of C. It is not the minimum-cardinality “at least two” problem. 
Math-Net

Krotov–Potapov's 2004 multifold-code paper likewise studies multifold perfect codes/MDS structures, including nonsplittability. Again, not your optimization problem. 
Math-Net

Their public MathNet profiles/preprint traces did not turn up a separate Q
8
	​

 double-cover computation. Potapov's profile is particularly useful because it exposes publications, talks, a personal-site link and database links; no indexed item there suggested an unpublished M=60 certificate. 
Math-Net

I did not manually inspect every DAIRO issue or every MathNet conference entry: NOT CHECKED.

Lane E — surveys/tables quoting a number without proof

Status: targeted CHECKED; two document bodies NOT CHECKED.

Exact-string and terminology searches for K(8,1,2), 7-limited packing of Q
8
	​

, double domination of Q
8
	​

, and radius-one binary multiple covering did not surface an independent later survey assigning a stronger value.

There is, however, an important old-table location: the 1997 Covering Codes book has a Chapter 14 section explicitly titled “Tables for multiple coverings.” I could verify the section's existence through public metadata/review material, but I did not obtain the relevant table page itself.

1997 book table page containing the n=8,μ=2 entry: NOT CHECKED.

I would expect it to reflect the period's known bounds rather than a modern IP result, but that expectation is not a check.

Lane F — the strongest new grey-literature lead

Status: metadata CHECKED; mathematical contents NOT CHECKED.

This is the item I would inspect next:

Toby W. Waterson, Minimum Cardinality of q-ary Covering and Multiple Covering Codes with Radius 1, Eindhoven University of Technology bachelor thesis, June 2025.

The official TU/e repository confirms the exact title, date, author, supervisors and a 1.15 MB thesis PDF. The title is unusually close to your exact optimization problem—not merely “perfect” multiple coverings or asymptotics. 
Eindhoven Research Portal

I searched the indexed title together with K(8,1,2), “binary,” solver terms, and the 59/64 bounds. Nothing exposed its internal tables. The PDF download itself returned 403 in this environment.

Therefore:

Waterson thesis contents: NOT CHECKED.

I cannot tell you whether it even treats binary n=8,μ=2, much less whether it proves infeasibility at 60. But this is a substantially stronger provenance lead than a generic related paper.

Email you can send yourself
Edit
Send
Recipients

Dear Professor [Name],

I am checking the prior-art status of a small multiple-covering parameter and would be grateful for any pointer you may remember.

For binary words of length 8, let (K(8,1,2)) be the minimum size of a set (C) such that every radius-1 Hamming ball contains at least two codewords. Equivalently, this is the double-domination number (\gamma_{\times2}(Q_8)), and also (256-L_7(Q_8)).

The published tables I have located give the familiar interval (59\le K(8,1,2)\le64). I am trying to determine whether stronger computational nonexistence information ever existed without making it into those tables.

Do you know of any published or unpublished computation for this parameter—old IP/exhaustive-search/tabu-search runs, source distributions, tables, theses, slides, or data files? In particular, was infeasibility at cardinality (M=60) ever obtained in an old solver run?

I am not assuming any stronger result is correct; I am only trying to establish provenance and avoid duplicating prior computation.

Many thanks,
[Name]

My best estimate

If the M=60 infeasibility result is already publicly sitting somewhere, my single best candidate is the 2025 Waterson TU/e thesis PDF, simply because its title targets minimum cardinality of radius-one multiple covering codes directly, rather than perfect coverings or general constructions. My confidence that the thesis contains material relevant to the binary n=8,μ=2 cell is only ~40%; my confidence that it specifically already contains K(8,1,2)≥61 or an M=60 infeasibility computation is ~15–20%.

If that thesis is negative, the largest remaining historical blind spot is archived/dead HUT-era files or private solver output around the Finnish covering-code group, because the Wayback/FTP reconstruction requested here is genuinely NOT CHECKED.

I would not lower the prior-art risk below “material” until two things happen: someone reads the Waterson thesis end-to-end, and a real Wayback/CDX sweep is performed on those old table/author/FTP pages.
