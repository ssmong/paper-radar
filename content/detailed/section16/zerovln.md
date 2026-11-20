### ZeroVLN

**Full title:** ZeroVLN: Learning to Navigate without Supervised Fine-Tuning of the VLM Brain

**Authors:** Zixuan Huang et al.

**Venue/Year:** — / 2026

**arXiv:** [2611.26414v1](https://arxiv.org/abs/2611.26414v1)

**Architecture:** A Qwen3.6-35B-A3B VLM brain sends natural-language movement requests through semantic tool calls. A 12-layer flow-matching action expert uses a Qwen3.5-4B visual encoder to execute them. The slow brain selects movements. The fast action expert updates continuous actions from new RGB observations.

**Key methodology:** First, a planner uses scene-mesh semantic maps and training-only geometry to ground requests from the frozen brain into reachable local goals and reference trajectories. The action expert learns only the executed prefix of each predicted action sequence. Then closed-loop RL jointly updates the brain and action expert. Both policies use a shared trajectory-level advantage with separate gradient paths. Rewards cover terminal success, first arrival, distance progress, and information discovery. The brain receives no navigation-domain SFT, but its weights change during RL.

**Robot / Tasks:** Simulated vision-language navigation on SAGE-Bench (SAGE-3D), R2R-CE, and RxR-CE. Physical robot: —. R2R-CE and RxR-CE require the agent to stop in the goal region; SAGE-Bench requires arrival.

**Main contributions:**

- Replaces geometric goal prediction with semantic tool requests, without navigation-domain SFT of the brain.
- Aligns action expert training with the brain's actual requests and the action prefix used during execution.
- Jointly improves movement decisions and continuous execution through RL while largely retaining general visual capabilities.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| SAGE-3D navigation | SR | 51.3%; NaVILA 23.5% | Same backbone and training episodes |
| R2R-CE navigation | SR | 52.7%; NaVILA 46.5% | Same backbone and training episodes; stopping required |
| RxR-CE navigation | SR | 51.4%; NaVILA 48.7% | Same backbone and training episodes; stopping required |
| R2R-CE / RxR-CE navigation | SPL | 29.2% / 28.1%; NaVILA 41.8% / 43.0% | Same backbone and training episodes; lower path efficiency despite higher OSR |
| Twelve general visual benchmarks | Mean accuracy | 59.16%; base brain 59.47% | Measures capability retention after navigation training |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Learning navigation while retaining general visual capabilities supports the study of shared robot brains. Other physical skills and real robots remain outside the evaluation. |
| Delta contribution | 8.0 | Semantic requests and joint slow–fast RL extend DualVLN's geometric interface. The design combines existing methods; transfer to other backbones remains unverified. |
| Method quality | 8.0 | Request grounding and execution-prefix supervision reduce training–execution mismatch. Training still needs semantic maps and a planner with privileged geometry. |
| Effectiveness | 7.0 | Comparisons with the same backbone and episodes support higher SR and capability retention. Lower R2R/RxR SPL limits the path-efficiency benefit. |
| Gap support | 8.0 | Controlled navigation results and visual evaluations that bypass answer formatting support capability retention. Evidence covers one brain backbone and VLN-CE. |

**Overall score:** 7.8/10.

**Limitations/Gaps:**

- R2R-CE and RxR-CE show higher OSR but lower SPL than NaVILA. Additional exploration can increase path length.
- Initial action expert training needs scene-mesh semantic maps and a planner with training-only geometry.
- Evaluation covers three VLN-CE benchmarks and one brain backbone. Effects on physical robots and other backbones remain unverified.
- Reducing unnecessary exploration while retaining goal reachability and general visual capabilities remains an open gap.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** —.
- **Deployment hardware:** —.

## Dataset / Data Collection

- **Training data:** A shared pool of 34,445 navigation episodes supports action expert adaptation and RL. Reference trajectories are generated from the frozen brain's movement requests.
- **Evaluation data:** SAGE-Bench, R2R-CE, and RxR-CE official evaluation sets; twelve general visual benchmarks for capability retention.

**Source:** [Paper text](https://arxiv.org/html/2611.26414v1), sections 2–5.
