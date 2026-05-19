# Text-to-Image Command Recipes

Use this for concrete mflux CLI and Python examples.

## Contents
- Quick Start
  - CLI (fastest path — using pre-saved 8-bit model)
  - Python API
  - 2. Text-to-Image: FLUX.2 Klein
  - 3. Text-to-Image: Qwen-Image
  - 4. Image Editing: FLUX.2 Klein
  - 5. Image Editing: Qwen-Image-Edit
  - 6. Image-to-Image (Style Transfer)
  - 7. Batch Generation

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

### 2. Text-to-Image: FLUX.2 Klein

#### CLI

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
- FLUX does NOT support `--negative-prompt`

#### Python

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

### 3. Text-to-Image: Qwen-Image

Qwen-Image excels at **text rendering in images** (English, Chinese, and other scripts), **complex prompt understanding**, and **multilingual generation**. It supports negative prompts and multiple aspect ratios.

#### CLI

```bash
# Using the shorthand model name (downloads ~58 GB on first run)
mflux-generate-qwen \
  --model qwen \
  --prompt "A coffee shop entrance with a neon sign reading 'Qwen Coffee'" \
  --steps 30 \
  --width 1328 --height 1328 \
  --seed 42 \
  --output coffee_shop.png

# With on-the-fly quantization (reduces memory)
mflux-generate-qwen \
  --model qwen \
  -q 4 \
  --prompt "A poster with elegant typography reading 'Hello World'" \
  --steps 30 \
  --width 1664 --height 928 \
  --seed 42 \
  --output poster.png

# Using pre-quantized MLX model from HuggingFace (faster first load)
mflux-generate-qwen \
  --model mlx-community/Qwen-Image-2512-4bit \
  --prompt "A vintage travel poster for Tokyo with Japanese text" \
  --steps 20 \
  --width 928 --height 1664 \
  --seed 42 \
  --output tokyo_poster.png

# With negative prompt (Qwen supports this, FLUX does not)
mflux-generate-qwen \
  --model qwen \
  -q 8 \
  --prompt "A photorealistic portrait, natural lighting, detailed skin texture" \
  --negative-prompt "blurry, low quality, cartoon, anime" \
  --steps 30 \
  --width 1328 --height 1328 \
  --seed 42 \
  --output portrait.png
```

Key options:
- `--steps 30` — Recommended for Qwen-Image (20-30 for Qwen-Image-2512)
- `--negative-prompt` — Exclude unwanted elements (not available in FLUX)
- `-q 4` or `-q 8` — On-the-fly quantization (4-bit needs ~24 GB, 8-bit needs ~34 GB)
- `--guidance` — Guidance scale (controls prompt adherence)
- `--lora-paths` / `--lora-scales` — Apply LoRA adapters
- `--lora-style` — Built-in style presets: couple, font, home, identity, illustration, portrait, ppt, sandstorm, sparklers, storyboard
- `--low-ram` — Enable low-RAM mode (slower but uses less memory)

#### Qwen-Image Supported Resolutions

- 1:1: 1328x1328
- 16:9: 1664x928
- 9:16: 928x1664
- 4:3: 1472x1140
- 3:4: 1140x1472
- 3:2: 1584x1056
- 2:3: 1056x1584

#### Python

```python
from mflux.models.common.config import ModelConfig
from mflux.models.qwen.variants.txt2img.qwen_image import QwenImage

model = QwenImage(quantize=8, model_config=ModelConfig.qwen_image())

image = model.generate_image(
    seed=42,
    prompt="A coffee shop entrance with a neon sign reading 'Qwen Coffee'",
    num_inference_steps=30,
    width=1328,
    height=1328,
)
image.save("coffee_shop.png")
```

### 4. Image Editing: FLUX.2 Klein

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

### 5. Image Editing: Qwen-Image-Edit

Qwen-Image-Edit uses `Qwen/Qwen-Image-Edit-2509` for natural language image editing. Supports LoRA adapters and guidance control.

#### CLI

```bash
# Basic editing
mflux-generate-qwen-edit \
  --image-paths input.jpg \
  --prompt "Change the sky to a dramatic sunset" \
  --steps 20 \
  --guidance 2.5 \
  --width 1024 --height 1024 \
  --seed 42 \
  --output edited.png

# Multi-image editing (combine elements)
mflux-generate-qwen-edit \
  --image-paths background.jpg object.png \
  --prompt "Place the object naturally in the scene" \
  --steps 20 \
  --seed 42 \
  --output composed.png

# With on-the-fly quantization
mflux-generate-qwen-edit \
  --image-paths photo.jpg \
  -q 4 \
  --prompt "Make it look like a watercolor painting" \
  --steps 20 \
  --seed 42 \
  --output watercolor.png

# With LoRA style preset
mflux-generate-qwen-edit \
  --image-paths photo.jpg \
  --lora-style illustration \
  --prompt "Convert to illustration style" \
  --steps 20 \
  --seed 42 \
  --output illustration.png
```

Key options:
- `--image-paths` — One or more input images (required)
- `--steps 20` — Recommended 8-30 steps
- `--guidance 2.5` — Guidance scale (controls edit strength)
- `--lora-style` — Built-in style presets
- `--lora-paths` / `--lora-scales` — Custom LoRA adapters
- `-q 4` or `-q 8` — On-the-fly quantization
- `--negative-prompt` — Exclude unwanted elements

#### Python

```python
from mflux.models.common.config import ModelConfig
from mflux.models.qwen.variants.edit.qwen_image_edit import QwenImageEdit

model = QwenImageEdit(model_config=ModelConfig.qwen_image_edit())

image = model.generate_image(
    seed=42,
    prompt="Change the sky to a dramatic sunset",
    image_paths=["input.jpg"],
    num_inference_steps=20,
)
image.save("edited.png")
```

### 6. Image-to-Image (Style Transfer)

Transform an existing image with a text prompt:

```bash
# FLUX Klein (fast)
mflux-generate-flux2 \
  --model flux2-klein-4b \
  --image-path input.jpg \
  --image-strength 0.7 \
  --prompt "Make it look like a watercolor painting" \
  --steps 4 \
  --seed 42 \
  --output styled.png

# Qwen-Image (higher quality)
mflux-generate-qwen \
  --model qwen \
  -q 8 \
  --image-path input.jpg \
  --image-strength 0.7 \
  --prompt "Make it look like a watercolor painting" \
  --steps 30 \
  --seed 42 \
  --output styled.png
```

- `--image-strength` — How much to change the image (0.0 = no change, 1.0 = full generation)

### 7. Batch Generation

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

Or via CLI with multiple seeds:

```bash
# Generate 5 images with seeds 0-4
mflux-generate-flux2 \
  --model flux2-klein-4b \
  --prompt "A cozy reading nook with warm lighting" \
  --steps 4 \
  --auto-seeds 5 \
  --output output/reading_nook.png

# Qwen-Image batch
mflux-generate-qwen \
  --model qwen \
  -q 8 \
  --prompt "A detailed botanical illustration" \
  --steps 30 \
  --auto-seeds 5 \
  --output output/botanical.png
```
