# Dataset contracts

The current condition-generation split is
[condition_generation_v9_after_evidence](condition_generation_v9_after_evidence/README.txt).
This repository includes its frozen manifest, prompt link, and source
screenshots. The current four-field split JSONL files and annotation sidecars
are not yet included.

| Split | Records |
| --- | ---: |
| Train | 880 accepted from 882 source instances |
| Validation | 71 |
| Test | 1,082 |

Each example contains a task goal, action, history, and ordered BEFORE/AFTER
images. The target is a four-field response:
`precondition → postcondition → reason → answer`.
The two excluded training rows are identified in the frozen manifest.

## Screenshots

The screenshot store preserves the original image bytes and filenames:

| Source split | Source records | Images | Directory |
| --- | ---: | ---: | --- |
| Training | 882 | 1,764 | `condition_generation_v9_after_evidence/images/train_val/` |
| Validation | 71 | 142 | `condition_generation_v9_after_evidence/images/train_val/` |
| Test | 1,082 | 2,164 | `condition_generation_v9_after_evidence/images/test/` |

All **4,070 images** are included (818,752,750 bytes, about 819 MB). The four
images associated with `train-243` and `train-589` remain in this source store;
their presence does not put those quarantined rows back into the 880-record
training split. No images from other training variants or experiment outputs
are included.

[SCREENSHOT_MANIFEST.json](SCREENSHOT_MANIFEST.json) records every image's
repository-relative path, SHA-256 hash, size, and source split. It is an image
inventory, separate from the frozen dataset's pending `image_sha256.json`.
All 526 images referenced by the frozen DPO manifest match its hashes exactly.

The local source annotations have the older two-field `answer` / `reason`
format and have not been imported as current training data. Full v9 training
and evaluation still require the matching four-field JSONL files, labels,
sidecars, and frozen image manifest.

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
paths resolve relative to `training/Rejection_Sampling_DPO/`.
`training/SFT/training_data_64/images` is a relative symlink to the included
`images/train_val/` store, so the frozen paths work without duplicating images.

Accepted teacher supervision covers 849 source instances after additional
filtering. That target file is an external training artifact; it is not another
train/validation/test split. Preference coverage differs from split size because
only transitions with eligible negatives produce pairs.

See the [training guide](../training/README.md) for the workflows that consume
these assets. Model weights are not included.
