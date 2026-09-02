# Off-site archive of the K(8,1,2) >= 60 evidence

Zenodo record **10.5281/zenodo.22217673** (<https://doi.org/10.5281/zenodo.22217673>), published 2026-09-02. Formerly a draft; the
DOI is now minted and the five files below are open access under CC BY 4.0. The
decision.

## Contents and checksums

| file | bytes | md5 | verified |
|---|---:|---|---|
| `cert_n8_M59_route1.json` | 4 214 | `2e2e5e94ebddefef71d5c74a9972ff76` | stored, matches local |
| `viprchk_n8_M59.log` | 774 | `b35cf23ddf1adc2c02dc1f65b8ec336e` | stored, matches local |
| `inst_n8_M59.opb` | 21 472 | `2db3705e97ced2616dc509051d6768c3` | stored, matches local |
| `cert_n8_M59.vipr` | 3 594 514 707 | `0612e943473044f252388e09695b05da` | stored, matches local |
| `cert_n8_M59_complete.vipr.gz` | 2 276 345 927 | `8d8c51b7f1732aa88eb5b81a778a37bc` | upload in progress |

SHA-256 of the two uncompressed route-2 certificates, recorded when they were
made and re-verified on disk:

    621fff24e30169057ca0a3f18561872ebba0bc5693fd55fd178832e81a50dbab  cert_n8_M59.vipr
    2f2a335f883e4b88630cebbaa3d47ce2ea30986b722df54084dcc4926d2d6ddf  cert_n8_M59_complete.vipr

## Why the last file is split into parts -- the diagnosis, settled

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

So the artifact is uploaded as **400 MB parts**, each a short transfer, each
retried independently so a failure costs one part rather than the whole file:

| part | bytes | md5 |
|---|---:|---|
| `...gz.part-aa` | 419 430 400 | `2ffa330f68babe2ef1a73e15e15192e1` |
| `...gz.part-ab` | 419 430 400 | `26b4be2e7b873fdefc7c893f8aaf0d45` |
| `...gz.part-ac` | 419 430 400 | `30c7b02bbccc10a710fb351c58a8288e` |
| `...gz.part-ad` | 419 430 400 | `e7bb9b3fde40615de4b547dab539d711` |
| `...gz.part-ae` | 419 430 400 | `8a72b96be1a763d15f247076ecd6def0` |
| `...gz.part-af` | 179 193 927 | `881050a2acc468e0da23b856ed336fc3` |

**To reassemble**, concatenate in lexical order, then decompress:

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

Nothing here concerns M=60; that computation is still running.

## Security note

The upload scripts read the token from a local token file (path not recorded here) and never echo it.
But `curl` receives it as a command-line argument, which makes it visible in
`ps` output to any local process. **Revoke the token and delete
a local token file (path not recorded here) once the deposit is settled.**
