# Package review — Fable 5.1 leg, round 2 (final gate before emailing DML)

Date: 2026-09-02. Reviewed: `review_brief_pkg.md`, `DML_RULES.md`, `dml_submission.tex`/`.pdf`,
`CHECKLIST.md`, `SUBMISSION_EMAIL.md`, `POLICY_QUERY_EMAIL.md`, the template in
`template/unz/DML-Template/DML-Template.tex`, `kp.txt`/`kp.pdf`, the fetched journal pages in
`pages/`, and the sampled DML PDFs in `pdfs/`. I did not author any of the package and I did not
edit any file in it. Compilation was done on a copy in a scratch directory so the package PDF was
not overwritten.

## Verdict: **APPROVE**

The package violates no rule the journal states, every displayed number reproduces under exact
rational arithmetic, all five references are bibliographically correct (checked against Crossref,
the MathSciNet serials list, and the template's own examples), and both emails are consistent with
the manuscript and with the addresses on the journal's Contact page. Nothing I found would make an
editor stop reading.

Two items below are **confirm-or-reword** tasks for the author (five minutes each): they are
statements about the contents of reference [1] (Hämäläinen–Honkala–Kaikkonen–Litsyn 1993) that no
reviewer in either round has been able to check against that paper. If the author has the paper
open and has checked them, send as is. Everything else is optional polish.

---

## 1. What I checked and found correct (coverage)

### Compilation
- `tectonic -X compile dml_submission.tex --outdir .` on a copy: **4 pages, A4 (595.28 × 841.89 pt)**,
  0 errors, no undefined references or citations. `pdftotext` of my build is **byte-identical** to
  `pdftotext` of the package `dml_submission.pdf`, so the shipped PDF is the shipped source.
- Warnings (identical on each of the three TeX passes): one overfull `\hbox` (15.0 pt) at lines
  39–51 (the template's own `\hglue-15pt` header `\makebox`) and four underfull `\hbox` (badness
  10000) at lines 53–64 (the `\\`-terminated `\noindent` title/author/affiliation/date lines the
  template dictates). **No warning originates in the body.** Compiling the untouched template
  produces the same warning pattern (see the batch result recorded in the final message).
- Page margin: 4 of 8 template pages; page 4 is roughly two-thirds full. The journal re-typesets in
  TeX Gyre Schola, which is wider than Computer Modern by well under 15 %; the published length will
  be 4–5 pages. Safe by a wide margin.

### Template fidelity (H2, §2.2, checklist items 2–3)
- Preamble up to `\begin{document}`: identical to the template except for dropped blank lines.
- Header `\makebox` block: identical except that the template's commented-out `%\vfill` line was
  removed. Immaterial.
- Class, geometry, package list, `titlesec` format (including the template's odd `{1em.}`),
  `caption[labelfont=bf]`, both `\counterwithin`, all ten `\newtheorem`s, `\fnsymbol` footnotes,
  `\allowdisplaybreaks[4]`, bibliography `itemsep` patch, `\baselineskip` settings,
  `\setcounter{page}{1} \thispagestyle{empty}`, the "Discrete Math. Lett. X (202X) XX--XX"
  placeholder and the "Day Month 202X" date line: all present and verbatim.
- No `eqnarray`, no `$$`, no added packages, no manual numbering.
- Author/affiliation lines follow the single-author form actually printed by the journal: P9
  (Lauri) reads "Juho Lauri∗ / Helsinki, Finland / ∗ E-mail address: juho.lauri@gmail.com" with no
  superscript numeral; the manuscript's page 1 renders line-for-line the same way. Verified from
  `pdfs/Lauri_v16_pp94-99.txt` and my rendered page 1.

### Front matter
- Title: Title Case, no formula, no abbreviation.
- Abstract: inside `abstract` with `\noindent`; 173 words (sample range 87–239); zero math mode;
  the one reference is in the bracketed inline form used by P2 and P9 (`[{\it IEEE Trans. Inform.
  Theory} {\bf 67} (2021) 3585--3598]`), and the volume/year/pages in it are correct (Crossref).
- Keywords: six, lower-case, semicolon-separated, terminal period. MSC: 94B65 ("Bounds on codes"),
  05B40 ("Combinatorial aspects of packing and covering"), 94B75 (covering radius etc.) — all three
  confirmed in `pdfs/classifications2020.txt`.

### References (item by item, against Crossref + `pdfs/mathscinet_serials.txt` + template examples)
| # | Entry | Verified |
|---|---|---|
| [1] | H. O. Hämäläinen, I. S. Honkala, M. K. Kaikkonen, S. Litsyn, Bounds for binary multiple covering codes, *Des. Codes Cryptogr.* **3** (1993) 251--275. | Authors, title, vol. 3, 1993, pp. 251–275 all match Crossref (DOI 10.1007/bf01388486). Abbreviation is the MathSciNet form (serials list line 682). |
| [2] | D. S. Krotov, V. N. Potapov, On multifold packings of radius-1 balls in Hamming graphs, *IEEE Trans. Inform. Theory* **67** (2021) 3585--3598. | Matches Crossref (DOI 10.1109/tit.2020.3046260): vol. 67, 2021, pp. 3585–3598. Sentence-case title. Abbreviation on serials list line 1054. |
| [3] | E. A. Seuranen, New lower bounds for multiple coverings, *Des. Codes Cryptogr.* **45** (2007) 91--94. | Crossref: "Esa Antero Seuranen", vol. 45, 2007, pp. 91–94 — so "E. A." is right (KP's own reference list prints "E. S.", which is KP's typo, not ours). |
| [4] | The On-Line Encyclopedia of Integer Sequences, https://oeis.org/A004045. | P4's form (`Name, URL.`) with the entry-specific URL. Alphabetised under "T" as in P4. |
| [5] | G. J. M. van Wee, Improved sphere bounds on the covering radius of codes, *IEEE Trans. Inform. Theory* **34** (1988) 237--245. | Matches Crossref (DOI 10.1109/18.2632): vol. 34, 1988, pp. 237–245. |

- Pattern matches the template's `Caporossi-2000` example exactly: initials-surname, comma-separated
  authors, sentence-case title, `{\it Abbrev.}` `{\bf Vol}` `(Year)` `first--last.`; single terminal
  period; no "pp.", no DOI/URL on journal entries.
- Order: Hämäläinen, Krotov, Seuranen, The On-Line…, van Wee — alphabetical by first author's
  surname; van Wee is last whether filed under V or W.
- `\cite` keys in the body = `\bibitem` keys exactly (five each); every `\ref`/`\eqref` resolves
  (15 labels, all used or defining). `\cite[Theorem 6]{KP-2021}` renders "[2, Theorem 6]".

### Mathematics (recomputed, exact `fractions` arithmetic; scripts run fresh, not the package's)
- Theorem 1.1 at n=6: 384/20 = 96/5 → 20. At n=8: 1536/26 = 768/13 → 60. Remark 3.1: ⌈48/11⌉ = 5.
- Ball-intersection numbers (3): exhaustively n+1, 2, 2, 0 at d = 0, 1, 2, ≥3 for n = 4, 6.
- The F₂³ code {000,001,110,111}: c(x) = 2 at all 8 words. The 20-word code printed in Section 5:
  20 distinct words, minimum coverage 2 (so a genuine twofold covering), E = 12 = 7·20 − 128.
- Table 4.1: ⌈L⌉ = 20, 60, 192, 647, 2235, 7865; ⌈KP⌉ = 19, 59, 188, 640, 2195, 7783; gains
  0(+1 over the formula), +1, +4, +7, +40, +82. All match. The five KP values are exactly the bold
  μ=2 lower bounds in KP's table on page 8 of `kp.pdf` (rendered and read), and each equals
  ⌈formula⌉, as the manuscript says.
- Theorem 4.1: the two difference identities hold exactly for all even n in [4,58]; gaps 8/15,
  16/39, 64/15 at n = 6, 8, 10; n=4 gap −1/7 with both ceilings 7; 2n−12 ≥ n/2 iff n ≥ 8;
  n(n+4)(3n+2) ≤ 8n³ ⇔ 5n²−14n−8 ≥ 0 (expansion checked), true for n ≥ 4; 2¹¹ = 2048 > 1936 =
  16·11²; 2n²/(n+1)² > 1 iff n ≥ 3; the n ≡ 2 (mod 4) gap dominates the n ≡ 0 one for all even n;
  ⌈L⌉ > ⌈KP⌉ at **all 98** even n in [6,200]; n²(L−KP)/2ⁿ → 2/3 (0.65 at n=400).
- KP Theorem 6 transcription: identical to `kp.txt` lines 483–495 (cases (a) and (c)).
- Proposition 6.1: re-derived; P(n,2) = L(n) for all even n ≤ 38; the P−KP identities hold for
  μ = 2, 4, 6, 8 and all even n ≤ 38; sign rules μ < n/3 and μ < n follow.
- **Section 6 numbers, with particular suspicion:** μ=4: n=10: P = 10240/27 → **380** vs KP =
  5632/15 → **376**; n=16: P = 1310720/84 → **15604** vs KP = 15564.8 → **15565**; n=8: P =
  1280/11 → **117** vs KP = 352/3 → **118** (loses, as stated); n=6: P − KP = **16/51** exactly, both
  ceilings **38**. All four statements are true. The false global claim from the prior round ("gain
  confined to μ=2") is gone; the current text claims only what the identities give and explicitly
  declines to classify after rounding. Correct and appropriately cautious.
- HHKL ε at r=1: 2⌈μ(n+1)/2⌉ − μ(n+1) is 0 for even μ, 1 for odd μ when n is even; the collapse to
  μ2ⁿ/(n+1) follows on the manuscript's reading of HHKL's Theorem 6 (see caveat A2).
- OEIS A004045 fetched today (revision #32, 2 May 2026): terms 2, 3, 4, 8, 12, 20, 32 (n = 1..7);
  the "lexicographically first optimal code for n = 6" is printed there as
  `0 1 2 4 8 23 27 29 30 31 39 43 45 46 47 48 49 50 52 56` — **exactly** the manuscript's list. So
  "recorded explicitly in [4]" and "lists exact values only through n = 7" are both true.
- HHKL's reference list (via the zbMATH API record for Zbl document 399367) contains
  "Chen, W. and Li, D. (forthcoming). Lower bounds for multiple covering codes." — the footnote's
  premise is verified. A published version does not surface on Crossref, Semantic Scholar, or web
  search; the only Chen–Li paper found is D. Li, W. Chen, IEEE Trans. Inform. Theory 40 (1994)
  1122–1129, which concerns ordinary K(n,R) and itself refers to the multiple-covering application
  as "forthcoming". The footnote is accurate as written.

### Ethics / disclosure (H7, ethics 1.6)
- Funding and conflict-of-interest statements are in the manuscript (Acknowledgment). The rules
  doc's checklist item 8 says nothing need be printed when there is nothing to declare; printing an
  explicit "none" is the safer reading of 1.6 and harms nothing.

### Emails
- `SUBMISSION_EMAIL.md`: To m.secretary@dmlett.com, no cc — matches H3 and the Contact page
  (`pages/contact.txt`: "m.secretary[at]dmlett.com" under Akbar Ali). Attachment is the PDF only.
  Body: title, author, email, "four pages in the DML template" (true), one-paragraph summary
  (consistent with the abstract), H5 originality wording, funding/COI/AI sentences consistent with
  the Acknowledgment. Nothing contradicts the manuscript.
- `POLICY_QUERY_EMAIL.md`: To ch.editor@dmlett.com (Contact page: "ch.editor[at]dmlett.com" under
  Akhlaq Ahmad Bhatti), cc m.secretary. "Dear Editors" is right: the Editorial Team page lists two
  Chief Editors (Bhatti, Brualdi). The description of the AI use matches the Acknowledgment word
  for word in substance; "half-page proof" matches "The proof occupies half a page". No attachment.
  Nothing contradicts the manuscript.

### Spelling / grammar
- Independent dictionary pass over the body prose: every non-dictionary token is a name, a
  technical term, or an inflection (codeword(s), Krotov, Potapov, Hamming, Seuranen, "suffices",
  "rearranges"…). No doubled words, none of the usual typo patterns. I read all four pages; I found
  no grammatical slip. Voice is consistently third person in the manuscript, first person in the
  emails, which is correct for each.

---

## 2. `CHECKLIST.md` audit — sampled PASS claims

| Item | Claim | My finding |
|---|---|---|
| 2 | Preamble "identical" to template via `diff -w` | **Slightly overstated.** `diff -w` still reports the template's dropped blank lines; the header block also lost the template's `%\vfill` comment line. Neither affects anything. The substance (no setting changed, no package added) is correct. |
| 3 | Header block "identical" | Same `%\vfill` nit. Placeholders retained: correct. |
| 4 | 4 pages, page 4 "about 70% full" | 4 pages confirmed. Page 4 is nearer 65 %; immaterial. |
| 7 | Only formatting/abstract wording changed since the math review | **Verified** by diffing `build/dml_submission.before_conformance.tex` against the final: title case, author/affiliation lines, abstract de-notationed + bracketed reference, "For example," in Remark 3.1, section-heading case, footnote voice, funding sentence, OEIS bibitem re-formed and moved. No theorem, proof, number or table entry changed. |
| 12 | P9 precedent for unaffiliated single author | **Verified** against `pdfs/Lauri_v16_pp94-99.txt`. |
| 14 | ~170 words, zero math | 173 words, zero `$`. Correct. |
| 16 | MSC codes verified | Correct (three hits in `classifications2020.txt`). |
| 24–26, 29 | Cite/bibitem hygiene, order, format, abbreviations | Correct; I additionally verified each entry's volume/year/pages against Crossref, which the checklist did not claim to do. |
| 33–35 | Recipient, attachment, body | Correct. |
| Build record | "Remaining TeX warnings are all inside the template's header/title skeleton" | Correct: lines 39–64 only. |

No PASS is wrong. Two evidence sentences ("identical") are stronger than the diff supports, by
blank lines and one comment.

---

## 3. Findings, ranked

### A. Confirm-or-reword before sending (author task; not a rewrite)

**A1. Section 5, "already present in the table of [1]."** The sentence attributes the upper
bound K(8,1,2) ≤ 64 to HHKL's 1993 table. KP's page-8 table prints "59 − 64" with no citation mark
on the 64 and says its table updates "[48, Table 1]" (Seuranen), not HHKL directly. The doubling
bound itself is trivially true and K(7,1,2) = 32 is on OEIS, but whether *HHKL's table* prints 64 at
(n, μ) = (8, 2) has not been checked by any reviewer. If the author has HHKL's PDF and has seen it,
keep. Otherwise reword to: "…the upper bound being the doubling K(8,1,2) ≤ 2K(7,1,2) = 64."
(dropping "already present in the table of [1]") — zero mathematical cost.

**A2. Introduction, "written $\overline{K}$ in [1]."** A specific notational attribution to a
paper no reviewer could open; the abstract and zbMATH summary are licence-blocked. Honkala or
Östergård are plausible referees and would notice a misattributed notation on line five. If checked
against the paper, keep; otherwise "Allowing repetitions gives a different quantity (see [1]), and
the hypothesis…" loses nothing. The same applies to the two statements about HHKL's Theorem 6
(that ε = 2⌈μ(n+1)/2⌉ − μ(n+1) is its radius-one correction term and that the bound collapses to
the sphere bound when ε = 0): the algebra was verified in round 1 on the author's transcription, not
on the source. The prior professor leg asked for the same confirmation; I repeat it.

### B. Optional polish (none affects acceptance)

**B1. Framing for a graph-theory-weighted board.** A twofold radius-one covering of the hypercube
is exactly a *double dominating set* of Qₙ (every vertex has ≥ 2 members of the set in its closed
neighbourhood), so K(n,1,2) is the double domination number γ×₂(Qₙ) and K(n,1,μ) the μ-tuple
domination number. One sentence in the Introduction saying so, plus the keyword "double
domination", would let every board member place the paper next to P9-style domination work
without changing a symbol. It needs one added reference (F. Harary, T. W. Haynes, Double domination
in graphs, Ars Combin. 55 (2000) 201–213 — **the author must verify this citation; I did not fetch
it this session**), filed under "Harary" after "Hämäläinen". I searched the graph-theory side for
prior art (double / k-tuple domination of hypercubes): nothing hypercube-specific surfaced, so the
reframing does not expose a novelty problem. Recommended; not required.

**B2. Affiliation "Fremont, CA, USA" → "Fremont, California, USA".** The journal "desires,
although not compulsory" no abbreviations in affiliations; P6 shows "CA … USA" is accepted. One
word; the author's call.

**B3. Submission email, "at lengths eight to sixteen" → "at the even lengths eight to sixteen".**
Matches the abstract's "eight, ten, twelve, fourteen and sixteen" exactly.

**B4. Section 5, "The value was previously established computationally [3]."** Seuranen 2007's
reference list (zbMATH API) cites GLPK and nauty, so "computationally" is safe; that the paper
determines K(6,1,2) = 20 specifically is something only the author, with the paper, can confirm
(OEIS credits a(6) to Tabatabai 2020, which is an OEIS-contribution credit, not a priority claim).
Table 4.1's "20 (exact value, [3])" rests on the same reading. Keep if checked.

**B5. `CHECKLIST.md` items 2–3.** Change "identical" to "identical apart from blank lines and one
comment" if the checklist is retained as a record. Cosmetic.

### C. Explicitly not defects
- Omitting ORCID (no field, none printed by the journal).
- Printing "no financial support … no conflict of interest" when the rules doc says nothing need
  be printed: 1.6 says "disclose in the submitted manuscript"; an explicit sentence is the safe
  reading.
- The excluded Lean 4 result (per the brief).
- The AI disclosure's absence of tool names/versions: no DML rule asks for them; add if the editor
  asks.

---

## 4. Answers to the brief's six questions

**1. Rule conformance.** Independently verified against every hard requirement (H1–H9), the
template hard-codes, the four stated reference formats, and the email mechanics. No violation. The
checklist's PASS marks are all correct; two evidence sentences are mildly overstated (§2).

**2. Desk-rejection.** Title is precise and formula-free. Abstract states the theorem's content in
words, the comparison target, the five improved positions, and the μ-extension, in 173 words. The
Introduction reaches the theorem in three short paragraphs and the proof is half a page: the
"alternative/short proof" and "progress on existing problems" framings the home page invites are
both visibly present. The graph-theory weighting of the board is the one real screening risk, and
B1 is the cheapest answer to it: the word "hypercube" is already in the title, abstract and
keywords; "double domination" would make the connection explicit to the majority of the board.
Sole authorship, no affiliation, and no prior publications are not defects in the journal's stated
criteria, and P9 is a published precedent for exactly this author profile.

**3. The emails.** Both are correct, brief, and free of anything that invites a bad decision. On
whether to send the policy query at all: *for* — the journal is silent, the ethics page delegates to
COPE, a three-month wait before a policy-based rejection would be the worst outcome, and a one-question
email with no attachment costs nothing; *against* — a cold question to a small journal may get no
reply for weeks (leaving the author waiting on nothing), and an editor who has not formed a view may
default to "no" when asked in the abstract, whereas the same editor reading the Acknowledgment during
screening judges the disclosure next to the mathematics. My weighing: a policy-based rejection would
in practice happen at screening, not after three months of review, so the downside of *not* asking
is smaller than the query's preamble suggests; and COPE's own position (disclose, no AI authorship)
is satisfied by the manuscript. Net: sending is reasonable and the email is well built, but put a
cap on the wait (e.g. two weeks) and then submit with the disclosure regardless. Do not let the
query become an indefinite blocker.

**4. AI disclosure.** Accurate to the stated facts (literature exploration, candidate arguments,
drafting), complete on the point that matters most (argument generation is named), and placed in
the only unnumbered pre-reference section the template provides. Three sentences; neither too much
nor too little. It reads as a declaration, not an apology, which is right.

**5. Embarrassments.** None found. Journal abbreviations correct; all bibliographic numbers
correct; the OEIS list is verbatim; "E. A. Seuranen" is right where KP themselves have it wrong;
the Chen–Li footnote is factually grounded in HHKL's reference list. Manuscript and emails agree on
every fact they share (title, length, author line, disclosure wording).

**6. Mathematics.** Every displayed number reproduces, including the four Section 6 comparisons
and the 16/51 boundary case. The round-1 false claim is gone and its replacement claims exactly
what the identities support. I found nothing wrong.

---

## 5. Residual unverified items (for the record)
- HHKL 1993 contents: K-bar notation (A2), Theorem 6 ε-form (A2), the (8,2) upper-bound table
  entry (A1). Paywalled; zbMATH summary licence-blocked.
- Seuranen 2007 contents beyond its reference list (B4).
- The Harary–Haynes citation in B1, if adopted.
