# text-to-image

A Claude Code skill that generates and edits images **locally** on Apple Silicon with MLX, using FLUX.2 Klein and Qwen-Image through the `mflux` package. No prompt or image leaves your Mac. It is for anyone who wants fast local drafts (Klein, ~14 s), text-heavy or multilingual images (Qwen-Image), image-to-image or multi-reference edits.

## Requirements

- Apple Silicon Mac (M1 or later). Intel Macs, Linux and Windows are not supported (mflux is MLX-only).
- Python 3.10+ (3.11 or 3.12 recommended) and `mflux` v0.16.0 or later.
- RAM: 16 GB minimum for FLUX.2 Klein 4B; 32 GB or more for Qwen-Image (about 24 GB at 4-bit, 34 GB at 8-bit).
- Disk: about 5 to 35 GB per model depending on quantization.
- A Hugging Face account is not required for the models listed below as far as the skill's notes go; if a download is refused, accept the terms on that model's page and run `hf auth login`.
- Models download on first use into the standard Hugging Face cache (`$HF_HUB_CACHE`, else `$HF_HOME/hub`, else `~/.cache/huggingface/hub`). Set `HF_HOME` to use another volume.

## Install

```bash
git clone https://github.com/techczech/text-to-image-skill ~/.claude/skills/text-to-image
cd ~/.claude/skills/text-to-image
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install mflux
mflux-generate-flux2 --help   # check the install
```

First test:

```bash
mflux-generate-flux2 --model flux2-klein-4b -q 8 \
  --prompt "A simple red circle on a white background" \
  --steps 4 --width 512 --height 512 --seed 42 --output test_output.png
```

Or ask Claude to generate an image. `references/SETUP.md` covers the optional step of saving a pre-quantized copy of a model for faster loading; `references/commands.md` has recipes for generation, editing and batches; `scripts/image_generate.py` is an optional wrapper. Generated images go to `output/` (gitignored); save finished work in your own project, not in the skill folder.

## Models and licences

Licences below are as recorded in this skill's `references/SETUP.md` and `references/models.md`; confirm on the model card before commercial use.

| Model | Source | Licence / terms |
|---|---|---|
| FLUX.2 Klein 4B (and Base 4B) | `black-forest-labs/FLUX.2-klein-4B` | Apache 2.0 |
| FLUX.2 Klein 9B (and Base 9B) | `black-forest-labs/FLUX.2-klein-9B` | **Non-commercial** |
| Qwen-Image | `Qwen/Qwen-Image` | Apache 2.0 |
| Qwen-Image-2512 | `Qwen/Qwen-Image-2512` (pre-quantized: `mlx-community/Qwen-Image-2512-{3,4,5,6,8}bit`) | Apache 2.0 |
| Qwen-Image-Edit | `Qwen/Qwen-Image-Edit-2509` | Apache 2.0 |
| mflux (runtime) | `mflux` on PyPI | See the package page |

## Licence

MIT. See `LICENSE`.
