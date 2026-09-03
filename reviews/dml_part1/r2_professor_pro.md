REVISE

The manuscript is close, and the main mathematics appears sound. The package is not ready to send unchanged, however. I found one genuine mathematical-domain defect, one material overstatement, one visible end-matter defect, and email wording that unnecessarily increases the chance of an adverse editorial decision. CHECKLIST.md is too generous when it says there are no failures. 

CHECKLIST

Blocking fixes, ranked
1. Restrict Proposition 6.1 to feasible multiplicities

The Introduction defines K(n,1,μ) as the least cardinality of a set C satisfying the covering condition. But every radius-one ball contains only n+1 words, so no such set exists when μ>n+1. No convention K(n,1,μ)=+∞ is stated. Proposition 6.1 nevertheless quantifies over every positive even integer μ, making the statement undefined for sufficiently large μ. 

dml_submission(1) +1

Replace the proposition opening with:

LaTeX
\begin{proposition}\label{prop-mu}
Let $n\ge 2$ be even and let $\mu$ be an even integer with
$2\le \mu\le n$. Then

Because n is even, n is the largest feasible even multiplicity. Alternatively, define K(n,1,μ)=+∞ when the feasible class is empty, but the explicit restriction is cleaner.

Also change every occurrence of “every even multiplicity” to “every feasible even multiplicity.” This affects the abstract and the end of the Introduction.

The algebraic proof of Proposition 6.1 is otherwise correct.

2. Correct the overclaim about exactly when the extension improves the Krotov–Potapov bound

The abstract says that the paper determines exactly when the extension “improves on the Krotov–Potapov bound and when it does not.” The Introduction makes the same unqualified claim. But Section 6 explicitly says that only the underlying real-valued expressions are classified and that strict improvement may disappear after taking ceilings. 

dml_submission(1) +2

Replace the abstract’s last sentence with:

The argument extends to every feasible even multiplicity. For the underlying real-valued bounds, we determine exactly when the resulting expression exceeds the Krotov–Potapov expression, while noting that a strict gain need not survive the ceiling.

Replace the final clause of the Introduction with:

LaTeX
and Section \ref{sec-mu} carries the argument to every feasible even
multiplicity and classifies when the underlying real-valued bound exceeds
the Krotov--Potapov bound.

I would also sharpen the opening of Section 6 to avoid suggesting that strict excess itself occurs only for even μ:

LaTeX
For even $n$, the ball sum at a codeword is odd. Thus parity alone forces
it to exceed the baseline $\mu(n+1)$ exactly when $\mu$ is even.

The present wording is defensible if “which happens” means “which is forced by rounding,” but it is unnecessarily easy to misread. 

dml_submission(1)

3. Remove the Section 7 footnote and put its content in the body

In my compiled four-page PDF, the Chen–Li footnote is physically printed at the very bottom of page 4, below the References. That makes the visible document end with a novelty disclaimer after the bibliography. It looks accidental and defeats the intended end-matter order, even though the footnote command occurs before the Acknowledgment in the source. 

dml_submission(1)

Replace the footnote with ordinary prose at the end of Section 7:

LaTeX
Reference \cite{HHKL-1993} also cites a forthcoming manuscript of
W.\ Chen and D.\ Li entitled \emph{Lower bounds for multiple covering
codes}. The author has not located a published version; the novelty
comparison above is therefore limited to accessible published literature.

Keep this disclosure. It is honest and potentially important. Just do not let TeX place it after the reference list.

4. Rewrite the policy query before sending it

I recommend sending a pre-submission query, but not the current version.

The trade-off is straightforward. A query may prompt a conservative editor to say no, but the same editor will see the disclosure during initial screening anyway. Because the use included generating candidate arguments and drafting text, asking first mainly moves the decision earlier and may avoid a months-long submission cycle. DML’s own published material remains silent about generative AI. 

DML_RULES

The current query contains two strategically harmful sentences:

“The main result is an elementary theorem with a half-page proof that a referee can check by hand” makes the contribution sound trivial.

“If it is not, I will not take up your referees’ time” unnecessarily supplies the editor with a rejection frame.

Its detailed inventory of every page searched is also more defensive than useful. 

