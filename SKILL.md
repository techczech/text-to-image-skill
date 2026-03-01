---
name: text-to-image
description: |
  Generate images from text prompts locally on Apple Silicon via MLX using mflux. Supports FLUX.2 Klein (fast 4-step generation, image editing) and Qwen-Image (high-quality text rendering, multilingual). Creates images and performs image editing without cloud APIs.

  TRIGGERS: Use when:
  - User asks to generate an image from a text prompt
  - User wants text-to-image, image generation, or AI art locally
  - User asks to create an illustration, diagram, or visual from a description
  - User wants to edit an image using natural language instructions
  - User wants image-to-image transformation or style transfer
  - User mentions FLUX Klein, Qwen-Image, mflux, or local image generation
  - User wants to generate images without cloud APIs (no DALL-E, no Midjourney)
  - Companion skill to text-to-speech (TTS)
---

# Text-to-Image Generation (Local Images on Apple Silicon)

Generate images locally on Apple Silicon using mflux (MLX-native). Supported models: FLUX.2 Klein (fast 4-step generation, image editing, Apache 2.0 license) and Qwen-Image (coming soon — excellent text rendering, multilingual). No cloud APIs required.

## Prerequisites

```bash
# Create venv (or reuse existing)
cd ~/gitrepos/x-experiments/image-gen
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install mflux

# Model cache (shared with other skills)
export HF_HUB_CACHE=~/local-models

# Save a pre-quantized model locally (already done for Klein 4B 8-bit)
mflux-save --path ~/local-models/flux2-klein-4b-8bit --model flux2-klein-4b --quantize 8
```

- **Apple Silicon required** (M1/M2/M3/M4), macOS 15.0+
- **Python 3.10+** (3.11 or 3.12 recommended)
- **RAM:** 16 GB minimum (Klein 4B 4-bit), 32 GB+ for Klein 9B or Qwen-Image
- **Disk:** ~8 GB for Klein 4B 8-bit, ~5-35 GB for other models
- **Reference setup:** `~/gitrepos/x-experiments/image-gen/`
- **Pre-saved model:** `~/local-models/flux2-klein-4b-8bit` (8 GB, ready to use)

## Quick Start

### CLI (fastest path — using pre-saved 8-bit model)

```bash
source ~/gitrepos/x-experiments/image-gen/venv/bin/activate

mflux-generate-flux2 \
  --model ~/local-models/flux2-klein-4b-8bit \
  --base-model flux2-klein-4b \
  --prompt "A photorealistic mountain landscape at golden hour" \
  --steps 4 \
  --width 1024 --height 1024 \
  --seed 42 \
  --output output.png
```

Or download on-the-fly (slower first run, auto-cached):

```bash
mflux-generate-flux2 \
  --model flux2-klein-4b \
  --prompt "A photorealistic mountain landscape at golden hour" \
  --steps 4 \
  --width 1024 --height 1024 \
  --seed 42 \
  --output output.png
```

### Python API

```python
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2Klein

model = Flux2Klein(model_config=ModelConfig.flux2_klein_4b())

image = model.generate_image(
    seed=42,
    prompt="A photorealistic mountain landscape at golden hour",
    num_inference_steps=4,
    width=1024,
    height=1024,
)
image.save("output.png")
```

> **Note:** First run downloads the model (~5-15 GB depending on variant). Subsequent runs use the cache at `~/local-models/`.

## Workflow

### 1. Choose a Model

| Model | Params | Steps | License | Memory (8-bit) | Best For |
|-------|--------|-------|---------|----------------|----------|
| **FLUX.2 Klein 4B** | 4B | 4 | Apache 2.0 | ~8.5 GB | Fast generation, commercial use |
| **FLUX.2 Klein 9B** | 9B | 4 | Non-Commercial | ~18 GB | Higher quality, personal use |
| **FLUX.2 Klein Base 4B** | 4B | ~50 | Apache 2.0 | ~8.5 GB | Fine-tuning base |
| **FLUX.2 Klein Base 9B** | 9B | ~50 | Non-Commercial | ~18 GB | Fine-tuning base |
| **Qwen-Image 2.0** | 7B | TBD | TBD | TBD | Text rendering, multilingual *(weights not yet released)* |
| **Qwen-Image-2512** | 20B | 20-30 | Apache 2.0 | ~34 GB | Text rendering *(available now, large)* |

**Recommendation:** Start with **FLUX.2 Klein 4B** — fastest, smallest, commercially licensed.

### 2. Text-to-Image Generation

#### FLUX.2 Klein (CLI)

```bash
mflux-generate-flux2 \
  --model flux2-klein-4b \
  --prompt "A watercolor painting of a Japanese garden in autumn" \
  --steps 4 \
  --width 1024 --height 1024 \
  --seed 42 \
  --output garden.png
```

