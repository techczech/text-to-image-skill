# Text-to-Image Setup Guide

## Overview

Local image generation on Apple Silicon using:
- **mflux** — MLX-native inference framework for diffusion models
- **FLUX.2 Klein** — Fast 4-step image generation (4B/9B params, from Black Forest Labs)
- **Qwen-Image** — High-quality image generation with excellent text rendering (20B params, from Alibaba/Qwen)
- **Qwen-Image-Edit** — Natural language image editing (from Alibaba/Qwen)

## System Requirements

- **Hardware:** Apple Silicon (M1/M2/M3/M4)
- **macOS:** 15.0+ (Sequoia or later)
- **Python:** 3.10+ (3.11 or 3.12 recommended)
- **RAM:** 16 GB minimum (Klein 4B), 32 GB+ for Qwen-Image
- **Disk:** ~5-35 GB per model depending on quantization
- **Not supported:** Intel Macs, Linux, Windows (mflux is MLX-only)

## Step-by-Step Setup

### Step 1: Create project directory

```bash
mkdir -p ~/gitrepos/x-experiments/image-gen
cd ~/gitrepos/x-experiments/image-gen
```

### Step 2: Create Python venv

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### Step 3: Install mflux

```bash
pip install mflux
```

Verify installation:

```bash
mflux-generate-flux2 --help
mflux-generate-qwen --help
mflux-generate-qwen-edit --help
```

You need **mflux v0.16.0+** for FLUX.2 Klein and Qwen-Image support.

### Step 4: Set HuggingFace cache (shared with other skills)

Add to `~/.zshrc` if not already set:

```bash
export HF_HUB_CACHE=~/local-models
```

This shares the model cache with text-to-speech, speech-to-text, and other skills.

### Step 5: Save a quantized model locally (already done)

A pre-quantized 8-bit Klein 4B model is saved at `~/local-models/flux2-klein-4b-8bit` (~8 GB).

To re-create or save other models:

```bash
mflux-save \
  --path ~/local-models/flux2-klein-4b-8bit \
  --model flux2-klein-4b \
  --quantize 8
```

### Step 6: Test generation

```bash
source venv/bin/activate

# FLUX Klein — Using pre-saved local model (fastest — ~7s at 512x512, ~18s at 1024x1024)
mflux-generate-flux2 \
  --model ~/local-models/flux2-klein-4b-8bit \
  --base-model flux2-klein-4b \
  --prompt "A simple red circle on a white background" \
  --steps 4 \
  --width 512 --height 512 \
  --seed 42 \
  --output test_output.png

# Qwen-Image — On-the-fly quantization (first run downloads ~58 GB)
mflux-generate-qwen \
  --model qwen \
  -q 4 \
  --prompt "A poster with the text 'Hello World' in elegant typography" \
  --steps 30 \
  --width 1328 --height 1328 \
  --seed 42 \
  --output test_qwen.png

# Qwen-Image-Edit — Edit an existing image
mflux-generate-qwen-edit \
  --image-paths test_qwen.png \
  --prompt "Add a golden frame around the poster" \
  --steps 20 \
  --seed 42 \
  --output test_qwen_edited.png
```

## Available Models

### FLUX.2 Klein (via mflux)

| Model | CLI Flag | Params | Steps | License | Memory (8-bit) |
|-------|----------|--------|-------|---------|----------------|
| FLUX.2 Klein 4B | `flux2-klein-4b` | 4B | 4 | Apache 2.0 | ~8.5 GB |
| FLUX.2 Klein 9B | `flux2-klein-9b` | 9B | 4 | Non-Commercial | ~18 GB |
| FLUX.2 Klein Base 4B | `flux2-klein-base-4b` | 4B | ~50 | Apache 2.0 | ~8.5 GB |
| FLUX.2 Klein Base 9B | `flux2-klein-base-9b` | 9B | ~50 | Non-Commercial | ~18 GB |

### Qwen-Image (via mflux)

| Model | CLI Flag / HF ID | Params | Steps | License | Memory (8-bit) |
|-------|-------------------|--------|-------|---------|----------------|
| Qwen-Image | `qwen` or `Qwen/Qwen-Image` | 20B | 30 | Apache 2.0 | ~34 GB |
| Qwen-Image-2512 | `Qwen/Qwen-Image-2512` | 20B | 20-30 | Apache 2.0 | ~34 GB |
| Qwen-Image-Edit | `Qwen/Qwen-Image-Edit-2509` | 20B | 8-30 | Apache 2.0 | ~34 GB |

### Pre-quantized MLX Models on HuggingFace

**FLUX Klein:**

| Repo | Base | Quant | Size |
|------|------|-------|------|
| `themindstudio/flux2-klein-4b-mlx-4bit` | Klein 4B | 4-bit | ~4.6 GB |
| `AITRADER/FLUX2-klein-4B-mlx-8bit` | Klein 4B | 8-bit | ~8.5 GB |

**Qwen-Image-2512:**