POLICY_QUERY_EMAIL

Use this instead:

Subject: Pre-submission policy query: disclosed use of generative AI

Dear Editors,

I am considering submitting a four-page research article to Discrete
Mathematics Letters. In preparing it, I used [ACTUAL TOOL NAMES]
substantially for literature exploration, generating candidate arguments,
and drafting text. I independently checked the mathematical arguments,
factual claims, and references, made all final scholarly decisions, and
would disclose this use in the manuscript.

Would a submission prepared in this way be acceptable under DML's policy?

I have not attached the manuscript because this is only a policy query.

With thanks,

Hanyu Yang
Fremont, California, United States
hanyu.yang.92@gmail.com

The proposed recipient—chief-editor address, with the managerial secretary copied—is reasonable, and no attachment is correct.

5. Shorten the submission email and do not repeat the full AI disclosure

The submission email is factually consistent with the manuscript, but it is not brief. It repeats front-matter metadata, an abstract-length contribution summary, funding and conflict statements, and the entire AI-use declaration. That makes the tooling, rather than the theorem, the final substantive thing the editor reads. 

SUBMISSION_EMAIL

Use:

Subject: Submission: A Parity Refinement of the Covering Excess Bound for
Twofold Coverings of the Hypercube

Dear Managerial Secretary,

Please find attached the PDF of “A Parity Refinement of the Covering
Excess Bound for Twofold Coverings of the Hypercube” for consideration as
an original research article in Discrete Mathematics Letters.

The paper gives an elementary parity lower bound for twofold radius-one
coverings of even-dimensional binary hypercubes. It improves the published
lower bounds at dimensions 8, 10, 12, 14, and 16, and gives a
noncomputational proof of the lower-bound half of the known value at
dimension 6.

The manuscript has not been published elsewhere, is not under
consideration elsewhere, and, if accepted by Discrete Mathematics Letters,
will not be published elsewhere.

