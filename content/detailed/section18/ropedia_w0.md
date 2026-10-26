### Ropedia W0

**Full title:** Ropedia W0: Scaling Loco-Manipulation World Models across Embodiments with Human Experience

**Authors:** Tianqi Liu et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.26855v1](https://arxiv.org/abs/2610.26855v1)

**Architecture:** A video diffusion transformer predicts future egocentric frames from an initial image, text, camera poses, and projected manipulator skeletons. Camera poses represent locomotion. Skeletons preserve the structure of each human or robot manipulator.

**Key methodology:** Xp-Data supports human pretraining followed by mixed human–robot training with the same camera-and-skeleton interface. Robot skeletons use forward kinematics where available, with extensive manual keypoint annotation and correction. Distillation produces a causal generator for long video rollouts and live VR interaction.

**Robot / Tasks:** Video prediction during locomotion and manipulation across humans, gripper robots, and dexterous humanoids. Evaluation uses DreamDojo, Ψ0, ω-HOME, Xp-Teleop, AgiBot, and held-out human videos. Xp-Teleop uses a Unitree G1 with two six-DoF dexterous hands.

**Main contributions:**

- Uses a common camera-and-skeleton interface to learn from human and robot motion.
- Builds Xp-Data with approximately 10,000 hours of human video and 3,000 hours of robot video with common multimodal annotations.
- Adds Xp-Teleop for long-horizon humanoid locomotion and dexterous manipulation. More human pretraining data improves human and robot prediction.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| EgoSuite + OpenAoE human video prediction | Absolute trajectory error | 1.542 cm | A14B human-pretrained model; 200 held-out clips; Cosmos3-Nano 16B: 1.931 cm |
| DreamDojo In-lab video prediction | PSNR | 20.854 dB | Ropedia W0 5B; 1% post-training data; DreamDojo 14B: 18.983 dB |
| Ψ0 dexterous humanoid video prediction | PSNR | 19.07 dB | A14B mixed-trained model; full-data post-training; Cosmos3-Nano 16B: 16.55 dB |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Reusing human experience can reduce costly robot data collection and adaptation. The size of the benefit for real decisions remains uncertain. |
| Delta contribution | 8.0 | The common camera-and-skeleton interface and unified data extend transfer across embodiments. Earlier work also uses rendered conditions. |
| Method quality | 8.0 | Separate camera and manipulator conditions connect different action spaces. Accurate robot skeletons require extensive manual correction. |
| Effectiveness | 7.0 | Human motion following and low-data robot prediction support transfer. Detailed results mainly measure video quality rather than planning or control. |
| Gap support | 7.0 | Prediction across embodiments partly supports joint locomotion and manipulation modeling. Zero-shot evaluation does not establish transfer to an unseen embodiment. |

**Overall score:** 7.6/10.

**Limitations/Gaps:**

- Robot skeleton annotation requires extensive manual work to correct inaccurate projections.
- Zero-shot means that the evaluation dataset was not used for training. The same embodiment can occur in other training datasets.
- Detailed numerical evidence centers on video quality and motion following. The size of planning and control benefits remains uncertain.
- Xp-Teleop covers 27 long takes, about one hour, on one humanoid platform.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** —. The distilled model generates 21.3 frames per second at 640×480 for minute-long interactive rollouts.
- **Deployment hardware:** —.

## Dataset / Data Collection

- **Training data:** Xp-Data combines approximately 10,000 human video hours and 3,000 robot video hours. Sources include 14 public human datasets, 13 public robot datasets, and in-house human recordings.
- **Evaluation data:** Five robot benchmarks and 200 held-out human clips from EgoSuite and OpenAoE. Xp-Teleop includes 27 takes with 543 annotated atomic segments across 30 skill classes.

**Source:** [Paper text](https://arxiv.org/html/2610.26855v1), sections 3–6.2; [Project](https://ropedia.github.io/ropedia-w0/).
