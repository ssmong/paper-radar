### SuperNav

**Full title:** SuperNav: An Agentic Navigation System for Any Task in Any Scene

**Authors:** Jinkai Zhang et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.12126v1](https://arxiv.org/abs/2610.12126v1)

**Architecture:** A pretrained MLLM selects navigation goals through a harness without navigation-specific fine-tuning. Navigation Skills give guidance for search, recovery, and completion. Tools return four RGB views, execution status, and diagnostics. A shared visual-point interface connects the MLLM to Geo-based Executor or Learned Executor.

**Key methodology:** The MLLM selects a destination in an image. The executor moves toward it and returns feedback for the next decision. Goal records track pending and completed items. Context management removes superseded image payloads but keeps text history and image paths. Geo-based Executor uses geometry and path planning. Learned Executor predicts local motion from RGB observations and marked image points.

**Robot / Tasks:** Instance and ordered multi-object navigation in Habitat-GS; demand-driven navigation in AI2-THOR; category-level navigation on HM3D. Real-robot examples use a Unitree Go2 to search for objects and visit successive goals.

**Main contributions:**

- Connects image-based destination selection to interchangeable motion executors.
- Combines Navigation Skills, goal records, and context management to support different requests.
- Evaluates several navigation task types and uses ablations to assess the harness.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| InteriorGS-based Habitat-GS, single-object navigation | SR | 78.00% | Geo-based Executor; 150 tasks; navmesh path distance below 1 m to an approved target viewpoint and explicit STOP |
| InteriorGS-based Habitat-GS, ordered multi-object navigation | SR | 34.00% | Geo-based Executor; 150 tasks with two to five targets; ordered arrivals and explicit STOP |
| Adapted Demand-Bench in AI2-THOR | SR | 59.50% | Geo-based Executor; 200 tasks; ordered arrival in 2 m target regions, without object reuse, and explicit STOP |
| HM3D-OVON val-unseen, Navigation Skills ablation | SR | 68.33% with Skills; 35.00% without Skills | Same 120 episodes, Geo-based Executor, GPT-5.6 Terra (high), and 0.25 m threshold |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Different requests in unfamiliar scenes matter for service robots. Inference cost, variable delay, and geometry requirements limit practical use. |
| Delta contribution | 6.0 | Interchangeable executors, Skills, and context management extend related harness methods. Direct comparisons with the closest harness methods are absent. |
| Method quality | 8.0 | Visual-point goals and execution feedback separate decisions from motion. Ablations with the same executor support the design, but semantic completion has no independent check. |
| Effectiveness | 7.0 | Results support several navigation task types. Different observation and execution conditions limit baseline comparisons; real-robot evidence is qualitative. |
| Gap support | 7.0 | Results support broader task and scene coverage beyond fixed workflows and navigation training data. Activity completion and long real-world sequences remain unverified. |

**Overall score:** 7.1/10.

**Limitations/Gaps:**

- Semantic judgments and goal records depend on the MLLM. They are not independent semantic checks.
- Geo-based Executor needs maps or scene geometry. MLLM inference adds cost and variable delay.
- Demand-driven evaluation measures ordered navigation to targets, rather than completion of the requested activities.
- Baselines retain their own inputs and history mechanisms. Observation and motion conditions differ from SuperNav.
- Real-robot evidence is qualitative. Reliability over long navigation sequences and wider real-world evaluation remain open.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** Variable; numerical latency: —.
- **Deployment hardware:** Unitree Go2 with four directional RGB cameras, LiDAR, and odometry; compute hardware: —.

## Dataset / Data Collection

- **Evaluation data:** InteriorGS-based Habitat-GS: 150 single-object and 150 ordered multi-object tasks. Adapted Demand-Bench: 200 tasks in AI2-THOR. Category-level evaluation: 120 HM3D-OVON val-unseen episodes and 1,000 HM3Dv2 validation episodes.

**Source:** [Paper text](https://arxiv.org/html/2610.12126v1), sections 3–5 and Appendix A.1; [Project](https://zju3dv.github.io/SuperNav/).
