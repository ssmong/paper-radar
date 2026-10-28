### UniWAM

**Full title:** UniWAM: Unified World-Action Model

**Authors:** Wenxuan Song et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.02054v3](https://arxiv.org/abs/2610.02054v3)

**Architecture:** A Mixture-of-Transformers (MoT) connects three experts through joint attention. The physical reasoner uses Qwen3-VL-2B-Instruct. The world generator uses the Wan2.2-TI2V-5B backbone. The action predictor generates continuous action chunks.

**Key methodology:** Natural-language descriptions of end-effector motion provide physical language supervision, following LAP. Pretraining combines VQA, human egocentric videos, and robot demonstrations, with supervision assigned by data source. Post-training adds noise to future visual latents and starts action flow matching from perturbed action history. These changes target dependence on precise future predictions and the number of inference steps.

**Robot / Tasks:** Simulated manipulation in LIBERO and LIBERO-Plus; 50-task bimanual manipulation in RoboTwin 2.0 Clean2Clean (C2C) and Clean2Random (C2R). C2R uses clean training data and domain randomization for evaluation. Real-robot hardware and task-level results are unavailable in the source excerpt.

**Main contributions:**

- Connects semantic understanding, future visual prediction, and action generation in one model.
- Combines supervision from three data sources with physical language and two post-training changes.
- Reports strong OOD manipulation results. The decoder structure is similar to Motus; the separate effects of the changes remain uncertain.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| LIBERO | Average success rate | 99.2% | Standard suites; Xiaomi-Robotics-0: 98.7% |
| LIBERO-Plus | Overall success rate | 92.6% | Highest reported value among the listed methods |
| RoboTwin 2.0 C2R | Mean task success rate | 68.32% | 50 tasks; GigaBrain-0.7: 67.90%; full pretraining budgets are not confirmed to match |
| RoboTwin 2.0 C2C | Mean task success rate | 75.14% | 50 tasks; OpenWAM-α: 89.4%; full pretraining budgets are not confirmed to match |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Joint learning of semantics and dynamics with human data addresses robot generalization and data scale. Transfer to complex real tasks remains uncertain. |
| Delta contribution | 7.0 | Three-source supervision and post-training changes extend a structure similar to Motus and physical language from LAP. Their separate effects remain uncertain. |
| Method quality | 8.0 | Joint attention, future-frame noise, and action-history initialization address the stated problem. The text and figure caption disagree on human-data supervision of the action predictor. |
| Effectiveness | 7.7 | LIBERO-Plus and C2R results support robustness to distribution shifts. C2C trails the best baseline, and real-robot results and inference latency are unavailable. |
| Gap support | 7.0 | OOD success partly supports closing the gap between VLA dynamics grounding and WAM semantic reasoning. Direct measurements of both abilities are limited. |

**Overall score:** 7.5/10.

**Limitations/Gaps:**

- The source excerpt has no quantitative real-robot, long-horizon, or scaling-law results. The abstract makes these claims.
- Human data supervise the VLM and VGM in the text, but the figure caption describes training all three experts.
- RoboTwin 2.0 C2C success is below OpenWAM-α. Full pretraining data and budgets are not confirmed to match across methods.
- Available results do not isolate the effects of physical language, visual generation, or post-training changes. Direct evidence of improved reasoning and dynamics understanding is limited.

**Open weights/code:** — / — (URLs are unavailable in the source excerpt).

## Inference / Deployment

- **Inference latency:** —
- **Deployment hardware:** —

## Dataset / Data Collection

- **Training data:** Robot demonstrations include AgiBot World, Bridge, Droid, Fractal, Robocoin, and Interdata-A1. Human egocentric data come from EgoVerse, EgoDex, and VITRA. VQA data add language supervision. Data processing screens trajectory and visual quality; EgoANT segments and annotates EgoDex subtasks.
- **Evaluation data:** LIBERO, LIBERO-Plus, and the 50-task RoboTwin 2.0 C2C and C2R evaluations.

**Source:** [Paper text](https://arxiv.org/html/2610.02054v3), abstract and sections 1–5.1.
