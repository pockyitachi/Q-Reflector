# Dataset contracts

The current condition-generation split is
[condition_generation_v9_after_evidence](condition_generation_v9_after_evidence/README.txt).
This repository includes its frozen manifests and prompt link; the split JSONL
files and screenshots are external assets.

| Split | Records |
| --- | ---: |
| Train | 880 accepted from 882 source instances |
| Validation | 71 |
| Test | 1,082 |

Each example contains a task goal, action, history, and ordered BEFORE/AFTER
images. The target is a four-field response:
`precondition → postcondition → reason → answer`.
The two excluded training rows are identified in the frozen manifest.

## Prompts and integrity

The dataset's `prompt_template.txt` is a relative link to the
[with-condition template](../MobileWorld/src/mobile_world/reflection/prompts/with_condition_generation.txt).
The [without-condition template](../MobileWorld/src/mobile_world/reflection/prompts/without_condition_generation.txt)
is available for controlled ablations.

Manifest `source` and `prompt_source` paths resolve relative to the manifest's
directory (`path_base: manifest_directory`). `original_manifest_sha256` records
the manifest before path metadata was normalized; the example, label, image,
and prompt hashes remain frozen. Reproducing a run that pins the original
manifest requires that original manifest and its matching external inputs.

## Preference data

The tracked [DPO dataset](../training/Rejection_Sampling_DPO/README.md) contains
**559 pairs from 263 training transitions** in the same 882-instance source
pool. It includes a construction manifest and per-candidate audit. Its image
paths resolve relative to `training/Rejection_Sampling_DPO/`; the screenshots
must be supplied under `training/SFT/training_data_64/images/`.

Accepted teacher supervision covers 849 source instances after additional
filtering. That target file is an external training artifact; it is not another
train/validation/test split. Preference coverage differs from split size because
only transitions with eligible negatives produce pairs.

See the [training guide](../training/README.md) for the workflows that consume
these assets. No model weights or screenshot-data download is included here.
