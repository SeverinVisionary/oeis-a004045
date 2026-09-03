# Two-model panel on the DML Part 1 submission — 2026-09-03

| leg | model | mode | verdict |
|---|---|---|---|
| professor | ChatGPT | **Pro** (`tierAtSend` = Pro, captured; AGENTS.md §9 repo default) | SEND AFTER FIXES |
| fable | Fable 5.1 | — | SEND AFTER FIXES |

Both legs got the identical brief and the full LaTeX source as attachments.
`chatgpt verify` returned CANNOT VERIFY (transcript did not render inside 60 s);
`verify --offline` exited 0 with `replyPresent: true`, the recovery marker
intact, and the tier captured as Pro. The run is therefore trusted on artifact
provenance, not on a live-page comparison — recorded here rather than glossed.

## Agreed CRITICALs — both legs, independently

1. **§6's comparison with Krotov–Potapov was false.** The claim that the
   refinement "loses at every even μ ≥ 4" and that "the gain is confined to
   μ = 2" is wrong. Both legs derived the same crossover independently:
   `P > KP ⟺ μ < n/3` for `n ≡ 0 (mod 4)` and `μ < n` for `n ≡ 2 (mod 4)`.
   The three numbers the manuscript printed (117/118, 174/176, 231/235) are all
   at n = 8, the single length where it loses; generalising from that one
   length was the error. Verified locally: the professor's exact difference
   identities match to 0 mismatches over μ ≤ 8, n ≤ 60.
   **The paper was understating its own results.**
2. **Abstract's literature-dominance claim was false**, and contradicted the
   paper's own Table 4.1: at n = 6 the theorem *matches* the known 20, it does
   not improve it. Dominance over the KP *formula* holds from n = 6; improvement
   over the *literature* only from n = 8.

## Where the legs disagreed, and how it was settled

- **Chen–Li.** Fable claimed the manuscript conflated a nonexistent item with
  Li–Chen 1994 and that the paragraph should go. **Refuted from the HHKL source
  text.** HHKL's reference list contains two distinct forthcoming manuscripts:
  `[2] Chen, W. and Li, D., Lower bounds for multiple covering codes` and
  `[29] Li, D. and Chen, W., New lower bounds for binary covering codes`
  (the latter became the 1994 IEEE paper on *ordinary* coverings). Their
  acknowledgment thanks Chen and Li "for sending us preprints of their papers",
  plural. The professor independently confirmed [2] is real and objected only to
  the rhetoric. Resolution: keep the fact, demote to a footnote, cut
  "may anticipate part or all" and the invitation to make contact.

## Professor-only findings, all applied

- Proposition 6.1 was asserted with "the same three steps then give"; the four-line
  proof is now written out, plus the rounded form.
- Theorem 4.1's asymptotic step used the `n ≡ 0 (mod 4)` gap without noting it is
  the smaller one; the ordering inequality is now stated (verified for even
  n ∈ [12,200]) along with the explicit `2^11 = 2048 > 1936` check.
- HHKL's Theorem 6 was quoted with undefined `k` and `V(n,r)`; it is now
  specialised to `r = 1`, where only ε matters. The two claims about HHKL's
  authorial motive and table attribution — neither independently reproducible —
  are removed.
- Johnson was credited twice in the text and appeared **zero** times in the
  bibliography. Since the exact Johnson reference could not be verified, the
  name is removed rather than a citation guessed.
- The AI acknowledgment omitted argument generation, the most material part;
  now stated. "Thanks the referees in advance" removed.
- Domain pinned: `n ≥ 2` even, μ a positive even integer.

## Corrections that came out of the panel

- **OEIS misattribution.** A004045 holds only `2,3,4,8,12,20,32`; the strings
  "59" and "64" appear nowhere in the entry. The 59–64 range is Krotov–Potapov's
  (lower) and HHKL 1993's (upper). Reattributed, and OEIS is now a numbered
  reference with an access date.
- **n = 6 upper bound was uncited.** OEIS carries an explicit 20-word optimal
  code contributed by Paul Tabatabai (Mar 2020). Verified locally: 20 distinct
  words, minimum coverage exactly 2, total 140 = 7 × 20. Now printed and cited,
  so `K(6,1,2) = 20` is closed on both halves.

## Not verified by anyone

- **van Wee 1988** (paywalled to both legs and to me). Fable claimed the
  manuscript's `K(n,1) ≥ 2^n/n` over-credits van Wee, whose actual radius-one
  bound is smaller. Unable to check, so the specific formula was dropped and the
  sentence weakened to "asymptotically `2^n/n`" — which serves the sentence's
  only purpose, namely warning against citing van Wee as proving this bound.
- HHKL 1993 and Seuranen 2007 beyond the pages already held locally.
- The professor compiled the source independently (4 A4 pages, no undefined
  references); so did we, with tectonic.

## Mathematical core — both legs, unchanged

Theorem 1.1 and its proof are correct. The parity step, the diagonal term, the
0-or-2 contribution of every other codeword, and the "odd and ≥ 2(n+1) hence
≥ 2(n+1)+1" rounding all check out. Theorem 4.1 is correct. Every displayed
number reproduces. Fable additionally confirmed `K(6,1,2) = 20` by ILP and
reproduced the published `59 ≤ K(8,1,2) ≤ 64`.

No CRITICAL was diluted by vote; the one cross-leg disagreement was settled
against a leg by going to the primary source.
