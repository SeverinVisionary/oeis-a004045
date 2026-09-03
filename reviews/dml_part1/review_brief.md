# Review request: a 4-page note for submission to Discrete Mathematics Letters

You are reviewing a manuscript that is about to be emailed to a journal. The
attached LaTeX source is the complete submission. Review it as a hostile referee
would, then tell me whether to send it.

## Context you need

- **Author:** one person, no institutional affiliation, no prior publications.
- **Venue:** *Discrete Mathematics Letters* — free, LaTeX template mandatory,
  hard 8-page cap, submitted as a PDF by email. Scope explicitly welcomes
  "non-trivial progress on existing problems" and short or alternative proofs.
- **Disclosure:** generative AI was used substantially, including to propose
  arguments and draft the text. This is disclosed in the acknowledgment. The
  author checked the mathematics.
- **This note is Part 1 of a larger package.** A separate Lean 4 formalisation
  establishes `K(8,1,2) >= 61`; that is deliberately NOT in this note, which
  claims only `K(8,1,2) >= 60` via the elementary theorem. Do not treat the
  omission as an error.
- Supporting code and certificates are public at
  https://github.com/SeverinVisionary/oeis-a004045 and
  https://doi.org/10.5281/zenodo.22217672

## What I most need from you

**1. Is the mathematics correct?** This is the priority. In particular:

  - **Theorem 1.1 and its proof (Section 3).** Step 1 claims the ball sum at a
    *codeword* is odd when `n` is even. Check the diagonal term, check that
    every non-diagonal codeword really contributes 0 or 2, and check that the
    "at least `2(n+1)`, and odd, so at least `2(n+1)+1`" step is valid. Is the
    set hypothesis (no repeated codewords) used exactly where Remark 3.2 says?
  - **Theorem 4.1 (dominance).** The two cross-multiplied identities, the three
    small cases handled by direct check (`n = 6, 8, 10`), and the asymptotic
    argument for `n >= 12`, including whether `2^n > 16n^2` for all `n >= 11`
    and whether the claimed monotonicity is enough.
  - **Every displayed number.** One arithmetic typo was already caught in this
    text: `ceil(768/20) = 20` should have been `ceil(384/20) = 20` (768/20 is
    38.4). Assume there may be more of the same kind. Verify the table values
    (192, 647, 2235, 7865), the gaps 8/15 and 16/39, and the Proposition 6.1
    numbers (117 vs 118, 174 vs 176, 231 vs 235).

**2. Is any claim overstated or under-hedged?** The note asserts strict
dominance over Krotov–Potapov at every even `n >= 6`, and asserts that the
HHKL bound collapses to the sphere bound at even `mu`. Are those defensible as
written? Is the claim about no `mu = 2` entry in HHKL's table being attributed
to their Theorem 6 too strong for a paper that cannot reproduce their table?

**3. Would this be desk-rejected, and why?** Be concrete. Length, framing,
title, abstract, whether an editor will see it as a real contribution or as an
incremental table update. The Chen–Li paragraph in Section 7 openly admits an
unlocated manuscript may anticipate the result — does that read as scholarly
integrity or as an invitation to reject?

**4. The AI disclosure.** DML publishes no generative-AI policy. The plan is to
email a policy query before submitting. Is the acknowledgment worded well? Too
much, too little, wrongly placed?

**5. Anything a referee would demand** that is missing: a definition, a
citation, a worked example, an explicit statement of what is new.

## Output

Give me a verdict — SEND / SEND AFTER FIXES / DO NOT SEND — and rank every
finding by severity. For each finding state the exact location, what is wrong,
and the concrete fix. If you find no error in a section, say so explicitly
rather than staying silent; I need to know what you checked.

Do not soften. A wrong theorem reaching a referee costs far more than a blunt
review.
