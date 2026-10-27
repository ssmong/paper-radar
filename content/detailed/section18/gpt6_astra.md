### Has GPT-6-Astra Achieved Embodied Intelligence?

**Full title:** Has GPT-6-Astra Achieved Embodied Intelligence?

**Authors:** SenseNova Joint Research Team; Zhongang Cai et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.22471v1](https://arxiv.org/abs/2610.22471v1)

**Architecture:** GPT-6-Astra acts as a high-level System 2 reasoner with fixed weights. In the collaboration study, π0.5, fine-tuned on RoboDojo, acts as a low-level System 1 VLA controller. Internal model architecture: —.

**Key methodology:** Training demonstrations produce a task-specific ICL knowledge package with notes and reusable code. The package is frozen before testing. Test episodes use separate sessions, with no information transfer between episodes. Standard (1×) and extended (10×) action budgets retain the same control interface and success criteria. Extensions continue the same episode without resets. RoboDojo ablations compare controller collaboration, action representations, and action chunking. In closed-loop collaboration, GPT-6-Astra accepts, modifies, or rejects proposed end-effector actions. Real-robot trials use no demonstrations; they use human-written context and wall-clock budgets.

**Robot / Tasks:** Twelve benchmarks cover tabletop manipulation, humanoid loco-manipulation, household activities, navigation, and dexterous hands. Eight real robot configurations cover single and dual arms, grippers, dexterous hands, wheeled mobile manipulators, and a humanoid.

**Main contributions:**

- Evaluates a fixed general model with demonstration-based ICL and separate standard and extended action budgets.
- Measures success and cost for direct control and closed-loop VLA collaboration.
- Examines deployment limits on real robots and proposes a benchmark prototype without in-domain demonstrations and with a running world clock.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| SIMPLE | Success rate | 90.8% | Task-level ICL; zero-shot: 70.8%; four common tasks, standard budget |
| RoboDojo | Unweighted mean of category success rates | 54.17% | ICL + closed-loop VLA; ICL direct control: 29.67%; controlled harness ablation |
| Real rigid pick-and-place | Successful trials | 17/18 | Zero-shot real-robot evaluation with human-written context |
| Real plug insertion | Successful trials | 0/11 | Across three platforms |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Results across robot types identify limits in reliability and efficiency. Economical deployment remains uncertain. |
| Delta contribution | 7.0 | ICL packages and closed-loop VLA review extend RoboRSI-based direct control. The main advance concerns evaluation and system integration. |
| Method quality | 8.0 | Frozen packages separate preparation from testing. Extensions of the same episode assess recovery, but package components are not isolated. |
| Effectiveness | 7.0 | Controlled ICL and collaboration comparisons show gains. Long inference times and real contact failures limit practical use. |
| Gap support | 7.3 | Budget comparisons and real trials clarify capability and deployment limits. Changes in demonstrations, time limits, and human context prevent isolation of transfer effects. |

**Overall score:** 7.4/10.

**Limitations/Gaps:**

- Knowledge packages depend on source tasks, with weak transfer beyond the demonstration distribution.
- High token costs and long execution times limit real-time use.
- Physical completion checks, recovery from irreversible failures, and retention of progress in long tasks remain unreliable.
- Real trials use platform-specific human context and some different success criteria, which limit direct comparisons.
- Package components are not separately evaluated for their causal contribution.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** —
- **Deployment hardware:** —

## Dataset / Data Collection

- **Training data:** Benchmark training demonstrations prepare frozen ICL knowledge packages; GPT-6-Astra weights remain fixed. The System 1 π0.5 controller is fine-tuned on RoboDojo.
- **Evaluation data:** Twelve benchmarks, including SIMPLE and RoboDojo, plus trials on eight real robot configurations. Real trials use no demonstration-derived knowledge packages.

**Source:** [Paper text](https://arxiv.org/html/2610.22471v1), abstract and sections 2–4.
