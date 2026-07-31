# Paper version audit

The live judge's six claim statements match arXiv
`2509.23162v1`, not the current v2 source.

| Source | Retrieved | SHA-256 | Use |
| --- | --- | --- | --- |
| v1 PDF | 2026-07-30 | `58b2f5128964af70f66049fc6a115f13bfa4530accc7ed94f282c5f1a8112baa` | canonical judged paper |
| v1 source | 2026-07-30 | `a88a9b572b0d3c28b62de7f9419885cd3367d25e8b453bf4ffeba36a68f1f6ee` | theorem text and Figures 3–8 |
| current source (v2) | 2026-07-30 | `a294dd76579191538f6141ce6647db09ac3bf38dc7dde0784ead83ade539fdd8` | version comparison only |
| ar5iv HTML | 2026-07-30 | `12972950e6f86841398b97457bbe3a8ee5c2e8a6cbdf0fd7eb319bbb6ebd1628` | navigable anchors |

Claims 5 and 6 are removed or materially changed in v2. They are not
silently replaced: the current verification explicitly tests the v1
Text8 and non-commuting experiments that the live judge scored.

The source audits for each claim record exact assumptions and
quantifiers. Claim 6 additionally hashes and digitizes the v1 Figure
8(b), while Claim 5 hashes the deleted executed author notebook that
contains the otherwise undisclosed experiment configuration.
