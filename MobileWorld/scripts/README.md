# Training and evaluation tools

Run these scripts from `MobileWorld/`. Shared helpers live in this directory;
the [training guide](../../training/README.md) explains the environments and data
required for each workflow.

## Current condition-generation workflows

| Purpose | Entry point |
| --- | --- |
| BF16 LoRA SFT and validation-based checkpoint selection | [qreflector_sft_v9.py](qreflector_sft_v9.py) |
| Four-field teacher supervision and candidate preference pairs | [qreflector_v9_distill_dpo.py](qreflector_v9_distill_dpo.py) |
| Student-response correction | [Round 1](qreflector_sol_round1.py), [round 2](qreflector_sol_round2.py) |
| Local-model offline comparison | [run_v9_local_baselines.py](run_v9_local_baselines.py) |
| GUI-Reflection native-prompt evaluation | [eval_gui_reflection_native_androidworld.py](eval_gui_reflection_native_androidworld.py) |
| Image-resolution comparison | [Validation](eval_qreflector_resolution.py), [test](eval_qreflector_test_resolution.py) |

The frozen dataset lives at `../datasets/qreflector/`.
See the [dataset guide](../../datasets/README.md) for the included split files, sidecars, and screenshots
and the [prompt index](../src/mobile_world/reflection/prompts/README.md) for the
with-condition and without-condition templates.

## Supporting tools

The directory also contains annotation preparation/review, teacher-target
validation, result summarization, and shared image/model helpers. Earlier
v6/v8 and OPSD implementations remain because the current workflows import
some of their helpers and because they define distinct experiments.
Use the matching historical inputs when reproducing those methods.

See [correction distillation](../../training/docs/correction-distillation.md)
and [OPSD](../../training/docs/opsd.md) for method-specific details. Training and
evaluation commands require the relevant GPU or API resources; their saved
paths and device defaults describe the original experiments and must be
configured for your environment.
