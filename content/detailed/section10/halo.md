# 10.12 HALO

- **Full title:** HALO: Human-Aligned Data Collection for WhoLe-body MObile Manipulation
- **Authors:** Shuai Yang, Fangyi Xu, Yishu Shen, Kecheng Zheng, Yinghao Xu (HKUST / Robbyant)
- **Venue/Year:** arXiv preprint, November 2026
- **arXiv:** [2611.16439v1](https://arxiv.org/abs/2611.16439v1)
- **Input modality:** Kinesthetic teaching and natural operator movement on a low-resistance passive platform
- **Target hand:** Redesigned bimanual grippers
- **Force feedback:** Direct physical feedback during kinesthetic teaching
- **Cost:** —

## Key methodology/design

The operator directly guides the robot end-effectors and moves a passive platform while teaching bimanual manipulation. The powered base is removed during collection. The platform preserves the nonholonomic motion constraints of the AgileX Tracer AGV 2 differential-drive base used during deployment.

CaRE-Ego, SAM2, and DiffuEraser segment, track, and remove the demonstrator's hands from recorded images. Base velocity calibration and response-delay correction align platform motion with deployment commands. The system uses fine-tuning of π0.5 on the processed demonstrations and asynchronous real-time action chunking (RTC) for execution.

## Main contributions

- Combines direct manipulation feedback with natural operator movement for whole-body demonstrations.
- Processes images and base actions to reduce differences between collection and autonomous deployment.
- Evaluates collection efficiency and learned policies against Mobile ALOHA and VR teleoperation.

## Quantitative results

Collection is limited to one hour per task, including resets and object preparation. The collection comparison uses one operator with no prior experience with the evaluated interfaces.

| Task / Setting | Metric | Result | Context |
|---|---|---|---|
| Push Chair demonstration collection | Collection speedup | 2.9× | Compared with Mobile ALOHA under matched collection conditions |
| Disassemble Lego | Policy success rate | 75.0% | 30/40 trials |
| Six-stage mobile box manipulation | Policy success rate | 73.3% | 11/15 trials |
| Zip-Tie Fastening | Succ. Rate | 30.0% | 10 trials |
| Push Chair hand-removal ablation | Success Rate | 55% → 85% | Same demonstrations; asynchronous inference with execution horizon 8 |

## AI research assessment

Mean scores from three AI reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Addresses the collection of coordinated mobility and bimanual demonstrations. Benefits beyond the evaluated tasks and platform remain uncertain. |
| Delta contribution | 7.0 | Replaces separated leader–follower control with direct teaching and a passive platform. Policy and visual processing use existing methods. |
| Method quality | 7.7 | Matches motion constraints and corrects visual and control differences. The separate effect of base calibration is not established. |
| Effectiveness | 6.7 | Policy results and the hand-removal ablation support practical use. Zip-Tie Fastening succeeds in only 30.0% of 10 trials. |
| Gap support | 7.0 | Matched collection conditions and the visual ablation support the alignment claim. One operator limits evidence across users. |

**Overall score:** 7.2/10.

## Limitations/Gaps

- Collection efficiency is compared with one operator; performance across operators is not established.
- Zip-Tie Fastening succeeds in only 30.0% of 10 trials. Sub-millimeter accuracy is a task requirement, not a separately measured accuracy result.
- Hardware evaluation uses one differential-drive base and a platform with matching motion constraints.
- The target table is fixed during Push Chair collection. Active perception is future work.

## Data quality impact

Hand removal reduces visual differences between demonstrations and autonomous execution. Base calibration and temporal alignment account for differences between passive collection and powered deployment. The Push Chair ablation supports hand removal; the separate effect of base calibration is not established.

## Open-source status

Code / weights: — / — (not reported). [Project page](https://robbyant-research.github.io/Lingbot-ALOHA/).

**Source:** [Paper text](https://arxiv.org/html/2611.16439v1), sections 3–5 and appendix B.
