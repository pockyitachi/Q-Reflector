# Q-Reflector dataset

The main Q-Reflector dataset contains **880 training**, **71 validation**, and
**1,082 test** examples. Every assistant target has four ordered string fields:

```text
precondition → postcondition → reason → answer
```

`answer` is `Yes` or `No`. Each input contains the task goal, action, history,
and ordered BEFORE/AFTER screenshots. The release includes the split JSONL
files, labels, input-only views, source mappings, annotation provenance, and
4,070 original source screenshots.

The training source pool has 882 records; `train-243` and `train-589` are
quarantined and excluded from `train.jsonl`.

See the [dataset guide](../README.md) for file descriptions and the CPU integrity
check. `DATASET_MANIFEST.json` identifies the public dataset as `qreflector`.
`DATASET_MANIFEST.original.json` and `README.txt` preserve the original server
records; their historical version names do not indicate a separate dataset.

The prompt was revised using earlier test-error analysis. Subsequent test
comparisons are exploratory; checkpoint selection uses validation data.
