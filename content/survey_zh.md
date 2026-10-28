# Contact-Rich Dexterous Manipulation：综合综述

> 最后更新: 2026-05-14
> 范围：dexterous manipulation、力感知VLA、impedance学习、RL策略及相关benchmark的论文、代码仓库和数据集（2018-2026年）。
> GitHub链接和权重可用性截至综述日期已验证；链接可能会失效。
>
> **标记说明：** ✅ = 可用/支持, ✗ = 不可用/不支持, — = 未报告或不适用。

**目的。** 本综述围绕三条研究主线的交叉展开：(1) dexterous多指manipulation，(2) 视觉-语言-动作模型，(3) 力/impedance感知控制。旨在梳理现有系统提供了哪些能力，以及哪些能力组合尚未充分探索，从而确定这些交叉领域的开放研究方向。范围特意聚焦于这三个领域；移动manipulation、工业自动化等相邻主题仅在与本综述核心主题交叉时涉及。

---

## 1. Dexterous工具使用与Manipulation

使用多指手系统执行grasping、工具使用或超越parallel-jaw gripper的物体manipulation。

| 论文 | 研究组 | 会议 | 年份 | 手部(自由度) | 任务 | Sim Platform | Sim2Real | 代码 | 权重 | VLA/Lang |
|---|---|---|---|---|---|---|---|---|---|---|
| [**SimToolReal**](https://arxiv.org/abs/2602.16863) | Stanford IPRL | arXiv | 2026 | Sharpa (22) + KUKA | 24个工具使用任务（锤子、螺丝刀、铲子） | IsaacGym | Yes | [GitHub](https://github.com/tylerlum/simtoolreal) ✅ | ✅ ckpt | ✗ |
| [**Grasp-to-Act**](https://arxiv.org/abs/2602.20466) | UIUC RoboTouch | arXiv | 2026 | LEAP (16) | 5个动态工具使用任务（锤子、锯、切割、搅拌、舀取） | Sim + real | Yes | ✗ | ✗ | ✗ |
| [**DexMachina**](https://arxiv.org/abs/2505.24853) | Stanford/NVIDIA | arXiv | 2025 | Inspire, Allegro, Xhand, Schunk | Bimanual铰接物体manipulation | Genesis | ✗ | [GitHub](https://github.com/MandiZhao/dexmachina) ✅ | ✗ (eval TODO) | ✗ |
| [**ManipTrans**](https://arxiv.org/abs/2503.21860) | BIGAI/Tsinghua/PKU | CVPR | 2025 | 4种手（Shadow, MANO, Inspire, Allegro） | Bimanual任务（笔帽、瓶盖旋拧） | IsaacGym P4 | ✗ | [GitHub](https://github.com/ManipTrans/ManipTrans) ✅ | ✅ imitator ckpt + HF | ✗ |
| [**SPIDER**](https://arxiv.org/abs/2511.09484) | Meta FAIR / Berkeley | arXiv | 2025 | 9种humanoid机器人 | 重定向的人类演示 | MuJoCo | ✅ (Franka+Allegro) | [GitHub](https://github.com/facebookresearch/spider) ✅ | ✗ | ✗ |
| **Scaffolding+VLM** | Stanford / KIT | NeurIPS | 2025 | Allegro (16) + KUKA | 铰接物体（苹果、瓶子、抽屉） | Sim + real | Yes | [GitHub](https://github.com/vdebakker/vlm-scaffolding) ✅ | ✗ | ✅ Gemini VLM |
| [**DexUMI**](https://arxiv.org/abs/2505.21864) | Stanford | CoRL Best Paper Finalist | 2025 | XHand, Inspire | 真实世界dexterous manipulation | 仅真实 | N/A | [GitHub](https://github.com/real-stanford/DexUMI) ✅ | ✗ | ✗ |
| [**DexterityGen**](https://arxiv.org/abs/2502.04307) | Berkeley/Meta | RSS | 2025 | Allegro (16) + 机械臂 | 工具使用（笔、螺丝刀、注射器） | IsaacGym | ✅ | ✗ | ✗ | ✗ |
| [**ArtiGrasp**](https://arxiv.org/abs/2309.03891) | ETH Zurich | 3DV | 2024 | MANO（人类代理） | Bimanual grasping + 铰接manipulation（8个物体） | RaiSim | ✗ | [GitHub](https://github.com/zdchan/artigrasp) ✅ | ✅ pretrained | ✗ |
| [**DexDeform**](https://arxiv.org/abs/2304.03223) | MIT-IBM | ICLR | 2023 | 多指（仿真） | 6个deformable物体任务（橡皮泥） | PlasticineLab | ✗ | [GitHub](https://github.com/sizhe-li/DexDeform) ✅ | ✗ | ✗ |

---

## 2. Dexterous VLA / 视觉-语言-动作

支持dexterous hand或语言条件dexterous manipulation的VLA模型。

| 论文 | 研究组 | 会议 | 年份 | 手部(自由度) | 任务 | 代码 | 权重 | 核心方法 |
|---|---|---|---|---|---|---|---|---|
| [**UniDex-VLA**](https://arxiv.org/abs/2603.22264) | UniDex-AI | CVPR | 2026 | 通过FAAS支持8种手（Allegro, LEAP, Shadow, Inspire, Wuji, Oymotion, Ability, Xhand） | 工具使用，81%任务进度 | [GitHub](https://github.com/unidex-ai/UniDex) ✅ | ✅ 3-epoch + 32-epoch on HF | 3D VLA + flow matching, FAAS统一动作 |
| [**DexGraspVLA**](https://arxiv.org/abs/2502.08142) | Psi-Robot | AAAI | 2026 | 定制dexterous hand | 杂乱场景grasping，90%+成功率 | [GitHub](https://github.com/Psi-Robot/DexGraspVLA) ✅ | ✅ controller ckpt (GDrive) | Qwen2.5-VL-72B规划器 + diffusion控制器 |
| [**DexVLA**](https://arxiv.org/abs/2502.05855) | Multi-inst. | CoRL | 2025 | Yes（课程式） | Dexterous技能学习 | [GitHub](https://github.com/juruobenruo/DexVLA) ✅ | ✅ ScaleDP-H/L on HF | 在冻结VLM上的插件式1B diffusion专家 |
| **Dexora** | Multi-inst. | ICRA | 2025 | Bimanual 36自由度 | Grasping放置、dexterous manipulation、装配、工具使用 | [GitHub](https://github.com/ZZongzheng0918/Dexora) ✅ | ✅ real data on HF | 12.2K真实 + 100K仿真数据 |
| [**Grasp as You Say**](https://arxiv.org/abs/2405.19291) | Sun Yat-sen | NeurIPS | 2024 | Shadow (24) | 语言引导grasping（"抓住杯子把手"） | [GitHub](https://github.com/iSEE-Laboratory/Grasp-as-You-Say) ✅ | ✗ | 语言条件dexterous grasp生成 |
| [**HumanoidGen**](https://arxiv.org/abs/2507.00833) | TeleHuman | NeurIPS | 2025 | Unitree H1_2 + Inspire (每手6自由度) | 20个桌面任务（bimanual、长时程） | [GitHub](https://github.com/TeleHuman/HumanoidGen) ✅ | ✅ HF (model + data) | LLM规划器 + MCTS + diffusion策略 |
| [**VLA+Diffusion Switch**](https://arxiv.org/abs/2410.14022) | — | arXiv | 2024 | ADAPT Hand (13) | 使用VLA切换的grasp放置 | ✗ | ✗ | VLA + diffusion策略切换，基于串联弹性多指手 |

---

## 3. 力感知VLA / Tactile VLA

融合force/torque或tactile感知用于contact-rich任务的模型。若系统使用VLM/VLA backbone或语言条件则归入此处；否则，不含VLM backbone的力/impedance系统归入§5。

| 论文 | 研究组 | 会议 | 年份 | 力输入 | Force/Impedance Output | 机器人 | 代码 | 权重 | 任务 |
|---|---|---|---|---|---|---|---|---|---|
| [**ForceVLA**](https://arxiv.org/abs/2505.22159) | SJTU/Fudan | NeurIPS | 2025 | 六轴F/T | ✗（仅位置） | Flexiv Rizon + gripper | [GitHub](https://github.com/ft-robotic/ForceVLA) ✅ | ✗ (data on HF) | 插件插入、擦拭、剥离（5个任务） |
| [**ForceVLA2**](https://arxiv.org/abs/2603.15169) | Shanghai AI Lab | CVPR | 2026 | 六轴F/T 300Hz | ✅ 混合力/位置 + 预测力 | Flexiv Rizon 4s + gripper | ✗ "coming soon" | ✗ | 按压、清洁、组装齿轮（5个任务） |
| [**FD-VLA**](https://arxiv.org/abs/2602.02142) | NUS | ICRA | 2026 | 蒸馏式（inference时无传感器） | ✗ | UR5e + gripper | ✗ | ✗ | 擦拭、插入、按钮按压（3个任务） |
| [**FAVLA**](https://arxiv.org/abs/2602.23648) | USTC | arXiv | 2026 | 六轴F/T高频 | ✗ | Monte bimanual X-ARM | ✗ | ✗ | USB插入、齿轮、擦拭（4个任务） |
| [**HapticVLA**](https://arxiv.org/abs/2603.15257) | Skoltech | arXiv | 2026 | Tactile（蒸馏移除） | ✗ | LeRobot SO-101 + tactile | 论文声称将发布；截至2026年5月未找到公开仓库 | 未验证 | 罐子/华夫饼/鸡蛋grasp放置 |
| [**DreamTacVLA**](https://arxiv.org/abs/2512.23864) | Northwestern | arXiv | 2025 | Tactile (V-JEPA2) | ✗ | Dobot Xtrainer + gripper + tactile | [GitHub](https://github.com/michaelyeah7/learning-to-feel-the-future)（仅代码） | ✗ | Tactile世界模型预测未来潜在表征→动作优化；4个contact-rich任务最高95% |
| [**OmniVTLA**](https://arxiv.org/abs/2508.08706) | - | arXiv | 2025 | 视觉tactile + 力觉tactile | ✗ | Gripper + dexterous hand | ✗（仅数据集） | ✗ | Grasp放置（dexterous hand 100%） |
| [**Tactile-VLA**](https://arxiv.org/abs/2507.09160) | Tsinghua | arXiv | 2025 | Tactile | ✅ 混合位置-力 | 未指定 | ✗ | ✗ | 充电器插入90% |
| [**TaF-VLA**](https://arxiv.org/abs/2601.20321) | - | arXiv | 2026 | GelSight + 六轴F/T | ✗ | Franka FR3 + gripper | ✗ | ✗ | 8个contact-rich任务 |
| [**TA-VLA**](https://arxiv.org/abs/2509.07962) | Tsinghua AIR | CoRL | 2025 | 关节torque | 辅助torque预测 | Cobot Magic ALOHA | ✗ | ✗ | 10个任务（按钮、充电器、USB…） |
| [**CRAFT**](https://arxiv.org/abs/2602.12532) | - | arXiv | 2026 | 力 | ✗ | Teleoperation机械臂 | ✗ | ✗ | Deformable物体、对准任务 |
| [**VLA-Touch**](https://arxiv.org/abs/2507.17294) | NUS | arXiv | 2025 | GelSight tactile | ✗（残差修正） | 机械臂 + gripper | [GitHub](https://github.com/jxbi1010/VLA-Touch) ✅ | ✅ ckpts + HF | Contact-rich manipulation |
| [**FoAR**](https://arxiv.org/abs/2411.15753) | SJTU | RA-L/IROS 2025 | 2024 | 六轴F/T | ✗ | Flexiv Rizon + gripper | [GitHub](https://github.com/Alan-Heoooh/FoAR) ✅ | ✗ | 擦拭、剥离 |
| [**FACTR**](https://arxiv.org/abs/2502.17432) | CMU | RSS | 2025 | 关节torque（伺服电流） | ✗ | Franka + gripper | [GitHub](https://github.com/RaindragonD/factr) ✅ | ✗（仅编码器） | 箱子提升、旋转、面团擀制 |
| [**ForceMimic**](https://arxiv.org/abs/2410.07554) | SJTU | ICRA | 2024 | 捕获的交互torque | ✅ Torque-位置混合 | Flexiv + gripper | [GitHub](https://github.com/ForceMimic/hybridil) ✅ | ✗ | 蔬菜削皮 |
| [**Reactive Diffusion Policy**](https://arxiv.org/abs/2503.02881) | - | RSS | 2025 | GelSight Mini | ✗（学习到的"类impedance"） | Flexiv Rizon 4 + gripper | [GitHub](https://github.com/xiaoxiaoxh/reactive_diffusion_policy) ✅ | ✅ ckpts + HF | 3个contact-rich任务 |
| [**ACP**](https://arxiv.org/abs/2410.09309) | Toyota/Columbia | ICRA | 2024 | 六轴F/T (ATI) | ✅ 标量stiffness (K) | UR5e + 被动工具 | ✗ | ✗ | 物品翻转、花瓶擦拭 |
| [**TacDiffusion**](https://arxiv.org/abs/2409.11047) | TU Munich MIRMI | ICRA | 2024 | Tactile | ✅ 6D torque | Gripper + tactile | [GitHub](https://github.com/popnut123/TacDiffusion) ✅ | ✗ | 力域diffusion，95.7% zero-shot |
| [**FARM**](https://arxiv.org/abs/2510.13324) | TU Munich MIRMI | arXiv | 2025 | GelSight Mini | ✅ grip force | 改装UMI gripper | ✗ | ✗ | 关节位置 + 力预测 |
| [**T-Dex**](https://arxiv.org/abs/2303.12076) | NYU (Pinto) | ICRA | 2024 | Tactile (DIGIT) | ✗（仅位置） | **Allegro (16) + DIGIT** + Kinova机械臂 | [GitHub](https://github.com/irmakguzey/tdex) ✅ | ✗ | 5个dexterous任务（操纵杆、书本、碗、销钉、橡皮泥）；比纯视觉提升1.7倍。§3中极少数使用dexterous hand的工作之一。 |

---

## 4. VLM引导的Impedance控制

由VLM/LLM生成或检索impedance参数（K, D）用于底层控制器的系统。

| 论文 | 研究组 | 会议 | 年份 | K/D适应方式 | Stiffness (K) | Damping (D) | 机器人 | Dex Hand? | 代码 | 权重 |
|---|---|---|---|---|---|---|---|---|---|---|
| [**CompliantVLA-adaptor**](https://arxiv.org/abs/2601.15541) | IIT Genoa / TU Darmstadt | arXiv | 2026 | VLM (GPT-4o-mini) zero-shot | ✅ (Kx,Ky,Kz) | ✅ (Dx,Dy,Dz) | Franka Panda + gripper | ✗ | 项目主页（待发布） | ✗（免训练） |
| [**OmniVIC**](https://arxiv.org/abs/2510.17150) | IIT Genoa / Georgia Tech | arXiv | 2025 | VLM + RAG自改进 | ✅ | ✅ | Franka Panda + F/T传感器 | ✗ | ✗ | ✗（使用GPT-4o-mini API） |
| [**HumanoidVLM**](https://arxiv.org/abs/2601.14874) | - | HRI | 2026 | VLM (Molmo-7B) + FAISS RAG | ✅（检索） | ✅（检索） | Unitree G1 humanoid | ✗ | ✗ | ✗ |
| **SafeHumanoid** | 同一团队 | HRI | 2026 | VLM + RAG检索 | ✅ | ✅ | Unitree G1 | ✗ | ✗ | ✗ |
| [**ImpedanceGPT**](https://arxiv.org/abs/2503.02723) | - | IROS | 2025 | VLM (Molmo) + RAG | ✅ | ✅ | 无人机群（非manipulation） | N/A | [GitHub](https://github.com/Faryal-Batool/ImpedanceGPT) ✅ | ✗ |

---

## 5. 学习型Impedance / Variable Compliance控制

不使用VLM backbone而学习或优化impedance/stiffness/damping参数的系统。VLM驱动的impedance方法见§4。仅以力作为输入但输出位置的论文（如FoAR、FACTR）归入§3。

| 论文 | 研究组 | 会议 | 年份 | Stiffness (K) | Damping (D) | 学习方法 | 机器人 | Dex Hand? | 仿真 | 代码 | 权重 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [**Comp-ACT**](https://arxiv.org/abs/2406.14990) | OMRON SINIC X / UTokyo | IROS | 2024 | ✅ (12D Cholesky) | ✗ | IL（基于VR演示的ACT） | 2x UR5e + gripper | ✗ | Robosuite (MuJoCo) | [GitHub](https://github.com/omron-sinicx/CompACT) ✅ | ✗ |
| [**Diff-Impedance**](https://arxiv.org/abs/2509.19696) | KIT / MIT | arXiv | 2025 | ✅ | ✅ | Diffusion + 基于能量的方法 | KUKA LBR iiwa | ✗ | Sim + real | [GitHub](https://github.com/StrokeAIRobotics/DiffusionBasedImpedanceLearning) ✅ | ✗ |
| [**VICES**](https://arxiv.org/abs/1906.08880) | Stanford / NVIDIA | IROS | 2019 | ✅ | ✅ | RL（策略梯度） | Franka/Sawyer + gripper | ✗ | Robosuite (MuJoCo) | [robosuite/vices](https://github.com/ARISE-Initiative/robosuite/tree/vices_iros19) ✅ | ✗ |
| [**CHIP**](https://arxiv.org/abs/2512.14689) | NVIDIA NVLabs | ICRA | 2025 | ✅（end-effector stiffness） | ✗ | RL（事后扰动） | Humanoid 35自由度 | ✗ | Isaac Sim | [Page](https://nvlabs.github.io/CHIP/) | ✗ |
| [**FILIC**](https://arxiv.org/abs/2509.17053) | Tsinghua/HKUST | arXiv | 2025 | 固定K | 固定B | IL（transformer，25Hz） | AIRBOT Play | ✗ | MuJoCo + real | [GitHub](https://github.com/OpenGHz/FILIC) ✅ | ✗ |
| [**CHEQ**](https://arxiv.org/abs/2501.07985) | RWTH Aachen | arXiv | 2025 | ✅ | ✅ | RL（混合自适应） | 机械臂（抛光） | ✗ | 真实硬件 | ✗ | ✗ |
| [**DA-VIL**](https://arxiv.org/abs/2410.19712) | IIIT/Brown | ICRA | 2024 | ✅ | 未报告 | RL + QP优化 | Bimanual | ✗ | Sim | 仅项目主页 | ✗ |
| [**DexForce**](https://arxiv.org/abs/2501.10356) | Stanford | RA-L | 2025 | 固定k_f | ✗ | 手动调参 | Allegro (16) | **✅** | ✗（仅真实） | ✗ | ✗ |
| [**Force Policy**](https://arxiv.org/abs/2602.22088) | SJTU/Flexiv | RSS | 2026 | 力目标 | ✗ | IL（teleoperation演示） | Flexiv + gripper | ✗ | ✗（仅真实） | ✗ | ✗ |
| [**IndustReal**](https://arxiv.org/abs/2305.17110) | NVIDIA | RSS | 2023 | 固定 | 固定 | RL (PPO) 学习位姿 | Franka + gripper | ✗ | IsaacGym | [GitHub](https://github.com/NVlabs/industreallib) ✅ | ✅ RL policies |
| [**Divide et Impera**](https://arxiv.org/abs/2410.01054) | MIT/KIT | arXiv | 2024 | ✅（参数族） | ✅ | 神经网络成功率预测器 | 真实机械臂 | ✗ | Real | ✗ | ✗ |
| [**DCM**](https://arxiv.org/abs/2403.13221) | Omron SINIC X | IROS | 2024 | VIC输入 | ✗ | Diffusion接触模型 | 机械臂 + gripper | ✗ | ✗ | ✗ | ✗ |

---

## 6. VLA基础模型：版本历史

### 6.1 Physical Intelligence pi系列

| 版本 | 日期 | 参数量 | VLM Backbone | 动作头 | Dex Hand | Force/Impedance | 开放权重 |
|---|---|---|---|---|---|---|---|
| **pi0** | 2024年10月 | 3.3B | PaliGemma 3B | Flow matching (300M) | ✗（gripper） | ✗ | ✅ Apache 2.0 ([openpi](https://github.com/Physical-Intelligence/openpi), [HF](https://huggingface.co/lerobot/pi0_base)) |
| **pi0-FAST** | 2025年1月 | 3.3B | PaliGemma 3B | 自回归（FAST tokenizer） | ✗ | ✗ | ✅ Apache 2.0 (openpi) |
| **pi0.5** | 2025年4月 | 3.3B | PaliGemma 3B | 两阶段：FAST预训练 → flow matching | ✗ | ✗ | ✅ Apache 2.0 ([HF](https://huggingface.co/lerobot/pi05_base)) |
| **pi0.6 / pi\*0.6** | 2025年11月 | ~5B | Gemma3 4B | Flow + token双重 | ✗ | ✗ | 未正式发布；存在第三方复现 |
| **pi0.7** | 2026年4月 | ~5B | Gemma3 4B + 400M视觉 | Flow matching (860M DiT) | ✗ | ✗ | 截至2026年5月未发布 |

所有pi版本仅使用parallel-jaw gripper。动作空间为18-19D（双6自由度机械臂 + gripper + 底座）。所有版本均无力或impedance输出。

### 6.2 NVIDIA GR00T系列

| 版本 | 日期 | 参数量 | VLM Backbone | DiT层数 | Dex Hand | Force/Impedance | 开放权重 |
|---|---|---|---|---|---|---|---|
| **GR00T N1** | 2025年3月 | 2.2B | Eagle-2 | 16 | Fourier手（humanoid集成） | ✗ | ✅ 非商用 ([HF](https://huggingface.co/nvidia/GR00T-N1-2B)) |
| **GR00T N1.5** | 2025年中 | 3B | Eagle 2.5（冻结） | 16 | 未记录 | ✗ | ✅ 非商用 ([HF](https://huggingface.co/nvidia/GR00T-N1.5-3B)) |
| **GR00T N1.6** | 2025年末 | 3B | Cosmos-2B | 32 | 未记录 | ✗ | ✅ ([HF](https://huggingface.co/nvidia/GR00T-N1.6-3B)) |
| **GR00T N1.7** | 2026年5月 | 3B | Cosmos-Reason2-2B (Qwen3-VL) | 32 | 22自由度（EgoScale/Sharpa表征） | ✗ | ✅ 商用可 ([HF](https://huggingface.co/nvidia/GR00T-N1.7-3B)) |

**GR00T-Dexterity** 是一个独立的RL工作流（非VLA模型），基于DextrAH-G。它支持Allegro Hand (16自由度) + Kuka，在Isaac Lab中使用geometric fabrics。GR00T N1.x VLA模型不直接输出多指手动作。

所有GR00T VLA版本仅输出位置目标。N1.7中的"22自由度手"源自EgoScale预训练framework，该framework将人手运动表示为22自由度Sharpa手关节角度。Unitree G1的物理手（Dex3-1）每只手仅有7个自由度。22自由度能力指的是人体视频预训练中使用的动作表征，而非deployment手。

### 6.3 其他主要VLA

| 论文 | 研究组 | 会议 | 年份 | Dex Hand? | 力输出？ | Open-Source代码 | 开放权重 | 核心特点 |
|---|---|---|---|---|---|---|---|---|
| [**Gemini Robotics**](https://arxiv.org/abs/2503.20020) | Google DeepMind | arXiv | 2025 | ✗（gripper） | ✗ | ✗ | ✗（封闭，受信测试者） | 基于Gemini 2.0的VLA；泛化benchmark 2倍SOTA；ALOHA/Franka/Apollo |
| **Gemini Robotics 1.5** | Google DeepMind | Blog | 2026 | ✗ | ✗ | ✗ | ✗（受信测试者） | VLA + inference；cross-embodiment；Gemini API (ER 1.5) |
| **Gemini Robotics On-Device** | Google DeepMind | Blog | 2025 | ✗ | ✗ | SDK（有限） | ✗ | 端侧VLA；50-100个演示即可fine-tuning；无网络依赖 |
| [**RT-2**](https://arxiv.org/abs/2307.15818) | Google DeepMind | CoRL | 2023 | ✗ | ✗ | ✗ | ✗（封闭） | 55B VLM联合fine-tuning用于机器人动作 |
| [**OpenVLA**](https://arxiv.org/abs/2406.09246) | Berkeley/Stanford | CoRL | 2024 | ✗ | ✗ | [GitHub](https://github.com/openvla/openvla) ✅ | ✅ HF | 7B VLA baseline，Apache 2.0 |
| [**OpenVLA-OFT**](https://arxiv.org/abs/2502.19645) | Stanford/Berkeley | RSS | 2025 | ✗ (ALOHA) | ✗ | [GitHub](https://github.com/moojink/openvla-oft) ✅ | ✅ | Inference速度提升26倍，并行解码 |
| [**Octo**](https://arxiv.org/abs/2405.12213) | Berkeley RAIL | RSS | 2024 | ✗ | ✗ | [GitHub](https://github.com/octo-models/octo) ✅ | ✅ HF | 93M，模块化fine-tuning |
| [**RDT-1B**](https://arxiv.org/abs/2410.07864) | Tsinghua thu-ml | ICLR | 2025 | ✗（bimanual） | ✗ | [GitHub](https://github.com/thu-ml/RoboticsDiffusionTransformer) ✅ | ✅ HF 1B | 最大open-source diffusion模型 |
| [**HPT**](https://arxiv.org/abs/2409.20537) | MIT (Kaiming He) | NeurIPS | 2024 | ✗ | ✗ | [GitHub](https://github.com/liruiw/HPT) ✅ | ✗ | 异构cross-embodiment预训练 |
| [**CogACT**](https://arxiv.org/abs/2411.19650) | Microsoft | arXiv | 2024 | ✗ | ✗ | [GitHub](https://github.com/microsoft/CogACT) ✅ | ✗ | 认知-动作分离 |
| [**EgoScale**](https://arxiv.org/abs/2602.16710) | NVIDIA/Berkeley | arXiv | 2026 | ✅ 22自由度 | ✗ | ✗ | ✗ | 2万小时人类视频，dexterous缩放定律 |
| [**SimpleVLA-RL**](https://arxiv.org/abs/2509.09674) | — | ICLR | 2025 | ✗ | ✗ | [GitHub](https://github.com/PRIME-RL/SimpleVLA-RL) ✅ | ✗ | VLA的RL fine-tuning |
| [**SpatialVLA**](https://arxiv.org/abs/2501.15830) | Shanghai AI Lab / Multi-inst. | RSS | 2025 | ✗ | ✗ | ✅（项目主页） | ✅ | 3.5B VLA，基于PaliGemma2的Ego3D位置编码 + 自适应动作网格 |
| [**TinyVLA**](https://arxiv.org/abs/2409.12514) | ECNU / Midea | AAAI | 2025 | ✗ | ✗ | ✗（仅项目主页） | ✗ | 1.3B VLA + diffusion解码器；以20倍速度匹配7B OpenVLA |
| [**LLARVA**](https://arxiv.org/abs/2406.11815) | UC Berkeley | arXiv | 2024 | ✗ | ✗ | ✗（仅项目主页） | ✗ | 视觉-动作指令调优，2D视觉轨迹辅助任务 |
| [**UniAct**](https://arxiv.org/abs/2501.10105) | Multi-inst. | CVPR | 2025 | 面向多样化设计 | ✗ | [GitHub](https://github.com/2toinf/UniAct) ✅ | ✗ | 通用动作码本 |

### 6.4 视觉运动策略（无语言条件）

未使用VLM backbone但被广泛用作dexterous manipulation baseline或模块的有影响力的视觉运动策略。

| 论文 | 研究组 | 会议 | 年份 | Dex Hand? | 力输出？ | Open-Source代码 | 开放权重 | 核心特点 |
|---|---|---|---|---|---|---|---|---|
| [**Diffusion Policy**](https://arxiv.org/abs/2303.04137) | Columbia (Shuran Song) | RSS | 2023 | ✗ | ✗ | [GitHub](https://github.com/real-stanford/diffusion_policy) ✅ | ✗ | 奠基性diffusion policy方法 |
| [**ACT / ALOHA**](https://arxiv.org/abs/2304.13705) | Stanford (Tony Zhao) | RSS | 2023 | ✗（gripper） | ✗ | [GitHub](https://github.com/tonyzhaozh/act) ✅ | ✗ | Action chunking transformer，bimanual teleoperation |
| [**DP3**](https://arxiv.org/abs/2403.03954) | Tsinghua (Yanjie Ze) | RSS | 2024 | ✅（仿真） | ✗ | [GitHub](https://github.com/YanjieZe/3D-Diffusion-Policy) ✅ | ✗ | 3D point cloud diffusion，72个任务 |
| [**iDP3**](https://arxiv.org/abs/2410.10803) | Stanford/Tsinghua | IROS | 2025 | ✅ Inspire (25自由度) | ✗ | [GitHub](https://github.com/YanjieZe/Improved-3D-Diffusion-Policy) ✅ | ✗ | 在Fourier GR1 humanoid上的自中心3D |
| [**DexWM**](https://arxiv.org/abs/2512.13644) | Meta FAIR / NYU | arXiv | 2025 | ✅ Allegro + Franka | ✗ | ✗ | ✗ | Dexterous hand-物体交互的世界模型 |

---

## 7. 基于RL的Dexterous Manipulation

### 7.1 Dexterous Grasping

| 论文 | 研究组 | 会议 | 年份 | RL Algo | 手部(自由度) | 仿真 | Sim2Real | 物体 | 代码 | 权重 |
|---|---|---|---|---|---|---|---|---|---|---|
| [**CrossDex**](https://arxiv.org/abs/2410.02479) | PKU-RL | ICLR | 2025 | PPO + DAgger | 6种手（Shadow, Allegro, LEAP, ...） | IsaacGym P4 | ✅ | 100 (YCB+GRAB) | [GitHub](https://github.com/PKU-RL/CrossDex) ✅ | 部分 |
| [**ResDex**](https://arxiv.org/abs/2410.01481) | PKU-RL | ICLR | 2025 | PPO + MoE + DAgger | Shadow (24) | IsaacGym P4 | ✗ | 3200个，88.8% | [GitHub](https://github.com/PKU-RL/ResDex) ✅ | 部分 |
| [**UniDexGrasp++**](https://arxiv.org/abs/2304.00464) | PKU-EPIC | ICCV | 2023 | PPO + DAgger | Shadow (24) | IsaacGym | ✗ | 3000+，85.4% | [GitHub](https://github.com/PKU-EPIC/UniDexGrasp2) ✅ | ✅ state ckpt |
| [**UniDexGrasp**](https://arxiv.org/abs/2303.00938) | PKU-EPIC | CVPR | 2023 | PPO（目标条件） | Shadow (24) | IsaacGym | ✗ | 3000+，~60% | [GitHub](https://github.com/PKU-EPIC/UniDexGrasp) ✅ | ✗ |
| [**BODex**](https://arxiv.org/abs/2412.16490) | PKU-EPIC | ICRA | 2025 | 双层优化 | Shadow, Allegro, LEAP | cuRobo | ✅ 81% | 5355 | [GitHub](https://github.com/JYChen18/BODex) ✅ | Dataset on HF |
| [**DexGrasp Anything**](https://arxiv.org/abs/2409.11159) | ShanghaiTech | CVPR Highlight | 2025 | Diffusion | Shadow | IsaacGym | ✗ | 15K+，340万抓取 | [GitHub](https://github.com/4DVLab/DexGrasp-Anything) ✅ | ✅ HF+GDrive |
| [**DexGraspNet 2.0**](https://arxiv.org/abs/2410.15590) | PKU-EPIC | CoRL | 2024 | Diffusion | Shadow | IsaacGym | ✅ 90.7% | 1319个，4.26亿抓取 | [GitHub](https://github.com/PKU-EPIC/DexGraspNet2) ✅ | ✅ HF |
| [**RobustDexGrasp**](https://arxiv.org/abs/2501.01771) | ETH Zurich | CoRL | 2025 | PPO + teacher-student | Allegro (16) + UR5 | RaiSim | ✅ 94.6% | 仿真247K，真实512 | [GitHub](https://github.com/zdchan/RobustDexGrasp) ✅ | ✅ |
| [**Dexonomy**](https://arxiv.org/abs/2504.01301) | PKU-EPIC | RSS | 2025 | 优化 | Shadow, Allegro, LEAP, Unitree G1 | MuJoCo + cuRobo | ✅ 82.3% | 10.7K，31种类型 | [GitHub](https://github.com/JYChen18/Dexonomy) ✅ | HF |
| [**UltraDexGrasp**](https://arxiv.org/abs/2603.05312) | InternRobotics | ICRA | 2026 | 多策略 | 多种 | BODex + cuRobo | ✅ 81.2% | 2000万帧 | [GitHub](https://github.com/InternRobotics/UltraDexGrasp) ✅ | ✗ |
| [**DexPoint**](https://arxiv.org/abs/2211.09423) | UCSD | CoRL | 2022 | PPO（point cloud） | Allegro (16) | IsaacGym | ✅ | 类别级新物体 | [GitHub](https://github.com/yzqin/dexpoint-release) ✅ | ✗ |
| [**AnyGrasp**](https://arxiv.org/abs/2212.08333) | SJTU (Cewu Lu) | IEEE T-RO | 2023 | 监督学习 (GSNet) | Parallel-jaw gripper | GraspNet-1B | ✅ 93.3% | 300+未见物体，>900次/小时 | [SDK](https://github.com/graspnet/anygrasp_sdk)（需许可） | ✗ | 上游grasp检测（parallel-jaw gripper）。作为dexterous VLA pipeline中广泛使用的感知模块纳入。 |
| [**DextrAH-G/RGB**](https://arxiv.org/abs/2407.02274) | NVIDIA | CoRL | 2024 | PPO + geometric fabrics | Allegro (16) + Kuka | Isaac Lab | ✅ | 多物体 | [GitHub](https://github.com/NVlabs/DEXTRAH) ✅ | ✗ |

### 7.2 In-Hand Manipulation / Reorientation

| 论文 | 研究组 | 会议 | 年份 | 手部(自由度) | 仿真 | Sim2Real | 代码 | 权重 |
|---|---|---|---|---|---|---|---|---|
| [**Dactyl**](https://arxiv.org/abs/1808.00177) | OpenAI | arXiv 2018 / IJRR 2020 | 2018 | Shadow (24) | MuJoCo | ✅ (ADR) | ✗ | ✗ |
| [**Hora**](https://arxiv.org/abs/2210.04887) | Berkeley/Meta | CoRL | 2022 | Allegro (16) | IsaacGym P4 | ✅ | [GitHub](https://github.com/HaozhiQi/hora) ✅ | ✅ |
| [**Rotating w/o Seeing**](https://arxiv.org/abs/2303.10880) | UCSD | RSS | 2023 | Allegro (16) + 二值tactile | IsaacGym | ✅ | [Page](https://touchdexterity.github.io) | ✗ |
| [**General In-Hand Rotation**](https://arxiv.org/abs/2309.09979) | Berkeley/Meta | CoRL | 2023 | Allegro (16) + DIGIT | IsaacGym | ✅ | (in hora repo) | ✗ |
| [**RotateIt**](https://arxiv.org/abs/2309.02388) | Berkeley/Meta/CMU | CoRL | 2023 | Allegro (16) + DIGIT | IsaacGym | ✅ | (in hora repo) | ✗ |
| [**AnyRotate**](https://arxiv.org/abs/2405.07391) | U. Bristol | CoRL | 2024 | Allegro (16) + tactile | IsaacGym | ✅ | ✗ | ✗ |
| [**Visual Dexterity**](https://arxiv.org/abs/2211.11744) | MIT CSAIL | Science Robotics | 2023 | D'Claw (9/12) | IsaacGym P3 | ✅ | [GitHub](https://github.com/Improbable-AI/dexenv) ✅ | ✅ |
| [**DeXtreme**](https://arxiv.org/abs/2210.13702) | NVIDIA | ICRA | 2023 | Allegro (16) | IsaacGym | ✅ | In IsaacGymEnvs ✅ | ✗ |
| [**DexPBT**](https://arxiv.org/abs/2305.12127) | NVIDIA | RSS | 2023 | Allegro (16) + Kuka | IsaacGym | ✗ | In IsaacGymEnvs ✅ | ✗ |
| [**SAPG**](https://arxiv.org/abs/2407.04890) | CMU | ICML Oral | 2024 | Allegro/Shadow (16-46) | IsaacGym P4 | ✗ | [GitHub](https://github.com/jayeshs999/sapg) ✅ | ✗ |
| [**DexHandDiff**](https://arxiv.org/abs/2411.18562) | HKU/Berkeley | CVPR | 2025 | Shadow | Adroit (MuJoCo) | ✗ | [GitHub](https://github.com/Liang-ZX/DexHandDiff) ✅ | ✅ HF |

### 7.3 长时程 / 多阶段 / Contact-Rich

| 论文 | 研究组 | 会议 | 年份 | 手部(自由度) | 任务 | 仿真 | Sim2Real | 代码 | 权重 |
|---|---|---|---|---|---|---|---|---|---|
| [**SeqDex**](https://arxiv.org/abs/2309.00987) | Stanford | CoRL | 2023 | Allegro (16) | 链式策略（搜索→定向→抓取→插入） | IsaacGym | ✅ | [GitHub](https://github.com/sequential-dexterity/SeqDex) ✅ | ✅ |
| [**Bi-DexHands**](https://arxiv.org/abs/2206.08686) | PKU-MARL | NeurIPS | 2022 | 2x Shadow (48) | 16+ bimanual任务 | IsaacGym | ✗ | [GitHub](https://github.com/PKU-MARL/DexterousHands) ✅ | ✅ |
| [**DexArt**](https://arxiv.org/abs/2305.05706) | UCSD | CVPR | 2023 | Allegro (16) | 4个铰接物体任务 | SAPIEN | ✗ | [GitHub](https://github.com/Kami-code/dexart-release) ✅ | ✅ |
| [**TCDM**](https://arxiv.org/abs/2209.11221) | Meta | ICRA | 2023 | 3种手平台 | 50个任务，34个物体 | MuJoCo | ✗ | [GitHub](https://github.com/facebookresearch/TCDM) ✅ | ✅ |
| [**VTDexManip**](https://arxiv.org/abs/2501.01370) | - | ICLR | 2025 | 多指（仿真） | 6个任务（瓶盖、水龙头、reorientation） | IsaacGym | ✗ | [GitHub](https://github.com/LQTS/VTDexManip) ✅ | ✅ 18个模型 |
| [**DexGarmentLab**](https://arxiv.org/abs/2503.18693) | Multi-inst. | NeurIPS Spotlight | 2025 | Bimanual dexterous | 15个衣物任务，2500+衣物 | IsaacSim | ✗ | [GitHub](https://github.com/wayrise/DexGarmentLab) ✅ | ✗ |
| [**Contact Trust Region**](https://arxiv.org/abs/2505.02291) | MIT CSAIL (Tedrake) | IJRR | 2025 | Allegro (16) | Contact-rich MPC | Drake | ✗ | ✗ | ✗ |
| [**Complementarity-Free**](https://arxiv.org/abs/2408.07855) | MIT CSAIL (Pang, Tedrake) | RSS | 2024 | Allegro (16) | 封闭形式可微接触，50-100 Hz MPC | Drake | ✗ | ✗ | ✗ |
| [**ComFree-Sim**](https://arxiv.org/abs/2603.12185) | — | arXiv | 2026 | LEAP Hand | 基于NVIDIA Warp的GPU并行接触MPC | Custom (Warp) | ✗ | ✗ | ✗ |

注：IndustReal（NVIDIA，RSS 2023）也使用RL解决contact-rich装配问题；详见§5。

### 7.4 近期其他RL工作

| 论文 | 研究组 | 会议 | 年份 | 手部(自由度) | 任务 | Sim2Real | 代码 |
|---|---|---|---|---|---|---|---|
| [**DQ-RISE**](https://arxiv.org/abs/2503.01766) | SJTU | ICRA | 2026 | OyMotion RoHand + Flexiv Rizon 4 | 6个真实任务，85.83% | ✅ | [GitHub](https://github.com/rise-policy/DQ-RISE) ✅ |
| [**DexTrack**](https://arxiv.org/abs/2501.15760) | PKU/Shanghai AI | ICLR | 2025 | Shadow (24), Allegro (16) | 动捕跟踪 | ✗ | [GitHub](https://github.com/Meowuu7/DexTrack) 部分 |
| [**BiDexHD**](https://arxiv.org/abs/2501.09821) | PKU | arXiv | 2025 | 2x Shadow (48) | 141个bimanual任务 (TACO) | ✗ | ✗ |
| [**DONIC**](https://arxiv.org/abs/2610.29997v1) | Ropedia | arXiv | 2026 | 2x Wuji Hand V1（自由度 —） | 双手参考轨迹跟踪（PPO + BC） | ✗ | — |
| [**HandelBot**](https://arxiv.org/abs/2603.12243) | Stanford | arXiv | 2026 | LEAP (16) bimanual | 真实钢琴弹奏 | ✅ | [GitHub](https://github.com/amberxie88/handelbot) ✅ |
| [**DexDrummer**](https://arxiv.org/abs/2603.22263) | Stanford | arXiv | 2026 | Bimanual dexterous | 打鼓（contact-rich） | ✗ | [GitHub](https://github.com/hc-fang/dexdrummer) ✅ |
| [**RoboPianist**](https://arxiv.org/abs/2304.04150) | Google/Berkeley | CoRL | 2023 | Humanoid bimanual | 钢琴（150首曲目） | ✗ | [GitHub](https://github.com/google-research/robopianist) ✅ |
| [**DemoStart**](https://arxiv.org/abs/2409.06613) | Google DeepMind | ICRA | 2024 | DEX-EE（三指） | 插件插入、立方体reorientation | ✅ | ✗ |
| **Closing Reality Gap** | - | arXiv | 2026 | 五指手 | 力控grasping | ✅ zero-shot | ✗ |
| [**Maniwhere**](https://arxiv.org/abs/2407.15815) | Shanghai AI Lab | CoRL | 2024 | Allegro (16) | 8个任务，视觉泛化 | ✅ | [GitHub](https://github.com/gemcollector/maniwhere) ✅ |
| [**Eureka**](https://arxiv.org/abs/2310.12931) | NVIDIA | ICLR | 2024 | Shadow (24，仿真) | LLM生成的奖励，转笔 | ✗ | [GitHub](https://github.com/eureka-research/Eureka) ✅ |
| [**DrEureka**](https://arxiv.org/abs/2406.01967) | NVIDIA | RSS | 2024 | Shadow（仿真）+ 四足 | LLM引导的domain randomization，sim2real | ✅ | [GitHub](https://github.com/eureka-research/DrEureka) ✅ |
| [**DexMV**](https://arxiv.org/abs/2108.05877) | UCSD | ECCV | 2022 | Adroit (30，仿真) | 从人类视频的IL（倒、放置、重定位） | ✗ | [GitHub](https://github.com/yzqin/dexmv-sim) ✅ |
| [**CyberDemo**](https://arxiv.org/abs/2402.14795) | UCSD | CVPR | 2024 | Allegro (16) | 增强仿真演示，阀门旋转 | ✅ | [GitHub](https://github.com/wang59695487/CyberDemo) ✅ |

---

## 8. 数据集

### 8.1 机器人Dexterous Hand数据集

| 数据集 | 年份 | 会议 | 规模 | 手类型 | 任务 | F/T or Tactile | 下载 | 格式 |
|---|---|---|---|---|---|---|---|---|
| **UniDex** | 2026 | CVPR | 900万帧，50K+轨迹 | 8种机器人手 (FAAS) | 多样化manipulation | ✗ | ✅ [HF](https://huggingface.co/datasets/UniDex-ai/UniDex) | HDF5 |
| **Dexora** | 2025 | ICRA | 12.2K集，40.5小时真实 | Bimanual 36自由度 | Grasping、manipulation、装配、工具 | ✗ | ✅ [HF](https://huggingface.co/datasets/ZZongzheng0918/Dexora) | Parquet+MP4 |
| **DexMimicGen** | 2024 | ICRA | 21K演示 | Bimanual dexterous | 9个任务 | ✗ | ✅ [HF](https://huggingface.co/datasets/MimicGen/dexmimicgen_datasets) 59.9GB | HDF5 |
| **DexGraspNet 2.0** | 2024 | CoRL | 4.26亿grasp | Shadow | Grasping | ✗ | ✅ [HF](https://huggingface.co/datasets/lhrlhr/DexGraspNet2.0) | WebDataset |
| **VTDexManip** | 2025 | ICLR | 56.5万帧，182个物体 | 多指（仿真） | 6个复杂任务 | ✅ 二值tactile | ✅ [GitHub](https://github.com/LQTS/VTDexManip) | IsaacGym |
| **ManipTrans/DexManipNet** | 2025 | CVPR | 3.3K集 | 6种手 | Bimanual manipulation | ✗ | ✅ [HF](https://huggingface.co/datasets/ManipTrans/DexManipNet) | MuJoCo |
| **CEDex** | 2026 | ICRA | 2000万grasp，50万物体 | Shadow, Allegro, LEAP | Cross-embodiment grasping | ✗ | ✅ [GitHub](https://github.com/GeorgeWuzy/CEDex-Grasp) | Custom |
| **Dexonomy** | 2025 | RSS | 950万grasp，10.7K物体 | Shadow（已发布；论文涵盖Allegro, LEAP） | 31种grasp类型 | ✗ | ✅ [HF](https://huggingface.co/datasets/JiayiChenPKU/Dexonomy) | Custom |
| **Dex1B** | 2025 | RSS | 10亿演示，6K+物体 | Shadow, Inspire, Ability | Grasping + 铰接 | ✗ | 不确定 | Custom |
| **Fourier ActionNet** | 2025 | — | 30K+轨迹，140小时 | Fourier dexterous hand | 真实humanoid bimanual | ✗ | ✅ [action-net.org](https://action-net.org/) | Custom |
| **RoboMIND** | 2025 | RSS | 107K轨迹，479个任务 | 多embodiment含dexterous | 多样化manipulation | ✗ | ✅ [HF](https://huggingface.co/datasets/x-humanoid-robomind/RoboMIND) | Custom |
| **Bi-DexHands** | 2022 | NeurIPS | 离线RL数据集 | 2x Shadow | 16+ bimanual任务 | ✗ | ✅ [GitHub](https://github.com/PKU-MARL/DexterousHands) | IsaacGym |
| **TCDM** | 2023 | ICRA | 50个任务，34个物体 | 3种手平台 | 多样化manipulation | ✗ | ✅ [GitHub](https://github.com/facebookresearch/TCDM) | MuJoCo |
| **DAPG** | 2018 | RSS | 每任务25个人类演示 | Shadow（仿真） | 笔、门、锤子、球 | ✗ | ✅ [GitHub](https://github.com/aravindr93/hand_dapg) | Pickle/NumPy |

### 8.2 Force / Tactile / 接触数据集

| 数据集 | 年份 | 会议 | 规模 | 传感器类型 | 手 | 下载 | 核心特点 |
|---|---|---|---|---|---|---|---|
| **ForceVLA-Data** | 2025 | NeurIPS | 244轨迹，14万步 | 六轴F/T | Gripper (Flexiv) | ✅ [HF](https://huggingface.co/datasets/qiaojunyu/ForceVLA-real-data) | Contact-rich 5个任务 |
| **REASSEMBLE** | 2024 | RSS | 4551个演示，781分钟 | F/T + 事件相机 + 音频 | Gripper | ✅ [TUData](https://researchdata.tuwien.ac.at/records/0ewrv-8cb44) | 多模态装配 |
| **RH20T** | 2023 | NeurIPS | 11万集，5000万帧 | F/T + 指尖tactile | Gripper | ✅ [Site](https://rh20t.github.io/) | 140+任务 |
| **Touch100k** | 2025 | Info. Fusion | 10.1万样本 | GelSight | N/A | ✅ [GitHub](https://github.com/cocacola-lab/TLV-Link) | 大规模tactile-语言-视觉数据集 |
| **Sparsh/TacBench** | 2024 | CoRL | 46万+图像 | DIGIT/GelSight（跨传感器） | N/A | ✅ [GitHub](https://github.com/facebookresearch/sparsh) | 跨传感器SSL tactile编码器，5任务benchmark |
| **TVL** | 2024 | ICML | 4.4万对 | DIGIT | N/A | ✅ [GitHub](https://github.com/Max-Fu/tvl) + [HF](https://huggingface.co/datasets/Max-Fu/TVL) | Tactile-视觉-语言对齐 |
| **FMB** | 2025 | IJRR | 22.5K演示 | F/T (Franka) | Gripper | ✅ [HF](https://huggingface.co/datasets/charlesxu0124/functional-manipulation-benchmark) | 功能性manipulation |
| **FeelSight** | 2024 | Science Robotics | 70个实验 | DIGIT + Allegro | Allegro (16) | ✅ [HF](https://huggingface.co/datasets/suddhu/Feelsight) | In-hand tactile-视觉跟踪 |
| **ContactPose** | 2020 | ECCV | 2306个grasp，290万图像 | 热接触 | 人手 | ✅ [GitHub](https://github.com/facebookresearch/ContactPose) | 功能性grasping |

### 8.3 人手 / 自中心数据集

| 数据集 | 年份 | 会议 | 规模 | 模态 | 任务 | 语言 | 下载 |
|---|---|---|---|---|---|---|---|
| **EgoDex** | 2025 | ICLR | 829小时，30Hz 1080p | 自中心RGB + 68关节3D (AVP) | 194个桌面 | ✅ LLM描述 | ✅ [GitHub](https://github.com/apple/ml-egodex) ~1.7TB |
| **DexCanvas** | 2025 | arXiv | 7000小时（v0.1=1%） | 多视角RGB-D + MANO | 21种操作类型 | ✗ | ✅ [HF](https://huggingface.co/datasets/DEXROBOT/DexCanvas) v0.1 |
| **GigaHands** | 2025 | CVPR | 34小时，14K片段 | 多视角RGB + 3D手 | Bimanual | ✅ 8.4万标注 | ✅ [Site](https://ivl.cs.brown.edu/research/gigahands.html) |
| **DexWild** | 2025 | RSS | 9.5K集，33小时 | 多视角RGB + 手套 | 5个任务 | ✅ | ✅ [HF](https://huggingface.co/datasets/boardd/dexwild-dataset) 2.14TB |
| **HOI4D** | 2022 | CVPR | 240万RGB-D，4K序列 | 自中心RGB-D + 3D手 | 类别级 | ✅ 动作标签 | ✅ [Site](https://hoi4d.github.io/) |
| **GRAB** | 2020 | ECCV | 162万帧 | SMPL-X + MANO + 接触 | 全身grasping | ✗ | ✅ [Site](https://grab.is.tue.mpg.de/)（需注册） |
| **ARCTIC** | 2023 | CVPR | 210万帧 | RGB + MANO + 接触 | Bimanual铰接 | ✗ | ✅ [Site](https://arctic.is.tue.mpg.de/) ~116GB |
| **OakInk / OakInk2** | 2022/24 | CVPR | 23万+帧 | RGB + MANO + 物体 | 手-物体交互 | ✅ (v2) | ✅ [HF](https://huggingface.co/datasets/kelvin34501/OakInk-v2) |
| **DexYCB** | 2021 | CVPR | 58.2万RGB-D | RGB-D + MANO + 物体 | Grasping（20个YCB物体） | ✗ | ✅ [Site](https://dex-ycb.github.io/) 119GB |
| **Ego-Exo4D** | 2024 | CVPR | 1286小时，740名参与者 | 自中心+外视角RGB + IMU + 注视 | 熟练活动 | ✅ | ✅ [Site](https://ego-exo4d-data.org/)（需注册） |
| **Humanoid Everyday** | 2025 | arXiv | 10.3K轨迹，300万帧 | RGB + 深度 + LiDAR + tactile | 260个dexterous任务 | ✅ | ✅ [HF](https://huggingface.co/datasets/USC-GVL/humanoid-everyday) |

### 8.4 Cross-Embodiment预训练数据集

| 数据集 | 年份 | 会议 | 规模 | Embodiment种类 | 任务 | 格式 | 下载 |
|---|---|---|---|---|---|---|---|
| [**Open X-Embodiment (OXE)**](https://arxiv.org/abs/2310.08864) | 2023 | arXiv/ICRA | ~100万集 | 22种机器人（仅gripper） | 527个技能，160K+任务 | RLDS (TF Datasets) | ✅ [Site](https://robotics-transformer-x.github.io/) |
| [**DROID**](https://arxiv.org/abs/2403.12945) | 2024 | arXiv | 76K演示，350小时 | Franka Panda（1种embodiment，564个场景） | 84个任务，50名操作员 | 双目RGB + proprioception + 语言 | ✅ [Site](https://droid-dataset.github.io/) |

---

## 9. 仿真Benchmark与平台

| Benchmark | 会议 | 年份 | Dex Hand | Sim Platform | 核心特点 | 安装 |
|---|---|---|---|---|---|---|
| [**ManiSkill3**](https://arxiv.org/abs/2410.00425) | RSS | 2025 | Allegro, DClaw | SAPIEN (GPU) | 快430倍，RL/IL/VLA baseline | `pip install mani-skill` |
| **MuJoCo Playground** | RSS demo | 2025 | LEAP Hand | MuJoCo | 分钟级训练，zero-shot sim2real | `pip install playground` |
| **MuJoCo Manipulus** | 2025 | 2025 | 工具manipulation | MuJoCo | 16个工具使用任务 | Open-source |
| **Adroit** | RSS | 2018 | Shadow (24) | MuJoCo | 标准RL baseline | `pip install gymnasium-robotics` |
| **Genesis** | Dec 2024 | 2024 | 任意URDF | Genesis | 430K倍实时，可微分 | `pip install genesis-world` |
| **DiffTactile** | ICLR | 2024 | 多指 | Custom | 可微分FEM tactile仿真 | [GitHub](https://github.com/Genesis-Embodied-AI/DiffTactile) |
| **TeleOpBench** | 2025 | 2025 | 3种humanoid | Isaac Sim | 30个任务，4种teleoperation模态 | [GitHub](https://github.com/cyjdlhy/TeleOpBench) |
| [**Isaac Lab**](https://isaac-sim.github.io/IsaacLab/) | RA-L / 2024 | 2024 | Allegro, Shadow, 任意URDF | Isaac Sim (PhysX 5) | IsaacGym继任者，GPU并行，RTX渲染 | `pip install isaaclab` |
| [**TACTO**](https://github.com/facebookresearch/tacto) | RA-L | 2022 | Gripper（DIGIT/GelSight仿真） | PyBullet + PyRender | 基于视觉的tactile传感器仿真器 | `pip install tacto` |
| [**BiGym 2.0**](https://arxiv.org/abs/2610.07594v2) | — | 2026 | Unitree G1，2个Dex1平行夹爪 | MuJoCo | 20个家务任务，每任务60个VR演示，共用全身控制器 | [GitHub](https://github.com/swirl-uk/BiGym2) |

---

## 10. Teleoperation系统

| 系统 | 研究组 | 会议 | 年份 | 输入 | 目标手 | 力反馈 | 成本 | 代码 |
|---|---|---|---|---|---|---|---|---|
| [**DexCap**](https://arxiv.org/abs/2403.07788) | Stanford | RSS | 2024 | SLAM + 电磁 | LEAP Hand | ✗ | ~$2K | [GitHub](https://github.com/j96w/DexCap) ✅ |
| [**BunnyVisionPro**](https://arxiv.org/abs/2407.03162) | HKU / UCSD | arXiv | 2024 | Apple Vision Pro | Bimanual dexterous | 低成本tactile | ~$3.5K+ | [GitHub](https://github.com/Dingry/BunnyVisionPro) ✅ |
| **AnyTeleop** | UCSD | RSS | 2023 | 视觉（摄像头） | 多种 | ✗ | 低 | 项目主页 |
| [**DOGlove**](https://arxiv.org/abs/2505.14635) | TEA Lab | RSS | 2025 | Tactile手套 | 任意dexterous hand | ✅ 5自由度 | <$600 | [GitHub](https://github.com/TEA-Lab/DOGlove) ✅ |
| [**DEXOP**](https://arxiv.org/abs/2509.04441) | Stanford | arXiv | 2025 | 被动外骨骼 | 任意dexterous hand | ✅ proprioception | - | [Page](https://dex-op.github.io/) |
| [**DEX-Mouse**](https://arxiv.org/abs/2604.15013) | - | arXiv | 2026 | 手持式接口 | 通用 | ✅ 动觉 | <$150 | 已open-source |
| [**Open TeleDex**](https://arxiv.org/abs/2510.14771) | - | arXiv | 2025 | 手机 | 任意臂 + 手 | ✗ | 极低 | [GitHub](https://github.com/omarrayyann/TeleDex) ✅ |
| [**OmniH2O**](https://arxiv.org/abs/2406.08858) | CMU LeCAR | CoRL | 2024 | VR/语音/RGB | Humanoid | ✗ | - | [GitHub](https://github.com/LeCAR-Lab/human2humanoid) ✅ |
| [**Open-TeleVision**](https://arxiv.org/abs/2407.10107) | UCSD | CoRL | 2024 | 立体VR | Bimanual dexterous | ✗ | - | [GitHub](https://github.com/OpenTeleVision/TeleVision) ✅ |
| [**HATO**](https://arxiv.org/abs/2404.16823) | UC Berkeley | ICRA | 2024 | Meta Quest 2 VR | 2x Psyonic Ability Hand (6自由度) + tactile传感器 | ✗（仅机器人端tactile） | 低（VR + 假肢手） | [GitHub](https://toruowo.github.io/hato/) ✅ |
| [**DexPilot**](https://arxiv.org/abs/1910.03135) | NVIDIA | ICRA | 2020 | 视觉（裸手，单RGB摄像头） | Allegro (16) + Kuka IIWA | ✗ | 极低（仅需摄像头） | [Page](https://sites.google.com/view/dex-pilot) |

---

## 11. 低成本Dexterous Hand硬件

| 手 | 研究组 | 年份 | 自由度 | 成本 | Sim2Real | Tactile | 设计文件 |
|---|---|---|---|---|---|---|---|
| **LEAP Hand V2** | CMU (Pathak) | 2024 | 16 + 掌部 | ~$3K | ✅ | ✗ | [Page](https://v2-adv.leaphand.com/) |
| **ORCA Hand** | ETH Zurich | 2025 | 17 | <$2K | ✅（1小时训练） | ✅ | [orcahand.com](https://www.orcahand.com/) 完全open-source |
| **ISyHand** | MPI-IS | 2025 | 18 (12+6掌部) | ~$1.3K | ✅ | ✗ | [Page](https://isyhand.is.mpg.de/) |
| **RUKA Hand** | NYU (Pinto) | 2025 | 15 | <$1.3K | ✅ | ✗ | [Page](https://ruka-hand.github.io/) |
| **FAIVE Hand** | ETH Zurich (SRL) | 2024 | 11+ | ~$500-800 | ✅ | ✗ | [GitHub](https://github.com/srl-ethz/faive-hand) 完全open-source |
| **Ability Hand** | PSYONIC Inc. | 2024 | 6 | 商用 | — | ✅ 指尖压力 | [psyonic.io](https://www.psyonic.io/ability-hand) 封闭源 |
| **XHand / Inspire Hand** | 中国制造商 | 2023+ | 12-16 | ~$1-3K | 部分 | ✗ | 封闭源商用 |
| **Digit 360** | Meta FAIR | 2024 | N/A（传感器） | - | N/A | ✅ 18+种模态 | 计划open-source |

---

## 12. Tactile表征模型

| 模型 | 研究组 | 会议 | 年份 | 核心特点 | 代码 |
|---|---|---|---|---|---|
| **Sparsh** | Meta FAIR/CMU | CoRL | 2024 | SSL跨传感器tactile编码器，TacBench 5任务benchmark | [GitHub](https://github.com/facebookresearch/sparsh) ✅，权重 ✅ |
| **UniTouch** | UCSD | CVPR | 2024 | 统一tactile-视觉-语言-声音对齐 | [GitHub](https://github.com/cfeng16/UniTouch) ✅，权重 ✅ |
| **AnyTouch** | Renmin Univ | ICLR | 2025 | 基于TacQuad 4传感器数据集的跨传感器SSL | [GitHub](https://github.com/GeWu-Lab/AnyTouch) ✅，权重 ✅ |
| **NeuralFeels** | Meta FAIR | Science Robotics | 2024 | 用于Allegro+DIGIT in-hand跟踪的神经场 | [GitHub](https://github.com/facebookresearch/neuralfeels) ✅ |

---

## 13. 足式与人形机器人学习

| 论文 | Year | Robot / 任务 | 核心方法 | 主要结果 | Code |
|---|---|---|---|---|---|
| [**Reflex**](https://arxiv.org/abs/2610.12772v1) | 2026 | Unitree G1；全身接住并保持人类抛出的箱子 | 三阶段学习：状态PPO、动力学潜变量学习、固定控制器下的RGB-D历史回归 | 接箱成功率：仿真85.7%；真实G1在2.5、5、7 m处分别为65%、40%、15%（每个条件20次试验） | — |
| [**λ_0**](https://arxiv.org/abs/2610.18950v1) | 2026 | Unitree G1；全身移动操作 | 将HumanVerse人类演示对齐到G1；依次进行手部运动预训练、人类全身运动中期训练和机器人后训练 | 成功率：SIMPLE 90.0%（按任务选择配置）；四项真实任务62.5%，Average weighted progress 80.4%（每项任务10次试验） | [代码](https://github.com/LambdaHumanoid/openlambda) |

---

## 14. 基于学习的最优与安全控制

| 论文 | Year | Robot / 任务 | 核心方法 | 主要结果 | Code |
|---|---|---|---|---|---|

---

## 15. 机器人操作与模仿学习

| 论文 | Year | Robot / 任务 | 核心方法 | 主要结果 | Code |
|---|---|---|---|---|---|
| [**HexaShell**](https://arxiv.org/abs/2610.23479v1) | 2026 | 仿真双臂ARX X5；42个RoboDojo操作任务 | GPT-6-Astra编程智能体编写并修复可复用工具；通过标定RGB三角测量与平面约束测量位置 | seed 0内的新布局：成功率39.7%，progress score 48.0；精密插入成功率8.3% | [代码](https://github.com/HexaFuture/HexaShell) |

---

## 16. 运动规划与决策

| 论文 | Year | Robot / 任务 | 核心方法 | 主要结果 | Code |
|---|---|---|---|---|---|
| [**SuperNav**](https://arxiv.org/abs/2610.12126v1) | 2026 | Unitree Go2；仿真中的实例、多对象、需求驱动及类别级导航 | 预训练MLLM无需导航专用微调；结合Navigation Skills、图像坐标目标、可替换执行器及执行反馈 | Geo-based Executor的SR：单对象78.00%、多对象34.00%（Habitat-GS），需求驱动59.50%（调整评估后的Demand-Bench） | — |

---

## 17. 状态估计与传感器融合

| 论文 | Year | Robot / 任务 | 核心方法 | 主要结果 | Code |
|---|---|---|---|---|---|

---

## 18. 机器人世界模型与具身基础模型

| 论文 | Year | Robot / 任务 | 核心方法 | 主要结果 | Code |
|---|---|---|---|---|---|
| [**Towards Agentic Robots: Model, Data, Environment, and Harness**](https://arxiv.org/abs/2610.20442v1) | 2026 | 综述实体与仿真机器人系统的任务执行和能力开发 | 回顾策略、VLA、世界模型和世界动作模型的发展；比较智能体决策、工具和反馈 | 以Model、Data、Environment、Harness四个领域及17个可重叠功能类别连接执行与能力开发 | [综述资料](https://github.com/chonghanqin/Awesome-Agentic-Robots) |
| [**GroundingPI**](https://arxiv.org/abs/2609.39601v1) | 2026 | 双臂操作（RoboTwin 2.0）、人形灵巧手操作（RoboCasa-GR1）；驾驶（nuScenes） | 4B grounding模型；点与框共享坐标token；预训练 + SFT + GRPO；操作使用Action DiT | 全部4个OOD操作设置排名第一；RoboTwin2.0-Clean2Random成功率17.60%，Rex-Omni为14.10%；nuScenes开环L2误差0.296 m | — |
| [**ScaleNav**](https://arxiv.org/abs/2610.25690v1) | 2026 | Unitree Go2；面向初始视野内目标的语言条件局部导航 | 共享DiT预测视频与动作块；互联网视频预训练 + 仿真动作对齐 + 联合微调；初始帧锚点 | 成功率：单视角Short-Horizon OVON为86.5%，HabitatGS-LN为94.9%，Go2为83.3%（60次试验） | [项目](https://zju3dv.github.io/ScaleNav/) |
| [**Ropedia W0**](https://arxiv.org/abs/2610.26855v1) | 2026 | 人类、夹爪机器人及灵巧人形机器人；移动与操作视频预测；Xp-Teleop中的Unitree G1 | 相机位姿与投影骨架条件视频扩散模型；Xp-Data人类预训练 + 人机混合训练；蒸馏 | DreamDojo In-lab PSNR：20.854 dB，DreamDojo 14B为18.983 dB（Ropedia W0 5B；1%后训练数据） | — |
| [**VQ-WM**](https://arxiv.org/abs/2610.25600v1) | 2026 | WidowX AI；四圆盘汉诺塔（H15）；仿真操作与Walker移动 | 首次到达时间驱动的状态量化；离散潜空间BFS + 连续视觉反馈控制 | 真实H15：短时play数据训练后任务进度100%（6个案例，每例3次）；Cube-Hard成功率：73.3 ± 0.9% | — |
| [**RynnUnify**](https://arxiv.org/abs/2610.32965v1) | 2026 | Astribot S1；多步操作；20个选定的RoboCasa365复合任务；视觉规划与未来状态推理 | 基于Cosmos3的16B MoT；结合场景记忆的交错视频–语言规划；RL智能体与视频–动作联合扩展 | Rynn-VP：比Cosmos 3 Nano高9.75分；控制成功率：选定RoboCasa365任务51.5%，三个真实机器人任务平均46.7% | [代码](https://github.com/alibaba-damo-academy/RynnUnify) |
| [**Has GPT-6-Astra Achieved Embodied Intelligence?**](https://arxiv.org/abs/2610.22471v1) | 2026 | 操作与导航；12个基准；8种真实机器人配置，涵盖机械臂、灵巧手、移动平台和人形机器人 | 固定模型权重；冻结基于演示的ICL知识包；1×/10×动作预算；闭环审查π0.5动作 | SIMPLE成功率：ICL为90.8%，zero-shot为70.8%（4个共同任务，标准预算）；RoboDojo：ICL + 闭环VLA为54.17%，ICL直接控制为29.67% | — |
| [**UniWAM**](https://arxiv.org/abs/2610.02054v3) | 2026 | LIBERO、LIBERO-Plus和RoboTwin 2.0中的仿真操作；双臂任务 | MoT联合注意力连接物理推理、视频生成与动作预测；VQA、人类和机器人数据预训练；未来帧噪声与历史条件流匹配 | 成功率：LIBERO-Plus为92.6%；RoboTwin 2.0 C2R为68.32%，C2C为75.14% | — |

---

## 19. 开放研究方向

本节重点介绍从综述文献中浮现的尚未充分探索的能力交叉点。这些方向并非详尽无遗；同期或未发表的工作可能已部分解决其中一些方向。

### 19.1 能力矩阵

下表将代表性系统映射到与contact-rich dexterous manipulation相关的属性。"仿真"指用于训练或评估的公开可用仿真环境。

|  | 多指手 | 工具使用 | Force/Impedance Output | VLA/Lang | 仿真 |
|---|---|---|---|---|---|
| **pi0~0.7** | ✗（仅gripper） | ✗ | ✗ | ✅ | ✗ |
| **GR00T N1~1.7** | 仅humanoid集成 | ✗ | ✗ | ✅ | ✅ Isaac Lab |
| **GR00T-Dexterity** | ✅ Allegro | ✗（仅grasping） | ✗ | ✗（仅RL） | ✅ Isaac Lab |
| **UniDex-VLA** | ✅ 8种手 | ✅ | ✗ | ✅ | 部分（reorientation环境） |
| **DexVLA** | ✅ | ✗ | ✗ | ✅ | ✗ |
| **SimToolReal** | ✅ Sharpa 22自由度 | ✅ 24个任务 | ✗ | ✗ | ✅ IsaacGym |
| **CompliantVLA-adaptor** | ✗（gripper） | ✗ | ✅ K, D | ✅（冻结VLA） | ✅ LIBERO |
| **CHIP** | Humanoid 35自由度 | ✗ | ✅ End-effector stiffness (K) | ✗ (RL) | ✅ |
| **TacDiffusion** | ✗（gripper） | ✗ | ✅ 6D torque | ✗ | ✗ |
| **DexForce** | ✅ Allegro | ✗ | 固定k_f（手动调参） | ✗ | ✗ |

### 19.2 观察与发现

使用多指手进行的contact-rich manipulation——例如工具使用、装配或处理易碎物体——需要调节交互力，而不仅仅是跟踪位置目标。力控制不足会导致物体滑落、工具损坏或环境破坏。虽然gripper通常可以通过机械compliance来补偿，但高自由度dexterous hand将接触分布在多个指尖，使得逐接触点力调节更加关键且更具挑战性。这促使我们审视现有系统是否将dexterous控制与力/impedance感知相结合。

能力矩阵和更广泛的综述揭示了以下几个模式：

**Dexterous VLA与力感知策略在很大程度上是独立发展的。** Dexterous VLA文献（§2）关注跨多种手的位置目标生成，而力/impedance文献（§3-5）关注gripper和机械臂的contact-rich控制。UniDex-VLA、DexVLA和DexGraspVLA均只输出位置目标。相反，输出impedance参数的系统（CompliantVLA-adaptor、CHIP、Comp-ACT、VICES）仅在gripper或机械臂上运行。DexForce是唯一一项结合力感知的dexterous hand工作，在Allegro Hand上使用手动调参的固定缩放。

**Cross-embodiment动作表征仍然碎片化。** 多种方法竞相表征cross-embodiment的dexterous hand动作：FAAS（UniDex-VLA）、特征grasp（CrossDex）、通用码本（UniAct）、异构stems（HPT）以及每embodiment MLP（GR00T）。目前尚无共识哪种表征最能支持跨手泛化，且这些方法之间的直接比较十分稀少。

**Dexterous数据采集是公认的瓶颈。** 低成本teleoperation系统（§10）的大量涌现——DexCap、DOGlove、DEXOP、DEX-Mouse，均发表于2024-2026年——表明社区将数据采集视为主要障碍。尽管付出了这些努力，大多数dexterous数据集（§8.1）仍然只捕获关节位置和视觉数据，force/torque模态几乎仅在基于gripper的系统（§8.2）中可用。

**Dexterous RL的sim-to-real迁移正在走向成熟。** 多篇近期论文展示了dexterous hand的zero-shot或接近zero-shot sim-to-real迁移：CrossDex（LEAP）、RobustDexGrasp（Allegro，94.6%）、DeXtreme（Allegro）、DQ-RISE（LEAP+Franka，85.8%）以及HandelBot（bimanual LEAP）。这表明仿真训练的dexterous策略正变得可实际deployment，降低了该领域基于仿真研究的门槛。

**VLA模型系列仍以gripper为中心。** 在所有综述的pi版本（pi0到pi0.7）和GR00T版本（N1到N1.7）中，没有任何版本原生支持独立的多指dexterous hand（§6.1-6.2）。GR00T-Dexterity增加了Allegro支持，但作为独立的RL工作流，而非VLA本身的一部分。Open-source VLA生态系统（openpi、Isaac-GR00T、OpenVLA）尚未被社区扩展到dexterous hand embodiment。

**基于模型的接触控制是一个互补维度。** 接触隐式MPC和可微分接触模型（Contact Trust Region、Complementarity-Free、ComFree-Sim）为contact-rich dexterous manipulation中的学习型impedance提供了替代方案。近期工作在Allegro和LEAP手上实现了50-100 Hz的实时MPC。这些方法提供了学习策略通常缺乏的形式化保证（如互补性约束、无源性），但需要精确的动力学模型，且在软体/deformable接触中面临困难。基于模型和基于学习的力控制如何在dexterous hand上结合——例如由基于模型的内环跟踪的学习型impedance设定点——在很大程度上仍未被探索。

---

## 20. 参考链接

### 重要GitHub组织 / 项目主页
- [Google DeepMind](https://deepmind.google/models/gemini-robotics/) — Gemini Robotics, Gemini Robotics-ER, RT-2
- [PKU-EPIC](https://github.com/PKU-EPIC) — DexGraspNet, UniDexGrasp, BODex, Dexonomy
- [PKU-RL](https://github.com/PKU-RL) — CrossDex, ResDex
- [NVlabs](https://github.com/NVlabs) — DextrAH, DexMimicGen, IndustReal, CHIP
- [UniDex-AI](https://github.com/unidex-ai) — UniDex-VLA
- [Physical-Intelligence](https://github.com/Physical-Intelligence) — openpi (pi0, pi0-FAST, pi0.5); pi0.6, pi0.7未公开发布
- [NVIDIA Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) — GR00T N1~N1.7
- [ForceMimic](https://github.com/ForceMimic) — ForceMimic, ForceCapture
- [Meta FAIR](https://github.com/facebookresearch) — SPIDER, TCDM, Sparsh, NeuralFeels
