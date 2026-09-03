# Discrete Mathematics Letters (DML) — submission rules, verified 2026-09-02

Working document for building and reviewing a DML submission package. Every rule
is quoted verbatim with its source URL. "The journal states" means text on
www.dmlett.com or in the journal's own LaTeX template; "published papers do"
means an observation from the nine PDFs read for §6–§7. Anything not verified is
marked **UNVERIFIED** with what was tried.

Journal identity (verified): *Discrete Mathematics Letters*, abbreviation
"Discrete Math. Lett." (https://www.dmlett.com/), E-ISSN 2664-2557 (schema.org
block in the home-page HTML), DOI prefix 10.47443 (every archive PDF), published
"in cooperation with Shahin Digital Publisher"
(https://www.dmlett.com/publication-frequency/).

## 0. Provenance — what was fetched and how

All pages were fetched with `curl` (desktop browser User-Agent) on 2026-09-02 and
returned **HTTP 200**; no dmlett.com page 403'd, so no cache fallback was needed.
Raw HTML and extracted text are in `scratchpad/dml/pages/`; PDFs and text in
`scratchpad/dml/pdfs/`; the template in `scratchpad/dml/template/`.

| Page | URL | Status |
|---|---|---|
| Home | https://www.dmlett.com/ | 200 |
| Manuscript Preparation/Submission | https://www.dmlett.com/manuscript-preparation-and-its-submission/ | 200 |
| Journal Information (index page only) | https://www.dmlett.com/journal-information/ | 200 |
| Editorial Team | https://www.dmlett.com/editorial-team/ | 200 |
| Abstracting and Indexing | https://www.dmlett.com/abstracting-and-indexing/ | 200 |
| Publication Frequency | https://www.dmlett.com/publication-frequency/ | 200 |
| Editorial Process | https://www.dmlett.com/editorial-process/ | 200 |
| Review Speed | https://www.dmlett.com/review-speed/ | 200 |
| Policies (index page only) | https://www.dmlett.com/policies/ | 200 |
| Privacy | https://www.dmlett.com/privacy/ | 200 |
| Open Access and Copyright | https://www.dmlett.com/open-access-and-copyright/ | 200 |
| Publication Ethics | https://www.dmlett.com/publication-ethics/ | 200 |
| Contact | https://www.dmlett.com/contact/ | 200 |
| Announcement (2021 special volume; stale) | https://www.dmlett.com/announcement/ | 200 |
| Journal Archive + Vol. 16, 17, 18 listings | https://www.dmlett.com/journal-archive/ (…/v16/, …/v17/, …/v18/) | 200 |
| LaTeX template (zip, 2,411 bytes, Last-Modified 4 Jan 2026) | https://www.dmlett.com/archive/DML-Template.zip | 200 |
| LaTeX template (.rar link on the submission page) | https://www.dmlett.com/archive/DML-Template.rar | **404** |
| Co-publisher pages | https://shahindp.com/ , /manuscript-preparation/ , /editorial-process/ , /review-speed/ , /journals/ | 200 |
| MathSciNet serial abbreviations (mandated list) | https://mathscinet.ams.org/msnhtml/serials.pdf | 200 (313,537 bytes) |
| DOAJ record | https://doaj.org/toc/2664-2557 | WebFetch 403; see §5.8 |

There is **no separate "Aims and Scope" or "For Authors" page**: scope text lives
on the home page; author instructions live entirely on the Manuscript
Preparation/Submission page. The template zip contains exactly one file,
`DML-Template/DML-Template.tex` (no `.cls`, `.sty`, `.bst`, or sample PDF).

PDFs read in full (text-extracted with `pdftotext -layout`):

| # | File | Paper | Type | Pages |
|---|---|---|---|---|
| P1 | v18/DML26_v18_pp16-20.pdf | Cherkashin, Shubin — Short Proofs of Three Combinatorial Results in the Johnson Scheme | Research Article | 5 |
| P2 | v18/DML26_v18_pp51-54.pdf | Omar — On a Quadratic Relation Between Stanley–Wilf Limits and Füredi–Hajnal Limits | Research Article | 4 |
| P3 | v18/DML26_v18_pp55-62.pdf | Kozerenko — Graphs with Small Triameters | Research Article | 8 |
| P4 | v18/DML26_v18_pp28-33.pdf | Blecher, Knopfmacher — Reservoirs in Permutations | Research Article | 6 |
| P5 | v18/DML26_v18_pp34-35.pdf | Lauri — Corrigendum to "Improved Bounds on the Domatic Numbers of Queens Graphs" | Corrigendum | 2 |
| P6 | v17/DML26_v17_pp1-6.pdf | Bowling, Low — Cozonality in Plane Graphs of Maximum Degree Four | Research Article | 6 |
| P7 | v17/DML26_v17_pp70-74.pdf | Stanić — Signed Toral Tessellations Whose Spectrum Consists of Exactly Two Symmetric Eigenvalues | Research Article | 5 |
| P8 | v17/DML26_v17_pp101-112.pdf | Ali, Gutman, Réti, Albalahi, Hamza — Survey on Extremal Results and Bounds for Elliptic Sombor and Euler–Sombor Indices | Review Article | 12 |
| P9 | v16/DML25_v16_pp94-99.pdf | Lauri — Improved bounds on the domatic numbers of queens graphs | Research Article | 6 |

P5 and P9 were chosen deliberately: their author lists no institution
(see §6.9).

---

## 1. Hard requirements — violation means not processed / rejected

All quotations from https://www.dmlett.com/manuscript-preparation-and-its-submission/
unless another URL is given.

**H1. Language and typesetting system.**
> "A manuscript to be submitted to Discrete Mathematics Letters (DML) for publication should be written in English using LaTeX. The writing must be clear, unambiguous, and grammatically correct. The authors are requested to run their paper through a spell checker before submission."

**H2. Template is mandatory; non-template submissions are not processed.**
> "The authors are required to use the DML-template for preparing their manuscript. Submissions not prepared using the journal template will not be processed."

The link text "DML-template" points to https://www.dmlett.com/archive/DML-Template.zip
(the second link, in the Length bullet, points to `DML-Template.rar`, which
returns 404 — use the zip).

**H3. Submission is a PDF attached to an email to the managerial secretary.**
> "A manuscript should be submitted by sending its PDF file as an email attachment to the managerial secretary via the email address m.secretary@dmlett.com."

**H4. Page cap — 8 template pages for original results; 30 for mini-reviews.**
> "Length: A manuscript with original results should not exceed 8 pages when prepared using DML-template. The page limit of mini-review articles is 30 pages."

Home page (https://www.dmlett.com/):
> "…a forum for the rapid publication of original articles, consisting of at most eight published pages, in all areas of discrete mathematics."
> "This journal also publishes mini-reviews of high quality. The page limit for mini-reviews is thirty pages. Moreover, this journal occasionally publishes autobiographical notes and interview articles (concerning well-known discrete mathematicians) without any page limit."

Note the two phrasings differ ("8 pages when prepared using DML-template" vs
"at most eight published pages"). Published papers are re-typeset in a
different text font (§6.13), so template page count and published page count
are not identical; the safe reading is to satisfy both — stay at or under 8
template pages with margin.

**H5. Originality / no simultaneous submission / exclusivity on acceptance.**
> "Submission of a manuscript to DML implies that the manuscript has not been published elsewhere, is not currently submitted for publication elsewhere, and if accepted by this journal, will not be published elsewhere."

Restated as an ethics rule at https://www.dmlett.com/publication-ethics/:
> "1.3. Simultaneous submission of a manuscript to more than one journal is actually an unethical publishing behavior and is unacceptable. An author should not publish manuscripts containing essentially the same/similar results in more than one journal. Submission of a manuscript to DML implies that the same/similar manuscript has not been published elsewhere, is not currently submitted for publication elsewhere, and, if accepted by this journal, will not be published elsewhere."

**H6. Scope — discrete mathematics; editorial-interest preference; what is "especially welcomed".** (https://www.dmlett.com/)
> "Manuscripts concerning all those areas of discrete mathematics that are closely associated with the research interests of the Editorial Team‘s members are preferred. Manuscripts contributing some non-trivial progress in the solution of existing problems and conjectures, as well as those consisting of an alternative/short proof of some well-known result of discrete mathematics, are especially welcomed."

Initial screening is a real gate (https://www.dmlett.com/editorial-process/):
> "Upon submission, every manuscript is initially evaluated by one or more members of the editorial team. Those manuscripts which pass this initial screening are sent to at least two referees for more detailed evaluation; this evaluation is called the external review process. Those manuscripts which do not pass the initial screening test are rejected without their external review process."

**H7. Ethics conditions that are stated as requirements** (https://www.dmlett.com/publication-ethics/):
> "1.4. Authors of the manuscripts submitted to DML are required to ensure that they have written entirely original works, and if the authors have used the works of others that this has been properly cited or quoted. Authors must cite publications that have influenced the nature of the work reported."
> "1.5. Fraudulent or knowingly inaccurate statements are considered unethical and are unacceptable. The authors should not submit a manuscript to DML if it is plagiarized or fraudulent/fabricated."
> "1.6. Every author is required to disclose in the submitted manuscript any financial or any other substantive conflict of interest that might be construed to influence the results or interpretation of the manuscript. All sources of financial support for the project should also be disclosed in the submitted manuscript."

**H8. Keywords and MSC minimums.** These sit in a list the page introduces as
"the following points are suggested to be considered", but each is phrased with
"should", and the template repeats them as instructions:
> "Keywords: The manuscript should contain at least three keywords."
> "2020 Mathematics Subject Classification (MSC): At least one 2020 MSC should be included."

Template (`DML-Template.tex`): `{\bf Keywords:} keyword 1; keyword 2; keyword 3; keyword 4; keyword 5 (provide at least three keywords).` and `{\bf 2020 Mathematics Subject Classification:} Classification 1, Classification 2, Classification 3 (provide at least one classification number).`

**H9. Fees: none.** (https://www.dmlett.com/)
> "This journal does not charge Article Submission/Publication/Processing Charges."

---

## 2. Formatting rules

### 2.1 What the journal states (https://www.dmlett.com/manuscript-preparation-and-its-submission/)

Preamble to the list:
> "While preparing a manuscript for submission to DML, the following points are suggested to be considered:"

- **Title.**
  > "Title: The title of the manuscript should be very precise and it should cover the theme of the manuscript. It is desired, although not compulsory, to avoid using any mathematical formula and/or abbreviation in the title."
- **Authors and affiliations.**
  > "Authors’ Names and Affiliations: Authors’ full names are preferred. However, in the case where an author has more than two names, at least two full names are required. It is desired, although not compulsory, to avoid using any abbreviations in the authors’ affiliations."
- **Abstract.**
  > "Abstract: The main findings should be stated briefly in the abstract. It is desired, although not compulsory, to avoid using any mathematical formula and/or reference(s) in the abstract."

  Template wording: `Write the abstract here.  If possible, please avoid writing mathematical formula in the abstract.`
- **Keywords / MSC.** See H8. Keywords: at least three. MSC: at least one, **2020** edition. (No maximum is stated for either.)
- **LaTeX environments.**
  > "LaTeX Environments: Sections, theorems, lemmas, definitions, remarks, equations, etc., should be organized into appropriate LaTeX environments."

  Template: `Make the sections and subsections according to your paper. Please organize all your theorems, lemmas, definitions, remarks, etc., into the appropriate LaTeX environments.`
- **Acknowledgment placement.**
  > "Acknowledgment: The acknowledgment section (if needed) should be placed at the end of the manuscript, but preceding the references section."
- **Figures, tables, footnotes, fonts, margins:** the journal's pages say **nothing** about figures, tables, footnotes, colour, font size or margins beyond what the template hard-codes (checked by grep over every page's raw HTML: the only "figure"/"table"/"font"/"margin" hits are WordPress CSS). Follow the template as-is.

### 2.2 What the template hard-codes (`DML-Template.tex`, from https://www.dmlett.com/archive/DML-Template.zip)

Do not change any of these; "prepared using the journal template" is the gate.

| Element | Template setting (verbatim) |
|---|---|
| Class | `\documentclass[10pt,a4paper]{article}` |
| Margins | `\usepackage[margin=1.1cm]{geometry}` |
| Packages | `\usepackage{amsmath,amsthm,amsfonts,amssymb,amscd,cite,graphicx}` plus `titlesec`, `caption` (`[labelfont=bf]`) |
| Section heading style | `\titleformat{\section}{\normalfont\fontsize{12}{15}\bfseries}{\thesection}{1em.}{}` |
| Figure/table numbering | `\counterwithin{figure}{section}` / `\counterwithin{table}{section}` → "Figure 3.1", "Table 1.1" |
| Theorem-like environments (all numbered within section, all amsthm default *plain* style) | `proposition`, `conjecture`, `corollary`, `lemma`, `definition`, `theorem`, `remark`, `example`, `counterexample` (prints "Counter Example"), `observation` — declared as `\newtheorem{X}{Name}[section]`, each with its **own** counter |
| Proofs | `\begin{proof} … \end{proof}` (amsthm) |
| Footnote marks | `\renewcommand{\thefootnote}{\fnsymbol{footnote}}` → ∗, †, ‡ … |
| Display breaks | `\allowdisplaybreaks[4]` |
| Line spacing | `\baselineskip=0.20in` (set several times; the first `\baselineskip=1.20in` before `\begin{document}` is overridden) |
| Page 1 | `\setcounter{page}{1} \thispagestyle{empty}` |
| Bibliography spacing | `\renewcommand{\thebibliography}[1]{\oldbibliography{#1}\setlength{\itemsep}{-2pt}}` and `\footnotesize` before `\begin{thebibliography}{00}` |

Header block (keep it; production fills in volume/pages):
```
\footnotesize{ {\bf Discrete Mathematics Letters} \\ \underline{www.dmlett.com}}
…
\normalsize {\it Discrete Math. Lett.}  {\bf X} (202X) XX--XX
```

Title / authors / affiliations / dates (verbatim skeleton):
```
\noindent
{\large \bf Title of the Research or Review Article}\\

\noindent
First Author$^{1,}\footnote{Corresponding author (xyz1@example.com)}$, Second Author$^{2}$\\

\noindent
\footnotesize $^1${\it Affiliation of the First Author}\\
\noindent
 $^2${\it Affiliation of the Second Author\/} \\

\noindent
 (\footnotesize Received: Day Month 202X. Received in revised form: Day Month 202X. Accepted: Day Month 202X. Published online: Day Month 202X.)\\
```
The corresponding author is marked by a `\footnote{Corresponding author (email)}`
attached to the author name; the date line is left with placeholders at
submission.

Abstract block (verbatim):
```
 \begin{abstract}
 \noindent
 Write the abstract here.  If possible, please avoid writing mathematical formula in the abstract.
 \\[2mm]
 {\bf Keywords:} keyword 1; keyword 2; keyword 3; keyword 4; keyword 5 (provide at least three keywords).\\[2mm]
 {\bf 2020 Mathematics Subject Classification:} Classification 1, Classification 2, Classification 3 (provide at least one classification number).
 \end{abstract}
```
Keywords are **semicolon**-separated; MSC codes are **comma**-separated; both
live inside the `abstract` environment.

Section skeleton in the template: `\section{Introduction}`, `\section{Main Results}\label{sec-2}`, then `\section*{Acknowledgment}` (unnumbered, starred), then the bibliography.

**Equation environments — the eqnarray prohibition (verbatim, template):**
> "In LaTeX, the environment eqnarray or eqnarray* is an old configured command. If we use this old environment, the spaces before and after the suitable operators, e.g. ``+'' or ``='', will be larger than the normal case. Please don't use this old environment. Replace it with other stable and well defined other mathematical environments to handle formulas with multiple rows. For example, please use the environments align (align*) or aligned (aligned*) or multline (multline*) or gather (gathered*) etc."

Nothing similar is said about `$$…$$`, `\[ \]`, `\over`, `\bf` in math, or
`\displaystyle`; only `eqnarray`/`eqnarray*` is named. (The template itself uses
`{\bf …}` / `{\it …}` for text, so those legacy font switches are evidently
tolerated.)

**Citations in text (verbatim, template):**
> "References to the literature should be numbered in square brackets like \cite{Burns-1995,debonothesis}. The entries in the reference list should be in alphabetical order according to the first author listed. Also, please follow the way by which references are quoted at the end of this document."

The `cite` package is loaded, so `\cite{a,b}` prints `[1,2]`-style compressed lists.

### 2.3 Elements added in production (not in the template — do **not** add them yourself)

Observed on every published PDF but absent from the template: the "Research
Article" / "Review Article" / "Corrigendum" label under the header; a `DOI:
10.47443/dml.YYYY.NNN` line in the header; the copyright line "© 2026 the
author(s). This is an open-access article under the CC BY (International 4.0)
license (www.creativecommons.org/licenses/by/4.0/)."; a running head "S.
Kozerenko / Discrete Math. Lett. 18 (2026) 55–62" with page numbers; and body
text in TeX Gyre Schola (see §6.13).

---

## 3. Reference style

### 3.1 Rules the journal states (https://www.dmlett.com/manuscript-preparation-and-its-submission/)

> "References: The command \cite{ … } should be used for citing references in the text, and unused references should be removed. The entries in the references list should be in alphabetical order according to the last name of the first author listed. The abbreviations of the journals’ names, provided by MathSciNet, should be used. If the authors cite the papers that have been retracted, they should include the rationale for doing so in the manuscript text, and they should indicate the articles retracted status in the references list. If the authors cite an erroneous paper whose corrections are available in another paper/note, they should also cite the paper/note addressing the corrections. For preparing the references list, the following way by which references are quoted is desired to follow:"

- **Ordering rule:** alphabetical by *last name of the first author*; numbered `[n]` in that order (`\begin{thebibliography}{00}`). Same rule in the template ("in alphabetical order according to the first author listed").
- **Journal-abbreviation rule:** MathSciNet abbreviations, linked to https://mathscinet.ams.org/msnhtml/serials.pdf (reachable, 313 KB PDF).
- **Hygiene rule:** every `\bibitem` must be `\cite`d somewhere ("unused references should be removed").
- **Self-citation (ethics page, https://www.dmlett.com/publication-ethics/):** "1.7. The authors should cite only the relevant publications, and they should refrain from self-citation as much as possible."

### 3.2 The four formats the journal gives (web page text; typographic instructions in parentheses are the journal's)

- **[Book]** "J. A. Bondy, U. S. R. Murty, Graph Theory, Springer, London, 2008. (Italics should be used for the book title.)"
- **[Edited Book]** "K. Burns, R. C. Entringer, A graph-theoretic view of the United States postal service, In: Y. Alavi, A. J. Schvenk (Eds.), Graph Theory, Combinatorics and Algorithms, Wiley, New York, 1995, 323-334. (Italics should be used for the book title.)"
- **[Journal Paper]** "G. Caporossi, P. Hansen, Variable neighborhood search for extremal graphs: 1. The AutoGraphiX system, Discrete Math. 212 (2000) 29-44. (Italics should be used for the journal name, and the volume number should be bold.)"
- **[Thesis]** "M. Debono, Threshold Graphs as Models of Real-World Networks, Master’s thesis, University of Malta, 2012. (Italics should be used for the thesis title.)"

The same four in LaTeX, verbatim from `DML-Template.tex`:
```latex
\bibitem{Bondy08} J. A. Bondy, U. S. R. Murty, {\it Graph Theory}, Springer, London, 2008.

\bibitem{Burns-1995} K. Burns, R. C. Entringer, A graph-theoretic view of the United States postal service, In: Y. Alavi, A. J. Schvenk (Eds.), {\it Graph Theory, Combinatorics and Algorithms}, Wiley, New York, 1995, pp. 323--334.

\bibitem{Caporossi-2000}  G. Caporossi, P. Hansen, Variable neighborhood search for extremal graphs: 1 The AutoGraphiX system, {\it Discrete Math.} {\bf 212} (2000) 29--44.

\bibitem{debonothesis} M. Debono, {\it Threshold Graphs as Models of Real-World Networks}, Master's thesis, University of Malta, 2012.
```
Two small inconsistencies between the web page and the template: the chapter
example has `pp. 323--334` in the template but `323-334` on the web page;
published papers print **without** "pp." (P1 ref. [14]: "…Springer, Cham, 2026,
261–326."). The template file is what gets compiled, but either form is
evidently accepted.

Pattern common to all four: initials-then-surname for every author (no "and",
no "&"); authors comma-separated; title in roman with sentence capitalisation;
no quotation marks around titles; journal abbreviated (italic) → bold volume →
(year) → page range; single terminal period.

### 3.3 Formats the journal does **not** give — worked examples copied from published papers

The journal gives no format for preprints, websites/databases, article-number
journals, "submitted"/"to appear", or PhD theses. Below is what is actually in
print (all from the PDFs listed in §0; verbatim from text extraction, en-dashes
as printed).

- **arXiv preprint** (P1, ref. [3]): `P. J. Cameron, Problems from BCC30, arXiv:2409.07216 [math.CO], (2024).`
- **arXiv preprint later accepted** (P1, ref. [10]): `P. Keevash, The existence of designs, arXiv:1401.3665 [math.CO], (2014); Ann. of Math., To appear.`
- **Website / database** (P4, ref. [11]): `The On-Line Encyclopedia of Integer Sequences, http://oeis.org/.` (alphabetised under "T", placed last).
- **Submitted, no venue** (P4, refs. [5],[6]): `A. Blecher, A. Knopfmacher, Reservoirs in words over the alphabet [k], Submitted.`
- **Journal with article number instead of pages** (P1 ref. [13]; P7 ref. [2]): `N. Keller, N. Lifshitz, The junta method for hypergraphs and the Erdős–Chvátal simplex conjecture, Adv. Math. 392 (2021) #107991.` and `F. Belardo, S. M. Cioabă, J. H. Koolen, J. Wang, Open problems in the spectral theory of signed graphs, Art Discrete Appl. Math. 1 (2018) #P2.10.`
- **Journal paper with issue number** (P2, ref. [1]): `J. Cibulka, On constants in the Füredi-Hajnal and the Stanley–Wilf conjecture, J. Combin. Theory Ser. A 116(2) (2009) 290–302.` — issue numbers appear in P2 and P3 ref. [4] only; most papers omit them. Either is accepted.
- **PhD thesis** (P6, ref. [1]): `A. Bowling, Zonality in Graphs, Ph.D. dissertation, Western Michigan University, Michigan, 2023.`
- **Book, 2nd edition** (P6, ref. [7]): `G. Chartrand, L. Lesniak, Graphs and Digraphs, 2nd Edition, Wadsworth & Brooks/Cole, Pacific Grove, 1986.`
- **Chapter in edited volume, in print** (P3, ref. [1]): `H.-J. Bandelt, V. Chepoi, Metric graph theory and geometry: a survey, In: J. E. Goodman, J. Pach, R. Pollack (Eds.), Surveys on Discrete and Computational Geometry: Twenty Years Later, Amer. Math. Soc., Providence, 2008, 49–86.`
- **DML's own papers** (P1, ref. [4]): `D. Cherkashin, On set systems without singleton intersections, Discrete Math. Lett. 14 (2024) 85–88.`
- **Corrigendum citing the corrected article** (P5, ref. [1] plus a title footnote): `J. Lauri, Improved bounds on the domatic numbers of queens graphs, Discrete Math. Lett. 16 (2025) 94–99.` with footnote `∗ Link to the referred article: https://doi.org/10.47443/dml.2025.112`.

Observed: none of the nine reference lists contains a DOI or URL for a journal
paper; only the OEIS entry and the corrigendum footnote carry a URL.

---

## 4. Submission mechanics

- **Address:** `m.secretary@dmlett.com` (https://www.dmlett.com/manuscript-preparation-and-its-submission/, quoted in H3). The Contact page (https://www.dmlett.com/contact/) lists this address under **Akbar Ali**, "University of Hail, Hail, Saudi Arabia — Email: m.secretary[at]dmlett.com, ak.ali[at]uoh.edu.sa". Note the Editorial Team page (https://www.dmlett.com/editorial-team/) names a different "Managerial Secretary — Saima Saleem, Gujrat, Pakistan"; the two pages disagree on who holds the role, but the address is the same.
- **Chief-editor address** (contact page): "Akhlaq Ahmad Bhatti … Email: ch.editor[at]dmlett.com, akhlaq.ahmad[at]nu.edu.pk". Contact page closing line: "If you have any queries, please contact any of the above-mentioned persons."
- **What to attach:** the journal asks for "its PDF file as an email attachment" — PDF only. **UNVERIFIED** whether the `.tex` source is requested later (after acceptance); no page mentions source files, and the word "tex" does not occur in any page's text (only inside the linked zip filename).
- **File formats:** LaTeX → PDF. No Word/other format is mentioned anywhere.
- **What the email should say:** **UNVERIFIED — the journal states nothing.** No page uses the phrase "cover letter", and there is no submission form. It is neither required nor prohibited. A short email identifying the title, authors, corresponding author, and (optionally) suggested referees is consistent with everything stated.
- **Suggesting referees — explicitly allowed, non-binding:**
  > "When submitting a manuscript, the corresponding author may suggest some potential referees. The editorial office may or may not use such suggestions."
- **Article types accepted:** original research articles (≤ 8 pages), mini-reviews (≤ 30 pages), and "occasionally … autobiographical notes and interview articles … without any page limit" (home page). The v18 archive also shows a "Corrigendum" type.
- **Special volumes:** the Announcement page (https://www.dmlett.com/announcement/) is dated "August 31, 2021" with a submission deadline of "March 31, 2022" — stale; ignore.
- **No online system, no account, no ORCID field, no fee.**

---

## 5. Policies

### 5.1 Peer review (https://www.dmlett.com/editorial-process/)
> "Discrete Mathematics Letters uses the single-blind peer-review model (that is, the reviewers know the authors’ identities but the authors do not know the reviewers’ identities). This journal relies on its editorial board members and referees to evaluate a paper for publication. Upon submission, every manuscript is initially evaluated by one or more members of the editorial team. Those manuscripts which pass this initial screening are sent to at least two referees for more detailed evaluation; this evaluation is called the external review process. Those manuscripts which do not pass the initial screening test are rejected without their external review process. Once the referees’ reports on a manuscript are received, they are sent to the corresponding author with an appropriate decision."

Since review is single-blind, the manuscript carries author names, affiliations and emails as in the template — do not anonymise.

### 5.2 Review speed (https://www.dmlett.com/review-speed/)
> "Efforts are made to make the first decision on every submitted manuscript within 3 months of its submission."

(Co-publisher's wording, https://shahindp.com/review-speed/: "Possible efforts will be made to provide the first decision on every article within twelve weeks of its submission date. However, the time duration of the first decision may be longer depending on several factors, including the depth of the article’s contents, the availability of reviewers, etc.")

### 5.3 Open access, licence, copyright (https://www.dmlett.com/open-access-and-copyright/)
> "Discrete Mathematics Letters provides immediate open access to all the content. Articles are released under the Creative Commons Attribution 4.0 International (CC BY 4.0) license, which permits unrestricted use, distribution, and reproduction in any medium, provided that appropriate credit to the original author(s) and the source is given. Authors retain the copyright of their articles."

No copyright-transfer or licence-to-publish form is mentioned anywhere.
Preprint posting (arXiv/Zenodo) is not addressed on any page — **UNVERIFIED**
as a journal rule; the DOAJ record declares `deposit_policy: {'has_policy':
False}` (§5.8), i.e. no self-archiving policy exists either way. Published
papers routinely cite arXiv versions of other work, and CC BY plus
author-retained copyright is compatible with prior preprints. H5's "has not been
published elsewhere" is the only text that could be read against it.

### 5.4 Fees (https://www.dmlett.com/)
> "This journal does not charge Article Submission/Publication/Processing Charges."

### 5.5 Publication ethics (https://www.dmlett.com/publication-ethics/) — full author section

Heading: "Publication Ethics and Publication Malpractice Statement". The journal
"follows the" AMS *Policy Statement on Ethical Guidelines*, IMU *Best Current
Practices for Journals*, EMS *Code of Practice* and its *Comments*, and COPE's
Guidelines; "It is expected that the authors, reviewers, and editors of DML
follow the best-practice guidelines on ethical behavior contained in the
above-mentioned documents." The author rules, verbatim:

> "1.1. Authorship should be limited to those who have made a significant contribution to the concept, design, execution, or interpretation of the research study. All those who have made significant contributions should be offered the opportunity to be listed as authors. Other individuals who have contributed to the study should be acknowledged, but not identified as authors.
> 1.2. The corresponding author should ensure that all appropriate co-authors (and no inappropriate co-authors) are included in the authors’ list of the manuscript and that all co-authors have seen and approved the final version of the manuscript and have agreed to its submission for publication.
> 1.3. [quoted in H5]
> 1.4. Authors of the manuscripts submitted to DML are required to ensure that they have written entirely original works, and if the authors have used the works of others that this has been properly cited or quoted. Authors must cite publications that have influenced the nature of the work reported.
> 1.5. Fraudulent or knowingly inaccurate statements are considered unethical and are unacceptable. The authors should not submit a manuscript to DML if it is plagiarized or fraudulent/fabricated. When an author discovers a significant error or inaccuracy in his/her own published paper, it is the author’s duty to promptly notify the journal’s editor/publisher and cooperate with the editor to retract or correct the paper.
> 1.6. Every author is required to disclose in the submitted manuscript any financial or any other substantive conflict of interest that might be construed to influence the results or interpretation of the manuscript. All sources of financial support for the project should also be disclosed in the submitted manuscript.
> 1.7. The authors should cite only the relevant publications, and they should refrain from self-citation as much as possible."

Editors' side relevant to authors: "2.3. Editorial office of DML is expected to release errata, clarifications or apology statements and expected to not refrain from retracting a publication if there is a clear evidence of scientific misconduct, unethical research, plagiarism or other violations of ethical scientific publishing." and "2.4. Editors of DML are expected to refrain from suggesting that authors include citations to their (or their associates’) work merely to increase citation counts…"

- **Plagiarism screening tool:** none named on the site, and the journal's DOAJ record declares `plagiarism: {'detection': False}` (§5.8). So no automated similarity check is declared; the plagiarism rule (1.4, 1.5) is enforced by editors/referees.
- **Author changes after submission:** **not stated on any page.** The only relevant text is 1.2 (corresponding author ensures the author list is right and all co-authors approved). **UNVERIFIED.**
- **Conflict-of-interest / funding statement:** required "in the submitted manuscript" (1.6). Published papers put funding in the Acknowledgment section and carry no separate "Conflict of interest"/"Declarations" section (§6.7).

### 5.6 Privacy (https://www.dmlett.com/privacy/)
> "Authors’ information (that is, names, email addresses, etc.) submitted to Discrete Mathematics Letters will be used only for the stated purposes and will not be made available to a third party."

### 5.7 Generative AI / LLM / machine-assisted writing — **no statement exists**

Search performed (case-insensitive) for `artificial intelligence`, `generative`,
`ChatGPT`, `LLM`, `language model`, `machine-assisted`, `AI tool`, and the
standalone token `AI` over the **raw HTML** of every page fetched:

- dmlett.com: home, manuscript-preparation-and-its-submission, journal-information, editorial-team, abstracting-and-indexing, publication-frequency, editorial-process, review-speed, policies, privacy, open-access-and-copyright, publication-ethics, contact, announcement, journal-archive, journal-archive/v16, /v17, /v18 — **0 matches**.
- The template `DML-Template.tex` — **0 matches**.
- shahindp.com (co-publisher): home, manuscript-preparation, editorial-process, review-speed, journals — **0 matches**.
- Web search (`"Discrete Mathematics Letters" dmlett generative AI OR ChatGPT OR "large language model" policy`) — no DML-specific result.

The ethics page delegates to the AMS, IMU, EMS and COPE documents by link; those
external documents were **not** fetched for this report, so whether any of them
now carries AI guidance that DML inherits by reference is **UNVERIFIED**. The
journal's own text is silent. Consequence for a package: nothing on DML's site
requires an AI-use disclosure, and nothing forbids one; the binding rules are
1.1 (authorship = significant human contribution), 1.4 (original work, proper
citation) and 1.5 (no fabrication), which apply regardless of tooling.

### 5.8 Third-party record (DOAJ)

The DOAJ web page (https://doaj.org/toc/2664-2557) returns 403 to both
WebFetch and curl, but the DOAJ API
(https://doaj.org/api/search/journals/issn%3A2664-2557, HTTP 200, record
`last_updated: 2026-09-01T18:19:02Z`) returns the journal's self-declared record.
Fields, verbatim from the JSON:

- `publisher: {'country': 'PK', 'name': 'Shahin Digital Publisher'}`; `eissn: 2664-2557`; `oa_start: 2019`; `boai: True`
- `license: [{'type': 'CC BY', 'BY': True, 'NC': False, 'ND': False, 'SA': False, 'url': 'https://creativecommons.org/licenses/by/4.0/'}]`
- `copyright: {'author_retains': True, 'url': 'http://www.dmlett.com/open-access-and-copyright/'}`
- `apc: {'has_apc': False, 'url': 'http://www.dmlett.com/'}`; `other_charges: {'has_other_charges': False}`
- **`plagiarism: {'detection': False, 'url': ''}`** — the journal declares to DOAJ that it runs **no** plagiarism-detection screening.
- `editorial: {'review_process': ['Anonymous peer review'], 'review_url': 'http://www.dmlett.com/editorial-process/', 'board_url': 'http://www.dmlett.com/editorial-team/'}` (DOAJ's label; the journal's own page says single-blind)
- **`publication_time_weeks: 12`** — declared average submission-to-publication; compare the observed median of 113 days ≈ 16 weeks in §7.
- `deposit_policy: {'has_policy': False}`; `preservation: {'has_preservation': False}`; `pid_scheme: {'has_pid_scheme': False}` — no declared self-archiving policy, no declared digital-preservation arrangement, no declared persistent-identifier scheme (even though every article carries a 10.47443 DOI).
- `keywords: ['discrete mathematics', 'combinatorics', 'combinatorial matrix theory', 'combinatorial number theory', 'theoretical computer science', 'discrete and computational geometry']`; `subject: ['Mathematics']`
- `ref.author_instructions: 'http://www.dmlett.com/manuscript-preparation-and-its-submission/'` — DOAJ points to the same single page used throughout this document.

This is what the journal told DOAJ, not a rule on dmlett.com; it is included
because it settles two questions the site leaves open (plagiarism screening:
none declared; preprint/self-archiving policy: none declared).

### 5.9 Indexing and frequency (for the record)

https://www.dmlett.com/abstracting-and-indexing/: "This journal is Abstracted/Indexed/included in the: Directory of Open Access Journals (DOAJ), Emerging Sources Citation Index (ESCI), Mathematical Reviews (MathSciNet), Scopus, Zentralblatt MATH (zbMATH)."

https://www.dmlett.com/publication-frequency/: "Discrete Mathematics Letters (DML) publishes two volumes every year. … Beginning with Volume 5 (2021), DML will be published in cooperation with Shahin Digital Publisher." Volume 18 (2026) is "In Progress" as of 2026-09-02 with 12 items published online.

---

## 6. Observed conventions from published papers (P1–P9)

Everything in this section is "published papers do X", not a stated rule.

1. **Length.** Research articles: 4, 5, 5, 6, 6, 6, 8 pages (P2, P1, P7, P4, P6, P9, P3). In the v17/v18 listings every research article is ≤ 8 pages and two (v17 pp. 7–14, pp. 93–100) are exactly 8. The one Review Article (P8) is 12 pages. The corrigendum (P5) is 2 pages.
2. **Abstract length and content.** 87–239 words (P1 87, P4 93, P3 97, P6 106, P7 122, P2 154, P9 239). Despite the "desired… avoid" guidance, abstracts **do** contain mathematics: P2 has a displayed formula (`F(c) = inf …`), P1 has binomial coefficients and set notation, P9 has `Q_n`, `n^2`, `dom(Q_n)`. Abstracts also **do** contain references, written inline rather than by number: P2 "In [J. Combin. Theory Ser. A 116(2) (2009) 290–302], Cibulka proved…"; P9 "Hedetniemi et al. [Congr. Numer. 235 (2024) 5–21]". So the convention for a citation in the abstract is a bracketed journal-style reference, not `\cite`.
3. **Keywords / MSC counts.** Keywords: 3, 3, 4, 4, 4, 4, 7. MSC codes: 2, 2, 2, 2, 2, 3, 3. Keywords are lower-case, semicolon-separated, terminated with a period ("Keywords: permutations; generating functions; reservoirs; key comparisons in quicksort."). MSC line: "2020 Mathematics Subject Classification: 05A05, 05D05."
4. **Date line** — printed exactly in the template's format, in parentheses, "Day Month Year":
   `(Received: 28 May 2026. Received in revised form: 16 July 2026. Accepted: 5 August 2026. Published online: 25 August 2026.)`
   All nine papers carry a "Received in revised form" date — every one was revised at least once.
5. **Title case.** All 2026 papers (P1–P8) are printed in Title Case ("Graphs with Small Triameters"). P9 (2025) is printed in sentence case ("Improved bounds on the domatic numbers of queens graphs") although the v16 web listing shows it in Title Case — production appears to have moved to Title Case in 2026. Use Title Case.
6. **Section / theorem / figure numbering.** "1. Introduction", "2. Main Definitions", "3. Main Results" (P3); "2. Formula Relating R(n) to R(n − 1)" (P4). Theorems "Theorem 3.1.", figures "Figure 3.1:", "Figure 1.1:" — section-numbered as the template dictates; the corrigendum (no numbered sections) uses "Table 1:" / "Figure 1:". Captions have a bold label and a colon.
7. **Acknowledgment wording and placement.** Always an unnumbered heading immediately after the last section and before "References". The heading spelling is **not normalised** by production — all four of "Acknowledgment" (P2, P3, P8), "Acknowledgments" (P1), "Acknowledgement" (P7), "Acknowledgements" (P6) appear. Contents seen: grant/funding ("The author is partially funded by research funds from York University, and NSERC Discovery Grant #RGPIN-2025-06304." — P2; "The work of Yakov Shubin (Theorem 1.1) was supported by the Russian Science Foundation (project No. 24-71-10021), and the work of Danila Cherkashin (Theorems 1.2 and 1.3) was supported by the Bulgarian NSF (grant No. KP-06-N72/6-2023)." — P1); thanks to referees ("The authors are grateful to the anonymous referees, whose valuable comments and suggestions improved the final manuscript." — P6); thanks to colleagues (P3). **Three papers have no acknowledgment at all** (P4, P5, P9) — the section is optional in practice as well as in the rules. No paper has a separate "Funding", "Conflict of interest", "Data availability", "Declarations" or "Author contributions" section.
8. **ORCID.** Not printed in any of the nine PDFs (grep for `orcid` → 0 hits). The Editorial Team page links a few editors' ORCID profiles, but authors' ORCIDs are not part of the article format.
9. **Authors without an institution (directly relevant).** P9 (research article, 6 pp.) and P5 (corrigendum) — author "Juho Lauri∗", affiliation slot reads exactly **"Helsinki, Finland"** (city, country; no institution, no "Independent researcher" label), footnote "∗ E-mail address: juho.lauri@gmail.com" (a personal gmail address). The paper went through normal review (received 18 Aug 2025 → accepted 1 Dec 2025). So the accepted convention for an unaffiliated author is: put *City, Country* in the `\footnotesize $^1${\it …}` affiliation line and give a reachable email in the footnote.
10. **Corresponding-author footnote wording.** Multi-author papers: "∗ Corresponding author (shubin.yakoff@gmail.com)." (P1, P4, P6). Single-author papers: "∗ E-mail address: omarmo@yorku.ca" (P2, P3, P7, P9, P5 with †). Both are the template's `\footnote{Corresponding author (…)}` slot, edited.
11. **Affiliation detail.** Ranges from full postal address ("Graph Theory and Network Analysis Laboratory, Kyiv School of Economics, Mykoly Shpaka str. 3, 03113 Kyiv, Ukraine" — P3) to department + institution + city + country (most) to city + country only (P9). Multiple authors sharing one affiliation drop the superscripts (P4).
12. **Reference lists.** Numeric `[n]`, alphabetical by first author's last name in every paper (checked all nine); en-dash page ranges; MathSciNet abbreviations (e.g. "European J. Combin.", "J. Combin. Theory Ser. A", "Discuss. Math. Graph Theory", "Czechoslovak Math. J."); no DOIs; 4 to 19 references in research articles (P2: 4; P1: 19); the review has 76+.
13. **Typesetting in print vs template.** Published PDFs are A4 (595.276 × 841.89 pt) as the template dictates, produced by "LaTeX with hyperref / pdfTeX-1.40.29", but the body text font is **TeX Gyre Schola** (regular/bold/italic) with Computer Modern only for math — the template loads no font package, so a template-compiled PDF renders in Computer Modern. Production therefore re-typesets; author-side page count is an approximation of the published page count. Keep a margin below 8 pages.
14. **Citing DML itself.** "Discrete Math. Lett. 14 (2024) 85–88" — the home-page abbreviation "Discrete Math. Lett." is used.
15. **Computational papers.** P9 (SAT-solver results) prints certificates as figures/tables within the paper; a grep of its full text for `github`, `available`, `repository`, `zenodo`, `source code`, `supplement` returned **zero** hits — no code-repository link and no data-availability statement. **UNVERIFIED** whether the journal would accept or expects a supplementary-material link; none of the nine papers has one, and no page mentions supplementary material.

---

## 7. Review timeline evidence (n = 9; small sample, all from Vol. 16–18)

Dates verbatim from each PDF's first page; days computed calendar-exactly.

| Paper | Received | Received in revised form | Accepted | Published online | Rcv→Rev | Rcv→Acc | Acc→Pub | Rcv→Pub |
|---|---|---|---|---|---|---|---|---|
| P1 v18 16–20 | 28 May 2026 | 16 July 2026 | 5 August 2026 | 25 August 2026 | 49 | 69 | 20 | 89 |
| P2 v18 51–54 | 31 March 2026 | 11 July 2026 | 10 August 2026 | 26 August 2026 | 102 | 132 | 16 | 148 |
| P3 v18 55–62 | 7 May 2026 | 15 August 2026 | 18 August 2026 | 29 August 2026 | 100 | 103 | 11 | 114 |
| P4 v18 28–33 | 28 April 2026 | 21 July 2026 | 6 August 2026 | 25 August 2026 | 84 | 100 | 19 | 119 |
| P5 v18 34–35 (corrigendum) | 23 June 2026 | 31 July 2026 | 4 August 2026 | 26 August 2026 | 38 | 42 | 22 | 64 |
| P6 v17 1–6 | 11 December 2025 | 7 January 2026 | 9 January 2026 | 10 January 2026 | 27 | 29 | 1 | 30 |
| P7 v17 70–74 | 15 December 2025 | 18 April 2026 | 21 April 2026 | 22 May 2026 | 124 | 127 | 31 | 158 |
| P8 v17 101–112 (review) | 1 March 2026 | 6 May 2026 | 21 May 2026 | 11 June 2026 | 66 | 81 | 21 | 102 |
| P9 v16 94–99 | 18 August 2025 | 24 November 2025 | 1 December 2025 | 9 December 2025 | 98 | 105 | 8 | 113 |

Summary (days):

| Interval | Median | Min | Max | Mean |
|---|---|---|---|---|
| Received → revised form (≈ first decision + revision) | **84** | 27 | 124 | 76.4 |
| Received → accepted | **100** | 29 | 132 | 87.6 |
| Accepted → published online | **19** | 1 | 31 | 16.6 |
| Received → published online | **113** | 30 | 158 | 104.1 |

Research articles only (P1–P4, P6, P7, P9; n = 7): median received→accepted
**103** days, received→published **114** days. Journal's stated target: first
decision "within 3 months" — consistent with the received→revised median of
84 days. Small sample; all nine went through one revision round; none were
accepted as submitted.

---

## 8. Package checklist — tick every line

**A. Gate conditions (fail = not processed / rejected)**
1. Manuscript is in English, spell-checked, grammatically clean (H1).
2. Built from `DML-Template.tex` (https://www.dmlett.com/archive/DML-Template.zip, 4 Jan 2026 version) with the preamble unchanged: `article` 10pt A4, `geometry margin=1.1cm`, the template's package list, `titlesec` section format, `caption[labelfont=bf]`, `\counterwithin` for figures/tables, the ten `\newtheorem` declarations, `\fnsymbol` footnotes, `\allowdisplaybreaks[4]`, the bibliography `itemsep` patch, `\baselineskip=0.20in` (H2, §2.2).
3. Template header block retained verbatim ("Discrete Mathematics Letters / www.dmlett.com" and "Discrete Math. Lett. X (202X) XX--XX" with placeholders), `\setcounter{page}{1} \thispagestyle{empty}` retained.
4. Compiled PDF is ≤ 8 pages for an original-results paper (≤ 30 for a mini-review), with visible margin because production re-typesets in a different font (H4, §6.13).
5. Work is not published, not under review elsewhere, and will not be published elsewhere if accepted; no simultaneous submission (H5, ethics 1.3).
6. Topic is discrete mathematics; ideally near an editorial-board member's stated research areas (https://www.dmlett.com/editorial-team/), and framed as "non-trivial progress in the solution of existing problems and conjectures" or "an alternative/short proof of some well-known result" where true (H6).
7. Content is entirely original; every influencing publication is cited; nothing fabricated (ethics 1.4, 1.5).
8. Any conflict of interest and every source of financial support is disclosed **in the manuscript** (ethics 1.6) — in practice in the Acknowledgment section; if there is no funding and no conflict, nothing is required to be printed (no published paper carries a "none" statement).

**B. Front matter**
9. Title: precise, covers the theme; no formulas or abbreviations unless unavoidable; Title Case (§2.1, §6.5).
10. Author names: full names ("at least two full names" if the author has more than two); `\large\bf` title line and author line exactly as in the template.
11. Corresponding-author footnote present on the author name: `\footnote{Corresponding author (email)}` for multi-author, or the observed `E-mail address: …` form for single-author (§6.10).
12. Affiliation line(s) in `\footnotesize` italics with superscript numbers; no abbreviations. **Unaffiliated author:** write `City, Country` only (precedent: "Helsinki, Finland", P9/P5, §6.9) and give a reachable email in the footnote.
13. Date line left as the template's placeholders ("Received: Day Month 202X. …") — production fills it.
14. Abstract inside `\begin{abstract}…\end{abstract}` with `\noindent`; states the main findings briefly; formulas and references avoided where possible — if a reference is unavoidable, use the inline bracketed journal form, not `\cite` (§6.2).
15. `{\bf Keywords:}` line inside the abstract block: ≥ 3 keywords, semicolon-separated, ending with a period (H8, §6.3).
16. `{\bf 2020 Mathematics Subject Classification:}` line: ≥ 1 code from **MSC 2020**, comma-separated, ending with a period (H8).

**C. Body**
17. Sections via `\section{…}`, starting with `\section{Introduction}`; subsections via `\subsection` only if needed; no manual numbering.
18. Every theorem, lemma, proposition, corollary, definition, remark, example, conjecture, observation is in the corresponding template environment (section-numbered); proofs in `\begin{proof}…\end{proof}` (§2.1 "LaTeX Environments").
19. If an environment the template lacks is needed (e.g. `question`, `problem`, `notation`, `claim`), it is added with the same `\newtheorem{x}{X}[section]` pattern, not by hand-formatting.
20. **No `eqnarray` / `eqnarray*` anywhere** — multi-line displays use `align`, `align*`, `aligned`, `multline`, `gather`, etc. (template prohibition, §2.2).
21. Figures/tables use `\caption` (bold label is automatic) and are referenced in the text; numbering is left to the section-based counters ("Figure 2.1", "Table 1.1").
22. Footnotes are rare and use the template's symbol marks (∗, †, …); the corresponding-author footnote takes ∗.
23. Acknowledgment (if any) is `\section*{Acknowledgment}` placed after the last section and before the bibliography; contains funding statements and thanks; nothing else goes after it except references (§2.1, §6.7).

**D. References**
24. Every reference is cited with `\cite{…}`; **no uncited `\bibitem`** (§3.1).
25. `\bibitem`s are in alphabetical order by the **last name of the first author**; `\begin{thebibliography}{00}` preceded by `\footnotesize` as in the template.
26. Each journal entry follows `Initials Surname, Initials Surname, Title in sentence case, {\it MathSciNet Abbrev.} {\bf Vol} (Year) first--last.` (§3.2); journal abbreviations checked against https://mathscinet.ams.org/msnhtml/serials.pdf.
27. Books: `{\it Title}, Publisher, City, Year.`; chapters: `…, In: Editors (Eds.), {\it Book Title}, Publisher, City, Year, first--last.`; theses: `{\it Title}, Master's thesis / Ph.D. dissertation, University, [Place,] Year.` (§3.2, §3.3).
28. arXiv items: `Authors, Title, arXiv:NNNN.NNNNN [math.XX], (Year).` — append `; Journal Abbrev., To appear.` if accepted (§3.3).
29. Web resources/databases: `Name, URL.` (OEIS precedent, §3.3). No DOIs/URLs on ordinary journal entries (none in print).
30. Retracted papers, if cited, carry the rationale in the text and "retracted" status in the entry; papers with known corrections are cited together with the correction (§3.1).
31. Self-citations kept to the minimum the argument needs (ethics 1.7).
32. Reference to any DML paper uses "Discrete Math. Lett." (§6.14).

**E. Email package**
33. Send to **m.secretary@dmlett.com** (§4); optionally cc nothing — no second address is requested.
34. Attach the **compiled PDF** (the only requested file). Do not attach `.tex` unless asked later (**UNVERIFIED** whether it is requested post-acceptance).
35. Email body: no cover letter is required or mentioned (**UNVERIFIED**, §4); if writing one, keep it to title, author(s), corresponding author's email, a one-sentence statement that the work is original and not under consideration elsewhere (mirrors H5), and — optionally — suggested referees with affiliations and emails (explicitly permitted, non-binding, §4).
36. Do **not** include: copyright-transfer forms, ORCID, fee/payment information, a data-availability or AI-use statement (none requested by any page; §5.7, §6.8) — unless a later request from the office asks for them.

**F. Post-submission expectations (for planning, not for the package)**
37. Expect initial editorial screening, then ≥ 2 referees, single-blind (§5.1).
38. Expect a first decision within ~3 months (stated) and, on the observed sample, received→revised ≈ 84 days median, received→accepted ≈ 100 days, accepted→online ≈ 19 days (§7). Every observed paper was revised once.
39. On acceptance: CC BY 4.0, authors retain copyright, no fee (§5.3, §5.4); the article receives a DOI `10.47443/dml.YYYY.NNN` and production-added labels (§2.3).
40. If an error is later found in the published paper, notify the editor promptly; corrigenda are published as separate 2-page items with their own DOI (ethics 1.5, P5).
