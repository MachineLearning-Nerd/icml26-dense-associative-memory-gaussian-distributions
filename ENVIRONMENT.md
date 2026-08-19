# Environment and reproduction contract

## Fixed command

```bash
uv sync --frozen
uv run python -m reproduction.run
```

## Recorded accepted run

The cumulative evidence was recorded at source commit
`856fea8914ea9289e565c5e7e58ce3d55936a377` using `uv 0.11.32`, Python
`3.12.13`, Linux `6.12.90-120.164.amzn2023.x86_64`, and the Hugging Face
`cpu-upgrade` flavor. The provisioned allocation was 8 vCPUs and 32 GB;
the recorded suite runtime was `945.2080230978318` seconds with a peak RSS
of `1539864 KiB`.

The complete runtime record is
[`candidate_space/evidence/cumulative/runtime.json`](candidate_space/evidence/cumulative/runtime.json).
The recorded run uses no GPU. Text8 follows the recovered executed author
configuration, which trains on the first 100,000 tokens of the canonical
17,005,207-token corpus; this discrepancy is disclosed in the Claim 5 page.

This cleanup records and verifies the existing evidence bundle; it does not
silently replace it with an untracked rerun.

