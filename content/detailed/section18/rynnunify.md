### RynnUnify

**Full title:** RynnUnify: Towards Unified Embodied Brain

**Authors:** Minghao Zhu et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.32965v1](https://arxiv.org/abs/2610.32965v1)

**Architecture:** A 16B model uses the Cosmos3 Mixture-of-Transformers (MoT) architecture. An 8B autoregressive reasoner and an 8B diffusion generator interact through joint attention. The reasoner architecture stays unchanged. The generator adds scene memory across video chunks and first-and-last-frame conditioning.

**Key methodology:** The reasoner selects the next subtask, describes its expected visual changes, and estimates its duration. The generator predicts a video. Its final frame becomes the observation for the next planning step. Four scene reference frames and a video prefix from the previous chunk retain scene and motion context. A separate 8B agent, trained with reinforcement learning, chooses when to use the frozen model for video predictions. A World-Action Model (WAM) extension uses latent planning and joint video–action training for robot control.

**Robot / Tasks:** Astribot S1 performs multi-step manipulation with body reorientation, precise object handling, and execution that depends on task history. Simulation evaluates 20 selected composite RoboCasa365 tasks. Rynn-VP evaluates long-horizon visual planning. Rynn-GEU evaluates reasoning about unobserved future states and interaction outcomes.

**Main contributions:**

- Connects embodied understanding with successive video predictions for long-horizon visual planning.
- Adds selective video generation for reasoning and extends the full model to robot control.
- Introduces Rynn-VP and Rynn-GEU to evaluate sustained visual planning and the value of video prediction for reasoning.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| Rynn-VP | Overall score improvement | 9.75 points | Compared with Cosmos 3 Nano |
| Rynn-GEU | Average score improvement | 6.0 points | Agentic extension compared with direct reasoning |
| RoboCasa365 | Success rate | 51.5% | WAM extension; 20 selected composite tasks |
| Real-robot manipulation | Average success rate | 46.7% | Three tasks; Astribot S1 |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Connecting understanding, prediction, and action addresses multi-step robot work. Use beyond the selected tasks remains uncertain. |
| Delta contribution | 6.3 | Scene memory and boundary-frame conditions extend Cosmos3 to sequential visual planning. The separate effects of these changes and added training data remain uncertain. |
| Method quality | 7.0 | Scene references and recent video context address scene loss and motion discontinuity. Evidence that separates their effects and measures error accumulation is limited. |
| Effectiveness | 6.0 | Planning gains and robot success rates support possible use. Real evaluation covers three tasks, and a separate RL agent limits attribution of reasoning gains to video generation alone. |
| Gap support | 6.0 | Two benchmarks and reported gains partly support sustained planning and prediction-assisted reasoning. Detailed controlled comparisons are limited. |

**Overall score:** 6.5/10.

**Limitations/Gaps:**

- Robot-control results cover selected simulation tasks and three real tasks on one platform.
- The available text does not establish the separate effects of scene memory, boundary-frame conditions, and added training data.
- Detailed evaluation conditions, trial counts, and failure analysis are unavailable in the source excerpt.

**Open weights/code:** — / [Code](https://github.com/alibaba-damo-academy/RynnUnify). The paper also links a [model collection](https://huggingface.co/collections/Alibaba-DAMO-Academy/RynnUnify); its contents are not reported in the excerpt.

## Inference / Deployment

- **Inference latency:** —
- **Deployment hardware:** —

## Dataset / Data Collection

- **Training data:** A 10% subset of the RynnBrain pretraining corpus supports general understanding. Other training covers spatial reasoning, physical prediction, affordance grounding, subtask planning, egocentric activities, robot manipulation, and embodied reasoning videos.
- **Evaluation data:** Rynn-VP, Rynn-GEU, 20 selected composite RoboCasa365 tasks, and three real-robot tasks.

**Source:** [Paper text](https://arxiv.org/html/2610.32965v1), abstract and sections 1–3.1.
