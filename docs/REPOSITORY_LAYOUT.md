# Repository guide

## Source layout

| Path | Contents |
| --- | --- |
| `training/SFT/` | Original supervised training and offline evaluation |
| `training/Teacher_Student_Distill/` | Teacher-response generation and distillation |
| `training/Rejection_Sampling_DPO/` | Candidate sampling, original DPO trainer, and frozen preference data |
| `training/GRPO/` | Original GRPO trainer and the separate current reward definition |
| `training/Data_Corruption/` | Synthetic negative construction |
| `training/Self_Improvement/` | Error-directed teacher correction |
| `training/environment/` | Original training dependency recipe |
| `training/docs/` | Additional training methods |
| `MobileWorld/src/mobile_world/reflection/` | Reflector adapters, prompts, parsing, and feedback |
| `MobileWorld/scripts/` | Condition-generation training, data preparation, and evaluation tools |
| `MobileWorld/tests/` | Data, protocol, and runtime regression checks |
| `MobileWorld/docs/` | Benchmark environment documentation |
| `datasets/` | Frozen split manifests and prompt link |

Run original training commands from their stage directory. Run MobileWorld
scripts from `MobileWorld/`, where they share local helpers. See the
[training guide](../training/README.md) for the corresponding environments.

## External assets

A source checkout includes code, prompts, split manifests, the 559-pair DPO
file, and its audit. Full split rows, screenshots, model weights, generated
responses, and emulator/application state must be provisioned separately.

- The split contract belongs under `datasets/condition_generation_v9_after_evidence/`.
- Its manifest paths use `path_base: manifest_directory`.
- DPO image paths resolve from `training/Rejection_Sampling_DPO/` and point to
  `training/SFT/training_data_64/images/`.
- MobileWorld model and environment assets belong under its ignored `artifacts/`
  directory. Some experiment scripts retain defaults for their original runs;
  use the matching data, processor, adapter, and configuration.

The [dataset guide](../datasets/README.md) documents the frozen hashes. Changing
a prompt or replacing historical inputs creates a different experiment.

## CPU checks

From the repository root, with Python 3.12 and pytest installed:

```bash
python -m pytest -q MobileWorld/tests/test_frozen_dpo_pairs.py
```

This checks the tracked preference data without image downloads. Once the
MobileWorld dependencies are installed, additional CPU checks are:

```bash
cd MobileWorld
uv run pytest -q tests/test_qreflector_v9_distill_dpo.py \
  tests/test_qreflector_reward_v9.py tests/unit/reflection/test_v9_protocol.py
```

The full DPO validator additionally checks the external images:

```bash
# From the repository root, after provisioning the image store.
python training/Rejection_Sampling_DPO/freeze_dpo_pairs.py validate
```

Tests for historical datasets and GUI-Reflection's native prompt require their
external data or vendor source. OPSD multimodal tests use the dedicated
[training environment](../training/docs/opsd.md); the host environment alone does
not supply every training dependency.

## Attribution

The imported MobileWorld base commit and local additions are documented in
[UPSTREAM.md](../MobileWorld/UPSTREAM.md). Upstream licenses, task assets, pinned
app submodules, and the dependency lockfile are retained.
