---
name: text-to-image
description: "Generate images locally."
---

# Text-to-Image Generation

## First Move

- Choose local MLX generation, then load only the needed reference.

## Use

- Generate or edit images on Apple Silicon.
- Prefer the target project for outputs; do not save new outputs in the skill repo.
- Use FLUX for speed and Qwen for text-heavy or multilingual images.

## References

- `references/workflow.md`: choose which reference to load
- `references/SETUP.md`: install or repair the local mflux environment
- `references/models.md`: choose FLUX/Qwen, quantization, resolution, and performance tradeoffs
- `references/commands.md`: run generation, editing, image-to-image, or batch recipes
- `references/troubleshooting.md`: debug model, memory, or output issues

## Scripts

- `scripts/image_generate.py`: optional wrapper for repeatable FLUX/Qwen generation

## Verification

- Confirm venv, `mflux`, and model cache before long runs.
- Inspect generated images before reporting success.
- Record prompt, seed, model, and output path when results matter.
