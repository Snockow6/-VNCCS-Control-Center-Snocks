# VNCCS Control Center (Snocks Edition)

An edited fork of the [VNCCS Control Center](https://github.com/miuproject/ComfyUI_VNCCS) custom node for ComfyUI. Adds VRAM-friendly text encoder quantization options (down to Q2_K for 16GB GPUs) and ships edited copies of the Clothes Designer and Character Creator V2 nodes that work with this control center.

## Requirements

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI_VNCCS](https://github.com/miuproject/ComfyUI_VNCCS) (original package — required for utility functions)
- [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) (for GGUF text encoder and UNet variants)

## Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Snockow6/-VNCCS-Control-Center-Snocks.git
```

## Nodes

| Node | Description |
|------|-------------|
| **VNCCS Control Center Edited** | Model/text encoder/VAE/LoRA selector with auto-download from HuggingFace |
| **VNCCS Clothes Designer** (edited) | Character costume design with Generate Preview support |
| **VNCCS Character Creator V2** (edited) | Character creation and sprite generation |

## Supported Models

### Diffusion Models (UNet)

| Model | Format | Size | Notes |
|-------|--------|------|-------|
| Qwen-Image-Edit-2511-Q2_K | GGUF | ~7.5 GB | Lowest VRAM |
| Qwen-Image-Edit-2511-Q3_K_S | GGUF | ~9.0 GB | Very low VRAM |
| Qwen-Image-Edit-2511-Q3_K_M | GGUF | ~9.7 GB | Low VRAM |
| Qwen-Image-Edit-2511-Q3_K_L | GGUF | ~10.4 GB | Low VRAM |
| Qwen-Image-Edit-2511-Q4_0 | GGUF | — | Balanced |
| Qwen-Image-Edit-2511-Q5_0 | GGUF | — | Higher quality |
| Qwen-Image-Edit-2511-Q8_0 | GGUF | — | Near lossless |
| Qwen-Image-Edit-2511-NVFP4 | safetensors | — | NVIDIA 5xxx only |
| Anima Base v1.0 | safetensors | — | Anima model |

### Text Encoders (CLIP)

| Encoder | Format | Size | Notes |
|---------|--------|------|-------|
| QIE2511 Text Encoder | safetensors | 8.8 GB | FP8 scaled |
| QIE2511 Text Encoder Q2_K | GGUF | 3.02 GB | Aggressive quantization (16GB VRAM) |
| QIE2511 Text Encoder Q4_K_M | GGUF | 4.68 GB | Balanced |
| QIE2511 Text Encoder Q8_0 | GGUF | 8.10 GB | Near lossless |
| Anima Qwen 3 0.6B | safetensors | — | For Anima model |

### VAEs

| VAE | For |
|-----|-----|
| QIE2511 VAE | Qwen Image Edit 2511 |
| Anima VAE | Anima v1.0 |

### Checkpoints (Illustrious)

- ILFlatMix
- Newgrounds Mix v2.0
- WAI Illustrious SDXL v1.70

### LoRAs

- VNCCS Clothes Core, Emotion Core, Pose Studio
- Qwen Image Edit 2511 Lightning (4-step)
- DMD2 SDXL Lightning (4-step)
- Anima Turbo LoRA (12-step)
- Mimimeter (age control)

## VRAM Recommendations

| VRAM | UNet | Text Encoder | Total |
|------|------|-------------|-------|
| 16 GB | Q2_K (~7.5 GB) | Q2_K (3 GB) | ~10.5 GB |
| 16 GB | Q3_K_S (~9 GB) | Q2_K (3 GB) | ~12 GB |
| 24 GB | Q4_0 | Q4_K_M (4.7 GB) | — |
| 24 GB+ | Q8_0 | Q8_0 (8.1 GB) | — |

## Differences from Original

- **Q2_K text encoder** added for low-VRAM setups (3 GB GGUF)
- **Dynamic VNCCS path resolution** — no hardcoded `/opt/ComfyUI` paths
- **Edited Clothes Designer** — JS patched to recognize `VNCCS_ControlCenter_Edited` node class
- **Edited Character Creator V2** — compatible with this control center
- **`/vnccs/control_center/clothes_preview`** endpoint added for Generate Preview

## License

MIT
