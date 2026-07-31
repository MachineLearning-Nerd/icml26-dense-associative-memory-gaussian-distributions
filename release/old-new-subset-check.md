# Protected judged revision subset check

Protected revision:
`DineshAI/uPHdNikfdo@5d96031f01d2b0e83e0e8cbdd3ad9baadb26ce45`.

- protected non-cache files: 13
- candidate non-cache files: 107
- protected paths missing from candidate: 0

The complete path lists are `protected-file-set.txt` and
`candidate-file-set.txt`; byte hashes are in
`protected-hash-comparison.txt`.

Ten protected paths are byte-identical, including
`pages/overview/page.md`, all static application files, and every
historical image asset. Exactly three navigation surfaces are modified
additively:

- `README.md`
- `logbook.json`
- `pages/index.md`

Those three files put current verification first and link the unchanged
historical page under the exact label **Historical rejected baseline**.
The old file set is therefore a strict subset of the candidate file set,
and historical evidence content remains byte-identical.
