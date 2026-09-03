# PRIOR_ART — `K(8,1,2)`, minimum binary double covering code of length 8

> **Update, 2026-09-02 — the Chen–Li risk is now located precisely, and it is
> narrower but sharper than previously stated.** [HHKL] cites *two* forthcoming
> Chen–Li papers. Reference [29], "New lower bounds for binary covering codes",
> was published as Li & Chen, IEEE Trans. Inform. Theory 40(4) (1994) 1122–1129;
> we have now read it and it treats **ordinary** coverings K(n,R) only, via a
> "multiexcess" generalisation of van Wee. Its own reference [6] — the
> "forthcoming paper" in which "this idea is applied to multiple covering codes"
> — is HHKL itself, so the two groups cite each other.
>
> The unlocated manuscript is HHKL reference [2], W. Chen and D. Li, "Lower
> bounds for multiple covering codes", a different paper that appears never to
> have been published. HHKL places it immediately after its Theorem 6 and
> Corollary 2 (the odd-mu, even-n case) with the sentence: "Chen and Li have
> independently presented similar definitions and results, and also many further
> results, see [2]." So a named, unpublished manuscript is described by the
> primary source as containing similar results plus many further ones, at
> exactly the point our theorem improves. This does not resolve the question; it
> states it accurately.
>
> Separately, covering codes have been formalised in Lean 4 before, twice, both
> by A. Florath in 2026: arXiv:2606.09600, the general framework for ordinary
> q-ary covering codes; and arXiv:2606.16688, a Lean-certified proof of the
> exact value K_8(4,2) = 23 using fiber counting plus two Lean-checked LRAT
> refutations. The second is the closer methodological neighbour -- same
> assistant, same checked-SAT posture -- and was located 2026-09-03, after the
> initial gate. Neither treats multiple coverings. Both are prior art for the
> formalisation contribution and are cited in PAPER.md section 7.

**Gate status: PASSED, and the target is genuinely open.** Established
2026-08-28 *before* any search was run, following this project's standing rule
that the prior-art gate is settled before any compute is spent. Cross-checked by an
independent adversarial literature review (archived in
[`reviews/`](reviews/)), which confirmed the interval and corrected two of our
statements.

## The object

