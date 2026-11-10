### ODE Policy

**Full title:** ODE Policy: Robot Learning via Action Dynamics, Not Actions

**Authors:** Jindou Jia et al.

**Venue/Year:** — / 2026

**arXiv:** [2611.01729v1](https://arxiv.org/abs/2611.01729v1)

**Architecture:** A neural ODE uses a FiLM-MLP vector field to model action dynamics. Images and instructions condition the field. Proprioception enters the field directly. A diversity head adds sampled velocity offsets for multi-modal behavior. The same formulation serves as a visuomotor policy, a VLA or WAM action head, and an RL actor.

**Key methodology:** In imitation learning (IL), path loss matches actions integrated over short chunks to demonstrations, without velocity labels. Contractive perturbation changes the starting action during training and teaches the path to return to the demonstration. At inference, integration continues from the last action across chunk boundaries. Observations and proprioception stay fixed within each chunk. In reinforcement learning (RL), the actor takes one Euler step from the previous action at each control step.

**Robot / Tasks:** LIBERO evaluates manipulation, and LIBERO-plus evaluates generalization. Real-robot evaluation covers 14 tasks on Franka Research 3, Galaxea R1 Lite, Sharpa North with Sharpa dexterous hands, and Unitree G1 with Inspire DFX dexterous hands. Tasks include precise, long-horizon, deformable, multi-modal, dexterous, and loco-manipulation tasks. RL evaluates a simulated Unitree G1 tracking 40 LAFAN1 motion clips with SuperMimic.

**Main contributions:**

- Learns an action vector field through paths integrated in physical time, without velocity labels.
- Connects action chunks by continuing from the previous action and uses a diversity head to retain distinct behavior modes.
- Applies the same action dynamics formulation to IL, VLA and WAM action heads, and model-based RL.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| LIBERO, visuomotor IL | Success rate | 79.2% | After 1 epoch; best compared baseline: 43.2%; four suites and three seeds |
| LIBERO, π0.5 | Success rate | 96.0% | After 1 epoch; FM-R: 75.5%; one seed; both action heads randomly initialized, with different structures and parameter counts |
| LIBERO, ImageWAM | Success rate | 82.6% | After 1 epoch; original flow matching head: 24.6%; one seed |
| LIBERO, visuomotor IL | Success rate | 87.7% | Epoch 100; 20 demonstrations per task; FM-DiT: 85.4% with 50 demonstrations per task; data conditions differ |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Data cost, inference cost, and action continuity affect many robot policies. Application to VLA, WAM, and RL gives the method a broad scope, but long-term operation remains unverified. |
| Delta contribution | 8.0 | Training integrated paths without velocity labels and continuing across chunks extends Streaming flow policy. Time alignment and dynamical policies have prior work. |
| Method quality | 8.0 | Short path integration and contractive perturbation address continuity and accumulated error. Fixed observations within chunks limit reaction to new events. |
| Effectiveness | 7.3 | Shared backbone, data, and training schedules support the comparisons; visuomotor experiments use three seeds. Large-model results use one seed, and baselines later catch up or converge. |
| Gap support | 7.0 | The integration structure and learning results support progress on continuity and cost. Detailed real-robot, smoothness, and ablation results are absent from the available excerpt. |

**Overall score:** 7.7/10.

**Limitations/Gaps:**

- Streaming actions do not mean continuous observation updates. Observations and proprioception stay fixed within a chunk.
- The π0.5 and ImageWAM learning curves use one seed. The pretrained π0.5 expert catches up from epoch 2; ImageWAM heads converge from epoch 6.
- Execution quality is measured only on successful episodes. It does not describe the quality of failed rollouts.
- LIBERO uses a separate classification head for binary gripper commands. These commands do not use the same continuous integration as the other actions.
- Early large-model gains on LIBERO do not establish the same gains on other tasks or under distribution changes.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** — (absolute latency not reported in the available excerpt).
- **Deployment hardware:** —.
- **Integration:** Standard visuomotor IL uses 8-step chunks and RK4. ImageWAM uses 12-step chunks with Euler; GR00T N1.7 uses 16-step chunks with Euler.

## Dataset / Data Collection

- **Training data:** LIBERO demonstrations; π0.5 uses 10 episodes per task and ImageWAM uses 25. Three real-robot tasks use data from another lab.
- **Evaluation data:** Four LIBERO suites; 20 episodes per task per visuomotor checkpoint, with three training seeds. Large-model learning curves use one seed. Real-robot evaluation uses 20 trials per task and method. RL evaluates all 40 LAFAN1 clips.

**Source:** [Paper text](https://arxiv.org/html/2611.01729v1), abstract and sections 1–6.1.2.
