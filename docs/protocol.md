# Verifier protocol

Q-Reflector evaluates a single executed GUI action. A `Yes` means the action
achieved its intended local effect and made valid progress toward the task;
it does not imply that the full task is complete.

## Inputs

| Input | Current online interface (`v9_geometry`) |
| --- | --- |
| Task | The user's overall goal |
| Action | Action type, arguments, and description |
| History | Up to three preceding actions; prior verdicts and explanations are excluded |
| Images | BEFORE followed by AFTER, resized with a maximum side of 1,024 pixels |
| Geometry | Original/resized image dimensions and normalized action coordinates |

The interface does not require a separate subgoal or textual screen descriptions.
See [prompt construction](../MobileWorld/src/mobile_world/reflection/protocol.py).

## Output

The response contains four ordered fields:

```json
{
  "precondition": "Relevant starting state and prerequisites.",
  "postcondition": "Expected local effect of the current action.",
  "reason": "Precondition check: ... Postcondition check: ... Task progress: ...",
  "answer": "Yes"
}
```

`answer` must be an explicit, unambiguous `Yes` or `No`. The runtime parser can
recover a verdict from some malformed responses, but ambiguous or missing
verdicts are recorded as unknown. Strict training-target validation additionally
checks the four fields and the three reason markers.

The prompt instructs the model to derive expectations from the task, action,
history, and BEFORE image, then compare those expectations with AFTER. Both
images are provided in a single call, so their availability is not causally
separated during condition generation.

## Host feedback

On `No`, the host receives an evidence-based hint derived from the outcome and
task-progress portions of `reason`. Generated conditions remain in the
reflection record; they are not separately inserted into the next host prompt.
`Yes` and unknown verdicts do not generate a failure hint. The default consecutive
failure threshold is zero, which disables reflection-triggered early stopping.
See [feedback formatting](../MobileWorld/src/mobile_world/reflection/format.py)
and the [evaluation guide](evaluation.md).

## Prompts and comparisons

- [With condition generation](../MobileWorld/src/mobile_world/reflection/prompts/with_condition_generation.txt): four-field output.
- [Without condition generation](../MobileWorld/src/mobile_world/reflection/prompts/without_condition_generation.txt): `reason` and `answer` output.

The current online protocol loads the with-condition template and checks its
frozen SHA-256. The ablation template is provided for controlled comparisons;
it is not a separately registered online protocol. Its
[metadata](../MobileWorld/src/mobile_world/reflection/prompts/without_condition_generation.metadata.json)
records the controls needed for comparison.

The `legacy_shared` protocol preserves the original two-field interface, with
512-pixel images and no action history. It should be paired with the original
model and data rather than substituted into a current checkpoint evaluation.
