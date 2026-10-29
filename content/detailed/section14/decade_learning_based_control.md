### A Decade of Learning-Based Control: From Theoretic Foundations to Practical Deployment

**Full title:** A Decade of Learning-Based Control: From Theoretic Foundations to Practical Deployment

**Authors:** Angela P. Schoellig et al.

**Venue/Year:** — / 2026

**arXiv:** [2610.29187v1](https://arxiv.org/abs/2610.29187v1)

**Architecture:** Tutorial on learning-based control. Connects control theory, dynamics learning, direct data-driven control, and policy learning.

**Key methodology:** Starts with a common nonlinear control problem and concepts for stability and safety. Reviews dynamics learning, direct data-driven control, reinforcement learning (RL), imitation learning (IL), and Bayesian optimization (BO). Table I connects learning objectives, prior knowledge, estimation errors, uncertainty models, controller design, and closed-loop guarantees. These guarantees depend on the assumptions of each method.

**Robot / Tasks:** —

**Main contributions:**

- Connects method families through uncertainty and closed-loop guarantees, complementing surveys of individual research areas.
- Uses Table I to relate learning methods to compatible control designs and representative guarantees.
- Shares implementations, illustrative examples, and tutorial resources to support practical exploration.

**Quantitative results:** —. The source excerpt does not report a quantitative comparison of control performance for this tutorial.

**AI research assessment:** Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Safety, reliability, and data costs matter for robot deployment. The tutorial's direct effect on deployment remains uncertain. |
| Delta contribution | 6.0 | Connects separate research areas through uncertainty and closed-loop guarantees. The contribution is a synthesis of knowledge. |
| Method quality | 6.7 | Connects learning objectives, prior knowledge, uncertainty, controllers, and guarantees. Representative methods, state feedback, and offline learning limit the scope. |
| Effectiveness | 6.0 | Table I connects method requirements and guarantees to support design choices. Improvements in method selection or deployment are not established. |
| Gap support | 7.0 | A common problem formulation and comparison table connect learning flexibility with control guarantees. Coverage is selective. |

**Overall score:** 6.5/10.

**Limitations/Gaps:**

- Covers representative directions motivated by the CDC Learning-Based Control Invited Sessions. Coverage is not exhaustive.
- Focuses on state feedback and offline learning. Output measurements, state estimation, and online learning receive selective treatment.
- Table I gives representative control methods and closed-loop guarantees, rather than a complete list.
- A research gap is how combined estimation, learning, and control change guarantee conditions with output measurements and online learning.

**Open weights/code:** — / —.

**Tutorial resources:** [Implementations, examples, and additional resources](https://learning-based-control.github.io/tutorial/).

## Inference / Deployment

- **Inference latency:** —
- **Deployment hardware:** —

## Dataset / Data Collection

- **Training data:** —
- **Evaluation data:** —

**Source:** [Paper text](https://arxiv.org/html/2610.29187v1), abstract and available body excerpt, including Table I.
