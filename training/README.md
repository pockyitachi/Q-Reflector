# Training workflows

Q-Reflector includes the original StepReflect training stages and subsequent
experiments with generated preconditions and postconditions. Choose the
workflow matching your prompt, data, and checkpoint; these stages are not a
single interchangeable recipe.

## Original pipeline

| Stage | Implementation and guide |
| --- | --- |
| Supervised fine-tuning and offline evaluation | [SFT](SFT/README.md) |
| Teacher-response distillation | [Teacher_Student_Distill](Teacher_Student_Distill/README.md) |
| Candidate sampling and preference optimization | [Rejection_Sampling_DPO](Rejection_Sampling_DPO/README.md) |
| Reward-based refinement | [GRPO](GRPO/README.md) |
| Synthetic negative construction | [Data_Corruption](Data_Corruption/README.md) |
| Error-directed teacher correction | [Self_Improvement](Self_Improvement/README.md) |

Run these scripts from their respective stage directories, for example
`training/SFT/`. Their relative data and model paths refer to sibling stages.
The [original environment recipe](environment/README.md) is separate from the
MobileWorld host environment. Reproducing an original run requires its original
external data, model weights, and configuration.

## Condition-generation workflows

Run the following entry points from `MobileWorld/`:

| Workflow | Entry point |
| --- | --- |
| BF16 LoRA SFT | [qreflector_sft_v9.py](../MobileWorld/scripts/qreflector_sft_v9.py) |
| Teacher supervision and preference-pair construction | [qreflector_v9_distill_dpo.py](../MobileWorld/scripts/qreflector_v9_distill_dpo.py) |
| Student-response correction | [Round 1](../MobileWorld/scripts/qreflector_correction_round1.py), [round 2](../MobileWorld/scripts/qreflector_correction_round2.py) |
| Same-vocabulary teacher/student OPSD | [Method and environment](docs/opsd.md) |

The current target has four ordered fields:
`precondition → postcondition → reason → answer`. The included frozen dataset has
880 training, 71 validation, and 1,082 test examples; the
[dataset guide](../datasets/README.md) explains the split rows, annotation
sidecars, source screenshots, and CPU integrity check.
The [correction-distillation guide](docs/correction-distillation.md) records
teacher inputs, filtering, student loss, and evaluation policies.
Configure external teacher model IDs using its
[teacher configuration](docs/correction-distillation.md#teacher-configuration)
instructions before preparing API-based runs.

## Preference and reward contracts

The frozen [DPO dataset](Rejection_Sampling_DPO/README.md) contains 559 pairs
covering 263 source transitions. Its pair IDs, audit, and hashes are tracked.
The original `train_dpo_simple.py` implements a historical reference-free loss
and intentionally rejects this four-field dataset. A compatible standard DPO
optimizer is not provided by that script.

The current [GRPO reward definition](GRPO/REWARD_V9.txt) and
[reward implementation](GRPO/reward_v9.py) are separate from the original trainer.
Their presence, and the consolidated preference data, do not establish a
completed DPO or GRPO training run with the current protocol.

## Evaluation

Use the dataset, prompt, image processing, and generation settings associated
with each checkpoint. In validation-selected workflows, choose the checkpoint
on validation data before evaluating the test split. Some historical correction
experiments evaluated a predetermined final checkpoint instead; their protocols
are documented separately.

See [online evaluation](../docs/evaluation.md) for host-agent integration and
[CPU checks](../docs/REPOSITORY_LAYOUT.md#cpu-checks) for data and protocol validation.