Key options:
- `--steps 4` — Use 4 for distilled Klein models (default). Use ~50 for base models.
- `--width` / `--height` — Output dimensions (default 1024x1024)
- `--seed` — Reproducible results
- `--guidance 1.0` — Guidance scale (1.0 for distilled models, higher for base)
- `-q 4` or `-q 8` — On-the-fly quantization to reduce memory

#### FLUX.2 Klein (Python)

```python
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2Klein

model = Flux2Klein(model_config=ModelConfig.flux2_klein_4b())

image = model.generate_image(
    seed=42,
    prompt="A watercolor painting of a Japanese garden in autumn",
    num_inference_steps=4,
    width=1024,
    height=1024,
)
image.save("garden.png")
```

#### FLUX.2 Klein 9B (higher quality)

```bash
mflux-generate-flux2 \
  --model flux2-klein-9b \
  --prompt "A detailed architectural blueprint of a modern house" \
  --steps 4 \
  --width 1024 --height 1024 \
  --seed 42 \
  --output blueprint.png
```

#### Using the Pre-saved Local Model

A pre-quantized 8-bit Klein 4B model is saved at `~/local-models/flux2-klein-4b-8bit`. Use `--model` with the local path and `--base-model` to identify the architecture:

```bash
mflux-generate-flux2 \
  --model ~/local-models/flux2-klein-4b-8bit \
  --base-model flux2-klein-4b \
  --prompt "Your prompt here" \
  --steps 4 \
  --seed 42 \
  --output output.png
```

To save additional quantized models:

```bash
# Save 4-bit quantized model (smaller, ~5 GB)
mflux-save --path ~/local-models/flux2-klein-4b-4bit --model flux2-klein-4b --quantize 4

# Save Klein 9B 8-bit (higher quality, ~18 GB)
mflux-save --path ~/local-models/flux2-klein-9b-8bit --model flux2-klein-9b --quantize 8
```

### 3. Image Editing

FLUX.2 Klein supports **multi-reference image editing** — combine multiple source images with a text instruction.

#### CLI

```bash
mflux-generate-flux2-edit \
  --model flux2-klein-9b \
  --image-paths person.jpg sunglasses.jpg \
  --prompt "Put the sunglasses on the person" \
  --steps 4 \
  --seed 42 \
  --output edited.png
```

#### Python

```python
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2KleinEdit

model = Flux2KleinEdit(model_config=ModelConfig.flux2_klein_9b())

image = model.generate_image(
    seed=42,
    prompt="Put the sunglasses on the person",
    image_paths=["person.jpg", "sunglasses.jpg"],
    num_inference_steps=4,
)
image.save("edited.png")
```

### 4. Image-to-Image (Style Transfer)

Transform an existing image with a text prompt:

```bash
mflux-generate-flux2 \
  --model flux2-klein-4b \
  --image-path input.jpg \
  --image-strength 0.7 \
  --prompt "Make it look like a watercolor painting" \
  --steps 4 \
  --seed 42 \
  --output styled.png
```

- `--image-strength` — How much to change the image (0.0 = no change, 1.0 = full generation)

### 5. Batch Generation

Generate multiple images with different seeds:

```python
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2Klein

model = Flux2Klein(model_config=ModelConfig.flux2_klein_4b())

prompt = "A cozy reading nook with warm lighting"

for seed in range(10):
    image = model.generate_image(
        seed=seed,
        prompt=prompt,
        num_inference_steps=4,
        width=1024,
        height=1024,
    )
    image.save(f"output/reading_nook_{seed:03d}.png")
    print(f"Generated seed {seed}")
```

### 6. Qwen-Image (Coming Soon)

> **Status:** Qwen-Image 2.0 (7B) was announced February 2026 but open-source weights have NOT been released yet. Expected Q1 2026. When available, mflux support should follow shortly.

#### Qwen-Image-2512 (Available Now — 20B, larger)

If you need Qwen-Image today (excellent text rendering in images), the 20B model is available:

```bash
mflux-generate-qwen \
  --model mlx-community/Qwen-Image-2512-4bit \
  --prompt "A poster with the text 'Hello World' in elegant typography" \
  --steps 20 \
  --width 1024 --height 1024 \
  --output poster.png
```

```bash
# Image editing with Qwen
mflux-generate-qwen-edit \
  --image-paths input.jpg \
  --prompt "Change the sky to a dramatic sunset" \
  --steps 20 \
  --output edited.png
```

