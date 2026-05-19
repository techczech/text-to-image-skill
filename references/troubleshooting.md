# Text-to-Image Troubleshooting

Use this when generation, model loading, output, or environment checks fail.

## Contents
- Troubleshooting
- Related Skills

## Troubleshooting

- `ModuleNotFoundError: mflux`: activate venv with `source ~/gitrepos/x-experiments/image-gen/venv/bin/activate`.
- `mflux-generate-flux2: command not found`: run `pip install --upgrade mflux`; need v0.16.0+.
- `mflux-generate-qwen: command not found`: run `pip install --upgrade mflux`; need v0.16.0+.
- Out of memory, FLUX: use `-q 4` or Klein 4B instead of 9B.
- Out of memory, Qwen: use `-q 4`, `--low-ram`, or fall back to FLUX Klein 4B.
- Slow generation: FLUX should use distilled 4-step models; Qwen at ~3 min for 30 steps is normal.
- Model download stalls: check internet; try `export HF_HUB_CACHE=~/local-models`.
- `--negative-prompt` ignored: FLUX does not support negative prompts; use Qwen-Image.
- Blurry or soft image: try 8-bit quantization, adjust prompt, or change seed.
- Qwen seeds do not vary much: expected; Qwen seed variation is weaker than FLUX.
- Wrong macOS version: MLX path requires macOS 15.0+.
- Model not found on HuggingFace: check exact model name and `HF_HUB_CACHE`.

## Related Skills

- **text-to-speech** — Generate speech and music locally on Apple Silicon
- **speech-to-text** — Transcribe audio to text locally on Apple Silicon
