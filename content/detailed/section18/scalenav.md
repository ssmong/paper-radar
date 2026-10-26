### ScaleNav

**Full title:** ScaleNav: Scalable Internet Video Pretraining for Language-Conditioned Local Navigation

**Authors:** Yihui Yang et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.25690v1](https://arxiv.org/abs/2610.25690v1)

**Architecture:** A unified world-action model follows DreamZero and uses a shared DiT backbone to predict future video and action chunks. An initial-frame anchor and recent observation-action history preserve the visual reference for navigation instructions.

**Key methodology:** Three stages connect Internet video experience to robot actions: instruction-conditioned video pretraining, action alignment with action-labeled simulated data, and joint fine-tuning. Internet videos require no proxy action labels. The model predicts executable action chunks without an external planner at inference.

**Robot / Tasks:** Language-conditioned local navigation to a target visible in the initial observation, followed by stopping at the described location. Evaluation uses single-view Short-Horizon OVON, HabitatGS-LN, and a Unitree Go2 quadruped in three indoor environments.

**Main contributions:**

- Transfers visual navigation dynamics from Internet egocentric videos to executable actions.
- Uses a shared video-action model and staged training to connect action-free videos with simulated action data.
- Evaluates the benefit of video pretraining in simulation and on a real quadruped.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| Single-view Short-Horizon OVON | Success rate | 86.5% | Single-view adaptation; variant without Internet videos: 81.1% |
| HabitatGS-LN | Success rate | 94.9% | Variant without Internet videos: 90.4% |
| Unitree Go2 indoor navigation | Overall success rate | 83.3% | 60 trials across three environments; manually assessed success |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Language-guided navigation addresses costly robot action data. Effects on long-range exploration remain unverified. |
| Delta contribution | 7.0 | Staged Internet video training transfers navigation priors without proxy action labels. The joint video-action architecture follows DreamZero. |
| Method quality | 8.0 | Shared video-action prediction and the initial-frame anchor fit the task. Action alignment and video replay have modest individual benefits. |
| Effectiveness | 8.0 | Ablations and real-robot comparisons support the transfer benefit. Robot evaluation covers limited tasks in three indoor environments. |
| Gap support | 8.0 | Gains with the same action data support transfer from action-free videos to executable actions. Evidence is limited to initially visible indoor object targets. |

**Overall score:** 7.8/10.

**Limitations/Gaps:**

- Quantitative evaluation focuses on indoor object targets visible in the initial view.
- Outdoor environments and region-level goals remain unevaluated.
- Real-robot evaluation uses three environments, four tasks per environment, and five trials per task. Success is assessed manually.
- Action alignment and video replay show modest individual benefits.

**Open weights/code:** — / [Project](https://zju3dv.github.io/ScaleNav/).

## Inference / Deployment

- **Inference latency:** 76 ms per executed action, amortized on RTX 4090 GPUs in simulation evaluation.
- **Deployment hardware:** Unitree Go2; deployment compute hardware: —.

## Dataset / Data Collection

- **Training data:** 18.2K Internet egocentric navigation segments with instructions; approximately 2.6K action-labeled simulated episodes from 650 InteriorGS scenes in Habitat-GS.
- **Evaluation data:** Single-view Short-Horizon OVON: 524 episodes in 36 HM3D scenes. HabitatGS-LN: 157 episodes in 45 held-out InteriorGS scenes. Real robot: 60 trials per method.

**Source:** [Paper text](https://arxiv.org/html/2610.25690v1), sections 3–5.
