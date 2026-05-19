# Text-to-Image Models and Settings

Use this after choosing local generation rather than cloud image APIs.

## Contents
- Workflow
  - 1. Choose a Model
- Quantization Guide
  - FLUX.2 Klein
  - Qwen-Image
- Model Comparison
- Performance Notes
- Output Formats

## Workflow

### 1. Choose a Model

- **FLUX.2 Klein 4B**: params 4B; steps 4; license Apache 2.0; 8-bit memory ~8.5 GB; best for fast generation, commercial use, low RAM.
- **FLUX.2 Klein 9B**: params 9B; steps 4; license Non-Commercial; 8-bit memory ~18 GB; best for higher quality personal use.
- **Qwen-Image**: params 20B; steps 30; license Apache 2.0; 8-bit memory ~34 GB; best for text rendering, multilingual output, quality.
- **Qwen-Image-2512**: params 20B; steps 20-30; license Apache 2.0; 8-bit memory ~34 GB; best for human realism and detail.

**Recommendations:**
- **Low RAM (16-32 GB) or fast drafts:** Use **FLUX.2 Klein 4B** — 4 steps, ~14s, ~8 GB
- **High quality, text in images, multilingual (32 GB+):** Use **Qwen-Image** — 30 steps, ~3 min, ~24-34 GB
- **Best human realism:** Use **Qwen-Image-2512** — similar specs to Qwen-Image

## Quantization Guide

### FLUX.2 Klein

- 3-bit: Klein 4B ~3 GB; Klein 9B ~6 GB; noticeable degradation; avoid.
- 4-bit: Klein 4B ~5 GB; Klein 9B ~10 GB; good balance; use on low-RAM Macs.
- 6-bit: Klein 4B ~6.5 GB; Klein 9B ~13 GB; better quality; good option.
- 8-bit: Klein 4B ~8.5 GB; Klein 9B ~18 GB; near-original quality; use on high-RAM Macs.
- Full bf16: Klein 4B ~15 GB; Klein 9B ~29 GB; original quality; use only when RAM allows.

### Qwen-Image

- 3-bit: ~22 GB; noticeable degradation; avoid.
- 4-bit: ~24 GB; good balance; use on 32-64 GB Macs.
- 5-bit: ~27 GB; better quality; good option.
- 6-bit: ~29 GB; good for editing; avoid lower quantization for edits.
- 8-bit: ~34 GB; near-original quality; use on 128 GB Macs.

Pre-quantized MLX models on HuggingFace (Qwen-Image-2512): `mlx-community/Qwen-Image-2512-{3,4,5,6,8}bit`

On-the-fly quantization:

```bash
# FLUX Klein
mflux-generate-flux2 --model flux2-klein-4b -q 4 --prompt "..." --steps 4
mflux-generate-flux2 --model flux2-klein-4b -q 8 --prompt "..." --steps 4

# Qwen-Image
mflux-generate-qwen --model qwen -q 4 --prompt "..." --steps 30
mflux-generate-qwen --model qwen -q 8 --prompt "..." --steps 30
```

On a 128 GB M4 Max, use **8-bit** for best quality with plenty of headroom.

## Model Comparison

- **FLUX.2 Klein 4B**: 4B params; 4 steps; Apache 2.0; good text rendering; basic multilingual text; no negative prompts; no LoRA; multi-ref editing; img-to-img; max 1024x1024; ~8 GB at 8-bit; ~5 GB at 4-bit; ~14s at 1024 on M4 Max; best for fast drafts and low RAM.
- **FLUX.2 Klein 9B**: 9B params; 4 steps; Non-Commercial; better text rendering; basic multilingual text; no negative prompts; no LoRA; multi-ref editing; img-to-img; max 1024x1024; ~18 GB at 8-bit; ~10 GB at 4-bit; ~30s estimated; best for higher quality personal work.
- **Qwen-Image**: 20B params; 30 steps; Apache 2.0; excellent text rendering; excellent CJK/multilingual text; negative prompts; LoRA; edit model; img-to-img; 1664x928+; ~34 GB at 8-bit; ~24 GB at 4-bit; ~3 min; best for text, multilingual images, quality.
- **Qwen-Image-2512**: 20B params; 20-30 steps; Apache 2.0; excellent text rendering; excellent CJK/multilingual text; negative prompts; LoRA; edit model; img-to-img; 1664x928+; ~34 GB at 8-bit; ~24 GB at 4-bit; ~3 min; best for human realism.

## Performance Notes

Measured generation times on M4 Max 128 GB (40 GPU cores):

- Klein 4B, 8-bit, 512x512: generation ~4s; total with load ~7s.
- Klein 4B, 8-bit, 1024x1024: generation ~14s; total with load ~18s.
- Klein 9B, 8-bit, 1024x1024: generation ~30s estimated; total ~35s estimated.
- Qwen-Image, 8-bit, 1328x1328: generation ~3 min estimated; total ~3.5 min estimated.
- Qwen-Image-2512, 4-bit, 1024x1024: generation ~1-3 min; total ~1-3 min.

> **Note:** Quantization (4-bit vs 8-bit) does not significantly impact generation speed on Apple Silicon — the bottleneck is compute, not memory bandwidth for these model sizes. Use higher quantization for better quality.

Loading from the pre-saved local model at `~/local-models/flux2-klein-4b-8bit` takes ~3s. First-ever download from HuggingFace takes ~15 min for Klein, ~30 min for Qwen-Image.

## Output Formats

- **PNG** — Default, lossless (recommended)
- **JPEG** — Lossy, smaller files
- Images saved via PIL/Pillow: `image.save("output.png")` or `image.save("output.jpg", quality=95)`