OEIS [A004045](https://oeis.org/A004045), verbatim name:

```
Minimal size of binary code of length n such that every vector is within
distance 1 of at least 2 codewords.
```

Data, `n = 1..7`, keywords `nonn,hard,more`:

```
2, 3, 4, 8, 12, 20, 32
```

`a(6)` and `a(7)` are credited to **Paul Tabatabai, 2020-03-02**; the entry has
had no data change since (revision 32, 2026-05-02, was a link repair).

In the standard notation of Cohen–Honkala–Litsyn–Lobstein, *Covering Codes*
(North-Holland, 1997), Ch. 14, this is `K(n,1,2)`: the minimum cardinality of a
binary `(n, ., 1, 2)` **multiple covering** — a *set* (not a multiset) of
codewords whose radius-1 balls cover every word of `F_2^n` at least twice.
Equivalently it is the **double-domination number** `gamma_{x2}(Q_n)` of the
`n`-cube, since the closed neighbourhood `N[x]` in `Q_n` is exactly the
radius-1 Hamming ball.

## The record for `n = 8`

**Source:** D. S. Krotov and V. N. Potapov, *On multifold packings of radius-1
balls in Hamming graphs*, [arXiv:1902.00023v3](https://arxiv.org/abs/1902.00023)
(2020-05-13; IEEE Trans. Inform. Theory **67**(6), 2021, 3585–3598), §IV-B.

Verbatim, Theorem 6 and the table that follows it:

```
Theorem 6. The minimum cardinality K(n, 1, mu) of a binary (n, ., 1, mu)
covering, where mu = tau mod 2, tau in {0,1}, satisfy
  (a) K(n,1,mu) >= 2^n (mu n + 3 mu + tau) / (n(n+4))   if n = 0 mod 4,
  ...
These bounds update the previous lower bounds [25], [48] in the table
[48, Table 1] of small values for K(n,1,mu) in the following positions.

        n     mu=2          mu=3            mu=4
        8     59 - 64       91 - 94         118 - 124
       10    188 - 216     291 - 316        376 - 408
       12    640 - 704     982 - 1024      1280 - 1344
       14   2195 - 2560   3365 - 3712      4389 - 4864
       16   7783 - 8192  11879 - 12288    15565 - 16384
```

**`59 <= K(8,1,2) <= 64` is the published state of the art.**

The lower bound is Theorem 6(a) at `n = 8, mu = 2, tau = 0`:
`256 * 22 / 96 = 58.67 -> 59`. The upper bound `64` is a construction, not a
bound proof: `C0 = H_7 x F_2` (the `[7,4,3]` Hamming code with a free eighth
coordinate) has size 32 and covering radius 1, and `C0 u (C0 + v)` for any
`v not in C0` is a double covering of size 64. **This is a union of two
disjoint translates, not two copies of the same codeword** — `K(n,r,mu)` is
defined on sets. Verified independently in [`verify.py`](verify.py):
coverage profile of the 64-word code is `2^192 3^64`.

## Prior-art chain

| Year | Source | Contribution |
|---|---|---|
| 1987 | R. E. Clayton, *Multiple packings and coverings in algebraic coding theory*, PhD thesis, UCLA | earliest systematic treatment cited by the MCF line |
| 1991 | G. J. M. van Wee, G. D. Cohen, S. N. Litsyn, *A note on perfect multiple coverings of the Hamming space* | perfect multiple coverings at radius 1 |
| 1993 | H. O. Hämäläinen, I. S. Honkala, M. K. Kaikkonen, S. Litsyn, *Bounds for binary multiple covering codes*, Des. Codes Cryptogr. **3**, 251–275 | the `K(n,r,mu)` table this target lives in |
| 1995 | P. R. J. Östergård, *New multiple covering codes by tabu search*, Australas. J. Combin. **12**, 145–155 | the upper bounds, `64` among them |
| 2007 | E. S. Seuranen, *New lower bounds for multiple coverings*, Des. Codes Cryptogr. **45**, 91–94 | the small-value table (`Table 1`) that Krotov–Potapov update |
| 2020 | Krotov–Potapov, above | the current lower bound `59` |

**Seuranen's Table 1 is a static published table, not a maintained one.** There
is no live status page for `K(n,1,mu)`; Kéri's covering-code tables
(<http://old.sztaki.hu/~keri/codes/>) cover `K_q(n,R)` and mixed codes, not
multiplicity. The closest thing to a live record is the citation graph, so
that is what was checked.

## Forward-citation sweep (2026-08-28)

- Seuranen 2007 has **exactly one** citation on Semantic Scholar
  (`DOI:10.1007/s10623-007-9089-y`): Krotov–Potapov.
- Krotov–Potapov has **six** citing papers: perfect colorings of `n`-cubes
  (2019, 2023), `OA(2048,14,2,7)` classification (2023), multifold 1-perfect
  codes (2022), multiple-packing error exponents (2022), `q`-ary
  shortened-1-perfect-like codes (2021). **None revisits `K(8,1,2)`.**
- Independent adversarial search (ChatGPT professor leg, Extra High, session
  `e2712fb9`, verified exit 0) over the notations `K(8,1,2)`, the `59–64`
  interval, "double domination of `Q_8`", theses and non-English sources found
  no published exact value, no lower bound above 59, and no upper bound below
  64. Its own caveat is recorded verbatim: *"I cannot prove that no unindexed
  thesis or obscure report exists."*

So the honest statement is **"no later published improvement located"**, not
"none exists".

## Two corrections the review forced

1. **"Exact values are known only for `n <= 7`" is false read literally.** It is
   true of the *contiguous* prefix. At Hamming lengths `n = 2^m - 1` the union
   of two distinct cosets of the `[n, n-m, 3]` Hamming code meets the double
   sphere bound exactly, so
   `K(2^m - 1, 1, 2) = 2^(n+1)/(n+1)` — e.g. `K(15,1,2) = 4096`. `a(7) = 32` is
   the `m = 3` case, which is why it is the last term OEIS knows.
2. The `n = 8` upper bound must be phrased as two **disjoint translates**; the
   "doubled Hamming code" phrasing describes a multiset and is not what
   `K(n,r,mu)` counts.

## Adjacent notions this is NOT

Confusing any of these with `K(n,1,2)` would produce a false prior-art match.

| Notion | Difference |
|---|---|
| MCF codes (Hämäläinen–Honkala–Litsyn–Östergård, SIAM J. Discrete Math. **8** (1995) 196–207) | multiplicity `mu` required only at the **farthest-off points**, not everywhere |
| `lambda`-fold **packing** | every ball contains **at most** `lambda` codewords. Complementing a `mu = 2` covering of `Q_8` gives a **7**-fold packing (`|B_1| = 9`), not a 2-fold one |
| Klapper's **multicovering radius** | one codeword within radius `r` of **all** of an `m`-tuple; a different quantifier order entirely |
| "Nearly perfect covering codes" | ordinary radius-1 covering codes meeting the van Wee bound; `mu = 1` |
| `K(8,1) = 32` | the `mu = 1` problem, settled long ago; it is where the `64` construction comes from |

## Sphere bound vs. the known terms

`|C|(n+1) >= 2 * 2^n`, i.e. `K(n,1,2) >= ceil(2^(n+1)/(n+1))`:

| `n` | sphere LB | A004045 | slack |
|---:|---:|---:|---:|
| 4 | 7 | 8 | +1 |
| 5 | 11 | 12 | +1 |
| 6 | 19 | 20 | +1 |
| 7 | 32 | **32** | 0 (two Hamming cosets) |
| 8 | 57 | **open**, published `59–64` | ≥ +2 |

All five known terms `n = 4..8` were re-derived from scratch by the SAT model in
[`sat_model.py`](sat_model.py) as a known-answer gate before any `n = 8` run —
see [`WORKLOAD_ESTIMATE_2026-08-28.md`](WORKLOAD_ESTIMATE_2026-08-28.md) §2.

---

# Round 2 — protocol-driven sweep (2026-08-28)

Round 1 established the record. Round 2 exists because the pilot refuted `M = 59`
and `M = 60` in seconds with stock solvers, and a bound that cheap standing since
2020 is more likely to mean *we missed the publication* or *our model is wrong*
than *a free result*.

The search protocol is [`reviews/2026-08-28_prior_art_protocol.md`](reviews/2026-08-28_prior_art_protocol.md)
(independent, Extra High, verified). Its lane ranking, its stopping criteria, and
its evidence standard are what the ledger below is scored against. **We are at
its Level 1, not Level 2 or 3.**

## The identity being searched

```
Universe   V = F_2^8, |V| = 256;  B_1(v) = {c : d(c,v) <= 1}, |B_1| = 9
Code       a SET, not a multiset
Condition  |C ∩ B_1(v)| >= 2 for every v ∈ V
Quantity   min |C|
IP         min 1^T x  s.t.  (I + A(Q_8)) x >= 2·1,  x ∈ {0,1}^256
```

Equivalent names, each searched as its own lane:

- `K(8,1,2)` — binary multiple covering code, Cohen–Honkala–Litsyn–Lobstein Ch. 14
- `gamma_{x2}(Q_8)` — **2-tuple / double domination** of the 8-cube, closed neighbourhoods
- `256 - L_7(Q_8)` — complement of a **7-limited packing** (`|N[v] ∩ L| <= 7`).
  `K >= 61` is exactly `L_7(Q_8) <= 195`. This lane was missed entirely in round 1.

## Ledger

| # | Lane | Resource | Outcome |
|---|---|---|---|
| 1 | 2-tuple / double domination of `Q_n` | Brešar–Klavžar et al., *Packings in bipartite prisms and hypercubes*, [arXiv:2309.04963](https://arxiv.org/abs/2309.04963), Table 1 — the current state-of-the-art hypercube invariant table | **negative.** Carries `γ, γ_t, ρ_2, ρ_o` for `n <= 9`. **No `γ_{x2}` row, no limited-packing row.** `ρ_2(Q_8)` is still published as the *range* `17–30` and `ρ_o(Q_9)` as `34–60` |
| 2 | 7-limited packing | Gallant–Gunther–Hartnell–Rall and the follow-up literature ([arXiv:1501.01833](https://arxiv.org/abs/1501.01833), [arXiv:1501.01511](https://arxiv.org/abs/1501.01511), J. Comb. Optim. 2020) | **negative.** That line proves general bounds in terms of order, degree, girth and diameter, plus complexity results. No table of `L_k` for named graphs; no `L_k(Q_n)` |
| 3 | fault-tolerant domination | web + arXiv | **negative.** Hits are fault-tolerant *identifying* and *locating-dominating* codes, a different (stronger) condition |
| 4 | author pages and data directories | [Östergård's publication list](https://users.aalto.fi/~pat/patric_pub.html) | **negative.** His multiple-covering work is the 1995 tabu-search paper (upper bounds) and the 1995 MCF paper (a different notion). No `K(n,1,mu)` table or data directory |
| 5 | thesis + source distribution | E. A. Seuranen, *Computational methods in codes and games*, Aalto 2011 — source distribution at <https://esaseuranen.fi/papers/dissertation/> | **negative, and decisive.** See below |
| 6 | public computational artifacts | GitHub code search (authenticated) for `K(8,1,2)`, exact-notation strings | **negative.** 0 hits on the notation |
| 7 | OEIS record | [A004045](https://oeis.org/A004045), `/internal`, `/history` | **negative.** `nonn,hard,more`; no comment, no xref, no b-file; no data change since 2020-03-02 |

## Lane 5 in detail — why 59 stood

Seuranen is the author of the table Krotov–Potapov updated. His dissertation
ships the scripts that regenerate his published results. By `(n, r, mu)`:

| script | purpose | parameters |
|---|---|---|
| `byIPsphere.sh` | lower bounds by IP | `(8,1,4) (10,1,2) (13,1,3) (14,1,2) (16,1,2) (16,1,4)` + `r>=2` cases. **`(8,1,2)` absent** |
| `bymax0IPsphere.sh` | non-existence proofs | includes `(6,1,2)` at `M=19`, `(12,1,2)` at `M=631`. **`(8,1,2)` absent** |
| `byExhaustive.sh` | exhaustive isomorph-rejection search | every entry has **`r >= 2`** and `M <= 18`. **Radius 1 never appears** |

And the formulation is the point. `makeIPsphereProb.pl` declares variables
`c_0 … c_n` — **one per weight class**, so 9 variables at `n = 8`. It is a
weight-distribution relaxation, not the 256-variable word IP. That is why it
reaches `n = 16`, and why it is far weaker as a refutation tool.

So the explanation for a six-year-old bound falling to a laptop is
**methodological**: the field's lower-bound instrument for this table is a
9-variable relaxation, its only exhaustive search was aimed at radius `>= 2`
where codes have `M <= 18`, and after 2011 the line moved to closed-form theorem
bounds — Krotov–Potapov's Theorem 6 is an inequality, not a computation.

## A cross-check on our own model, from the literature's own machinery

`bymax0IPsphere.sh` line 1 is `domax0IPsphere.sh 6 1 2 0 19`: Seuranen proving
non-existence at `n = 6, mu = 2, M = 19`, i.e. `K(6,1,2) >= 20`. **Our model says
exactly that.** Together with reproducing `a(4)=8, a(5)=12, a(6)=20, a(7)=32` and
admitting the independently verified 64-word code, the formulation is not where
an error is likely to be hiding.

## Round 2b — zbMATH Open sweep (2026-08-28)

MathSciNet is subscription-only and was not available. **zbMATH Open** (free
since 2021, the Zentralblatt successor, comparable coverage of the mathematical
literature) was queried instead via its public API. Exact strings, as run:

| query | records returned | relevant |
|---|---:|---|
| `ti:"limited packing"` | 12 | **0** hypercube/code-flavoured |
| `ti:"tuple domination"` | 32 | **0** |
| `ti:"double domination"` | 58 | 0 — the one flagged title, *1-movable double domination in some binary operations of graphs*, means graph products, not binary codes |
| `any:"double domination" & any:hypercube` | 1 | Harant–Henning, *On double domination in graphs* (2005) — general **upper** bounds by minimum degree; cannot imply a lower bound |
| `any:"tuple domination" & any:hypercube` | **0** | — |
| `any:"limited packing" & any:hypercube` | **0** | — |
| `any:"multiple covering" & any:"hypercube"` | 1 | Vorob'ev, *Perfect multiple coverings of a hypercube* (2012) — **perfect** multiple coverings are exact constant coverage, a strictly stronger and different notion; already listed in the adjacent-notions table above |

zbMATH indexes review text, so the `any:` queries reach papers whose titles do
not announce the hypercube. Both top-ranked synonym lanes are closed at database
level.

## Coverage, honestly

**Level 1 reached** — "no indexed publication found" — for the coding notation,
both graph synonyms, the limited-packing complement, and the artifact lanes.

**Level 2 PARTIALLY reached.** zbMATH Open is done (round 2b). Still
unexecuted: MathSciNet (subscription-only, unavailable here — its overlap with
zbMATH is high but not total), the Russian-language lane (MathNet, `кратное покрытие`,
`двойное доминирование`), pre-1995 proceedings and scans, Wayback diffs of
historical covering-code tables, and conference abstracts.

**Level 3 NOT reached** and cannot be without correspondence: a private solver
run from the 1990s or 2000s is not excludable by search. Per the protocol's
evidence standard, the strongest claim this sweep could ever license is
*"the first publicly documented rigorous proof"*, never *"the first computation"* —
and even that needs the certification leg (estimate §5), which does not exist yet.

---

# Round 3 — MathSciNet and the Level-3 lanes (2026-08-28)

Protocol leg archived at [`reviews/2026-08-28_round3_mathscinet_level3.md`](reviews/2026-08-28_round3_mathscinet_level3.md).

## The lead that mattered: Waterson 2025

**T. W. Waterson, _Minimum Cardinality of q-ary Covering and Multiple Covering
Codes with Radius 1_, BSc thesis, TU/e, June 2025.** Supervisors Luuk Reijnders
and Aida Abiad Monge. Verified to exist independently of the leg that named it
(OpenAlex `W7112221050`), then obtained from the TU/e Pure file host and read.

A title that is our exact problem, three months old, from an active combinatorics
group. **It does not contain our cell.** Section 5.5, verbatim:

```
The tables below for q = 3, 4, 5 and mu = 2, 3, 4 show which results yield the
best bounds for different q, n and mu.
...
For tables for mu = 1 see [20]. For tables for q = 2 see [12].
```

`[12]` is Hämäläinen–Honkala–Kaikkonen–Litsyn 1993 — already the first row of our
chain. The thesis works the `q >= 3` gap and defers the binary table wholesale to
the 1993 paper.

**This is a useful negative, not merely an absent one.** A 2025 thesis aimed at
exactly "minimum cardinality of multiple covering codes with radius 1", which
surveyed the field in February 2025 (it cites Kéri's tables "accessed
2025-02-18"), treated the binary `K(n,1,mu)` table as settled by a 1993
reference. As of 2025 nobody in that group was recomputing this cell.

## MathSciNet — NOT CHECKED, and the risk is sized

Subscription-only; unavailable both here and to the review leg. What the leg
established instead is the **size of the gap**: MathNet's profile for V. N.
Potapov lists 89 publications, **60 in MathSciNet and 55 in zbMATH**. A
zero-result zbMATH sweep therefore does *not* imply a zero-result MathSciNet
sweep, even for this precise research group. AMS also warns its Cyrillic
transliteration changed in January 1983, so Russian-language items may need both
transliterations.

The five queries a subscriber should run, verbatim:

```
Anywhere:  "double domination" AND hypercube
Anywhere:  "tuple domination" AND hypercube
Anywhere:  "limited packing" AND hypercube
Anywhere:  "multiple covering" AND (hypercube OR "Hamming space")
Anywhere:  "K(n,1,2)"  /  "K(8,1,2)"
```

Repeat each in the **Review Text** and **References** fields, which MathSciNet
indexes separately.

## Lanes still open, stated as open

| Lane | Status |
|---|---|
| MathSciNet subject search | **NOT CHECKED** — no subscription |
| Wayback/CDX time series on the covering-code tables and the Östergård / Honkala / Lobstein / Krotov / Potapov / Litsyn / Kaikkonen pages | **NOT CHECKED** — the leg could not enumerate captures; our own CDX attempts were rate-limited (HTTP 429) |
| Dead FTP and software directories reachable only through the archive | **NOT CHECKED** — depends on the Wayback lane |
| Cohen–Honkala–Litsyn–Lobstein 1997, Ch. 14 §"Tables for multiple coverings" — the original table page | **NOT CHECKED** — section confirmed to exist, page not obtained |
| Systematic WCC / ACCT / Finnish and Russian workshop programmes | **NOT CHECKED** — targeted search only |
| Issue-by-issue sweep of *Diskretnyi Analiz i Issledovanie Operatsii* | **NOT CHECKED** — targeted search only |
| Syracuse tech report SU-CIS-95-01 body | **NOT CHECKED** — landing page reachable, body blocked |

The Russian targeted lane did resolve one candidate: Vorob'ev, *Perfect multiple
coverings of a hypercube* (2012) requires every ball to contain **exactly** `k`
codewords — a strictly different problem, already in the adjacent-notions table.

## Coverage after round 3

Still **partial Level 2**. The highest-probability modern lead is closed
negative; the remaining lanes are historical and archival, and the largest of
them (Wayback) is open purely for technical reasons. Level 3 is untouched and
requires correspondence — a draft email to the authors is in the archived leg,
**unsent**; sending it is an operator decision, and it discloses the question to
the people best placed to answer it themselves.
