### TCP4D

**Full title:** TCP4D: A Unified Tool-Center-Point Tracking and Generation Model for Robot Manipulation

**Authors:** Haosong Peng et al.

**Venue/Year:** — / 2026

**arXiv:** [2611.23143v1](https://arxiv.org/abs/2611.23143v1)

**Architecture:** A DINOv2-based Transformer backbone follows 4RC and builds a shared 4D scene representation. Initial 2D TCP queries guide direct prediction of TCP poses in SE(3), gripper states, scene geometry, and camera parameters. A DiT generates future TCP states from local track features, robot state, wrist images, and language. Frozen DINOv2 and T5-base encode wrist images and instructions.

**Key methodology:** First, train geometry and TCP reconstruction together. Then jointly fine-tune the backbone, tracker, and generator with flow matching. Cross-embodiment augmentation recovers motion from RGB video, retargets it through IK, removes the source robot, completes the background, and renders the target robot. This process can operate without recorded source-robot states. The target robot must be able to reach the recovered motion.

**Robot / Tasks:** TCP tracking uses DROID and RoboLab. Manipulation evaluation covers 48 RoboTwin tasks and two CoBoT Magic tasks: placing pens and stacking bowls. Cross-embodiment policy evaluation uses four tasks with Aloha-AgileX source demonstrations and ARX-X5 and UR5-WSG target robots.

**Main contributions:**

- Directly recovers virtual TCP poses and gripper states, without fitting rigid motion to surface points.
- Connects TCP tracking and future action generation through a shared 4D scene representation.
- Converts RGB videos into target-robot demonstrations without recorded source-robot states.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| DROID / RoboLab | ATE | 7.60 / 16.07 mm | After Sim(3) alignment |
| RoboLab Unseen | RRE | 6.80° | MoSE3: 0.99°; TCP4D has higher rotation error |
| RoboTwin, 48 tasks | Mean success rate | 69.19% clean2clean / 10.94% clean2random | 100 trials per task; TCP4D uses third view, compared baselines use head view |
| CoBoT Magic, two tasks | Mean success rate | 78.33% | 30 trials per task and method; DP3: 63.33%; DP3 uses depth point clouds, TCP4D uses RGB |
| ARX-X5, four tasks | Mean success rate | 72.0% vs 30.5% | DP with source + augmented data vs augmented-only data; same training budget; 50 episodes per task |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Reusing videos without action labels can increase robot training data. Target reachability limits which motions can transfer. |
| Delta contribution | 8.0 | Direct virtual TCP recovery removes the need for surface-point fitting and recorded source states. The backbone and generation method extend existing designs. |
| Method quality | 7.7 | Direct pose recovery and track-conditioned flow matching connect action reconstruction with generation. The separate effects of the shared representation and track conditioning are not isolated. |
| Effectiveness | 7.0 | Tracking, real-robot tasks, and augmented-data policy results support practical use. Low clean2random success and higher RoboLab rotation error limit the result. |
| Gap support | 7.0 | Tracking and target-policy results support recovery of action labels and augmentation without source states. Reachability and the narrow task range leave gaps. |

**Overall score:** 7.5/10.

**Limitations/Gaps:**

- The generator trains only on clean demonstrations. RoboTwin clean2random success falls to 10.94%.
- Real-robot generator evaluation covers two CoBoT Magic tasks, with 30 trials per task and method.
- RoboTwin camera views differ between TCP4D and the compared baselines. DP3 uses depth point clouds in the real-robot comparison.
- ATE uses Sim(3) alignment. These values do not establish metric pose accuracy before alignment.
- Target robots must be able to reach the recovered motion. The shared representation and track conditioning lack separate effect estimates.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** —.
- **Deployment hardware:** —.
- **Integration:** Four Euler updates generate the future action sequence. CoBoT Magic uses cuRobo for IK; measured depth is not required at inference.

## Dataset / Data Collection

- **Training data:** DROID and RoboTwin for tracker training; 60 demonstrations per CoBoT Magic task. Augmentation uses 50 Aloha-AgileX source demonstrations per task, yielding 199 ARX-X5 and 198 UR5-WSG demonstrations across four tasks.
- **Evaluation data:** DROID and RoboLab tracking; 48 RoboTwin tasks with 100 trials per task; two CoBoT Magic tasks with 30 trials per task and method; cross-embodiment policies with 50 episodes per task and policy–embodiment pair.

**Source:** [Paper text](https://arxiv.org/html/2611.23143v1), abstract and sections 1–5. [Project](https://livioni.github.io/TCP4D/).
