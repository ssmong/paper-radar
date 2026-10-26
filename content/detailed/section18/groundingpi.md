### GroundingPI

**Full title:** GroundingPI: A Grounding Foundation Model towards Physical Intelligence with Visual Primitives

**Authors:** Qize Yu et al.

**Venue/Year:** — / 2026

**arXiv:** [2609.39601v1](https://arxiv.org/abs/2609.39601v1)

**Architecture:** A 4B grounding foundation model combines a MoonViT-V2 visual encoder and a Qwen3-4B language decoder. Points and bounding boxes use a shared vocabulary with quantized coordinate tokens.

**Key methodology:** Multimodal and spatial pretraining, supervised fine-tuning (SFT), and GRPO train precise perception. For manipulation, intermediate features condition an Action DiT through layer-wise cross-attention. Backbone comparisons keep the action expert, action data, training budget, action representation, and inference procedure fixed within each benchmark.

**Robot / Tasks:** RoboTwin 2.0 evaluates fixed-base bimanual tabletop manipulation. RoboCasa-GR1 evaluates humanoid dexterous-hand manipulation. nuScenes evaluates open-loop driving trajectory prediction.

**Main contributions:**
- Extends generative coordinate grounding to broad perceptual pretraining and transfer to action learning.
- Ranks first in all four reported OOD manipulation settings across scene and entity changes.
- On RoboCasa-GR1, uses 50% of demonstrations to exceed compared baselines trained with 75%.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| RoboTwin2.0 Full | Task success rate | 66.20% | Matched downstream architecture and training protocol |
| RoboTwin2.0-Clean2Random | Task success rate | 17.60% | Rex-Omni: 14.10%; train on Clean, evaluate on Randomized scenes |
| RoboCasa-GR1 Full | Task success rate | 37.75% | RynnBrain: 39.00%; in-distribution evaluation |
| nuScenes | Average open-loop L2 error | 0.296 m | Trajectory prediction; closed-loop performance is not established |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Precise perception can reduce the burden on scarce action data. Practical effects beyond the reported evaluations remain uncertain. |
| Delta contribution | 7.0 | Broad perceptual pretraining and action transfer extend prior grounding models. Quantized coordinate generation uses an existing approach. |
| Method quality | 8.0 | GRPO targets localization, omissions, and duplicates. Fixed Action DiT comparisons help, but backbone and pretraining differences remain. |
| Effectiveness | 7.0 | Leads all four OOD manipulation settings. Clean2Random success remains low, and driving gains are small. |
| Gap support | 7.3 | Grounding and controlled action transfer support the perception bottleneck claim. Open-loop driving does not establish closed-loop performance. |

**Overall score:** 7.4/10.

**Limitations/Gaps:**
- RoboCasa-GR1 Full success is below RynnBrain, and Clean2Random success remains low.
- nuScenes results do not establish closed-loop performance, latency, or the separate effect of sign reading.
- Different backbone architectures and pretraining prevent full isolation of the contribution from grounding training.
- VisDrone remains difficult; some spatial and GUI benchmarks favor GPT-6 Astra.

**Open weights/code:** — / — (not reported in the paper).

## Inference / Deployment

- **Inference latency:** —
- **Deployment hardware:** —

## Dataset / Data Collection

- **Training data:** Public datasets and a dedicated data engine with multiple teachers and task-specific validation.
- **Evaluation data:** RoboTwin 2.0, RoboCasa-GR1, and nuScenes; 34 grounding benchmarks across 11 perceptual capabilities.

**Source:** [Paper text](https://arxiv.org/html/2609.39601v1), sections 3–5.2.2.
