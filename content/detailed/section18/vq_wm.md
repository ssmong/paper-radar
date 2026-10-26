### VQ-WM

**Full title:** Vector-Quantized World Model: Latent Feedback Motion Planning for Robot Manipulation

**Authors:** Xuezhou Xu, Chung-Pang Wang, Zhenzhen Li, Benjamin Riviere

**Venue/Year:** — / 2026

**arXiv:** [2610.25600v1](https://arxiv.org/abs/2610.25600v1)

**Architecture:** A frozen V-JEPA 2 encoder maps observations to latent states. A continuous latent predictor and a goal-conditioned controller estimate reachability. State and action codebooks and a discrete latent predictor support graph search.

**Key methodology:** First-passage time measures the number of controller calls needed to reach a target. Closed-loop rollouts in the learned world model estimate this cost. Greedy set cover selects a state codebook. Breadth-first search (BFS) uses the most likely next states to find a path with the fewest graph transitions. A continuous controller follows the targets with visual feedback. Experiments use one plan per episode.

**Robot / Tasks:** A WidowX AI arm transfers four disks in Tower of Hanoi. H1 requires one puzzle move; the full H15 task requires 15 moves. Simulation covers Stable-WorldModel Cube and Scene manipulation, DeepMind Control Walker goal poses, and a MuJoCo Tower of Hanoi ablation.

**Main contributions:**

- Uses controller-dependent first-passage time to define discrete planning states.
- Combines discrete search with continuous visual feedback to execute long plans from short-play data.
- Evaluates manipulation and locomotion, including proprioceptive inputs to the Walker controller.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| Stable-WorldModel Cube-Easy | Success rate | 84.7 ± 2.5% | Goal 25 steps ahead; execution budget: 50 steps |
| Stable-WorldModel Cube-Hard | Success rate | 73.3 ± 0.9% | Held-out grasp-centered windows; execution budget: 30 steps |
| Stable-WorldModel Scene | Success rate | 75.3 ± 5.0% | Goal 50 steps ahead; execution budget: 100 steps |
| DeepMind Control Walker | Success rate | 97.3 ± 2.5% | Images and proprioception; images only: 22.0 ± 5.9% |
| WidowX AI Tower of Hanoi H15 | Task progress | 100% | Non-expert short-play setting; six cases, three trials per case; this metric is not a separate completion success rate |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Long plans from short behaviors can reduce the need for full-task demonstrations. Use across multiple real tasks remains unverified. |
| Delta contribution | 7.0 | World-model first-passage time and set cover extend reachability-based planning. Reachability graphs and local behavior composition have precedents in SoRB and L3P. |
| Method quality | 7.7 | Controller-dependent states connect planning and execution. Reachability depends on model estimates, and BFS retains only the most likely transitions. |
| Effectiveness | 8.0 | Simulation results and real H15 task progress support long-plan execution. Real evaluation covers six cases of one puzzle. |
| Gap support | 7.7 | H15 results and ablations support a closer match between planned targets and controller reachability. The ablation also changes target-switching rules. |

**Overall score:** 7.6/10.

**Limitations/Gaps:**

- Real-robot evaluation covers one four-disk puzzle and six test cases.
- The real-robot 100% result measures task progress. A separate completion success rate is not reported.
- The quantization ablation also changes target-switching rules, which limits attribution to the distance measure alone.
- Recovery through replanning, language instructions, and multi-task use remain unevaluated.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** A complete plan for approximately five minutes of robot execution takes under one second on an NVIDIA RTX 5080 GPU.
- **Deployment hardware:** WidowX AI arm; one NVIDIA RTX 5080 GPU for inference.

## Dataset / Data Collection

- **Training data:** Offline observation-action trajectories. Tower of Hanoi play data is collected autonomously at 30 Hz with legal move sequences and predefined Cartesian pick-and-place motions. The non-expert setting uses short-play subtasks of at most five puzzle moves.
- **Evaluation data:** Cube and Scene manipulation benchmarks; Walker goal poses; six real Tower of Hanoi cases with three trials per case. The MuJoCo ablation uses three seeds and 50 trajectories per seed for each point.

**Source:** [Paper text](https://arxiv.org/html/2610.25600v1), sections IV–VI.