| Repo | Quant | Size |
|------|-------|------|
| `mlx-community/Qwen-Image-2512-3bit` | 3-bit | ~22 GB |
| `mlx-community/Qwen-Image-2512-4bit` | 4-bit | ~24 GB |
| `mlx-community/Qwen-Image-2512-5bit` | 5-bit | ~27 GB |
| `mlx-community/Qwen-Image-2512-6bit` | 6-bit | ~29 GB |
| `mlx-community/Qwen-Image-2512-8bit` | 8-bit | ~34 GB |

## CLI Reference

```bash
# === FLUX Klein ===

# Basic generation using pre-saved local model (fastest)
mflux-generate-flux2 --model ~/local-models/flux2-klein-4b-8bit --base-model flux2-klein-4b --prompt "..." --steps 4 --seed 42

# Basic generation (downloads on-the-fly, cached after first run)
mflux-generate-flux2 --model flux2-klein-4b --prompt "..." --steps 4 --seed 42

# Higher quality (Klein 9B)
mflux-generate-flux2 --model flux2-klein-9b --prompt "..." --steps 4 --seed 42

# With on-the-fly quantization (reduce memory)
mflux-generate-flux2 --model flux2-klein-4b -q 4 --prompt "..." --steps 4

# Image editing (multi-reference)
mflux-generate-flux2-edit --model flux2-klein-9b --image-paths a.jpg b.jpg --prompt "..." --steps 4

# Image-to-image
mflux-generate-flux2 --model flux2-klein-4b --image-path input.jpg --image-strength 0.7 --prompt "..." --steps 4

# === Qwen-Image ===

# Basic generation (shorthand)
mflux-generate-qwen --model qwen --prompt "..." --steps 30 --seed 42

# With quantization
mflux-generate-qwen --model qwen -q 4 --prompt "..." --steps 30

# Using pre-quantized model
mflux-generate-qwen --model mlx-community/Qwen-Image-2512-4bit --prompt "..." --steps 20

# With negative prompt
mflux-generate-qwen --model qwen -q 8 --prompt "..." --negative-prompt "blurry, low quality" --steps 30

# With LoRA style
mflux-generate-qwen --model qwen --lora-style illustration --prompt "..." --steps 30

# Low-RAM mode
mflux-generate-qwen --model qwen -q 4 --low-ram --prompt "..." --steps 30

# Batch generation (auto seeds)
mflux-generate-qwen --model qwen -q 8 --prompt "..." --steps 30 --auto-seeds 5

# === Qwen-Image-Edit ===

# Basic editing
mflux-generate-qwen-edit --image-paths input.jpg --prompt "Change the sky to sunset" --steps 20

# With quantization and guidance
mflux-generate-qwen-edit --image-paths input.jpg -q 4 --guidance 2.5 --prompt "..." --steps 20

# Multi-image editing
mflux-generate-qwen-edit --image-paths bg.jpg object.png --prompt "Place object in scene" --steps 20

# With LoRA style
mflux-generate-qwen-edit --image-paths photo.jpg --lora-style portrait --prompt "..." --steps 20
```

## Performance Benchmarks (M4 Max 128 GB, 40 GPU cores)

| Model | Quantization | First Download | Generation (512x512) | Generation (1024x1024) |
|-------|-------------|----------------|---------------------|----------------------|
| Klein 4B | 8-bit (local) | ~15 min | **~4s (~7s total)** | **~14s (~18s total)** |
| Klein 9B | 8-bit | ~20 min | ~10s (est.) | ~30s (est.) |
| Qwen-Image | 8-bit | ~30 min | N/A | ~3 min (est.) |
| Qwen-Image-2512 | 4-bit | ~30 min | N/A | ~1-3 min |

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `ModuleNotFoundError: mflux` | Activate venv: `source ~/gitrepos/x-experiments/image-gen/venv/bin/activate` |
| `mflux-generate-flux2: command not found` | `pip install --upgrade mflux` (v0.16.0+ required) |
| `mflux-generate-qwen: command not found` | `pip install --upgrade mflux` (v0.16.0+ required) |
| Out of memory (FLUX) | Use `-q 4` or switch to Klein 4B |
| Out of memory (Qwen) | Use `-q 4` (~24 GB), `--low-ram`, or fall back to FLUX Klein |
| Slow generation | FLUX: use distilled model (4 steps). Qwen: ~3 min is normal |
| Model download stalls | Check connection; set `HF_HUB_CACHE=~/local-models` |

## Links

- mflux: https://github.com/filipstrand/mflux
- mflux FLUX.2 docs: https://github.com/filipstrand/mflux/blob/main/src/mflux/models/flux2/README.md
- mflux Qwen docs: https://github.com/filipstrand/mflux/blob/main/src/mflux/models/qwen/README.md
- FLUX.2 Klein 4B: https://huggingface.co/black-forest-labs/FLUX.2-klein-4B
- FLUX.2 Klein 9B: https://huggingface.co/black-forest-labs/FLUX.2-klein-9B
- Qwen-Image: https://huggingface.co/Qwen/Qwen-Image
- Qwen-Image-2512: https://huggingface.co/Qwen/Qwen-Image-2512
- Qwen-Image-Edit: https://huggingface.co/Qwen/Qwen-Image-Edit-2509
- Qwen-Image GitHub: https://github.com/QwenLM/Qwen-Image
- mlx-community models: https://huggingface.co/mlx-community
