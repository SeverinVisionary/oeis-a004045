# DML Part 1 — build/review/iterate log

Loop requested by the operator: build the rules context, build the package,
review with an independent Fable 5.1 leg and the ChatGPT professor leg at Pro,
iterate until both approve.

| round | Fable 5.1 | professor (ChatGPT, Pro) | outcome |
|---|---|---|---|
| 1 (manuscript) | SEND AFTER FIXES | SEND AFTER FIXES | both criticals applied |
| 2 (package) | APPROVE | **REVISE** | REVISE honoured in full — no vote dilution |
| 3 (package) | **APPROVE** | **APPROVE** | converged |

`tierAtSend` was captured as **Pro** on every professor leg and verified with
`chatgpt verify --offline` (exit 0, reply present, recovery marker intact). The
live-page comparison returned CANNOT VERIFY on one run because the transcript
did not render inside 60 s; that run is trusted on artifact provenance only,
and it is recorded here rather than glossed.

## The defect that justified the loop

Round 2 split. Fable approved; the professor found that **Proposition 6.1
quantified over multiplicities for which no code can exist** — it read "every
positive even integer μ", but `|B(x)| = n+1` and `C` is a set, so no μ-fold
covering exists for `μ > n+1`. At `n = 8` the formula returned 287.35 for
`μ = 10`, a bound on an undefined quantity. Verified independently here, then
restricted to `2 ≤ μ ≤ n` (for even `n`, `n+1` is odd, so `n` is the largest
feasible even multiplicity). Round 3 confirmed the range is correct and
exhaustive and that nothing downstream depended on the old one.

This is why a single approving leg is not a gate.

## Other round-2 findings, all applied

- The abstract claimed to determine "exactly when the extension improves and
  when it does not" while §6 deliberately classifies only the real-valued
  bounds — an internal contradiction, now qualified in both places.
- The Chen–Li footnote was physically printing **below the References** on
  page 4. Moved into §7 as body prose.
- The full bibliographic reference was removed from the abstract (DML prefers
  reference-free abstracts and it was avoidable).
- The acknowledgment now names the actual tools and broadens its verification
  claim to cover factual claims and references, not mathematics alone.
- Title strengthened; the previous one undersold a paper already found to be
  underselling itself.
- Both legs independently recommended the graph-theory bridge (μ-tuple / double
  dominating set) for a graph-theory-weighted board. Applied, with the keyword.

## Claims resolved against primary sources rather than by editing

- **HHKL's table** genuinely contains the `n = 8` row `32 | 58-64 | 90-94 |
  114-125`, so "64 already present in the table of [1]" stands. Note their lower
  end is 58; Krotov–Potapov later raised it to 59.
- **ε's definition** matches the manuscript verbatim:
  `ε := (r+1)⌈μ(n+1)/(r+1)⌉ − μ(n+1)`.
- **K(6,1,2) ≥ 20 is Seuranen's**, established computationally: his dissertation
  source distribution ships `bymax0IPsphere.sh`, whose first line is
  `domax0IPsphere.sh 6 1 2 0 19` — non-existence at `n=6, μ=2, M=19`. Caveat
  carried forward: that evidence is from the 2011 dissertation, while the
  manuscript cites the 2007 paper.

## Claim withdrawn for lack of evidence

The manuscript had said the repeated-codeword quantity is "written `K̄` in [1]".
HHKL plainly uses two distinct symbols, but the available scan's OCR dropped the
overbar and neither leg nor this session could establish which one is barred.
Replaced with "treated separately in [1]" rather than guessed.

## Math invariance

Checked by token-level diff after every edit round, against the version the
round-1 mathematics panel approved. The only differences in the entire body are
the feasibility restriction (`2≤μ≤n`, `μ=n`, `μ>n+1`) and the removal of
`\overline{K}`. No theorem, proof step, table entry or numerical value changed
at any point.

## Not verified by anyone

- van Wee 1988 (paywalled to both legs and to this session). The specific
  radius-one formula was dropped and the sentence weakened to "asymptotically
  `2^n/n`", which serves its only purpose — warning against citing van Wee as
  proving this bound.
- Seuranen 2007 at page level; HHKL beyond the pages held locally.
- Whether DML's linked AMS/IMU/EMS/COPE documents carry AI guidance by
  inheritance.

## Standing note

`CHECKLIST.md` from the build stage is stale in roughly fifteen places after
three rounds of edits and was deliberately NOT carried into this archive. Both
round-3 legs were told not to treat it as evidence, and neither did.
