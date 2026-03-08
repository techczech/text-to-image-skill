#!/usr/bin/env python3
"""
Image generation using mflux (MLX-native) on Apple Silicon.

Default: FLUX.2 Klein 4B (fast, 4 steps, ~14s).
Use --qwen for Qwen-Image (quality, text rendering, ~3 min).
Use --klein-9b for higher-quality Klein variant.

Usage:
    # FLUX Klein 4B (default — fast)
    python image_generate.py --prompt "A mountain landscape"

    # FLUX Klein 9B (higher quality, non-commercial)
    python image_generate.py --klein-9b --prompt "A mountain landscape"

    # Qwen-Image (quality, text rendering, multilingual)
    python image_generate.py --qwen --prompt "A poster reading 'Hello World'"
    python image_generate.py --qwen -q 4 --prompt "A poster" --steps 30

    # Qwen-Image with negative prompt
    python image_generate.py --qwen --prompt "A portrait" --negative-prompt "blurry, cartoon"

    # FLUX Klein image editing (multi-reference)
    python image_generate.py --edit --image-paths person.jpg glasses.jpg --prompt "Put glasses on person"

    # Qwen image editing
    python image_generate.py --qwen --edit --image-paths photo.jpg --prompt "Change sky to sunset"

    # Batch generation
    python image_generate.py --batch 5 --prompt "A cozy reading nook"

Requires: pip install mflux (v0.16.0+)
"""

import argparse
import os
import time

# Ensure shared model cache
os.environ.setdefault("HF_HUB_CACHE", os.path.expanduser("~/local-models"))

KLEIN_CONFIGS = {
    "4b": ("flux2-klein-4b", 4),
    "9b": ("flux2-klein-9b", 4),
}


def generate_flux(prompt: str, seed: int = 42, width: int = 1024, height: int = 1024, variant: str = "4b"):
    """Generate a single image using FLUX.2 Klein."""
    from mflux.models.common.config import ModelConfig
    from mflux.models.flux2.variants import Flux2Klein

    config_map = {
        "flux2-klein-4b": ModelConfig.flux2_klein_4b,
        "flux2-klein-9b": ModelConfig.flux2_klein_9b,
    }

    model_id, steps = KLEIN_CONFIGS[variant]
    print(f"Loading model: {model_id}...")
    t0 = time.time()
    gen = Flux2Klein(model_config=config_map[model_id]())
    print(f"Model loaded in {time.time() - t0:.1f}s")

    print(f"Generating image (seed={seed}, {width}x{height}, steps={steps})...")
    t0 = time.time()
    image = gen.generate_image(
        seed=seed,
        prompt=prompt,
        num_inference_steps=steps,
        width=width,
        height=height,
    )
    elapsed = time.time() - t0
    print(f"Generated in {elapsed:.1f}s")

    os.makedirs("output", exist_ok=True)
    output_path = f"output/klein_{variant}_{seed:04d}.png"
    image.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


def generate_qwen(prompt: str, seed: int = 42, width: int = 1328, height: int = 1328, steps: int = 30, quantize: int = 8, negative_prompt: str = ""):
    """Generate a single image using Qwen-Image."""
    from mflux.models.common.config import ModelConfig
    from mflux.models.qwen.variants.txt2img.qwen_image import QwenImage

    print(f"Loading Qwen-Image (quantize={quantize})...")
    t0 = time.time()
    gen = QwenImage(quantize=quantize, model_config=ModelConfig.qwen_image())
    print(f"Model loaded in {time.time() - t0:.1f}s")

    print(f"Generating image (seed={seed}, {width}x{height}, steps={steps})...")
    t0 = time.time()
    image = gen.generate_image(
        seed=seed,
        prompt=prompt,
        num_inference_steps=steps,
        width=width,
        height=height,
    )
    elapsed = time.time() - t0
    print(f"Generated in {elapsed:.1f}s")

    os.makedirs("output", exist_ok=True)
    output_path = f"output/qwen_{seed:04d}.png"
    image.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


def generate_flux_edit(prompt: str, image_paths: list[str], seed: int = 42, variant: str = "9b"):
    """Edit images using FLUX.2 Klein multi-reference editing."""
    from mflux.models.common.config import ModelConfig
    from mflux.models.flux2.variants import Flux2KleinEdit

    config_map = {
        "flux2-klein-4b": ModelConfig.flux2_klein_4b,
        "flux2-klein-9b": ModelConfig.flux2_klein_9b,
    }

    model_id, steps = KLEIN_CONFIGS[variant]
    print(f"Loading FLUX edit model: {model_id}...")
    t0 = time.time()
    gen = Flux2KleinEdit(model_config=config_map[model_id]())
    print(f"Model loaded in {time.time() - t0:.1f}s")

    print(f"Editing with {len(image_paths)} reference image(s)...")
    t0 = time.time()
    image = gen.generate_image(
        seed=seed,
        prompt=prompt,
        image_paths=image_paths,
        num_inference_steps=steps,
    )
    elapsed = time.time() - t0
    print(f"Edited in {elapsed:.1f}s")

    os.makedirs("output", exist_ok=True)
    output_path = f"output/klein_edit_{seed:04d}.png"
    image.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


