# Package review — Fable 5.1 leg, round 3 (final gate before emailing DML)

Date: 2026-09-03. Reviewed from scratch: `review_brief_pkg.md` (incl. ROUND 3), `DML_RULES.md`,
`dml_submission.tex` (+ diff against `dml_submission.prev.tex`), `SUBMISSION_EMAIL.md`,
`POLICY_QUERY_EMAIL.md`, `CHECKLIST.md`, `prof_pkg.md`, `review_fable_pkg.md`, `kp.txt`/`kp.pdf`
(table re-rendered and read as an image), `pages/contact.txt`, `pages/editorial-team.txt`, the
template in `template/unz/DML-Template/`. Compiled with `tectonic -X compile dml_submission.tex
--outdir /tmp/r3check`; the shipped PDF was not touched. No file in the package directory was
edited; this review is the only file written.

## Verdict: **APPROVE**

Every item the round-2 REVISE demanded is applied correctly, the new Proposition 6.1 range is
exactly right, nothing downstream depended on the old range, every displayed number reproduces
under exact rational arithmetic (recomputed fresh, not from the package scripts), the rendered
page 4 ends at the References, the abstract and Introduction now claim precisely what Section 6
proves, and both emails are consistent with the manuscript and with the journal's Contact page.

One precondition, stated first because it is the only thing in the package I could not close:
**item A1 below** — an attribution to reference [3] that no round has checked against [3]
itself. If the author has [3] open and Table 1 there gives K(6,1,2) = 20, send as is. If the
author has not seen [3], apply the two-line reword in A1 before sending; do not send a claim about
a paper's contents that nobody has read while the Acknowledgment says the references were checked.

Everything else is optional. `CHECKLIST.md` is stale in eleven places (§5) but is not part of what
is sent.

---

## 1. The six things the brief asked me to check hard

### 1.1 Proposition 6.1's new range `2 ≤ μ ≤ n` — correct and sufficient

