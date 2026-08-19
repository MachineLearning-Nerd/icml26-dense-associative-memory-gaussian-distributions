# Source audit

The live judge assessed arXiv `2509.23162v1`, not the current v2 source.
The v1 scope is therefore the canonical evidence target for this repository.

| Source | Retrieved | SHA-256 | Role |
| --- | --- | --- | --- |
| arXiv v1 PDF | 2026-07-30 | `58b2f5128964af70f66049fc6a115f13bfa4530accc7ed94f282c5f1a8112baa` | Judged paper |
| arXiv v1 source | 2026-07-30 | `a88a9b572b0d3c28b62de7f9419885cd3367d25e8b453bf4ffeba36a68f1f6ee` | Theorem text and Figures 3–8 |
| arXiv v2 source | 2026-07-30 | `a294dd76579191538f6141ce6647db09ac3bf38dc7dde0784ead83ade539fdd8` | Version comparison only |
| ar5iv HTML | 2026-07-30 | `12972950e6f86841398b97457bbe3a8ee5c2e8a6cbdf0fd7eb319bbb6ebd1628` | Navigable source anchors |

Claims 5 and 6 are removed or materially changed in v2. The reproduction
does not silently substitute v2 for the claims that were judged against v1.
Claim 5 also records the hash-pinned executed author notebook used to recover
the otherwise undisclosed Text8 configuration. Claim 6 hashes and digitizes
the v1 Figure 8(b) evidence.

Detailed per-claim assumptions and quantifiers are in the source-audit files
under [`candidate_space/evidence`](candidate_space/evidence).