def generate_qwen_edit(prompt: str, image_paths: list[str], seed: int = 42, steps: int = 20, quantize: int = 8, guidance: float = 2.5):
    """Edit images using Qwen-Image-Edit."""
    from mflux.models.common.config import ModelConfig
    from mflux.models.qwen.variants.edit.qwen_image_edit import QwenImageEdit

    print(f"Loading Qwen-Image-Edit (quantize={quantize})...")
    t0 = time.time()
    gen = QwenImageEdit(quantize=quantize, model_config=ModelConfig.qwen_image_edit())
    print(f"Model loaded in {time.time() - t0:.1f}s")

    print(f"Editing {len(image_paths)} image(s) (steps={steps})...")
    t0 = time.time()
    image = gen.generate_image(
        seed=seed,
        prompt=prompt,
        image_paths=image_paths,
        num_inference_steps=steps,
    )
    elapsed = time.time() - t0
    print(f"Edited in {elapsed:.1f}s")

    os.makedirs("output", exist_ok=True)
    output_path = f"output/qwen_edit_{seed:04d}.png"
    image.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


def generate_batch(prompt: str, count: int = 5, variant: str = "4b"):
    """Generate multiple images with different seeds."""
    from mflux.models.common.config import ModelConfig
    from mflux.models.flux2.variants import Flux2Klein

    config_map = {
        "flux2-klein-4b": ModelConfig.flux2_klein_4b,
        "flux2-klein-9b": ModelConfig.flux2_klein_9b,
    }

    model_id, steps = KLEIN_CONFIGS[variant]
    print(f"Loading model: {model_id}...")
    gen = Flux2Klein(model_config=config_map[model_id]())

    os.makedirs("output", exist_ok=True)
    for seed in range(count):
        print(f"Generating {seed + 1}/{count} (seed={seed})...")
        t0 = time.time()
        image = gen.generate_image(
            seed=seed,
            prompt=prompt,
            num_inference_steps=steps,
            width=1024,
            height=1024,
        )
        elapsed = time.time() - t0
        output_path = f"output/batch_{seed:04d}.png"
        image.save(output_path)
        print(f"  Saved: {output_path} ({elapsed:.1f}s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate images locally on Apple Silicon (FLUX Klein default, Qwen-Image optional)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s --prompt "A mountain landscape"                    # Klein 4B (fast, default)
  %(prog)s --klein-9b --prompt "A mountain landscape"         # Klein 9B (higher quality)
  %(prog)s --qwen --prompt "A poster with text 'Hello'"       # Qwen-Image (best text)
  %(prog)s --qwen -q 4 --prompt "A poster"                   # Qwen 4-bit (less RAM)
  %(prog)s --edit --image-paths a.jpg b.jpg --prompt "..."    # Klein edit
  %(prog)s --qwen --edit --image-paths a.jpg --prompt "..."   # Qwen edit
  %(prog)s --batch 5 --prompt "A cozy nook"                   # 5 variants
""",
    )

    # Engine selection (mutually exclusive flags)
    engine = parser.add_mutually_exclusive_group()
    engine.add_argument("--qwen", action="store_true", help="Use Qwen-Image (20B, best text rendering, ~3 min, needs 32GB+ RAM)")
    engine.add_argument("--klein-9b", action="store_true", help="Use FLUX Klein 9B (higher quality, non-commercial license)")

    # Common options
    parser.add_argument("--prompt", default="A photorealistic mountain landscape at golden hour, dramatic clouds", help="Text prompt")
    parser.add_argument("--negative-prompt", default="", help="Negative prompt (Qwen only)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--width", type=int, help="Image width (default: 1024 FLUX, 1328 Qwen)")
    parser.add_argument("--height", type=int, help="Image height (default: 1024 FLUX, 1328 Qwen)")
    parser.add_argument("--steps", type=int, help="Inference steps (default: 4 FLUX, 30 Qwen, 20 Qwen-Edit)")
    parser.add_argument("-q", "--quantize", type=int, default=8, choices=[3, 4, 5, 6, 8], help="Quantization level (Qwen, default: 8)")
    parser.add_argument("--guidance", type=float, default=2.5, help="Guidance scale (Qwen-Edit)")
    parser.add_argument("--output", "-o", help="Output file path (default: output/<engine>_<seed>.png)")

    # Modes
    parser.add_argument("--edit", action="store_true", help="Image editing mode (requires --image-paths)")
    parser.add_argument("--image-paths", nargs="+", help="Source images for editing")
    parser.add_argument("--batch", type=int, help="Generate N images with different seeds")

    args = parser.parse_args()

    klein_variant = "9b" if args.klein_9b else "4b"

    if args.batch:
        generate_batch(args.prompt, count=args.batch, variant=klein_variant)
    elif args.edit:
        if not args.image_paths:
            parser.error("--edit requires --image-paths")
        if args.qwen:
            s = args.steps or 20
            generate_qwen_edit(args.prompt, args.image_paths, seed=args.seed, steps=s, quantize=args.quantize, guidance=args.guidance)
        else:
            generate_flux_edit(args.prompt, args.image_paths, seed=args.seed, variant=klein_variant)
    elif args.qwen:
        w = args.width or 1328
        h = args.height or 1328
        s = args.steps or 30
        generate_qwen(args.prompt, seed=args.seed, width=w, height=h, steps=s, quantize=args.quantize, negative_prompt=args.negative_prompt)
    else:
        w = args.width or 1024
        h = args.height or 1024
        generate_flux(args.prompt, seed=args.seed, width=w, height=h, variant=klein_variant)
