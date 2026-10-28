### λ_0

**Full title:** $λ_0$: Scaling Open-World Egocentric Human Data for Humanoid Loco-Manipulation

**Authors:** Lambda-humanoid Team

**Venue/Year:** — / 2026

**arXiv:** [2610.18950v1](https://arxiv.org/abs/2610.18950v1)

**Architecture:** A Qwen3.5-2B vision–language backbone conditions a generative action expert. The policy uses an egocentric image, language instruction, and robot state. It predicts 50-step action chunks. Each G1 action has a 64-dimensional SONIC motion latent and two 6-dimensional Revo2 hand commands.

**Key methodology:** The pipeline aligns camera viewpoints and arm appearance. It corrects human motion references, robot motion references, and controller inputs offline. Training has three stages: hand-motion pretraining, whole-body human mid-training on aligned HumanVerse data, and robot post-training. Stages II and III use flow matching.

**Robot / Tasks:** Unitree G1 with Revo2 hands performs whole-body loco-manipulation. The four real evaluation tasks are Bottle Disposal, Toy Storage, Box Transport, and Chair Placement. A separate transfer experiment uses task-specific human demonstrations without target-task robot demonstrations. The full λ_0 policy uses robot post-training.

**Main contributions:**

- Introduces HumanVerse: 500 hours of egocentric video with synchronized body and hand motion, before conversion and validity filtering.
- Aligns human observations and actions to the G1 controller interface.
- Studies human-data scale and training stages while keeping robot demonstrations fixed.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| SIMPLE | Success rate | 90.0% | Six tasks, Levels 0–2; ten trials per task–level pair; task-wise configuration selection |
| Four real G1 tasks | Average success rate | 62.5% | Ten fixed initial configurations per task and policy |
| Four real G1 tasks | Average weighted progress | 80.4% | Equal task weights; StarVLA reports 54.6% with the same initial configurations and scoring criteria |
| Four real G1 tasks, without Stage II | Average success rate | 22.5% | Same architecture, action representation, vision–language initialization, and Stage-III robot post-training |
| Offline action alignment | Mean end-effector position / orientation error | 17.03 → 3.83 cm / 36.06° → 10.85° | Robot-reference and dynamics-aware stages evaluated on 50 tasks, about 1 h of data |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Addresses costly humanoid demonstrations and joint learning of locomotion and manipulation. Collection-efficiency evidence covers representative tasks. |
| Delta contribution | 7.3 | Combines HumanVerse, G1 alignment, and scaling with fixed robot data. HALOMI and EMMA have related alignment and human-data learning methods. |
| Method quality | 8.0 | Separates geometry and controller errors and uses a shared action interface. Controlled ablations support the design; alignment validation is limited. |
| Effectiveness | 8.0 | Real G1 results and the Stage-II ablation support the benefit of human whole-body data. Evaluation covers four real tasks with ten trials each. |
| Gap support | 8.0 | Alignment, collection-effort measurements, and scaling support transfer of human experience to humanoid supervision. Broader embodiment transfer and scale extrapolation remain unproven. |

**Overall score:** 7.8/10.

**Limitations/Gaps:**

- Real λ_0 evaluation covers only G1, four tasks, and ten initial configurations per task.
- SIMPLE results use task-wise configuration selection. Public baseline entries retain their source evaluation protocols.
- Scaling-loss fits use single runs. They do not establish reproducibility across seeds or extrapolation beyond the measured range.
- HumanVerse's 500 hours are recorded data before conversion and validity filtering. Hand motion is reconstructed from RGB.
- The full policy requires robot post-training. Transfer without target-task robot demonstrations is a separate experiment.

**Open weights/code:** — / [GitHub](https://github.com/LambdaHumanoid/openlambda).

## Inference / Deployment

- **Inference latency:** —.
- **Deployment hardware:** Unitree G1 with Revo2 hands and a head-mounted GoPro HERO13. SONIC executes motion tokens. Deployment uses robot images and state without human motion streams.

## Dataset / Data Collection

- **HumanVerse:** 500 recorded hours, 32,993 episodes, 87 million pose frames, and 827 task types. Wearable body tracking is synchronized with egocentric video; hand motion is reconstructed from video.
- **Training data:** Public egocentric hand–object datasets for Stage I, aligned HumanVerse for Stage II, and robot demonstrations for Stage III.
- **Data split:** Recording sessions are split before temporal windows are extracted. Task-specific human demonstrations for downstream post-training are separate from HumanVerse.

**Source:** [Paper text](https://arxiv.org/html/2610.18950v1), abstract and sections 3–5.