- **Is `μ ≤ n` right, or should it be `μ ≤ n+1` with an evenness caveat?** `μ ≤ n` is exactly
  right and is the cleaner statement. For even n, n+1 is odd, so {even μ : μ ≤ n+1} = {even μ :
  μ ≤ n}. The parenthetical in the statement ("no μ-fold covering exists for μ > n+1, so μ = n is
  the largest feasible even multiplicity") is a correct one-step inference from "n even". μ = n
  is genuinely feasible: C = F₂ⁿ has c(y) = n+1 ≥ n everywhere. So the range is precisely the set
  of even μ for which K(n,1,μ) is defined — no caveat needed.
- **KP's own range agrees.** KP Theorem 6 is derived (kp.txt line 482, page 8 of kp.pdf) from
  Theorem 4 on λ-fold 1-packings via μ = |B₁| − λ = n+1−λ with λ ≥ 1, i.e. μ ≤ n. I re-derived
  case (a): n(n+4) − (λn+3λ−4+σ) with λ = n+1−μ gives μn+3μ+(1−σ), and for even n, τ = 1−σ ≡ μ
  (mod 2). So the transcription in Section 4 is consistent with KP's derivation and the comparison
  in Section 6 runs over exactly the μ for which both expressions are bounds.
- **Nothing downstream depended on the old range.** The two P−KP identities are algebraic
  identities in (n, μ): I expanded them by hand ((μ+1)n(n+4) − (n+3)D = n−3μ and
  (μ+1)n(n+2) − (n+1)D = n−μ with D = (μ+1)(n+1)−1) and confirmed them exactly for all even
  n ≤ 80 and all even μ ≤ 2n (so also beyond the new range). The crossover rule (P > KP ⟺ μ < n/3
  for n ≡ 0, μ < n for n ≡ 2 mod 4) was checked by brute force against the sign of P−KP over every
  even μ in [2, n] for even n ≤ 78: zero mismatches. At the new boundary μ = n the rule behaves:
  P = KP exactly for n ≡ 2 (mod 4) (P−KP = 0 at n = 2, 6, 10, 14) and P < KP for n ≡ 0 (mod 4).
  All four μ = 4 examples (n = 6, 8, 10, 16) satisfy μ ≤ n. P(n,2) = L(n) for all even n ≤ 58.
- **Sanity against exact values** (exhaustive search over all subsets of F₂ⁿ): K(2,1,2) = 3 =
  ⌈P(2,2)⌉; K(4,1,2) = 8 ≥ 7 = ⌈P(4,2)⌉; K(4,1,4) = 14 = ⌈P(4,4)⌉. At μ = n the bound also matches
  the complement/sphere-packing value 2ⁿ − A(n,3) at n = 4 (14) and n = 6 (56). No contradiction
  anywhere.
- **The proof itself**: g_μ ≥ 0 gives s_μ ≤ E_μ; the codeword ball sum (n+1)+2N₂(x) is odd while
  μ(n+1) is even, so the sum is ≥ μ(n+1)+1; the incidence count gives |C| ≤ E_μ + μ s_μ ≤ (μ+1)E_μ;
  rearranging (μ+1)((n+1)|C| − μ2ⁿ) ≥ |C| gives the stated bound. Correct.
- The reworded opening sentence of Section 6 ("parity alone forces it to exceed the baseline
  μ(n+1) exactly when μ(n+1) is even") is now unambiguous.

### 1.2 Rendered page 4 ends at the bibliography — confirmed

`tectonic` into `/tmp/r3check`: **4 pages, A4 (595.28 × 841.89 pt)**, 0 errors; the only
warnings are the template's own header/title skeleton (lines 39–64), identical to the untouched
template. Page 4 rendered to PNG and read: Proposition 6.1 → Section 7 → Chen–Li paragraph as body
prose → Acknowledgment → References [1]–[5] → page number "4". **Nothing prints below the
References.** The Chen–Li text now sits as the last paragraph of Section 7, before the
Acknowledgment. `pdftotext` of my build is byte-identical to `pdftotext` of the shipped
`dml_submission.pdf`, so the shipped PDF is the shipped source. Page 4 is about 85 % full (the
checklist's "70 %" is stale but immaterial). One footnote remains (∗ e-mail); my earlier grep count
of 5 was `\footnotesize` ×4 + `\footnote` ×1.

### 1.3 Every displayed number, recomputed from scratch (exact `fractions`)

| Claim | Value | OK |
|---|---|---|
| Thm 1.1 at n = 6: ⌈384/20⌉ | 96/5 → 20 | ✓ |
| Thm 1.1 at n = 8: ⌈1536/26⌉ | 768/13 → 60 | ✓ |
| Remark 3.1: ⌈48/11⌉ | 5; K(3,1,2) = 4 (OEIS a(3)) | ✓ |
| Table 4.1 ⌈L⌉ | 20, 60, 192, 647, 2235, 7865 | ✓ |
| Table 4.1 ⌈KP⌉ / printed | 19, 59, 188, 640, 2195, 7783 — the five printed values equal ⌈formula⌉ | ✓ |
| Table 4.1 gains | 0, +1, +4, +7, +40, +82 | ✓ |
| L−KP identities | exact for all even n in [4, 38]; sign by 2n−12 / 2n−4 | ✓ |
| Gaps at n = 6, 8, 10 | 8/15, 16/39, 64/15 | ✓ |
| n = 4 | L = 48/7, KP = 7; both ceilings 7 | ✓ |
| Residue-class comparison | (2n−4)(n+4) − (2n−12)(n+2) = 12n+8 > 0 | ✓ |
| 2n−12 ≥ n/2 | iff n ≥ 8 | ✓ |
| n(n+4)(3n+2) ≤ 8n³ ⟺ 5n²−14n−8 ≥ 0 | 8n³ − n(n+4)(3n+2) = n(5n²−14n−8); −5 at n = 3, 16 at n = 4 | ✓ |
| 2¹¹ = 2048 > 1936 = 16·11² | ✓; 2n²/(n+1)² > 1 iff n ≥ 3 | ✓ |
| ⌈L⌉ > ⌈KP⌉ over even n ∈ [6, 200] | all **98** values | ✓ |
| Additive gap ~ (2/3)·2ⁿ/n² | n²(L−KP)/2ⁿ = 0.632 (n = 200), 0.660 (n = 1000) | ✓ |
| μ = 4, n = 10 | P = 10240/27 → **380**; KP = 5632/15 → **376** | ✓ |
| μ = 4, n = 16 | P = 327680/21 → **15604**; KP = 77824/5 → **15565** | ✓ |
| μ = 4, n = 8 | P = 1280/11 → **117**; KP = 352/3 → **118** (loses) | ✓ |
| μ = 4, n = 6 | P−KP = **16/51**; both ceilings **38** | ✓ |
| Both P−KP identities | exact, all even n ≤ 80, all even μ ≤ 2n | ✓ |
| Equation (1) | E = (n+1)|C| − 2ⁿ⁺¹ | ✓ |
| 20-word code in §5 | 20 distinct words, min coverage 2, E = 12 = 7·20−128; Step-1 parity (odd, ≥ 15) holds at all 20 codewords | ✓ |
| OEIS A004045 (fetched today, #32, 2 May 2026) | terms 2,3,4,8,12,20,32 (n = 1..7); the n = 6 code is printed there verbatim | ✓ |
| KP table (page 8, rendered) | 59−64 at n = 8 with 59 bold; **188 at n = 10 is non-bold and carries mark [48] = Seuranen** — so Table 4.1's "188 \cite{Seuranen-2007,KP-2021}" is the right attribution, and "each printed lower bound there equals the value of their formula" is true (188 = ⌈2816/15⌉) | ✓ |
| KP Theorem 6 transcription | identical to kp.txt lines 483–495, cases (a) and (c) | ✓ |

Correction to my own round-2 review: I wrote there that all five KP μ = 2 values are bold. The
n = 10 entry is not; it is Seuranen's. The manuscript already cites it correctly.

### 1.4 Abstract and Introduction no longer overclaim — confirmed

- Abstract: "The argument extends to every feasible even multiplicity; for the underlying
  real-valued bounds we determine exactly when the resulting expression exceeds the
  Krotov–Potapov expression, noting that a strict gain need not survive the ceiling." This is
  exactly the content of the two displayed equivalences in Section 6 plus its final sentence.
- Introduction, last paragraph: "carries the argument to every feasible even multiplicity and
  classifies when the underlying real-valued bound exceeds the Krotov–Potapov bound." Same.
- The abstract's other claims re-checked against the body: "for every even length" (Thm 1.1,
  n ≥ 2 even); "exceeds ... for every even length from six onwards" after ceilings (Thm 4.1);
  "five lengths eight … sixteen" (Table 4.1); "at length six … recovers the exact value" (§5).
  The abstract is 174 words, zero math mode, zero references; 7 keywords; 3 MSC codes.

### 1.5 The two emails

- **Submission email.** To `m.secretary@dmlett.com` (H3; Contact page under Akbar Ali), no cc,
  PDF only. Subject and body carry the new title verbatim. "Dear Managerial Secretary" is a real
  role (Editorial Team page: "Managerial Secretary — Saima Saleem"); addressing the role is the
  right call given the two pages disagree on the person. "even lengths 8, 10, 12, 14 and 16" and
  "the lower-bound half of the known value at length 6" match the manuscript. H5 wording mirrored.
  Signature block (Fremont, California, United States; gmail) matches the manuscript's affiliation
  line and footnote. The optional post-reply sentence states the answer, not just the enquiry.
  Nothing invites a bad decision; the tooling is no longer the last thing the editor reads.
- **Policy query.** To `ch.editor@dmlett.com` (Contact page under Akhlaq Ahmad Bhatti), cc the
  secretary, no attachment. "Dear Editors" is right (two Chief Editors: Bhatti, Brualdi). The tool
  list and the verification sentence match the Acknowledgment word for word in substance. The two
  harmful sentences the professor flagged are gone. The two-week cap is stated and is consistent
  with the submission email's header. One optional nit: "acceptable under the journal's policy"
  presupposes a policy DML does not have; "acceptable to the journal" avoids a "we have no policy"
  non-answer (B2 below).
- **Cross-consistency**: title, affiliation, e-mail, tool names, verification wording and the
  "four-page" claim agree across manuscript and both emails.

### 1.6 CHECKLIST.md — stale items (see §5 for the full list)

Eleven entries describe the pre-round-3 package: the old title (item 9), "Fremont, CA, USA"
(caveat 3, item 12), the abstract's bracketed reference (caveat 2, items 7 and 14), six keywords
(item 15), two footnotes (item 22), the AI sentence in the submission email (caveat 4, items 35
and 36), the referee note in the email (item 35), and item 7's "no theorem … changed" (Proposition
6.1's statement did change). Item 23, which the professor correctly marked FAIL in the rendered
output, is now a genuine PASS. Not treated as evidence for anything above.

---

## 2. Findings, ranked

### A. Confirm before sending (no edit if it checks out)

**A1. K(6,1,2) = 20 attributed to Seuranen 2007 — Table 4.1 "20 (exact value, [3])" and §5 "The
value was previously established computationally [3]".** No round has opened [3]; round 2 (mine)
flagged this as B4 and it is not among the items the brief says were resolved against a source.
What I found today:
- OEIS A004045's edit history: from Jan 2015 until 2 Mar 2020 the entry carried the comment
  "Next 2 terms are 19 or 20, 32" (sourced from the 1995 *Amer. Math. Monthly* "Football pools"
  paper); a(6) = 20 and a(7) = 32 were added by Paul Tabatabai on 2 Mar 2020 ("EXTENSIONS
  a(6)-a(7) from Paul Tabatabai"). So in 1995 the value was open (19–20), which rules out HHKL 1993
  as its source, and OEIS never learned of a 2007 closure.
- Seuranen 2007 is a 4-page "New lower bounds for multiple coverings" whose reference list (zbMATH)
  has GLPK and nauty, and KP call its Table 1 "the table … of small values for K(n,1,μ)". A
  computational closure of the smallest open case in that paper is entirely plausible and fits the
  timeline. I could not read the paper or its Table 1 (Springer paywalled; Aalto repository, S2,
  zbMATH, OpenAlex all withhold the text or the abstract).
- The mathematical claim is safe regardless: Theorem 1.1 gives ≥ 20 and the printed code gives
  ≤ 20, so the manuscript itself establishes K(6,1,2) = 20. Only the *attribution* is at risk.

Action: if Seuranen's Table 1 shows 20 (not 19–20) at (n, μ) = (6, 2), send as is. If the author
has not seen it, reword to remove the attribution at zero mathematical cost:
- Table 4.1, n = 6 row: `$20$ (exact value, \cite{OEIS-A004045})` → or simply `$20$ \cite{OEIS-A004045}`.
- §5: replace "The value was previously established computationally \cite{Seuranen-2007};
  Theorem \ref{thm-main} replaces the lower-bound half of that determination by a one-line
  argument, while the upper half still rests on the construction above." with "The value is
  recorded in \cite{OEIS-A004045}, where the lower bound rests on computation; Theorem
  \ref{thm-main} supplies a one-line proof of that half, while the upper half still rests on the
  construction above."
The submission email's "non-computational proof of the lower-bound half of the known value at
length 6" survives either way. A referee from the Östergård–Seuranen school would notice a wrong
attribution here on page 3, which is why this is the one item I will not wave through unread.

### B. Optional polish (none affects acceptance)

**B1. §7, "their bound then reduces to the sphere covering bound".** The brief confirms ε's
definition matches HHKL verbatim; the *form* of HHKL's Theorem 6 (that ε = 0 collapses it to
μ2ⁿ/(n+1)) is still only the author's reading. Same residual as round 2; keep if checked.

**B2. Policy query**: "acceptable under the journal's policy?" → "acceptable to the journal?"
(DML has no policy; avoid handing the editor a literal "we have none" reply).

**B3. §1, "μ-tuple dominating set … double dominating set"** is used without a citation. Standard
terms (Harary–Haynes, *Ars Combin.* 55 (2000) 201–213 — the author must verify before adding);
fine to leave uncited in a Letters paper.

**B4. §6 first sentence** reads "for even n … that is, for even n, exactly when μ is even" — "for
even n" twice. Correct; could drop the second.

**B5. Thm 4.1 proof** verifies 2ⁿ/(16n²) > 1 at n = 11 for a claim needed at even n ≥ 12. Valid via
monotonicity; a reader may pause. No change needed.

### C. Explicitly checked and not defects
- The Acknowledgment naming specific commercial models; no DML rule restricts it, and it matches
  the policy query.
- ORCID omitted; Lean 4 result omitted (per brief).
- Header block differs from the template only by a dropped `%\vfill` comment line; preamble
  differs only by blank lines (`diff -w`).
- Unreferenced `\label`s (sec-notation, sec-proof, rem-parity, rem-set, thm-dominance): harmless.

---

## 3. Rule conformance re-audit (independent of CHECKLIST.md)

H1 English, spell-checked: dictionary pass over the rendered text — every non-dictionary token is a
name, technical term or inflection; no typos found. H2/§2.2 template: class, geometry, package
list, `titlesec` format, `caption[labelfont=bf]`, both `\counterwithin`, ten `\newtheorem`s,
`\fnsymbol`, `\allowdisplaybreaks[4]`, bibliography `itemsep` patch, baselineskips, header
`\makebox`, placeholders, `\setcounter{page}{1} \thispagestyle{empty}` — all verbatim. H3
address ✓. H4: 4 of 8 pages ✓. H5 wording in email ✓ (author attestation). H6 scope ✓; the new
double-domination sentence and keyword give the graph-theory-weighted board a translation. H7/1.6:
funding and COI stated in the manuscript ✓. H8: 7 keywords, 3 MSC 2020 codes ✓. Title: Title Case,
no formula, no abbreviation ✓. Affiliation: no abbreviations now ✓. Abstract: no math, no
references ✓ (fully satisfies the stated preference). No `eqnarray`, no `$$` ✓. Table captioned,
labelled, referenced ✓. Acknowledgment before References, nothing after References ✓. Five
`\bibitem`s = five `\cite` keys ✓; alphabetical by first author's surname ✓; journal entries in the
template pattern with MathSciNet abbreviations ✓; Crossref re-verified today: HHKL vol. 3 (1993)
251–275; KP vol. 67 (2021) 3585–3598; Seuranen "Esa Antero" → "E. A." correct (KP's own list prints
"E. S."), vol. 45 (2007) 91–94; van Wee vol. 34 (1988) 237–245 ✓.

---

## 4. Answers to the brief's original six questions (round-3 state)

1. **Rule conformance**: no violation; see §3.
2. **Desk rejection**: the retitled paper reads as a general lower bound with five tabulated
   improvements and a one-line proof of a known value — both "especially welcomed" categories. The
   double-domination bridge addresses the board-composition risk at zero cost.
3. **Emails**: correct, brief, consistent; send the query first, cap the wait, then submit.
4. **AI disclosure**: accurate, names tools, covers references and factual claims, placed in the
   only unnumbered pre-reference section. Right length.
5. **Embarrassments**: none found except the unverified attribution in A1.
6. **Mathematics**: everything checkable from the text reproduces; Proposition 6.1 is now
   correctly quantified; no defect found.

---

## 5. CHECKLIST.md — items now wrong or needing re-marking

| Where | Now says | Should say |
|---|---|---|
| Header | "Checked 2026-09-02" against the old package | re-date; note round-3 changes |
| Caveat 2 | abstract carries one bracketed reference that "cannot avoid" | abstract has no reference (professor was right that it was avoidable) |
| Caveat 3 | "Fremont, CA, USA" | "Fremont, California, United States"; the exception is gone |
| Caveat 4 | AI disclosure "in one sentence of the submission email" | email no longer carries it |
| Item 1 | evidence cites the §7 footnote's voice | footnote no longer exists; body prose, third person |
| Item 4 | "Page 4 is about 70% full" | ~85 %; still 4 pages |
| Item 7 | "no theorem … changed"; numbers added = abstract reference | Prop 6.1's statement changed (range added); abstract reference removed; `\overline{K}` claim removed. Mark as "author attestation" per the professor |
| Item 9 | old title | "A Parity Lower Bound for Twofold Radius-One Coverings of the Binary Hypercube" |
| Item 12 | "Fremont, CA, USA", "see caveat 3" | plain PASS, no abbreviations |
| Item 14 | "One reference … in the P2/P9 form" | zero references; 174 words |
| Item 15 | six keywords listed | seven; "double domination" added |
| Item 22 | "Two footnotes: ∗ and †" | one footnote (∗) |
| Item 23 | PASS by source position | now PASS in the rendered output too (was FAIL per professor) |
| Item 35 | "Suggested referees … a note explains the option"; H5 wording quoted | new email has no referee note; wording is "is not under consideration elsewhere" |
| Item 36 | "PASS with a deliberate exception" | plain PASS; the email no longer has the AI sentence |
| Build record | fine | add: Chen–Li footnote → body prose; page 4 ends at References |
