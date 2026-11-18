## 3.21 ForceHarness

- **Full title:** ForceHarness: Turning Force into Action and Physics for Frozen Frontier Models
- **Authors:** Ke Sun, Kevin Yuchen Ma, Yike Zhang, Yanzhe Chen, Mike Zheng Shou
- **Group:** Show Lab, National University of Singapore
- **Venue/Year:** arXiv preprint, 2026
- **arXiv:** [2611.21099v1](https://arxiv.org/abs/2611.21099v1)

**Force/tactile input type:** Calibrated force from a wrist F/T sensor or external joint torques. The real robot uses joint torques without a wrist F/T sensor.

**Force/impedance output:** The model selects force primitives and their parameters. Each primitive regulates force through target poses and the robot's existing impedance controller. This is active force regulation beneath the model.

**Robot platform:** Franka FR3 with a parallel gripper, a wrist RGB-D camera, and an exterior RGB camera.

**Tasks:** Six real tasks: wipe a whiteboard, drive a screw, peel an eggplant, insert a USB plug, sort bottles by weight, and tell soft objects from hard objects. Simulation uses eight ForceBench tasks and seven HiddenPhys tasks.

**Key methodology:** Three layers connect a frozen model to the robot without demonstrations or fine-tuning. Force calibration removes offsets and uses readings taken at rest. Self-terminating force primitives use admittance control and stop at contact events, goals, force caps, or time limits. A physics translation layer returns physical quantities, uncertainty estimates, and status flags from each force trace. The model reads each result and selects the next action.

**Architecture/Parameters:** An API-only frozen model calls tools above the force-control loop. The framework has twelve force primitives and ten other tools. Model architecture and parameter counts: —.

**Main contributions:**

- Combines force calibration, self-terminating control, and physical feedback without model training.
- Adds HiddenPhys, a seven-task MuJoCo benchmark with hidden physical variables, expert force controllers, and learned policies.
- Evaluates the system on a real arm without a wrist F/T sensor and on two simulation benchmarks.

**Quantitative results:** GPT-6 Astra with ForceHarness versus the same model without force.

| Benchmark / Task | Metric | Without force | ForceHarness | Context |
|---|---|---|---|---|
| Franka FR3, six tasks | Success rate | 3.3% (2/60) | 90.0% (54/60) | Same instructions; 10 episodes per task and condition |
| ForceBench, eight tasks | Mean success rate | 70.0% | 87.5% | First 10 seeds; tools and thresholds tuned on eight of these seeds |
| HiddenPhys, seven tasks | Successful episodes | 87/140 | 135/140 | Same 20 test seeds per task; ForceHarness has zero handle-damage episodes |

**AI research assessment:** Mean scores from three AI reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Connects frozen models to contact control without fine-tuning or a wrist sensor on the real robot. Model delays limit fast coordination. |
| Delta contribution | 7.0 | Integrates force control and calibrated physical feedback beyond raw readings or generated control code. Components use existing methods; no direct FORCA comparison is reported. |
| Method quality | 8.0 | Separates fast contact control from slow model decisions. Feedback ablations support the design, but only in simulation. |
| Effectiveness | 7.7 | Real-robot and HiddenPhys comparisons show clear gains. ForceBench tuning on evaluation seeds and different learned-baseline protocols limit generalization claims. |
| Gap support | 7.3 | Success and ablations support force use without training. Physical feedback benefits depend on the model; fast reactive coordination remains unresolved. |

**Overall score:** 7.6/10.

**Limitations/Gaps:**

- Model calls take seconds between primitives. The fixed primitive menu limits new motion laws and reactive coordination.
- Ablations run only in simulation. Real-robot trials use 10 episodes per task and condition.
- ForceBench tools and perception thresholds were tuned on eight of ten evaluation seeds. Stove Press and Nut Thread were revised after initial runs. Some public success checks omit release or clearance.
- ForceBench learned-baseline results are cited rather than reproduced. Their demonstrations, inputs, instructions, and evaluation counts differ, so their performance gap does not isolate the effect of force.
- HiddenPhys gives frozen models noisy object poses rather than images. Under OOD shifts, only frozen models receive instructions with the changed ranges.
- Physical-quantity feedback helps smaller models more; GPT-6.1 Sol also performs well with raw force numbers.

**Open weights/code:** — / —.

## Inference / Deployment

- **Inference latency:** Model decisions take seconds; exact latency: —.
- **Deployment hardware:** Franka FR3 and cameras as listed above. Compute hardware: —.
- **Real-time capable?** Primitives regulate contact beneath the model. Model calls prevent fast reactive coordination between primitives.

## Dataset / Data Collection

- **Training data:** ForceHarness requires no demonstrations or fine-tuning. Learned baselines on HiddenPhys use about 200 demonstrations per task.
- **Evaluation data:** Six real tasks, eight ForceBench tasks, and seven HiddenPhys tasks with hidden physical variables.
- **Data format / public availability:** — / —.

**Source:** [Paper text](https://arxiv.org/html/2611.21099v1), sections 1–5 and limitations.
