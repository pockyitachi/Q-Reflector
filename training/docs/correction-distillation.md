# Student-response correction distillation

These workflows generate student responses on training inputs, ask a teacher
to correct them, and train the student on eligible corrections. They use
assistant-only cross entropy on teacher text. They are separate from
[token-distribution OPSD](opsd.md), which requires a same-vocabulary teacher.

## Data flow

1. The student receives the task, action, available history, and ordered
   BEFORE/AFTER screenshots, and samples a response.
2. The teacher receives that input, the student draft, and the training reference
   annotation. It returns a corrected response, a usability flag, and a review note.
3. The validator excludes malformed, incomplete, overlong, flagged, or
   label-disagreeing targets. Labels are preserved; disagreements are quarantined.
4. The student learns from the corrected response under its original input.
   Teacher instructions, reference annotations, drafts, and review notes are
   not added to the student prompt or target.

Validation and test examples are excluded from teacher correction and training.
Agreement with a training label is an eligibility check, not held-out accuracy
or proof that every explanation is semantically correct.

## Teacher configuration

The public workflows use `teacher-a` and `teacher-b` as role labels. Supply
actual API model IDs before preparing a run:

```bash
export QREFLECTOR_TEACHER_MODEL='your-teacher-model-id'
export QREFLECTOR_CORRECTION_MODEL='your-correction-model-id'
```

The first role is used for annotation, legacy correction, and distillation;
the second is used for the later correction rounds. The paired pilot uses
both and requires distinct models. Run plans record the configured model IDs,
and requests resolve role labels before calling the API. These configurable
roles do not specify the identity of a historical experiment's teacher; use
that experiment's original run metadata when reproducing it.

Token usage is always reported. Cost estimates are optional: set
`QREFLECTOR_TEACHER_PRICES_JSON` to a JSON object keyed by role, with each
role's `input`, `cached_input`, `cache_write`, and `output` prices in USD per
million tokens. Prepared runs snapshot these rates. Without supplied rates,
cost estimates are `null`.

## Historical v6 correction

Implementation: [qreflector_teacher_correction.py](../../MobileWorld/scripts/qreflector_teacher_correction.py).
This workflow requires the original external v6 inputs.

| Setting | Value |
| --- | --- |
| Initial student | BF16 LoRA SFT epoch 6 |
| Training inputs | 882 examples, one seeded pass, accumulation 8 |
| Teacher | `teacher-a`, medium reasoning, 2,048 output tokens including reasoning |
| Student sampling | Temperature 1, top-p 1, top-k 0, maximum 512 tokens |
| Image maximum side | 512 pixels |
| Accepted target limit | 1,024 tokens, no truncation; 8,192-token total context |
| Optimizer | AdamW, LR 5e-6, 10% warmup, cosine decay |
| Evaluation | Predetermined final checkpoint on 1,082 test rows; greedy Yes/No scoring |

Gradients are averaged over accepted examples, including partial batches.
Empty batches do not update the optimizer. An independent eight-example smoke
run precedes the full run; both initialize from the original checkpoint.
Resume checkpoints retain optimizer and RNG state. Teacher requests are cached
by complete request hash, with up to three transient retries and a 1,100-request
cap. The CLI exposes `prepare`, `audit`, and `train` stages.

## Teacher comparison on v9

Implementation: [qreflector_teacher_pilot_v9.py](../../MobileWorld/scripts/qreflector_teacher_pilot_v9.py).
This comparison produces candidate targets and audit reports without updating
student weights.

| Setting | Value |
| --- | --- |
| Student | Qwen3-VL-8B BF16 + v9 LoRA, LR 2e-4 SFT epoch 9 (step 990) |
| Sample | 100 distinct training rows; seed 20261008; 58 Yes / 42 No |
| Teachers | `teacher-a` and `teacher-b` |
| Teacher settings | Medium reasoning, 4,096 output tokens, strict JSON |
| Student sampling | Temperature 1, top-p 1, top-k 0, maximum 1,024 tokens |
| Image maximum side | 512 pixels |

Both teachers receive the same drafts and references; only the teacher model
changes. The stages are `prepare`, `student`, `teachers`, and `report`. The
[summarizer](../../MobileWorld/scripts/summarize_qreflector_teacher_pilot.py)
recomputes request hashes and usage, including cache writes. Teacher agreement,
format compliance, flags, and usage can be compared; downstream gains require
student training and held-out evaluation.

## V9 correction rounds

Round 1 uses [CPU stages](../../MobileWorld/scripts/qreflector_correction_round1.py) and
[GPU stages](../../MobileWorld/scripts/qreflector_correction_round1_gpu.py):

| Setting | Value |
| --- | --- |
| Initial student | The same v9 epoch-9 / step-990 adapter |
| Inputs | 880 accepted training rows; 100 matching pilot drafts reused, 780 generated |
| Student sampling | Temperature 1, top-p 1, top-k 0, maximum 1,024 tokens |
| Teacher | `teacher-b`, medium reasoning, 4,096 output tokens, four workers |
| Teacher geometry | Original/resized image dimensions and action coordinates |
| Filtering | Four-field JSON, all three reason markers, usable flag, label agreement; disputed `train-90` excluded |
| Acceptance gate | At least 75% of 880 corrections |
| Student update | One epoch; assistant-only cross entropy; no auxiliary original-target SFT |
| Optimizer | Fresh AdamW, LR 5e-6, cosine schedule, 10% warmup, batch 1, accumulation 8, clipping 1 |
| Trainable parameters | 43,646,976 LoRA parameters; BF16 base frozen |
| Evaluation | Predetermined final checkpoint; 1,082 test rows; greedy, 1,024-token limit |

Round 1 did not use validation for checkpoint selection. Geometry is provided
to its teacher, while the student retains its original input. Invalid final
answers count as incorrect. Reports include accuracy, success/failure
recognition, invalid outputs, paired errors, and teacher usage.

[Round 2](../../MobileWorld/scripts/qreflector_correction_round2.py) generates new drafts
from the updated student and uses the
[geometry-aware input builder](../../MobileWorld/scripts/qreflector_geometry_prompt.py).
A correction round is a generate/correct/update cycle, not necessarily one epoch.
Cached corrections from older drafts cannot replace corrections of changed
student outputs.

## Artifacts

Record source/data/prompt hashes and model settings in a run manifest. Keep
student rollouts, raw teacher responses, eligible and quarantined targets,
optimizer recovery checkpoints, predictions, and usage summaries together.
These generated assets are external to Git. Configure device, memory limits,
model paths, and matching environment explicitly for a new deployment.
