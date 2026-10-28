### Reflex

**Full title:** Reflex: Visually Grounded Reactive Humanoid Control

**Authors:** Taoyang Jia et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.12772v1](https://arxiv.org/abs/2610.12772v1)

**Architecture:** A CNN locates the box in RGB-D images. A geometric layer extracts eight features. A GRU uses these features and camera ego-motion history to predict an eight-dimensional dynamics latent. The fixed action decoder uses this latent and robot state for whole-body control.

**Key methodology:** Stage 1 trains a state-based catching policy with PPO. Stage 2 learns the dynamics latent from delayed box observations through action matching, DAgger, and joint encoder/decoder PPO. Stage 3 learns to predict this latent from egocentric RGB-D history while the controller stays fixed.

**Robot / Tasks:** A 29-DoF Unitree G1 catches human-thrown boxes on its forearms against its torso and retains them without falling. A downstream demonstration uses SONIC for carrying and handover.

**Main contributions:**

- Extends RMA-style fixed-decoder latent regression to fast objects viewed from a moving humanoid camera.
- Separates control, dynamics inference, and visual learning, with direct supervision for each stage.
- Reports real G1 catch success from onboard RGB-D without external box measurements.

**Quantitative results:**

| Benchmark / Task | Metric | Value | Context |
|---|---|---|---|
| Simulated box catching | Catch success | 85.7% | RGB-D; 3290/3840 throws across six controllers |
| Simulated box catching, privileged reference | Catch success | 87.9% | Same decoder; privileged box input and visual input have different fields of view |
| Real G1, regular box | Catch success | 65% / 40% / 15% | Throw distances 2.5 / 5 / 7 m; 20 trials per condition |
| Real downstream sequence | Cumulative success | 65% / 35% / 30% / 25% | After catching / carrying / handover / return; 20 trials |

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Onboard vision and whole-body response address dynamic object interaction. Evidence focuses on box catching and limited downstream tasks. |
| Delta contribution | 7.0 | Extends fixed-decoder latent regression to fast objects and moving cameras. Core learning tools are established, and concurrent work also studies visual humanoid box catching. |
| Method quality | 8.0 | Separate stages and direct supervision connect control and perception. The learned latent does not preserve box size, which limits retention strategies. |
| Effectiveness | 7.0 | Strong simulation results and real G1 catches support the approach. Small real trial counts, long distances, and low downstream success limit practical evidence. |
| Gap support | 7.3 | Real RGB-D catches connect whole-body control, fast dynamics inference, and onboard vision. Size and distance limits leave the broader capability gap only partly addressed. |

**Overall score:** 7.4/10.

**Limitations/Gaps:**

- The latent does not preserve box size. Small and large boxes often make contact but are not retained.
- Visual training uses throws from 3.0–3.5 m. Performance falls for longer, faster throws.
- Real evaluation has 20 trials per condition. The 95% Wilson intervals span up to about ±20 percentage points.
- Catch success does not establish a settled posture. Torso excursion varies substantially across visual controllers.
- The full downstream sequence succeeds in 25% of 20 trials.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** —.
- **Deployment hardware:** Unitree G1 with a torso-mounted RGB-D camera. The controller uses robot state, without box pose, box velocity, or external-camera measurements.

## Dataset / Data Collection

- **Control training:** Simulated state-based PPO followed by action-labeled data aggregation and latent-controller PPO.
- **Visual training:** Simulated RGB-D and ego-motion histories, with privileged latent targets and auxiliary box position/velocity targets; visual-policy data aggregation.
- **Evaluation data:** Six controllers with 640 held-out throws each for the initialization comparison; real G1 evaluation uses 20 trials per condition.

**Source:** [Paper text](https://arxiv.org/html/2610.12772v1), abstract and sections I–V.
