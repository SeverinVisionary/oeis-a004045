# Off-site archive: the Zenodo deposit

Zenodo concept DOI **10.5281/zenodo.22217672** — always resolves to the current
version, and is the DOI to cite. Version history, all 2026-09-02:

| version | DOI | what it said |
|---|---|---|
| 1.0 | `10.5281/zenodo.22217673` | certificates only; `K >= 60` |
| 2.0 | `10.5281/zenodo.22261609` | added the package and Lean; `61 <= K <= 64` |
| 2.1 | `10.5281/zenodo.22261737` | paper restructured with abstract and contributions |
| 2.2 | `10.5281/zenodo.22262409` | current; correctness/consistency pass after an adversarial audit |

The v1.0 metadata described `K >= 61` as a candidate and the Lean formalisation
as unfinished; both were corrected in v2.0.

## Contents

Seven files. Two are the package itself; five are the exact-rational refutation
of `|C| = 59`, carried forward from v1.0 by Zenodo's versioning (**inherited,
not re-uploaded** — worth knowing, since the two large ones live on external
media).

| file | bytes | md5 |
|---|---:|---|
| `oeis-a004045.tar.gz` | see record | the complete repository at the released commit |
| `PAPER.md` | see record | the paper on its own |
| `cert_n8_M59_route1.json` | 4 214 | `2e2e5e94ebddefef71d5c74a9972ff76` |
| `viprchk_n8_M59.log` | 774 | `b35cf23ddf1adc2c02dc1f65b8ec336e` |
| `inst_n8_M59.opb` | 21 472 | `2db3705e97ced2616dc509051d6768c3` |
| `cert_n8_M59.vipr` | 3 594 514 707 | `0612e943473044f252388e09695b05da` |
| `cert_n8_M59_complete.vipr.gz` | 2 276 345 927 | `8d8c51b7f1732aa88eb5b81a778a37bc` |

Sizes for the first two are whatever the current version records; they change
each release, so read them off the record rather than trusting a copy here.

SHA-256 of the two uncompressed route-2 certificates, recorded when they were
made and re-verified on disk:

    621fff24e30169057ca0a3f18561872ebba0bc5693fd55fd178832e81a50dbab  cert_n8_M59.vipr
    2f2a335f883e4b88630cebbaa3d47ce2ea30986b722df54084dcc4926d2d6ddf  cert_n8_M59_complete.vipr

`viprchk` does not read gzip; the uncompressed `.vipr` is the checkable one.

## Licence on the deposit

Zenodo records a single licence, and this deposit records **MIT**. The
authoritative split is the repository's: code MIT (`LICENSE`), documentation and
certificates CC BY 4.0 (`LICENSE-DOCS`). The deposit description states the
split; if the two ever disagree, the repository governs.

## A note on matching the deposit to a commit

The tarball's top-level directory is named for the commit it was built from.
Releases up to v2.1 were built before a history rewrite, so those directory
names refer to commits that no longer exist on GitHub. v2.2's tarball is
`oeis-a004045-d3993d0/`, which is a public commit.

## Why the large upload once had to be split -- the diagnosis, settled

**Historical.** The current record holds `cert_n8_M59_complete.vipr.gz` as a
single 2 276 345 927-byte file; the parts below no longer exist as separate
files on Zenodo. The diagnosis is kept because the failure mode is generic and
cost real time.

This took three wrong answers before the right one, all recorded because the
failure mode is generic.

1. "Zenodo rejects files above ~4 GB." Inferred from the 3.59 GB file uploading
   and the 6.47 GB one failing. **Wrong** -- the gzipped 2.28 GB file failed too.
2. "It is a total outage." A plain API GET returned 504, so the service really
   was down for a stretch. **True at the time but not the whole story.**
3. "Size is irrelevant, the upload path is simply down." A 1 MB probe was
   failing identically to a 2.28 GB one. **Wrong once the service recovered**:
   the 1 MB probe then returned 201 while the 2.28 GB PUT still 502'd.

The actual cause is **upstream throughput**. A 100 MB probe did not finish in
nine minutes, so this link moves well under 1 MB/s. A 2.28 GB single PUT
therefore runs for hours and is cut by Zenodo's nginx with a 502. Size matters
only through duration, which is why every size-threshold theory half-worked.

The artifact was therefore uploaded as **400 MB parts**, each a short transfer,
each retried independently so a failure cost one part rather than the whole
file. (It was later consolidated into the single file the record now serves;
the part checksums are kept only as a record of that upload.)

| part | bytes | md5 |
|---|---:|---|
| `...gz.part-aa` | 419 430 400 | `2ffa330f68babe2ef1a73e15e15192e1` |
| `...gz.part-ab` | 419 430 400 | `26b4be2e7b873fdefc7c893f8aaf0d45` |
| `...gz.part-ac` | 419 430 400 | `30c7b02bbccc10a710fb351c58a8288e` |
| `...gz.part-ad` | 419 430 400 | `e7bb9b3fde40615de4b547dab539d711` |
| `...gz.part-ae` | 419 430 400 | `8a72b96be1a763d15f247076ecd6def0` |
| `...gz.part-af` | 179 193 927 | `881050a2acc468e0da23b856ed336fc3` |

**If you ever hold the parts**, concatenate in lexical order, then decompress:

    cat cert_n8_M59_complete.vipr.gz.part-* > cert_n8_M59_complete.vipr.gz
    # md5 of the reassembled archive: 8d8c51b7f1732aa88eb5b81a778a37bc
    gunzip cert_n8_M59_complete.vipr.gz

`viprchk` does not read `.gz` (VeriPB does), so the gunzip step is required.
The recovered file must have

    md5    34c48df67d0bfa6d2296856beba63a5a
    sha256 2f2a335f883e4b88630cebbaa3d47ce2ea30986b722df54084dcc4926d2d6ddf

## What this evidence does and does not cover

It is the **route-2 (exact-rational SCIP -> VIPR)** refutation of M=59, which
gives `K(8,1,2) >= 60`.

The route-1 (RoundingSat -> VeriPB) proof of the same rung was **lost with the
sandbox that produced it** and has not been regenerated. So `K >= 60` currently
has one surviving re-checkable machine proof, not two -- though it now also has
an independent elementary proof (`EXCESS_THEOREM.md`), which is a stronger form
of corroboration than a second certificate.

The M=60 rung -- which gives `K >= 61` -- is not certified by anything in this
deposit's certificate files. It is established instead by the Lean 4
development in the package tarball, which carries the whole argument with zero
`sorry`s. An independent pseudo-Boolean certificate for that rung is a separate
effort and is not part of this deposit.

## Security note

The upload scripts read the Zenodo API token from a local file outside the
repository and never echo it. No token is in the repository or its history.
But `curl` receives it as a command-line argument, which makes it visible in
`ps` output to any local process. **Revoke the token and delete
a local token file (path not recorded here) once the deposit is settled.**
