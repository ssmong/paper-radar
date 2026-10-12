# 9.10 BiGym 2.0

- **Full title:** BiGym 2.0: Benchmarking Learned and Agent-Developed Policies for Humanoid Household Manipulation
- **Authors:** Zexi Zhang, Zecheng Zhu, Zidong Chen, Zulkhuu Tuya, Stephen James
- **Venue/Year:** — / 2026 ([arXiv 2610.07594v2](https://arxiv.org/abs/2610.07594v2))
- **Sim platform:** MuJoCo
- **Dexterous support:** Unitree G1 with two Dex1 parallel grippers
- **Tasks:** 20 household tasks in reaching, tabletop, dishwasher, and kitchen-counter scenes
- **Demonstrations:** 60 successful human VR demonstrations per task; 1,200 episodes in total
- **Evaluation:** Success rates on nine representative tasks for VLA fine-tuning, imitation learning, demonstration-driven RL, and coding-agent programs

## Key methodology/design

BiGym 2.0 adapts BiGym to household manipulation with the Unitree G1. Human VR demonstrations and policy evaluation use the same frozen GR00T-WBC walking and balance controller. Policies receive three onboard RGB camera views and robot proprioception. They send arm, gripper, and body commands through a common interface. Evaluation resets restore simulator and controller state.

## Main contributions

- 20 household tasks adapted to the G1 workspace and walking dynamics
- Human VR demonstrations with synchronized camera views and full-body execution records
- A common execution interface for learned policies and programs developed by coding agents
- Controller-state restoration for repeatable evaluation

## Limitations/Gaps

- All evaluations use simulation with one frozen whole-body controller per robot. Physical deployment and other controllers are not evaluated.
- Coding agents receive one demonstration per task; learned policies train on 60.
- VLA fine-tuning uses one training run per task. The other learned methods use three runs.
- Cross-task reuse of verified programs and skills is not evaluated.
- Cross-workspace stacking remains an open challenge. Multi-object transport remains difficult for imitation learning, demonstration-driven RL, and coding-agent programs.

## Coverage gaps

| Criterion | Covered? |
|-----------|----------|
| Force/torque evaluation metrics | — (not reported) |
| Deformable object tasks | — (not reported) |
| Tactile sensing | — (not reported) |
| Multi-stage / long-horizon tasks | Yes (cross-workspace block stacking; remains an open challenge) |
| Multi-hand coordination | Yes (dual reaching and bimanual manipulation) |

## Open-source status

The source reports that environments, human demonstrations, and evaluation traces are open-source. GitHub: [swirl-uk/BiGym2](https://github.com/swirl-uk/BiGym2). Installation command and policy-weight availability: — (not reported).