**Caveats:**
- 20B model needs ~24-34 GB depending on quantization
- 20-30 steps required (slower than Klein's 4 steps)
- Images come out softer compared to FLUX
- 6-bit or below can noticeably degrade quality
- Seeds don't vary results as much as FLUX

#### Qwen-Image 2.0 (Pending Weight Release)

When weights are released, expect:
- **7B parameters** (down from 20B) — ~3x faster, ~3x less memory
- **Native 2K resolution** (2048x2048)
- **1,000 token prompts** — detailed descriptions
- Estimated ~8-14 GB quantized, likely **under 30 seconds** on M4 Max

<!-- TODO: Update this section when Qwen-Image 2.0 weights are released -->
<!-- Expected: mflux CLI `mflux-generate-qwen` with new model ID -->
<!-- Expected: MLX-community quantized models on HuggingFace -->

## Quantization Guide

| Quantization | Klein 4B Size | Klein 9B Size | Quality | Recommended |
|-------------|---------------|---------------|---------|-------------|
| 3-bit | ~3 GB | ~6 GB | Noticeable degradation | No |
| **4-bit** | ~5 GB | ~10 GB | Good balance | Yes (low RAM) |
| 6-bit | ~6.5 GB | ~13 GB | Better | Yes |
| **8-bit** | ~8.5 GB | ~18 GB | Near-original | Yes (128 GB Mac) |
| Full (bf16) | ~15 GB | ~29 GB | Original | If RAM allows |

On a 128 GB M4 Max, use **8-bit** for best quality with plenty of headroom.

On-the-fly quantization:

```bash
# 4-bit (smallest)
mflux-generate-flux2 --model flux2-klein-4b -q 4 --prompt "..." --steps 4

# 8-bit (best balance)
mflux-generate-flux2 --model flux2-klein-4b -q 8 --prompt "..." --steps 4
```

## Model Comparison

| Feature | FLUX.2 Klein 4B | FLUX.2 Klein 9B | Qwen-Image-2512 | Qwen-Image 2.0 |
|---------|----------------|----------------|-----------------|----------------|
| Parameters | 4B | 9B | 20B | 7B |
| Steps | 4 | 4 | 20-30 | TBD |
| License | Apache 2.0 | Non-Commercial | Apache 2.0 | TBD |
| Text rendering | Good | Better | Excellent | Excellent |
| Image editing | Yes (multi-ref) | Yes (multi-ref) | Yes | TBD |
| Img-to-img | Yes | Yes | No | TBD |
| Max resolution | 1024x1024 | 1024x1024 | 1024x1024 | 2048x2048 |
| Memory (8-bit) | ~8 GB | ~18 GB | ~34 GB | ~14 GB (est.) |
| Speed (M4 Max, 1024x) | **~14s** | ~30s (est.) | ~1-3 min | TBD |
| Status | Available | Available | Available | Weights pending |

## Performance Notes

Measured generation times on M4 Max 128 GB (40 GPU cores):

| Model | Quantization | Resolution | Generation | Total (incl. load) |
|-------|-------------|------------|------------|-------------------|
| **Klein 4B** | **8-bit** | **512x512** | **~4s** | **~7s** |
| **Klein 4B** | **8-bit** | **1024x1024** | **~14s** | **~18s** |
| Klein 9B | 8-bit | 1024x1024 | ~30s (est.) | ~35s (est.) |
| Qwen-Image-2512 | 4-bit | 1024x1024 | ~1-3 min | ~1-3 min |
| Qwen-Image 2.0 | TBD | 1024x1024 | TBD | TBD |

> **Note:** Quantization (4-bit vs 8-bit) does not significantly impact generation speed on Apple Silicon — the bottleneck is compute, not memory bandwidth for these model sizes. Use higher quantization for better quality.

Loading from the pre-saved local model at `~/local-models/flux2-klein-4b-8bit` takes ~3s. First-ever download from HuggingFace takes ~15 min.

## Output Formats

- **PNG** — Default, lossless (recommended)
- **JPEG** — Lossy, smaller files
- Images saved via PIL/Pillow: `image.save("output.png")` or `image.save("output.jpg", quality=95)`

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `ModuleNotFoundError: mflux` | Activate venv: `source ~/gitrepos/x-experiments/image-gen/venv/bin/activate` |
| `mflux-generate-flux2: command not found` | `pip install --upgrade mflux` (need v0.16.0+) |
| Out of memory | Use `-q 4` for 4-bit quantization, or use Klein 4B instead of 9B |
| Slow generation | Ensure you're using distilled model (4 steps), not base model (50 steps) |
| Model download stalls | Check internet connection; try `export HF_HUB_CACHE=~/local-models` |
| `--negative-prompt` not working | FLUX.2 does NOT support negative prompts. Remove the flag. |
| Image looks blurry/soft | Try higher quantization (8-bit), adjust prompt, or try a different seed |
| Qwen-Image 2.0 not available | Weights not yet released. Use Qwen-Image-2512 or FLUX Klein for now. |
| Wrong macOS version | Requires macOS 15.0+ for MLX support |
| Model not found on HuggingFace | Check exact model name; ensure `HF_HUB_CACHE` is set |

## Related Skills

- **text-to-speech** — Generate speech and music locally on Apple Silicon
- **speech-to-text** — Transcribe audio to text locally on Apple Silicon