[On DATE, NAME confirmed that the disclosed use of generative AI is
acceptable under the journal's policy.]

Thank you for considering the manuscript.

Yours sincerely,

Hanyu Yang
Fremont, California, United States
hanyu.yang.92@gmail.com

Insert the bracketed sentence only after an affirmative policy response. The existing optional sentence—“This use was the subject of my enquiry of DATE, which NAME kindly answered on DATE”—is awkward and does not say what the answer was. 

SUBMISSION_EMAIL

Strongly recommended manuscript fixes
Remove the full bibliographic reference from the abstract

DML expressly prefers abstracts without references where possible. The reference here is plainly avoidable because Krotov and Potapov are cited normally in the Introduction. 

DML_RULES

Replace:

After taking ceilings the bound exceeds the general lower bound of Krotov and Potapov [full journal reference] …

with:

After taking ceilings, the bound exceeds the general lower bound of Krotov and Potapov for every even length from six onward.

This also supplies the missing comma after the introductory phrase. The checklist’s assertion that this reference “cannot avoid” appearing is wrong. 

CHECKLIST

Improve, but retain, the AI disclosure

The disclosure is accurately placed in the Acknowledgment and matches the stated use. It is neither too extensive nor inappropriate. The funding and conflict statements are also exactly where DML requires them to be. 

dml_submission(1)

 

DML_RULES

Its wording can be improved in three ways:

Name the actual tools rather than only the category.

Replace the awkward compound “artificial-intelligence.”

Do not limit the verification statement to mathematics when the tools were also used for literature exploration and prose.

Use:

LaTeX
The author used [ACTUAL TOOL NAMES, WITH VERSIONS IF KNOWN] for literature
exploration, generating candidate arguments, and drafting text. The author
independently checked the mathematical arguments, factual claims, and
bibliographic references, made all final scholarly decisions, and takes
full responsibility for the final manuscript. No financial support was
received for this work, and the author declares no conflict of interest.

Only retain “checked the factual claims and bibliographic references” after completing those checks.

A correction to my interim assessment: DML’s actual ethics page links an EMS PDF approved in 2012, not clearly the EMS’s replacement 2025 code. Therefore naming the tools is not demonstrated to be a binding DML requirement. The current EMS code nevertheless recommends a declaration describing the automated tools and the nature of their use, so naming them is the safer current practice. 
Discrete Math Letters
+2
Mathematical Union
+2

Desk-rejection assessment

A format-based desk rejection should not occur after the fixes. The paper uses the prescribed template, is far below the eight-page cap, is in scope, and presents both nontrivial progress on published bounds and a short elementary proof—two categories DML expressly welcomes. 

DML_RULES

The scientific desk-rejection risk is real but not excessive. The contribution is substantial enough for this particular journal:

a new general elementary lower bound;

strict improvements at five tabulated even lengths;

improvement of the first unresolved OEIS position from 59 to 60;

a noncomputational lower-bound proof for the exact value at length six;

an extension to feasible even multiplicities.

Those claims are visible in the theorem, comparison table, and small-length consequences. 

dml_submission(1) +1

The current title is accurate, but “A Parity Refinement of the Covering Excess Bound…” sounds more incremental than the paper actually is. A stronger optional title is:

A Parity Lower Bound for Twofold Radius-One Coverings of the Binary Hypercube

Because the board is graph-theory-weighted, add one sentence immediately after the definition:

LaTeX
Equivalently, such a code is a double dominating set in the
$n$-dimensional hypercube graph.

Also add double domination as a keyword. This gives a graph theorist an immediate translation without changing the paper’s coding-theoretic focus. The brief correctly identifies initial screening and board fit as the important editorial risk. 

review_brief_pkg

CHECKLIST.md PASS labels I do not accept

Item 7: originality and completeness of attribution cannot be established by a token-level comparison between drafts. It should read “author attestation; literature review partially checked,” not unqualified PASS. 

CHECKLIST

Item 14: qualified at best. The abstract reference is avoidable and contrary to DML’s stated preference. 

CHECKLIST

Item 23: FAIL in the rendered output until the Section 7 footnote is moved; the PDF visibly has substantive text below the References. 

CHECKLIST

Item 35: the submission email is correct but not minimal and contains strategically unnecessary material. 

CHECKLIST

Item 36: “PASS with a deliberate exception” is not a literal PASS against the rules document’s own recommendation. It is an intentional, defensible exception—not a journal-rule violation. 

DML_RULES

Item 12 is acceptable because avoiding affiliation abbreviations is only a preference and published precedent supports the current form. Nevertheless, the exception disappears entirely if all three files use “Fremont, California, United States.”

Independent checks that passed

I read all six files completely and audited the TeX rather than relying on the checklist.

I compiled the supplied TeX twice. It produces a four-page A4 PDF with no undefined references or citations. The only box warnings arise from the retained template header/title skeleton.

The preamble, theorem declarations, header, page placeholders, footnote symbols, counter settings, and bibliography modifications match the settings recorded from the mandatory DML template. The manuscript is comfortably within the eight-page limit. 

DML_RULES

The title has no formula or abbreviation. There are six semicolon-separated keywords and three comma-separated MSC 2020 codes. 

dml_submission(1)

The theorem-like material and proofs use proper environments. There is no eqnarray. The table has a caption, label, and textual reference.

Funding and conflict of interest are explicitly disclosed in the manuscript, satisfying the journal’s ethics requirement. 

DML_RULES

All five bibliography entries are cited. Their order is alphabetical by first-author surname; the journal abbreviations and entry forms conform to the stated style; no ordinary journal entry contains a DOI or URL. 

DML_RULES

 

dml_submission(1)

The submission address and PDF-only attachment mechanics are correct. 

DML_RULES

I independently checked the central double count, the ceiling comparison in Theorem 4.1, the table values, and the numerical examples in Section 6. They reproduce. I also checked the listed twenty-word length-six construction directly: every word is covered at least twice. I found no error in Theorem 1.1 or Theorem 4.1. Proposition 6.1’s proof is algebraically sound once its feasible parameter range is stated.

After the four blocking fixes, removal of the abstract citation, and regeneration of the PDF, I would approve the mathematical manuscript for submission. The policy query should go first in its shortened form; the submission email should follow only after either an affirmative response or an explicit decision to proceed despite silence.

MARKER-DML-PKG-2026-09-03.
