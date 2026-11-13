# Ropedia Xperience 2

- **Full title:** Ropedia Xperience 2: A Gold Standard for Scaling Physical AI Environments and Behaviors
- **Authors:** Hao Li et al.
- **Venue/Year:** arXiv / 2026
- **Paper:** [2611.17060v1](https://arxiv.org/abs/2611.17060v1)
- **Released scans:** 1,589 metric-scale 3D scans and their reconstructions.
- **Collection inventory:** 4,230 egocentric recordings of 74 tasks, totaling 131 h. These counts describe the collection, not a verified set of released, registered recordings.
- **Modalities:** Egocentric RGB, LiDAR scene scans, camera trajectories, depth, estimated hand and body motion, and hierarchical language captions.

## Key methodology/design

One operator first scans a scene with a handheld LiDAR scanner, then records tasks with the HOMIE head-mounted recorder. Collection requires no robot or motion-capture system on site. The processing pipeline produces scene meshes and 3D Gaussian representations. It also estimates camera trajectories and human motion and generates language annotations.

SIFT, RANSAC, PnP, and robust Umeyama alignment register recordings to the scene. Held-out frames, IMU gravity consistency, and an ICP check assess the alignment. The estimated body motion uses SMPL-H with 52 body and finger joints at 30 Hz.

## Main contributions

- Extends Xperience-10M with metric scene scans and scene–recording registration.
- Shows four reuse routes: Real-to-Sim, human–robot retargeting, virtual teleoperation, and long-horizon trajectory generation.
- Uses scan reconstructions as reference geometry for depth and geometry estimation, 3D object detection, and spatial reasoning benchmarks.

## Reported results

Retargeting uses four recordings from one scene, totaling 10.3 min of motion. The recordings are slowed down 2×. Median fingertip error is 0.40–0.55 cm; 95th-percentile error is below 2 cm.

In one converted home scene, all 30 held-out rollouts complete one task with eight consecutive subtasks without breaking a task rule. Each subtask uses a policy program and a whole-body controller. This result shows trajectory generation; it does not establish general policy learning gains across scenes and tasks.

## AI research assessments

Mean scores from three reviewers, on a 10-point scale.

| Dimension | Score | Reason |
|---|---|---|
| Importance | 8.0 | Joint environment and behavior collection can support robot learning without on-site robots. The size of learning and collection-cost benefits remains uncertain. |
| Contribution beyond prior work | 7.0 | Metric scans and scene–recording registration extend Xperience-10M. The pipeline combines existing alignment and motion estimation methods. |
| Method quality | 7.0 | Separate capture devices and geometric alignment checks suit the data collection problem. A single transform cannot correct local SLAM drift. |
| Effectiveness | 6.0 | Retargeting and 30 successful eight-subtask rollouts show reuse. Evaluation uses one scene for retargeting and one task for long-horizon generation. |
| Support for addressing the research gap | 6.0 | Four reuse routes partly address the lack of joint environment and behavior resources. The extent of released, registered recordings and policy learning gains remains uncertain. |

**Overall score:** 6.7/10.

## Limitations/Gaps

- Released scans mainly cover home interiors. Reuse-grade scans can have partial coverage or reconstruction defects.
- Release grades include overrides and decisions on conflicting quality labels. They do not mean that all scans passed the same visual and geometric checks.
- Separate scans can show the same physical space. Recording counts and duration describe the broader collection inventory.
- A single registration transform cannot correct local SLAM drift. Unobserved body parts, especially legs, are inferred from a motion prior.
- Retargeting uses slowed recordings from one scene. Long-horizon generation covers one task in one home scene. General policy learning gains remain uncertain.

## Availability

- **Dataset download:** —. The paper reports 1,589 released scans; no download address is reported in the source text.
- **Code / weights:** — / —.

**Source:** [Paper text](https://arxiv.org/html/2611.17060v1), sections 2–6.
