# MobileWorld provenance

This directory incorporates [Tongyi-MAI/MobileWorld](https://github.com/Tongyi-MAI/MobileWorld)
as the host-agent and evaluation framework for Q-Reflector.

- Imported upstream base: `2c43f6a6160fa37596a717194f2301e93fbed559`.
- License: [Apache-2.0](LICENSE), with upstream source notices retained.
- The directory includes local modifications; it is not an unchanged upstream checkout.

## Local additions

Q-Reflector adds MAI-UI and GUI-Owl reflection feedback, verifier adapters,
condition-generation prompts, image-coordinate metadata, token accounting,
environment recovery, training/evaluation scripts, and regression tests.
The original MobileWorld documentation and benchmark assets remain available.

## Runtime assets

Model weights, screenshot datasets, experiment outputs, Android virtual disks,
credentials, and application database volumes are external to the source tree.
Follow the included [setup documentation](README.md) to provision a new
environment and the [Q-Reflector evaluation guide](../docs/evaluation.md) to
configure reflection.

The three app-source submodules under `resources/` retain their pinned commits.
Their declarations live in the repository-root `.gitmodules`. Initialize them
only if needed for your build, from the repository root:

```bash
git submodule update --init --recursive
```
