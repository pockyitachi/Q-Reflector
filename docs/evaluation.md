# Online evaluation

The included MobileWorld runner executes an actor, captures each transition,
asks the configured reflector for a verdict, and provides failure feedback to
the actor's next step. The current host integrations include MAI-UI and GUI-Owl.

## Install and provision

From the repository root, with Python 3.12 and uv available:

```bash
cd MobileWorld
uv sync --extra dev
uv run mobile-world eval --help
```

Follow the included [MobileWorld setup guide](../MobileWorld/README.md) to
configure the emulator, application backends, and actor endpoint. Its upstream
clone command is unnecessary when using this checkout. Emulator evaluation
requires the documented Linux/Docker/KVM environment; installing the Python
package alone does not provision Android or model weights.

Initialize the pinned application sources only if your environment build needs
them, running from the repository root:

```bash
git submodule update --init --recursive
```

## Reflection modes

| Mode | Backend | Protocol |
| --- | --- | --- |
| `none` | Actor without reflection | No verifier |
| `qreflector_v9_retry` | Local BF16 Qwen3-VL with a condition-generation LoRA adapter | `v9_geometry` |
| `gpt_retry` | OpenAI-compatible vision-language endpoint | `v9_geometry` or `legacy_shared` |
| `anthropic_retry` | Anthropic endpoint | `v9_geometry` or `legacy_shared` |
| `gui_reflection_retry` | Local GUI-Reflection | Shared protocol, or its native prompt under `legacy_shared` |
| `qverifier_retry` / `qverifier_early_stop` | Original 4-bit Q-Verifier | `legacy_shared` |

Select `--reflection-protocol v9_geometry` explicitly for the current
condition-generation interface. It uses three prior actions, 1,024-pixel
images, a 1,024-token response limit, and evidence-based feedback.

## Example: an OpenAI-compatible reflector

After provisioning an actor endpoint and a running MobileWorld environment,
set these environment variables for your deployment:

```bash
export ACTOR_MODEL="your-served-actor-model"
export ACTOR_BASE_URL="http://localhost:8000/v1"
export REFLECTOR_MODEL="your-served-vision-language-model"
export REFLECTOR_BASE_URL="http://localhost:8001/v1"
export MW_HOST="http://localhost:6800"
export MW_TASK="your-mobileworld-task-id"
```

The actor reads `API_KEY`; the reflector reads `OPENAI_API_KEY`. Set these for
your endpoints without committing credentials. Run one configured task from
`MobileWorld/`:

```bash
uv run mobile-world eval \
  --agent-type mai_ui_agent \
  --model-name "$ACTOR_MODEL" \
  --llm-base-url "$ACTOR_BASE_URL" \
  --aw-host "$MW_HOST" \
  --task "$MW_TASK" \
  --max-step 50 \
  --max-concurrency 1 \
  --auto-retry 0 \
  --reflection-mode gpt_retry \
  --reflection-protocol v9_geometry \
  --reflection-gpt-model "$REFLECTOR_MODEL" \
  --reflection-gpt-base-url "$REFLECTOR_BASE_URL" \
  --reflection-max-consecutive-failures 0 \
  --log-file-root ./traj_logs/reflector-example
```

`gpt_retry` is the compatibility backend name; the endpoint determines the
actual model. It must accept images and the generated-condition prompt.
The command above uses one attempt per task. Use identical task lists, actor
settings, and retry policies when comparing reflection backends.

## Local Q-Reflector

The local backend requires the trained adapter, BF16 base, matching processor,
generation configuration, and isolated inference environment. They are external
assets, and the CLI retains the selected experiment's default paths. See
[`QReflectorV9`](../MobileWorld/src/mobile_world/reflection/qreflector_v9.py)
for those paths and constructor overrides.

With those assets provisioned, replace the reflection options above with:

```bash
--reflection-mode qreflector_v9_retry \
--reflection-protocol v9_geometry \
--reflection-qverifier-path /absolute/path/to/adapter \
--reflection-qreflector-python /absolute/path/to/environment/bin/python \
--reflection-qreflector-gpu-uuid GPU-your-device-uuid
```

The GPU UUID must identify an available physical device. Specifying an adapter
alone does not replace the base model, processor, or generation configuration.

## Outputs and comparison

Keep each run's configuration, model/prompt hashes, trajectories, verdicts,
token usage, and summary together. An unknown verdict is not a `Yes` and does
not inject a failure hint. Reflection-triggered early stopping is disabled when
`--reflection-max-consecutive-failures 0` is used.

The [protocol guide](protocol.md) defines feedback behavior. Offline evaluation
and checkpoint selection belong to the corresponding [training workflow](../training/README.md).
