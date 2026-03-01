#!/usr/bin/env python3
"""
FLUX.2 Klein image generation demo using mflux (MLX-native).

Usage:
    python generate_flux_klein.py
    python generate_flux_klein.py --prompt "Your custom prompt" --seed 42
    python generate_flux_klein.py --edit --image-paths person.jpg glasses.jpg --prompt "Put glasses on person"

Requires: pip install mflux (v0.16.0+)
"""

import argparse
import os
import time

# Ensure shared model cache
os.environ.setdefault("HF_HUB_CACHE", os.path.expanduser("~/local-models"))


def generate_basic(prompt: str, seed: int = 42, width: int = 1024, height: int = 1024, model: str = "flux2-klein-4b"):
    """Generate a single image from a text prompt."""
    from mflux.models.common.config import ModelConfig
    from mflux.models.flux2.variants import Flux2Klein

    config_map = {
        "flux2-klein-4b": ModelConfig.flux2_klein_4b,
        "flux2-klein-9b": ModelConfig.flux2_klein_9b,
    }

    print(f"Loading model: {model}...")
    t0 = time.time()
    gen = Flux2Klein(model_config=config_map[model]())
    print(f"Model loaded in {time.time() - t0:.1f}s")

    print(f"Generating image (seed={seed}, {width}x{height})...")
    t0 = time.time()
    image = gen.generate_image(
        seed=seed,
        prompt=prompt,
        num_inference_steps=4,
        width=width,
        height=height,
    )
    elapsed = time.time() - t0
    print(f"Generated in {elapsed:.1f}s")

    os.makedirs("output", exist_ok=True)
    output_path = f"output/klein_{model.split('-')[-1]}_{seed:04d}.png"
    image.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


def generate_edit(prompt: str, image_paths: list[str], seed: int = 42, model: str = "flux2-klein-9b"):
    """Edit images using multi-reference image editing."""
    from mflux.models.common.config import ModelConfig
    from mflux.models.flux2.variants import Flux2KleinEdit

    config_map = {
        "flux2-klein-4b": ModelConfig.flux2_klein_4b,
        "flux2-klein-9b": ModelConfig.flux2_klein_9b,
    }

    print(f"Loading edit model: {model}...")
    t0 = time.time()
    gen = Flux2KleinEdit(model_config=config_map[model]())
    print(f"Model loaded in {time.time() - t0:.1f}s")

    print(f"Editing with {len(image_paths)} reference image(s)...")
    t0 = time.time()
    image = gen.generate_image(
        seed=seed,
        prompt=prompt,
        image_paths=image_paths,
        num_inference_steps=4,
    )
    elapsed = time.time() - t0
    print(f"Edited in {elapsed:.1f}s")

    os.makedirs("output", exist_ok=True)
    output_path = f"output/klein_edit_{seed:04d}.png"
    image.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


def generate_batch(prompt: str, count: int = 5, model: str = "flux2-klein-4b"):
    """Generate multiple images with different seeds."""
    from mflux.models.common.config import ModelConfig
    from mflux.models.flux2.variants import Flux2Klein

    config_map = {
        "flux2-klein-4b": ModelConfig.flux2_klein_4b,
        "flux2-klein-9b": ModelConfig.flux2_klein_9b,
    }

    print(f"Loading model: {model}...")
    gen = Flux2Klein(model_config=config_map[model]())

    os.makedirs("output", exist_ok=True)
    for seed in range(count):
        print(f"Generating {seed + 1}/{count} (seed={seed})...")
        t0 = time.time()
        image = gen.generate_image(
            seed=seed,
            prompt=prompt,
            num_inference_steps=4,
            width=1024,
            height=1024,
        )
        elapsed = time.time() - t0
        output_path = f"output/klein_batch_{seed:04d}.png"
        image.save(output_path)
        print(f"  Saved: {output_path} ({elapsed:.1f}s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FLUX.2 Klein image generation demo")
    parser.add_argument("--prompt", default="A photorealistic mountain landscape at golden hour, dramatic clouds", help="Text prompt")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--width", type=int, default=1024, help="Image width")
    parser.add_argument("--height", type=int, default=1024, help="Image height")
    parser.add_argument("--model", default="flux2-klein-4b", choices=["flux2-klein-4b", "flux2-klein-9b"], help="Model variant")
    parser.add_argument("--edit", action="store_true", help="Image editing mode")
    parser.add_argument("--image-paths", nargs="+", help="Source images for editing")
    parser.add_argument("--batch", type=int, help="Generate N images with different seeds")
    args = parser.parse_args()

    if args.batch:
        generate_batch(args.prompt, count=args.batch, model=args.model)
    elif args.edit:
        if not args.image_paths:
            parser.error("--edit requires --image-paths")
        generate_edit(args.prompt, args.image_paths, seed=args.seed, model=args.model)
    else:
        generate_basic(args.prompt, seed=args.seed, width=args.width, height=args.height, model=args.model)
