# Cumulative evaluator guide

Run:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

Successful run `52ab44ba-6855-4d43-a90c-33b50fdf0b79` at Git
`856fea8914ea9289e565c5e7e58ce3d55936a377` produced:

| Claim | Verdict |
| --- | --- |
| 1 | VERIFIED |
| 2 | VERIFIED |
| 3 | VERIFIED |
| 4 | VERIFIED |
| 5 | VERIFIED |
| 6 | FALSIFIED |

The complete raw JSON is `raw/result.json`. Every verifier includes an
independent checker and a negative control. The command exits nonzero if
any claim is neither VERIFIED nor FALSIFIED.
