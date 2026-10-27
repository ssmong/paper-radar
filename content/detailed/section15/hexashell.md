### HexaShell

**Full title:** HexaShell: A Thin Harness for Exploring the Limits of VLM Agents as Robot Coding Agents

**Authors:** Hongcheng Gao et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.23479v1](https://arxiv.org/abs/2610.23479v1)

**Architecture:** Two coding agents use Codex with GPT-6-Astra at medium reasoning effort. A thin command-line harness converts commands into joint motion. The acting agent receives three calibrated RGB views, robot poses, and joint angles. Tools use only robot observations.

**Key methodology:** The acting agent uses tools to attempt a layout. After a failure, an optimizer agent reads the log and camera frames, then writes or repairs a tool. The same layout runs again. Tools measure positions through triangulation and plane constraints. Wrist-camera movements give extra views and use action steps. Tools are developed on ten layouts, then frozen for evaluation on new layouts within seed 0.

**Robot / Tasks:** RoboDojo has 42 simulated manipulation tasks for a dual-arm ARX X5 in Isaac Sim 5.1. Its task groups are Generalization, Memory, Long-Horizon, Precision, and Open. Standard and cluttered Generalization tasks produce 54 variants in total.

**Main contributions:**

- Keeps reusable robot tools across episodes and repairs them from failure logs without model training.
- Compares RGB geometry with Depth Anything V2 Base under the same harness, model, and development layouts.
- Maps performance and failures across contact types to show where the tools work and where they remain limited.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| RoboDojo, all 42 tasks | Success rate / progress score | 39.7% / 48.0 | Frozen tools; new layouts within seed 0; leaderboard aggregation |
| RoboDojo development layouts | Success-rate gain | 8.7 percentage points | Triangulation compared with Depth Anything V2; same layouts, harness, loop, and model |
| Pushing / memory tasks | Success rate | 92.5% / 65.0% | New-layout evaluation |
| Tight insertion | Success rate | 8.3% | New-layout evaluation |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 7.3 | Reusable code from robot failures supports robot development and capability analysis. Simulation and long model delays limit evidence for practical use. |
| Delta contribution | 6.3 | Persistent tool repair and a full benchmark analysis extend a fixed harness. Related systems such as URAI also separate tool writing from execution. |
| Method quality | 7.3 | Calibrated RGB geometry and frozen evaluation fit the problem. Earlier depth tools and extra task notes prevent isolation of the repair loop's effect. |
| Effectiveness | 7.0 | Matched development layouts support the benefit of triangulation. Low insertion success and model delays limit practical use. |
| Gap support | 6.7 | New-layout results and contact-type analysis clarify the tools' limits. One seed and observational failure labels cannot establish contact as the main cause of failure. |

**Overall score:** 6.9/10.

**Limitations/Gaps:**

- New-layout evaluation stays within seed 0. Leaderboard baselines use different episode counts and seed conditions.
- RGB development starts from earlier depth tools. For 25 tasks, the optimizer also receives notes about checker requirements.
- Comparisons with a fixed harness change both the interface and tool use. They do not isolate the repair loop's effect.
- Tight insertion and articulated-object tasks remain difficult. Failure labels do not separate perception, reasoning, and control causes.
- RoboDojo does not charge model latency against the action budget.

**Open weights/code:** — / [Code](https://github.com/HexaFuture/HexaShell).

## Inference / Deployment

- **Inference latency:** A retest episode takes a median of 739 s for 26 s of robot time. Most elapsed time is model latency.
- **Deployment hardware:** One RTX 4090 per run; evaluation uses simulation.

## Dataset / Data Collection

- **Tool development:** Ten layouts per task within seed 0; no model training. Generalization tasks use five standard and five cluttered layouts.
- **Evaluation data:** Ten new layouts per task within seed 0. Generalization tasks use five new standard and five new cluttered layouts. The benchmark's own checkers judge success.

**Source:** [Paper text](https://arxiv.org/html/2610.23479v1), abstract and sections 2–5.
