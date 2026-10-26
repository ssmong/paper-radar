# Contact-Rich Dexterous Manipulation: A Comprehensive Survey

> Last updated: 2026-05-14
> Scope: Papers, repos, and datasets for dexterous manipulation, force-aware VLAs, impedance learning, RL policies, and related benchmarks (2018-2026).
> GitHub links and weight availability were checked as of the survey date; links may become stale.
>
> **Notation:** ✅ = available/supported, ✗ = not available/not supported, — = not reported or not applicable.

**Purpose.** This survey is organized around the intersection of three research threads: (1) dexterous multi-finger manipulation, (2) vision-language-action models, and (3) force/impedance-aware control. It aims to map which capabilities existing systems provide and where combinations remain under-explored, in order to identify open research directions at these intersections. The scope is intentionally focused on these three areas; adjacent topics such as locomotion, mobile manipulation, and industrial automation are covered only where they intersect with the survey's core themes.

---

## 1. Dexterous Tool Use & Manipulation

Multi-fingered hand systems performing grasping, tool use, or object manipulation beyond parallel-jaw grippers.

| Paper | Group | Venue | Year | Hand (DoF) | Tasks | Sim Platform | Sim2Real | Code | Weights | VLA/Lang |
|---|---|---|---|---|---|---|---|---|---|---|
| [**SimToolReal**](https://arxiv.org/abs/2602.16863) | Stanford IPRL | arXiv | 2026 | Sharpa (22) + KUKA | 24 tool-use tasks (hammer, screwdriver, spatula) | IsaacGym | Yes | [GitHub](https://github.com/tylerlum/simtoolreal) ✅ | ✅ ckpt | ✗ |
| [**Grasp-to-Act**](https://arxiv.org/abs/2602.20466) | UIUC RoboTouch | arXiv | 2026 | LEAP (16) | 5 dynamic tool-use (hammer, saw, cut, stir, scoop) | Sim + real | Yes | ✗ | ✗ | ✗ |
| [**DexMachina**](https://arxiv.org/abs/2505.24853) | Stanford/NVIDIA | arXiv | 2025 | Inspire, Allegro, Xhand, Schunk | Bimanual articulated object manipulation | Genesis | ✗ | [GitHub](https://github.com/MandiZhao/dexmachina) ✅ | ✗ (eval TODO) | ✗ |
| [**ManipTrans**](https://arxiv.org/abs/2503.21860) | BIGAI/Tsinghua/PKU | CVPR | 2025 | 4 hands (Shadow, MANO, Inspire, Allegro) | Bimanual (pen cap, bottle unscrew) | IsaacGym P4 | ✗ | [GitHub](https://github.com/ManipTrans/ManipTrans) ✅ | ✅ imitator ckpt + HF | ✗ |
| [**SPIDER**](https://arxiv.org/abs/2511.09484) | Meta FAIR / Berkeley | arXiv | 2025 | 9 humanoid embodiments | Retargeted human demos | MuJoCo | ✅ (Franka+Allegro) | [GitHub](https://github.com/facebookresearch/spider) ✅ | ✗ | ✗ |
| **Scaffolding+VLM** | Stanford / KIT | NeurIPS | 2025 | Allegro (16) + KUKA | Articulated objects (apple, bottle, drawer) | Sim + real | Yes | [GitHub](https://github.com/vdebakker/vlm-scaffolding) ✅ | ✗ | ✅ Gemini VLM |
| [**DexUMI**](https://arxiv.org/abs/2505.21864) | Stanford | CoRL Best Paper Finalist | 2025 | XHand, Inspire | Real-world dexterous manipulation | Real only | N/A | [GitHub](https://github.com/real-stanford/DexUMI) ✅ | ✗ | ✗ |
| [**DexterityGen**](https://arxiv.org/abs/2502.04307) | Berkeley/Meta | RSS | 2025 | Allegro (16) + arm | Tool use (pen, screwdriver, syringe) | IsaacGym | ✅ | ✗ | ✗ | ✗ |
| [**ArtiGrasp**](https://arxiv.org/abs/2309.03891) | ETH Zurich | 3DV | 2024 | MANO (human proxy) | Bimanual grasp + articulation (8 objects) | RaiSim | ✗ | [GitHub](https://github.com/zdchan/artigrasp) ✅ | ✅ pretrained | ✗ |
| [**DexDeform**](https://arxiv.org/abs/2304.03223) | MIT-IBM | ICLR | 2023 | Multi-finger (sim) | 6 deformable object tasks (play-doh) | PlasticineLab | ✗ | [GitHub](https://github.com/sizhe-li/DexDeform) ✅ | ✗ | ✗ |

---

## 2. Dexterous VLA / Vision-Language-Action

VLA models with dexterous hand support or language-conditioned dexterous manipulation.

| Paper | Group | Venue | Year | Hand (DoF) | Tasks | Code | Weights | Key Method |
|---|---|---|---|---|---|---|---|---|
| [**UniDex-VLA**](https://arxiv.org/abs/2603.22264) | UniDex-AI | CVPR | 2026 | 8 hands via FAAS (Allegro, LEAP, Shadow, Inspire, Wuji, Oymotion, Ability, Xhand) | Tool use, 81% task progress | [GitHub](https://github.com/unidex-ai/UniDex) ✅ | ✅ 3-epoch + 32-epoch on HF | 3D VLA + flow matching, FAAS unified action |
| [**DexGraspVLA**](https://arxiv.org/abs/2502.08142) | Psi-Robot | AAAI | 2026 | Custom dexterous | Grasping in clutter, 90%+ success | [GitHub](https://github.com/Psi-Robot/DexGraspVLA) ✅ | ✅ controller ckpt (GDrive) | Qwen2.5-VL-72B planner + diffusion controller |
| [**DexVLA**](https://arxiv.org/abs/2502.05855) | Multi-inst. | CoRL | 2025 | Yes (curriculum) | Dexterous skill learning | [GitHub](https://github.com/juruobenruo/DexVLA) ✅ | ✅ ScaleDP-H/L on HF | Plug-in 1B diffusion expert on frozen VLM |
| **Dexora** | Multi-inst. | ICRA | 2025 | Bimanual 36-DoF | Pick-place, dexterous manip, assembly, tool use | [GitHub](https://github.com/ZZongzheng0918/Dexora) ✅ | ✅ real data on HF | 12.2K real + 100K sim episodes |
| [**Grasp as You Say**](https://arxiv.org/abs/2405.19291) | Sun Yat-sen | NeurIPS | 2024 | Shadow (24) | Language-guided grasping ("grasp mug by handle") | [GitHub](https://github.com/iSEE-Laboratory/Grasp-as-You-Say) ✅ | ✗ | Language-conditioned dexterous grasp generation |
| [**HumanoidGen**](https://arxiv.org/abs/2507.00833) | TeleHuman | NeurIPS | 2025 | Unitree H1_2 + Inspire (6 DoF/hand) | 20 tabletop tasks (bimanual, long-horizon) | [GitHub](https://github.com/TeleHuman/HumanoidGen) ✅ | ✅ HF (model + data) | LLM planner + MCTS + diffusion policy |
| [**VLA+Diffusion Switch**](https://arxiv.org/abs/2410.14022) | — | arXiv | 2024 | ADAPT Hand (13) | Pick-and-place with VLA switching | ✗ | ✗ | VLA + diffusion policy switching on series-elastic multi-finger hand |

---

## 3. Force-aware VLA / Tactile VLA

Models incorporating force/torque or tactile sensing for contact-rich tasks. Included here if the system uses a VLM/VLA backbone or language conditioning; otherwise, force/impedance-focused systems without a VLM backbone appear in §5.

| Paper | Group | Venue | Year | Force Input | Force/Impedance Output? | Robot | Code | Weights | Tasks |
|---|---|---|---|---|---|---|---|---|---|
| [**ForceVLA**](https://arxiv.org/abs/2505.22159) | SJTU/Fudan | NeurIPS | 2025 | 6-axis F/T | ✗ (position only) | Flexiv Rizon + gripper | [GitHub](https://github.com/ft-robotic/ForceVLA) ✅ | ✗ (data on HF) | Plug insertion, wiping, peeling (5 tasks) |
| [**ForceVLA2**](https://arxiv.org/abs/2603.15169) | Shanghai AI Lab | CVPR | 2026 | 6-axis F/T 300Hz | ✅ hybrid F/P + predicted force | Flexiv Rizon 4s + gripper | ✗ "coming soon" | ✗ | Press, clean, assemble gears (5 tasks) |
| [**FD-VLA**](https://arxiv.org/abs/2602.02142) | NUS | ICRA | 2026 | Distilled (no sensor at inference) | ✗ | UR5e + gripper | ✗ | ✗ | Wiping, insertion, button press (3 tasks) |
| [**FAVLA**](https://arxiv.org/abs/2602.23648) | USTC | arXiv | 2026 | 6-axis F/T high-freq | ✗ | Monte dual-arm X-ARM | ✗ | ✗ | USB insertion, gear, wiping (4 tasks) |
| [**HapticVLA**](https://arxiv.org/abs/2603.15257) | Skoltech | arXiv | 2026 | Tactile (distilled away) | ✗ | LeRobot SO-101 + tactile | Paper claims release; no public repo found as of May 2026 | Not verified | Jar/waffle/egg pick-and-place |
| [**DreamTacVLA**](https://arxiv.org/abs/2512.23864) | Northwestern | arXiv | 2025 | Tactile (V-JEPA2) | ✗ | Dobot Xtrainer + gripper + tactile | [GitHub](https://github.com/michaelyeah7/learning-to-feel-the-future) (code only) | ✗ | Tactile world model predicts future latent → action refinement; up to 95% across 4 contact-rich tasks |
| [**OmniVTLA**](https://arxiv.org/abs/2508.08706) | - | arXiv | 2025 | Vision-based + force-based tactile | ✗ | Gripper + Dex Hand | ✗ (dataset only) | ✗ | Pick-and-place (100% dex hand) |
| [**Tactile-VLA**](https://arxiv.org/abs/2507.09160) | Tsinghua | arXiv | 2025 | Tactile | ✅ hybrid pos-force | Not specified | ✗ | ✗ | Charger insertion 90% |
| [**TaF-VLA**](https://arxiv.org/abs/2601.20321) | - | arXiv | 2026 | GelSight + 6-axis F/T | ✗ | Franka FR3 + gripper | ✗ | ✗ | 8 contact-rich tasks |
| [**TA-VLA**](https://arxiv.org/abs/2509.07962) | Tsinghua AIR | CoRL | 2025 | Joint torque | Aux torque prediction | Cobot Magic ALOHA | ✗ | ✗ | 10 tasks (button, charger, USB...) |
| [**CRAFT**](https://arxiv.org/abs/2602.12532) | - | arXiv | 2026 | Force | ✗ | Teleop arm | ✗ | ✗ | Deformable, alignment tasks |
| [**VLA-Touch**](https://arxiv.org/abs/2507.17294) | NUS | arXiv | 2025 | GelSight tactile | ✗ (residual correction) | Arm + gripper | [GitHub](https://github.com/jxbi1010/VLA-Touch) ✅ | ✅ ckpts + HF | Contact-rich manipulation |
| [**FoAR**](https://arxiv.org/abs/2411.15753) | SJTU | RA-L/IROS 2025 | 2024 | 6-axis F/T | ✗ | Flexiv Rizon + gripper | [GitHub](https://github.com/Alan-Heoooh/FoAR) ✅ | ✗ | Wiping, peeling |
| [**FACTR**](https://arxiv.org/abs/2502.17432) | CMU | RSS | 2025 | Joint torque (servo current) | ✗ | Franka + gripper | [GitHub](https://github.com/RaindragonD/factr) ✅ | ✗ (encoder only) | Box lift, pivot, dough rolling |
| [**ForceMimic**](https://arxiv.org/abs/2410.07554) | SJTU | ICRA | 2024 | Captured interaction wrench | ✅ wrench-position hybrid | Flexiv + gripper | [GitHub](https://github.com/ForceMimic/hybridil) ✅ | ✗ | Vegetable peeling |
| [**Reactive Diffusion Policy**](https://arxiv.org/abs/2503.02881) | - | RSS | 2025 | GelSight Mini | ✗ (learned "impedance-like") | Flexiv Rizon 4 + gripper | [GitHub](https://github.com/xiaoxiaoxh/reactive_diffusion_policy) ✅ | ✅ ckpts + HF | 3 contact-rich tasks |
| [**ACP**](https://arxiv.org/abs/2410.09309) | Toyota/Columbia | ICRA | 2024 | 6-axis F/T (ATI) | ✅ scalar stiffness | UR5e + passive tools | ✗ | ✗ | Item flipping, vase wiping |
| [**TacDiffusion**](https://arxiv.org/abs/2409.11047) | TU Munich MIRMI | ICRA | 2024 | Tactile | ✅ 6D wrench | Gripper + tactile | [GitHub](https://github.com/popnut123/TacDiffusion) ✅ | ✗ | Force-domain diffusion, 95.7% zero-shot |
| [**FARM**](https://arxiv.org/abs/2510.13324) | TU Munich MIRMI | arXiv | 2025 | GelSight Mini | ✅ grip force | Modified UMI gripper | ✗ | ✗ | Joint position + force prediction |
| [**T-Dex**](https://arxiv.org/abs/2303.12076) | NYU (Pinto) | ICRA | 2024 | Tactile (DIGIT) | ✗ (position only) | **Allegro (16) + DIGIT** + Kinova arm | [GitHub](https://github.com/irmakguzey/tdex) ✅ | ✗ | 5 dexterous tasks (joystick, book, bowl, peg, playdough); 1.7x over vision-only. One of very few §3 entries with a dex hand. |

---

## 4. VLM-guided Impedance Control

Systems where a VLM/LLM generates or retrieves impedance parameters (K, D) for a low-level controller.

| Paper | Group | Venue | Year | How K/D Adapted | Stiffness (K) | Damping (D) | Robot | Dex Hand? | Code | Weights |
|---|---|---|---|---|---|---|---|---|---|---|
| [**CompliantVLA-adaptor**](https://arxiv.org/abs/2601.15541) | IIT Genoa / TU Darmstadt | arXiv | 2026 | VLM (GPT-4o-mini) zero-shot | ✅ (Kx,Ky,Kz) | ✅ (Dx,Dy,Dz) | Franka Panda + gripper | ✗ | Project page (pending) | ✗ (training-free) |
| [**OmniVIC**](https://arxiv.org/abs/2510.17150) | IIT Genoa / Georgia Tech | arXiv | 2025 | VLM + RAG self-improving | ✅ | ✅ | Franka Panda + F/T sensor | ✗ | ✗ | ✗ (uses GPT-4o-mini API) |
| [**HumanoidVLM**](https://arxiv.org/abs/2601.14874) | - | HRI | 2026 | VLM (Molmo-7B) + FAISS RAG | ✅ (retrieved) | ✅ (retrieved) | Unitree G1 humanoid | ✗ | ✗ | ✗ |
| **SafeHumanoid** | Same group | HRI | 2026 | VLM + RAG retrieval | ✅ | ✅ | Unitree G1 | ✗ | ✗ | ✗ |
| [**ImpedanceGPT**](https://arxiv.org/abs/2503.02723) | - | IROS | 2025 | VLM (Molmo) + RAG | ✅ | ✅ | Drone swarm (not manipulation) | N/A | [GitHub](https://github.com/Faryal-Batool/ImpedanceGPT) ✅ | ✗ |

---

## 5. Learned Impedance / Variable Compliance Control

Systems that learn or optimize impedance/stiffness/damping parameters without a VLM backbone. For VLM-based impedance approaches, see §4. Papers that use force as input but output only positions (e.g., FoAR, FACTR) are in §3.

| Paper | Group | Venue | Year | Stiffness (K) | Damping (D) | Learning Method | Robot | Dex Hand? | Sim | Code | Weights |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [**Comp-ACT**](https://arxiv.org/abs/2406.14990) | OMRON SINIC X / UTokyo | IROS | 2024 | ✅ (12D Cholesky) | ✗ | IL (ACT from VR demos) | 2x UR5e + gripper | ✗ | Robosuite (MuJoCo) | [GitHub](https://github.com/omron-sinicx/CompACT) ✅ | ✗ |
| [**Diff-Impedance**](https://arxiv.org/abs/2509.19696) | KIT / MIT | arXiv | 2025 | ✅ | ✅ | Diffusion + energy-based | KUKA LBR iiwa | ✗ | Sim + real | [GitHub](https://github.com/StrokeAIRobotics/DiffusionBasedImpedanceLearning) ✅ | ✗ |
| [**VICES**](https://arxiv.org/abs/1906.08880) | Stanford / NVIDIA | IROS | 2019 | ✅ | ✅ | RL (policy gradient) | Franka/Sawyer + gripper | ✗ | Robosuite (MuJoCo) | [robosuite/vices](https://github.com/ARISE-Initiative/robosuite/tree/vices_iros19) ✅ | ✗ |
| [**CHIP**](https://arxiv.org/abs/2512.14689) | NVIDIA NVLabs | ICRA | 2025 | ✅ (EE stiffness) | ✗ | RL (hindsight perturbation) | Humanoid 35-DoF | ✗ | Isaac Sim | [Page](https://nvlabs.github.io/CHIP/) | ✗ |
| [**FILIC**](https://arxiv.org/abs/2509.17053) | Tsinghua/HKUST | arXiv | 2025 | Fixed K | Fixed B | IL (transformer, 25Hz) | AIRBOT Play | ✗ | MuJoCo + real | [GitHub](https://github.com/OpenGHz/FILIC) ✅ | ✗ |
| [**CHEQ**](https://arxiv.org/abs/2501.07985) | RWTH Aachen | arXiv | 2025 | ✅ | ✅ | RL (hybrid adaptive) | Arm (polishing) | ✗ | Real hardware | ✗ | ✗ |
| [**DA-VIL**](https://arxiv.org/abs/2410.19712) | IIIT/Brown | ICRA | 2024 | ✅ | Not reported | RL + QP optimization | Dual-arm | ✗ | Sim | Project page only | ✗ |
| [**DexForce**](https://arxiv.org/abs/2501.10356) | Stanford | RA-L | 2025 | Fixed k_f | ✗ | Hand-tuned | Allegro (16) | **✅** | ✗ (real only) | ✗ | ✗ |
| [**Force Policy**](https://arxiv.org/abs/2602.22088) | SJTU/Flexiv | RSS | 2026 | Force targets | ✗ | IL (teleop demos) | Flexiv + gripper | ✗ | ✗ (real only) | ✗ | ✗ |
| [**IndustReal**](https://arxiv.org/abs/2305.17110) | NVIDIA | RSS | 2023 | Fixed | Fixed | RL (PPO) learns poses | Franka + gripper | ✗ | IsaacGym | [GitHub](https://github.com/NVlabs/industreallib) ✅ | ✅ RL policies |
| [**Divide et Impera**](https://arxiv.org/abs/2410.01054) | MIT/KIT | arXiv | 2024 | ✅ (families) | ✅ | NN success predictor | Real arm | ✗ | Real | ✗ | ✗ |
| [**DCM**](https://arxiv.org/abs/2403.13221) | Omron SINIC X | IROS | 2024 | VIC input | ✗ | Diffusion contact model | Arm + gripper | ✗ | ✗ | ✗ | ✗ |

---

## 6. VLA Foundation Models: Version History

### 6.1 Physical Intelligence pi Family

| Version | Date | Params | VLM Backbone | Action Head | Dex Hand | Force/Impedance | Open Weights |
|---|---|---|---|---|---|---|---|
| **pi0** | Oct 2024 | 3.3B | PaliGemma 3B | Flow matching (300M) | ✗ (gripper) | ✗ | ✅ Apache 2.0 ([openpi](https://github.com/Physical-Intelligence/openpi), [HF](https://huggingface.co/lerobot/pi0_base)) |
| **pi0-FAST** | Jan 2025 | 3.3B | PaliGemma 3B | Autoregressive (FAST tokenizer) | ✗ | ✗ | ✅ Apache 2.0 (openpi) |
| **pi0.5** | Apr 2025 | 3.3B | PaliGemma 3B | Two-stage: FAST pretrain → flow matching | ✗ | ✗ | ✅ Apache 2.0 ([HF](https://huggingface.co/lerobot/pi05_base)) |
| **pi0.6 / pi\*0.6** | Nov 2025 | ~5B | Gemma3 4B | Flow + token dual | ✗ | ✗ | Not officially released; third-party reimplementations exist |
| **pi0.7** | Apr 2026 | ~5B | Gemma3 4B + 400M vision | Flow matching (860M DiT) | ✗ | ✗ | Not released as of May 2026 |

All pi versions use parallel-jaw grippers only. Action space is 18-19D (dual 6-DoF arms + grippers + base). No force or impedance output in any version.

### 6.2 NVIDIA GR00T Family

| Version | Date | Params | VLM Backbone | DiT Layers | Dex Hand | Force/Impedance | Open Weights |
|---|---|---|---|---|---|---|---|
| **GR00T N1** | Mar 2025 | 2.2B | Eagle-2 | 16 | Fourier hands (humanoid-integrated) | ✗ | ✅ Non-commercial ([HF](https://huggingface.co/nvidia/GR00T-N1-2B)) |
| **GR00T N1.5** | Mid 2025 | 3B | Eagle 2.5 (frozen) | 16 | Not documented | ✗ | ✅ Non-commercial ([HF](https://huggingface.co/nvidia/GR00T-N1.5-3B)) |
| **GR00T N1.6** | Late 2025 | 3B | Cosmos-2B | 32 | Not documented | ✗ | ✅ ([HF](https://huggingface.co/nvidia/GR00T-N1.6-3B)) |
| **GR00T N1.7** | May 2026 | 3B | Cosmos-Reason2-2B (Qwen3-VL) | 32 | 22-DoF (EgoScale/Sharpa repr.) | ✗ | ✅ Commercial OK ([HF](https://huggingface.co/nvidia/GR00T-N1.7-3B)) |

**GR00T-Dexterity** is a separate RL workflow (not a VLA model) based on DextrAH-G. It supports Allegro Hand (16 DoF) + Kuka with geometric fabrics in Isaac Lab. The GR00T N1.x VLA models do not directly output multi-finger hand actions.

All GR00T VLA versions output position targets only. "22 DoF hands" in N1.7 originates from the EgoScale pretraining framework, which represents human hand motion as 22-DoF Sharpa hand joint angles. The Unitree G1's physical hand (Dex3-1) has only 7 DoF per hand. The 22-DoF capability refers to the action representation used during human video pretraining, not the deployment hand.

### 6.3 Other Major VLAs

| Paper | Group | Venue | Year | Dex Hand? | Force Output? | Open Code | Open Weights | Key Feature |
|---|---|---|---|---|---|---|---|---|
| [**Gemini Robotics**](https://arxiv.org/abs/2503.20020) | Google DeepMind | arXiv | 2025 | ✗ (gripper) | ✗ | ✗ | ✗ (closed, trusted testers) | Gemini 2.0-based VLA; 2x SOTA on generalization benchmark; ALOHA/Franka/Apollo |
| **Gemini Robotics 1.5** | Google DeepMind | Blog | 2026 | ✗ | ✗ | ✗ | ✗ (trusted testers) | VLA + reasoning; cross-embodiment; Gemini API (ER 1.5) |
| **Gemini Robotics On-Device** | Google DeepMind | Blog | 2025 | ✗ | ✗ | SDK (limited) | ✗ | On-device VLA; fine-tune with 50-100 demos; no network dependency |
| [**RT-2**](https://arxiv.org/abs/2307.15818) | Google DeepMind | CoRL | 2023 | ✗ | ✗ | ✗ | ✗ (closed) | 55B VLM co-fine-tuned for robot actions |
| [**OpenVLA**](https://arxiv.org/abs/2406.09246) | Berkeley/Stanford | CoRL | 2024 | ✗ | ✗ | [GitHub](https://github.com/openvla/openvla) ✅ | ✅ HF | 7B VLA baseline, Apache 2.0 |
| [**OpenVLA-OFT**](https://arxiv.org/abs/2502.19645) | Stanford/Berkeley | RSS | 2025 | ✗ (ALOHA) | ✗ | [GitHub](https://github.com/moojink/openvla-oft) ✅ | ✅ | 26x faster inference, parallel decoding |
| [**Octo**](https://arxiv.org/abs/2405.12213) | Berkeley RAIL | RSS | 2024 | ✗ | ✗ | [GitHub](https://github.com/octo-models/octo) ✅ | ✅ HF | 93M, modular fine-tuning |
| [**RDT-1B**](https://arxiv.org/abs/2410.07864) | Tsinghua thu-ml | ICLR | 2025 | ✗ (bimanual) | ✗ | [GitHub](https://github.com/thu-ml/RoboticsDiffusionTransformer) ✅ | ✅ HF 1B | Largest open diffusion model |
| [**HPT**](https://arxiv.org/abs/2409.20537) | MIT (Kaiming He) | NeurIPS | 2024 | ✗ | ✗ | [GitHub](https://github.com/liruiw/HPT) ✅ | ✗ | Heterogeneous embodiment pre-training |
| [**CogACT**](https://arxiv.org/abs/2411.19650) | Microsoft | arXiv | 2024 | ✗ | ✗ | [GitHub](https://github.com/microsoft/CogACT) ✅ | ✗ | Cognition-action separation |
| [**EgoScale**](https://arxiv.org/abs/2602.16710) | NVIDIA/Berkeley | arXiv | 2026 | ✅ 22-DoF | ✗ | ✗ | ✗ | 20K hrs human video, dexterous scaling law |
| [**SimpleVLA-RL**](https://arxiv.org/abs/2509.09674) | — | ICLR | 2025 | ✗ | ✗ | [GitHub](https://github.com/PRIME-RL/SimpleVLA-RL) ✅ | ✗ | RL fine-tuning of VLA |
| [**SpatialVLA**](https://arxiv.org/abs/2501.15830) | Shanghai AI Lab / Multi-inst. | RSS | 2025 | ✗ | ✗ | ✅ (project page) | ✅ | 3.5B VLA with Ego3D position encoding + adaptive action grids on PaliGemma2 |
| [**TinyVLA**](https://arxiv.org/abs/2409.12514) | ECNU / Midea | AAAI | 2025 | ✗ | ✗ | ✗ (project page only) | ✗ | 1.3B VLA + diffusion decoder; matches 7B OpenVLA at 20x speed |
| [**LLARVA**](https://arxiv.org/abs/2406.11815) | UC Berkeley | arXiv | 2024 | ✗ | ✗ | ✗ (project page only) | ✗ | Vision-action instruction tuning with 2D visual trace auxiliary task |
| [**UniAct**](https://arxiv.org/abs/2501.10105) | Multi-inst. | CVPR | 2025 | Designed for diverse | ✗ | [GitHub](https://github.com/2toinf/UniAct) ✅ | ✗ | Universal action codebook |

### 6.4 Visuomotor Policies (without language conditioning)

Influential visuomotor policies that do not use a VLM backbone but are widely adopted as baselines or building blocks for dexterous manipulation.

| Paper | Group | Venue | Year | Dex Hand? | Force Output? | Open Code | Open Weights | Key Feature |
|---|---|---|---|---|---|---|---|---|
| [**Diffusion Policy**](https://arxiv.org/abs/2303.04137) | Columbia (Shuran Song) | RSS | 2023 | ✗ | ✗ | [GitHub](https://github.com/real-stanford/diffusion_policy) ✅ | ✗ | Foundational diffusion policy method |
| [**ACT / ALOHA**](https://arxiv.org/abs/2304.13705) | Stanford (Tony Zhao) | RSS | 2023 | ✗ (gripper) | ✗ | [GitHub](https://github.com/tonyzhaozh/act) ✅ | ✗ | Action chunking transformer, bimanual teleop |
| [**DP3**](https://arxiv.org/abs/2403.03954) | Tsinghua (Yanjie Ze) | RSS | 2024 | ✅ (sim) | ✗ | [GitHub](https://github.com/YanjieZe/3D-Diffusion-Policy) ✅ | ✗ | 3D point cloud diffusion, 72 tasks |
| [**iDP3**](https://arxiv.org/abs/2410.10803) | Stanford/Tsinghua | IROS | 2025 | ✅ Inspire (25 DoF) | ✗ | [GitHub](https://github.com/YanjieZe/Improved-3D-Diffusion-Policy) ✅ | ✗ | Egocentric 3D on Fourier GR1 humanoid |
| [**DexWM**](https://arxiv.org/abs/2512.13644) | Meta FAIR / NYU | arXiv | 2025 | ✅ Allegro + Franka | ✗ | ✗ | ✗ | World model for dexterous hand-object interaction |

---

## 7. RL-based Dexterous Manipulation

### 7.1 Dexterous Grasping

| Paper | Group | Venue | Year | RL Algo | Hand (DoF) | Sim | Sim2Real | Objects | Code | Weights |
|---|---|---|---|---|---|---|---|---|---|---|
| [**CrossDex**](https://arxiv.org/abs/2410.02479) | PKU-RL | ICLR | 2025 | PPO + DAgger | 6 hands (Shadow, Allegro, LEAP, ...) | IsaacGym P4 | ✅ | 100 (YCB+GRAB) | [GitHub](https://github.com/PKU-RL/CrossDex) ✅ | Partial |
| [**ResDex**](https://arxiv.org/abs/2410.01481) | PKU-RL | ICLR | 2025 | PPO + MoE + DAgger | Shadow (24) | IsaacGym P4 | ✗ | 3200, 88.8% | [GitHub](https://github.com/PKU-RL/ResDex) ✅ | Partial |
| [**UniDexGrasp++**](https://arxiv.org/abs/2304.00464) | PKU-EPIC | ICCV | 2023 | PPO + DAgger | Shadow (24) | IsaacGym | ✗ | 3000+, 85.4% | [GitHub](https://github.com/PKU-EPIC/UniDexGrasp2) ✅ | ✅ state ckpt |
| [**UniDexGrasp**](https://arxiv.org/abs/2303.00938) | PKU-EPIC | CVPR | 2023 | PPO (goal-conditioned) | Shadow (24) | IsaacGym | ✗ | 3000+, ~60% | [GitHub](https://github.com/PKU-EPIC/UniDexGrasp) ✅ | ✗ |
| [**BODex**](https://arxiv.org/abs/2412.16490) | PKU-EPIC | ICRA | 2025 | Bilevel optimization | Shadow, Allegro, LEAP | cuRobo | ✅ 81% | 5355 | [GitHub](https://github.com/JYChen18/BODex) ✅ | Dataset on HF |
| [**DexGrasp Anything**](https://arxiv.org/abs/2409.11159) | ShanghaiTech | CVPR Highlight | 2025 | Diffusion | Shadow | IsaacGym | ✗ | 15K+, 3.4M grasps | [GitHub](https://github.com/4DVLab/DexGrasp-Anything) ✅ | ✅ HF+GDrive |
| [**DexGraspNet 2.0**](https://arxiv.org/abs/2410.15590) | PKU-EPIC | CoRL | 2024 | Diffusion | Shadow | IsaacGym | ✅ 90.7% | 1319, 426M grasps | [GitHub](https://github.com/PKU-EPIC/DexGraspNet2) ✅ | ✅ HF |
| [**RobustDexGrasp**](https://arxiv.org/abs/2501.01771) | ETH Zurich | CoRL | 2025 | PPO + teacher-student | Allegro (16) + UR5 | RaiSim | ✅ 94.6% | 247K sim, 512 real | [GitHub](https://github.com/zdchan/RobustDexGrasp) ✅ | ✅ |
| [**Dexonomy**](https://arxiv.org/abs/2504.01301) | PKU-EPIC | RSS | 2025 | Optimization | Shadow, Allegro, LEAP, Unitree G1 | MuJoCo + cuRobo | ✅ 82.3% | 10.7K, 31 types | [GitHub](https://github.com/JYChen18/Dexonomy) ✅ | HF |
| [**UltraDexGrasp**](https://arxiv.org/abs/2603.05312) | InternRobotics | ICRA | 2026 | Multi-strategy | Multiple | BODex + cuRobo | ✅ 81.2% | 20M frames | [GitHub](https://github.com/InternRobotics/UltraDexGrasp) ✅ | ✗ |
| [**DexPoint**](https://arxiv.org/abs/2211.09423) | UCSD | CoRL | 2022 | PPO (point cloud) | Allegro (16) | IsaacGym | ✅ | Category-level novel | [GitHub](https://github.com/yzqin/dexpoint-release) ✅ | ✗ |
| [**AnyGrasp**](https://arxiv.org/abs/2212.08333) | SJTU (Cewu Lu) | IEEE T-RO | 2023 | Supervised (GSNet) | Parallel-jaw gripper | GraspNet-1B | ✅ 93.3% | 300+ unseen, >900 picks/hr | [SDK](https://github.com/graspnet/anygrasp_sdk) (license) | ✗ | Upstream grasp detection (parallel-jaw). Included as widely-used perception module upstream of dexterous VLA pipelines. |
| [**DextrAH-G/RGB**](https://arxiv.org/abs/2407.02274) | NVIDIA | CoRL | 2024 | PPO + geometric fabrics | Allegro (16) + Kuka | Isaac Lab | ✅ | Multi-object | [GitHub](https://github.com/NVlabs/DEXTRAH) ✅ | ✗ |

### 7.2 In-Hand Manipulation / Reorientation

| Paper | Group | Venue | Year | Hand (DoF) | Sim | Sim2Real | Code | Weights |
|---|---|---|---|---|---|---|---|---|
| [**Dactyl**](https://arxiv.org/abs/1808.00177) | OpenAI | arXiv 2018 / IJRR 2020 | 2018 | Shadow (24) | MuJoCo | ✅ (ADR) | ✗ | ✗ |
| [**Hora**](https://arxiv.org/abs/2210.04887) | Berkeley/Meta | CoRL | 2022 | Allegro (16) | IsaacGym P4 | ✅ | [GitHub](https://github.com/HaozhiQi/hora) ✅ | ✅ |
| [**Rotating w/o Seeing**](https://arxiv.org/abs/2303.10880) | UCSD | RSS | 2023 | Allegro (16) + binary tactile | IsaacGym | ✅ | [Page](https://touchdexterity.github.io) | ✗ |
| [**General In-Hand Rotation**](https://arxiv.org/abs/2309.09979) | Berkeley/Meta | CoRL | 2023 | Allegro (16) + DIGIT | IsaacGym | ✅ | (in hora repo) | ✗ |
| [**RotateIt**](https://arxiv.org/abs/2309.02388) | Berkeley/Meta/CMU | CoRL | 2023 | Allegro (16) + DIGIT | IsaacGym | ✅ | (in hora repo) | ✗ |
| [**AnyRotate**](https://arxiv.org/abs/2405.07391) | U. Bristol | CoRL | 2024 | Allegro (16) + tactile | IsaacGym | ✅ | ✗ | ✗ |
| [**Visual Dexterity**](https://arxiv.org/abs/2211.11744) | MIT CSAIL | Science Robotics | 2023 | D'Claw (9/12) | IsaacGym P3 | ✅ | [GitHub](https://github.com/Improbable-AI/dexenv) ✅ | ✅ |
| [**DeXtreme**](https://arxiv.org/abs/2210.13702) | NVIDIA | ICRA | 2023 | Allegro (16) | IsaacGym | ✅ | In IsaacGymEnvs ✅ | ✗ |
| [**DexPBT**](https://arxiv.org/abs/2305.12127) | NVIDIA | RSS | 2023 | Allegro (16) + Kuka | IsaacGym | ✗ | In IsaacGymEnvs ✅ | ✗ |
| [**SAPG**](https://arxiv.org/abs/2407.04890) | CMU | ICML Oral | 2024 | Allegro/Shadow (16-46) | IsaacGym P4 | ✗ | [GitHub](https://github.com/jayeshs999/sapg) ✅ | ✗ |
| [**DexHandDiff**](https://arxiv.org/abs/2411.18562) | HKU/Berkeley | CVPR | 2025 | Shadow | Adroit (MuJoCo) | ✗ | [GitHub](https://github.com/Liang-ZX/DexHandDiff) ✅ | ✅ HF |

### 7.3 Long-Horizon / Multi-Stage / Contact-Rich

| Paper | Group | Venue | Year | Hand (DoF) | Tasks | Sim | Sim2Real | Code | Weights |
|---|---|---|---|---|---|---|---|---|---|
| [**SeqDex**](https://arxiv.org/abs/2309.00987) | Stanford | CoRL | 2023 | Allegro (16) | Chained policies (search→orient→grasp→insert) | IsaacGym | ✅ | [GitHub](https://github.com/sequential-dexterity/SeqDex) ✅ | ✅ |
| [**Bi-DexHands**](https://arxiv.org/abs/2206.08686) | PKU-MARL | NeurIPS | 2022 | 2x Shadow (48) | 16+ bimanual tasks | IsaacGym | ✗ | [GitHub](https://github.com/PKU-MARL/DexterousHands) ✅ | ✅ |
| [**DexArt**](https://arxiv.org/abs/2305.05706) | UCSD | CVPR | 2023 | Allegro (16) | 4 articulated object tasks | SAPIEN | ✗ | [GitHub](https://github.com/Kami-code/dexart-release) ✅ | ✅ |
| [**TCDM**](https://arxiv.org/abs/2209.11221) | Meta | ICRA | 2023 | 3 hand platforms | 50 tasks, 34 objects | MuJoCo | ✗ | [GitHub](https://github.com/facebookresearch/TCDM) ✅ | ✅ |
| [**VTDexManip**](https://arxiv.org/abs/2501.01370) | - | ICLR | 2025 | Multi-finger (sim) | 6 tasks (bottle cap, faucet, reorientation) | IsaacGym | ✗ | [GitHub](https://github.com/LQTS/VTDexManip) ✅ | ✅ 18 models |
| [**DexGarmentLab**](https://arxiv.org/abs/2503.18693) | Multi-inst. | NeurIPS Spotlight | 2025 | Bimanual dex | 15 garment tasks, 2500+ garments | IsaacSim | ✗ | [GitHub](https://github.com/wayrise/DexGarmentLab) ✅ | ✗ |
| [**Contact Trust Region**](https://arxiv.org/abs/2505.02291) | MIT CSAIL (Tedrake) | IJRR | 2025 | Allegro (16) | Contact-rich MPC | Drake | ✗ | ✗ | ✗ |
| [**Complementarity-Free**](https://arxiv.org/abs/2408.07855) | MIT CSAIL (Pang, Tedrake) | RSS | 2024 | Allegro (16) | Closed-form differentiable contact, 50-100 Hz MPC | Drake | ✗ | ✗ | ✗ |
| [**ComFree-Sim**](https://arxiv.org/abs/2603.12185) | — | arXiv | 2026 | LEAP Hand | GPU-parallel contact MPC on NVIDIA Warp | Custom (Warp) | ✗ | ✗ | ✗ |

Note: IndustReal (NVIDIA, RSS 2023) also addresses contact-rich assembly with RL; see §5 for details.

### 7.4 Additional Recent RL

| Paper | Group | Venue | Year | Hand (DoF) | Tasks | Sim2Real | Code |
|---|---|---|---|---|---|---|---|
| [**DQ-RISE**](https://arxiv.org/abs/2503.01766) | SJTU | ICRA | 2026 | OyMotion RoHand + Flexiv Rizon 4 | 6 real tasks, 85.83% | ✅ | [GitHub](https://github.com/rise-policy/DQ-RISE) ✅ |
| [**DexTrack**](https://arxiv.org/abs/2501.15760) | PKU/Shanghai AI | ICLR | 2025 | Shadow (24), Allegro (16) | MoCap tracking | ✗ | [GitHub](https://github.com/Meowuu7/DexTrack) partial |
| [**BiDexHD**](https://arxiv.org/abs/2501.09821) | PKU | arXiv | 2025 | 2x Shadow (48) | 141 bimanual tasks (TACO) | ✗ | ✗ |
| [**HandelBot**](https://arxiv.org/abs/2603.12243) | Stanford | arXiv | 2026 | LEAP (16) bimanual | Real piano playing | ✅ | [GitHub](https://github.com/amberxie88/handelbot) ✅ |
| [**DexDrummer**](https://arxiv.org/abs/2603.22263) | Stanford | arXiv | 2026 | Bimanual dexterous | Drumming (contact-rich) | ✗ | [GitHub](https://github.com/hc-fang/dexdrummer) ✅ |
| [**RoboPianist**](https://arxiv.org/abs/2304.04150) | Google/Berkeley | CoRL | 2023 | Anthropomorphic bimanual | Piano (150 pieces) | ✗ | [GitHub](https://github.com/google-research/robopianist) ✅ |
| [**DemoStart**](https://arxiv.org/abs/2409.06613) | Google DeepMind | ICRA | 2024 | DEX-EE (3-finger) | Plug insertion, cube reorientation | ✅ | ✗ |
| **Closing Reality Gap** | - | arXiv | 2026 | 5-finger hand | Force-controlled grasping | ✅ zero-shot | ✗ |
| [**Maniwhere**](https://arxiv.org/abs/2407.15815) | Shanghai AI Lab | CoRL | 2024 | Allegro (16) | 8 tasks, visual generalization | ✅ | [GitHub](https://github.com/gemcollector/maniwhere) ✅ |
| [**Eureka**](https://arxiv.org/abs/2310.12931) | NVIDIA | ICLR | 2024 | Shadow (24, sim) | LLM-generated rewards, pen spinning | ✗ | [GitHub](https://github.com/eureka-research/Eureka) ✅ |
| [**DrEureka**](https://arxiv.org/abs/2406.01967) | NVIDIA | RSS | 2024 | Shadow (sim) + quadruped | LLM-guided DR, sim2real | ✅ | [GitHub](https://github.com/eureka-research/DrEureka) ✅ |
| [**DexMV**](https://arxiv.org/abs/2108.05877) | UCSD | ECCV | 2022 | Adroit (30, sim) | IL from human video (pour, place, relocate) | ✗ | [GitHub](https://github.com/yzqin/dexmv-sim) ✅ |
| [**CyberDemo**](https://arxiv.org/abs/2402.14795) | UCSD | CVPR | 2024 | Allegro (16) | Augmented sim demos, valve rotation | ✅ | [GitHub](https://github.com/wang59695487/CyberDemo) ✅ |

---

## 8. Datasets

### 8.1 Robot Dexterous Hand Datasets

| Dataset | Year | Venue | Scale | Hand Type | Tasks | F/T or Tactile | Download | Format |
|---|---|---|---|---|---|---|---|---|
| **UniDex** | 2026 | CVPR | 9M frames, 50K+ traj | 8 robot hands (FAAS) | Diverse manipulation | ✗ | ✅ [HF](https://huggingface.co/datasets/UniDex-ai/UniDex) | HDF5 |
| **Dexora** | 2025 | ICRA | 12.2K eps, 40.5h real | Bimanual 36-DoF | Pick, manip, assembly, tool | ✗ | ✅ [HF](https://huggingface.co/datasets/ZZongzheng0918/Dexora) | Parquet+MP4 |
| **DexMimicGen** | 2024 | ICRA | 21K demos | Bimanual dexterous | 9 tasks | ✗ | ✅ [HF](https://huggingface.co/datasets/MimicGen/dexmimicgen_datasets) 59.9GB | HDF5 |
| **DexGraspNet 2.0** | 2024 | CoRL | 426M grasps | Shadow | Grasping | ✗ | ✅ [HF](https://huggingface.co/datasets/lhrlhr/DexGraspNet2.0) | WebDataset |
| **VTDexManip** | 2025 | ICLR | 565K frames, 182 objects | Multi-finger (sim) | 6 complex tasks | ✅ binary tactile | ✅ [GitHub](https://github.com/LQTS/VTDexManip) | IsaacGym |
| **ManipTrans/DexManipNet** | 2025 | CVPR | 3.3K episodes | 6 hands | Bimanual manipulation | ✗ | ✅ [HF](https://huggingface.co/datasets/ManipTrans/DexManipNet) | MuJoCo |
| **CEDex** | 2026 | ICRA | 20M grasps, 500K objects | Shadow, Allegro, LEAP | Cross-embodiment grasps | ✗ | ✅ [GitHub](https://github.com/GeorgeWuzy/CEDex-Grasp) | Custom |
| **Dexonomy** | 2025 | RSS | 9.5M grasps, 10.7K objects | Shadow (released; paper covers Allegro, LEAP) | 31 grasp types | ✗ | ✅ [HF](https://huggingface.co/datasets/JiayiChenPKU/Dexonomy) | Custom |
| **Dex1B** | 2025 | RSS | 1B demos, 6K+ objects | Shadow, Inspire, Ability | Grasp + articulation | ✗ | Unclear | Custom |
| **Fourier ActionNet** | 2025 | — | 30K+ traj, 140 hrs | Fourier Dex Hands | Real humanoid bimanual | ✗ | ✅ [action-net.org](https://action-net.org/) | Custom |
| **RoboMIND** | 2025 | RSS | 107K traj, 479 tasks | Multi-embodiment incl. dex | Diverse manipulation | ✗ | ✅ [HF](https://huggingface.co/datasets/x-humanoid-robomind/RoboMIND) | Custom |
| **Bi-DexHands** | 2022 | NeurIPS | Offline RL datasets | 2x Shadow | 16+ bimanual tasks | ✗ | ✅ [GitHub](https://github.com/PKU-MARL/DexterousHands) | IsaacGym |
| **TCDM** | 2023 | ICRA | 50 tasks, 34 objects | 3 hand platforms | Diverse manipulation | ✗ | ✅ [GitHub](https://github.com/facebookresearch/TCDM) | MuJoCo |
| **DAPG** | 2018 | RSS | 25 human demos/task | Shadow (sim) | Pen, door, hammer, ball | ✗ | ✅ [GitHub](https://github.com/aravindr93/hand_dapg) | Pickle/NumPy |

### 8.2 Force / Tactile / Contact Datasets

| Dataset | Year | Venue | Scale | Sensor Type | Hand | Download | Key Feature |
|---|---|---|---|---|---|---|---|
| **ForceVLA-Data** | 2025 | NeurIPS | 244 traj, 140K steps | 6-axis F/T | Gripper (Flexiv) | ✅ [HF](https://huggingface.co/datasets/qiaojunyu/ForceVLA-real-data) | Contact-rich 5 tasks |
| **REASSEMBLE** | 2024 | RSS | 4551 demos, 781 min | F/T + event cam + audio | Gripper | ✅ [TUData](https://researchdata.tuwien.ac.at/records/0ewrv-8cb44) | Multi-modal assembly |
| **RH20T** | 2023 | NeurIPS | 110K eps, 50M frames | F/T + fingertip tactile | Gripper | ✅ [Site](https://rh20t.github.io/) | 140+ tasks |
| **Touch100k** | 2025 | Info. Fusion | 101K samples | GelSight | N/A | ✅ [GitHub](https://github.com/cocacola-lab/TLV-Link) | Large-scale touch-language-vision dataset |
| **Sparsh/TacBench** | 2024 | CoRL | 460K+ images | DIGIT/GelSight (cross-sensor) | N/A | ✅ [GitHub](https://github.com/facebookresearch/sparsh) | Cross-sensor SSL tactile encoder, 5-task benchmark |
| **TVL** | 2024 | ICML | 44K pairs | DIGIT | N/A | ✅ [GitHub](https://github.com/Max-Fu/tvl) + [HF](https://huggingface.co/datasets/Max-Fu/TVL) | Touch-vision-language alignment |
| **FMB** | 2025 | IJRR | 22.5K demos | F/T (Franka) | Gripper | ✅ [HF](https://huggingface.co/datasets/charlesxu0124/functional-manipulation-benchmark) | Functional manipulation |
| **FeelSight** | 2024 | Science Robotics | 70 experiments | DIGIT + Allegro | Allegro (16) | ✅ [HF](https://huggingface.co/datasets/suddhu/Feelsight) | In-hand tactile-visual tracking |
| **ContactPose** | 2020 | ECCV | 2306 grasps, 2.9M imgs | Thermal contact | Human | ✅ [GitHub](https://github.com/facebookresearch/ContactPose) | Functional grasping |

### 8.3 Human Hand / Egocentric Datasets

| Dataset | Year | Venue | Scale | Modality | Tasks | Language | Download |
|---|---|---|---|---|---|---|---|
| **EgoDex** | 2025 | ICLR | 829h, 30Hz 1080p | Ego RGB + 68-joint 3D (AVP) | 194 tabletop | ✅ LLM descriptions | ✅ [GitHub](https://github.com/apple/ml-egodex) ~1.7TB |
| **DexCanvas** | 2025 | arXiv | 7000h (v0.1=1%) | Multi-view RGB-D + MANO | 21 manip types | ✗ | ✅ [HF](https://huggingface.co/datasets/DEXROBOT/DexCanvas) v0.1 |
| **GigaHands** | 2025 | CVPR | 34h, 14K clips | Multi-view RGB + 3D hand | Bimanual | ✅ 84K annotations | ✅ [Site](https://ivl.cs.brown.edu/research/gigahands.html) |
| **DexWild** | 2025 | RSS | 9.5K eps, 33h | Multi-view RGB + gloves | 5 tasks | ✅ | ✅ [HF](https://huggingface.co/datasets/boardd/dexwild-dataset) 2.14TB |
| **HOI4D** | 2022 | CVPR | 2.4M RGB-D, 4K seq | Ego RGB-D + 3D hand | Category-level | ✅ action labels | ✅ [Site](https://hoi4d.github.io/) |
| **GRAB** | 2020 | ECCV | 1.62M frames | SMPL-X + MANO + contact | Whole-body grasping | ✗ | ✅ [Site](https://grab.is.tue.mpg.de/) (registration) |
| **ARCTIC** | 2023 | CVPR | 2.1M frames | RGB + MANO + contact | Bimanual articulated | ✗ | ✅ [Site](https://arctic.is.tue.mpg.de/) ~116GB |
| **OakInk / OakInk2** | 2022/24 | CVPR | 230K+ frames | RGB + MANO + object | Hand-object interaction | ✅ (v2) | ✅ [HF](https://huggingface.co/datasets/kelvin34501/OakInk-v2) |
| **DexYCB** | 2021 | CVPR | 582K RGB-D | RGB-D + MANO + object | Grasping (20 YCB) | ✗ | ✅ [Site](https://dex-ycb.github.io/) 119GB |
| **Ego-Exo4D** | 2024 | CVPR | 1286h, 740 participants | Ego+exo RGB + IMU + gaze | Skilled activities | ✅ | ✅ [Site](https://ego-exo4d-data.org/) (registration) |
| **Humanoid Everyday** | 2025 | arXiv | 10.3K traj, 3M frames | RGB + depth + LiDAR + tactile | 260 dexterous tasks | ✅ | ✅ [HF](https://huggingface.co/datasets/USC-GVL/humanoid-everyday) |

### 8.4 Cross-Embodiment Pretraining Datasets

| Dataset | Year | Venue | Scale | Embodiments | Tasks | Format | Download |
|---|---|---|---|---|---|---|---|
| [**Open X-Embodiment (OXE)**](https://arxiv.org/abs/2310.08864) | 2023 | arXiv/ICRA | ~1M episodes | 22 robots (grippers only) | 527 skills, 160K+ tasks | RLDS (TF Datasets) | ✅ [Site](https://robotics-transformer-x.github.io/) |
| [**DROID**](https://arxiv.org/abs/2403.12945) | 2024 | arXiv | 76K demos, 350h | Franka Panda (1 embodiment, 564 scenes) | 84 tasks, 50 operators | Stereo RGB + proprio + lang | ✅ [Site](https://droid-dataset.github.io/) |

---

## 9. Simulation Benchmarks & Platforms

| Benchmark | Venue | Year | Dex Hand | Sim Platform | Key Feature | Install |
|---|---|---|---|---|---|---|
| [**ManiSkill3**](https://arxiv.org/abs/2410.00425) | RSS | 2025 | Allegro, DClaw | SAPIEN (GPU) | 430x faster, RL/IL/VLA baselines | `pip install mani-skill` |
| **MuJoCo Playground** | RSS demo | 2025 | LEAP Hand | MuJoCo | Train in minutes, zero-shot sim2real | `pip install playground` |
| **MuJoCo Manipulus** | 2025 | 2025 | Tool manipulation | MuJoCo | 16 tool use tasks | Open source |
| **Adroit** | RSS | 2018 | Shadow (24) | MuJoCo | Standard RL baseline | `pip install gymnasium-robotics` |
| **Genesis** | Dec 2024 | 2024 | Any URDF | Genesis | 430Kx real-time, differentiable | `pip install genesis-world` |
| **DiffTactile** | ICLR | 2024 | Multi-finger | Custom | Differentiable FEM tactile sim | [GitHub](https://github.com/Genesis-Embodied-AI/DiffTactile) |
| **TeleOpBench** | 2025 | 2025 | 3 humanoids | Isaac Sim | 30 tasks, 4 teleop modalities | [GitHub](https://github.com/cyjdlhy/TeleOpBench) |
| [**Isaac Lab**](https://isaac-sim.github.io/IsaacLab/) | RA-L / 2024 | 2024 | Allegro, Shadow, any URDF | Isaac Sim (PhysX 5) | IsaacGym successor, GPU-parallel, RTX rendering | `pip install isaaclab` |
| [**TACTO**](https://github.com/facebookresearch/tacto) | RA-L | 2022 | Gripper (DIGIT/GelSight sim) | PyBullet + PyRender | Vision-based tactile sensor simulator | `pip install tacto` |
| [**BiGym 2.0**](https://arxiv.org/abs/2610.07594v2) | — | 2026 | Unitree G1, 2 Dex1 parallel grippers | MuJoCo | 20 household tasks, 60 VR demos/task, shared whole-body controller | [GitHub](https://github.com/swirl-uk/BiGym2) |

---

## 10. Teleoperation Systems

| System | Group | Venue | Year | Input | Target Hand | Force Feedback | Cost | Code |
|---|---|---|---|---|---|---|---|---|
| [**DexCap**](https://arxiv.org/abs/2403.07788) | Stanford | RSS | 2024 | SLAM + electromagnetic | LEAP Hand | ✗ | ~$2K | [GitHub](https://github.com/j96w/DexCap) ✅ |
| [**BunnyVisionPro**](https://arxiv.org/abs/2407.03162) | HKU / UCSD | arXiv | 2024 | Apple Vision Pro | Bimanual dex | Low-cost haptic | ~$3.5K+ | [GitHub](https://github.com/Dingry/BunnyVisionPro) ✅ |
| **AnyTeleop** | UCSD | RSS | 2023 | Vision (camera) | Multiple | ✗ | Low | Project page |
| [**DOGlove**](https://arxiv.org/abs/2505.14635) | TEA Lab | RSS | 2025 | Haptic glove | Any dex hand | ✅ 5-DoF | <$600 | [GitHub](https://github.com/TEA-Lab/DOGlove) ✅ |
| [**DEXOP**](https://arxiv.org/abs/2509.04441) | Stanford | arXiv | 2025 | Passive exoskeleton | Any dex hand | ✅ proprioceptive | - | [Page](https://dex-op.github.io/) |
| [**DEX-Mouse**](https://arxiv.org/abs/2604.15013) | - | arXiv | 2026 | Handheld interface | Universal | ✅ kinesthetic | <$150 | Open-sourced |
| [**Open TeleDex**](https://arxiv.org/abs/2510.14771) | - | arXiv | 2025 | Phone-based | Any arm + hand | ✗ | Very low | [GitHub](https://github.com/omarrayyann/TeleDex) ✅ |
| [**OmniH2O**](https://arxiv.org/abs/2406.08858) | CMU LeCAR | CoRL | 2024 | VR/voice/RGB | Humanoid | ✗ | - | [GitHub](https://github.com/LeCAR-Lab/human2humanoid) ✅ |
| [**Open-TeleVision**](https://arxiv.org/abs/2407.10107) | UCSD | CoRL | 2024 | Stereo VR | Bimanual dex | ✗ | - | [GitHub](https://github.com/OpenTeleVision/TeleVision) ✅ |
| [**HATO**](https://arxiv.org/abs/2404.16823) | UC Berkeley | ICRA | 2024 | Meta Quest 2 VR | 2x Psyonic Ability Hand (6 DoF) + touch sensors | ✗ (touch on robot only) | Low (VR + prosthetic hands) | [GitHub](https://toruowo.github.io/hato/) ✅ |
| [**DexPilot**](https://arxiv.org/abs/1910.03135) | NVIDIA | ICRA | 2020 | Vision (bare hand, single RGB camera) | Allegro (16) + Kuka IIWA | ✗ | Very low (camera only) | [Page](https://sites.google.com/view/dex-pilot) |

---

## 11. Low-Cost Dexterous Hand Hardware

| Hand | Group | Year | DoF | Cost | Sim2Real | Tactile | Design Files |
|---|---|---|---|---|---|---|---|
| **LEAP Hand V2** | CMU (Pathak) | 2024 | 16 + palm | ~$3K | ✅ | ✗ | [Page](https://v2-adv.leaphand.com/) |
| **ORCA Hand** | ETH Zurich | 2025 | 17 | <$2K | ✅ (1hr train) | ✅ | [orcahand.com](https://www.orcahand.com/) fully open |
| **ISyHand** | MPI-IS | 2025 | 18 (12+6 palm) | ~$1.3K | ✅ | ✗ | [Page](https://isyhand.is.mpg.de/) |
| **RUKA Hand** | NYU (Pinto) | 2025 | 15 | <$1.3K | ✅ | ✗ | [Page](https://ruka-hand.github.io/) |
| **FAIVE Hand** | ETH Zurich (SRL) | 2024 | 11+ | ~$500-800 | ✅ | ✗ | [GitHub](https://github.com/srl-ethz/faive-hand) fully open |
| **Ability Hand** | PSYONIC Inc. | 2024 | 6 | Commercial | — | ✅ fingertip pressure | [psyonic.io](https://www.psyonic.io/ability-hand) closed |
| **XHand / Inspire Hand** | Chinese manufacturers | 2023+ | 12-16 | ~$1-3K | Partial | ✗ | Closed-source commercial |
| **Digit 360** | Meta FAIR | 2024 | N/A (sensor) | - | N/A | ✅ 18+ modalities | Planned open-source |

---

## 12. Tactile Representation Models

| Model | Group | Venue | Year | Key Feature | Code |
|---|---|---|---|---|---|
| **Sparsh** | Meta FAIR/CMU | CoRL | 2024 | SSL cross-sensor tactile encoder, TacBench 5-task benchmark | [GitHub](https://github.com/facebookresearch/sparsh) ✅, weights ✅ |
| **UniTouch** | UCSD | CVPR | 2024 | Unified touch-vision-language-sound alignment | [GitHub](https://github.com/cfeng16/UniTouch) ✅, weights ✅ |
| **AnyTouch** | Renmin Univ | ICLR | 2025 | Cross-sensor SSL with TacQuad 4-sensor dataset | [GitHub](https://github.com/GeWu-Lab/AnyTouch) ✅, weights ✅ |
| **NeuralFeels** | Meta FAIR | Science Robotics | 2024 | Neural field for Allegro+DIGIT in-hand tracking | [GitHub](https://github.com/facebookresearch/neuralfeels) ✅ |

---

## 13. Legged & Humanoid Robot Learning

| Paper | Year | Robot / Tasks | Key Method | Main Result | Code |
|---|---|---|---|---|---|

---

## 14. Learning-based, Optimal & Safe Control

| Paper | Year | Robot / Tasks | Key Method | Main Result | Code |
|---|---|---|---|---|---|

---

## 15. General Robot Manipulation & Imitation Learning

| Paper | Year | Robot / Tasks | Key Method | Main Result | Code |
|---|---|---|---|---|---|

---

## 16. Motion Planning & Decision Making

| Paper | Year | Robot / Tasks | Key Method | Main Result | Code |
|---|---|---|---|---|---|

---

## 17. State Estimation & Sensor Fusion

| Paper | Year | Robot / Tasks | Key Method | Main Result | Code |
|---|---|---|---|---|---|

---

## 18. Robot World Models & Embodied Foundation Models

| Paper | Year | Robot / Tasks | Key Method | Main Result | Code |
|---|---|---|---|---|---|
| [**GroundingPI**](https://arxiv.org/abs/2609.39601v1) | 2026 | Bimanual manipulation (RoboTwin 2.0), humanoid dexterous-hand manipulation (RoboCasa-GR1); driving (nuScenes) | 4B grounding model; shared point/box coordinate tokens; pretraining + SFT + GRPO; Action DiT for manipulation | First in all 4 OOD manipulation settings; RoboTwin2.0-Clean2Random success 17.60% vs Rex-Omni 14.10%; nuScenes open-loop L2 0.296 m | — |
| [**ScaleNav**](https://arxiv.org/abs/2610.25690v1) | 2026 | Unitree Go2; language-conditioned local navigation to initially visible targets | Shared DiT predicts video and action chunks; Internet video pretraining + simulated action alignment + joint fine-tuning; initial-frame anchor | Success: 86.5% on single-view Short-Horizon OVON, 94.9% on HabitatGS-LN, 83.3% on Go2 (60 trials) | [Project](https://zju3dv.github.io/ScaleNav/) |
| [**Ropedia W0**](https://arxiv.org/abs/2610.26855v1) | 2026 | Humans, gripper robots, and dexterous humanoids; locomotion and manipulation video prediction; Unitree G1 in Xp-Teleop | Video diffusion model with camera-pose and projected-skeleton conditions; Xp-Data human pretraining + human–robot training; distillation | DreamDojo In-lab PSNR: 20.854 dB vs DreamDojo 14B at 18.983 dB (Ropedia W0 5B; 1% post-training data) | — |

---

## 19. Open Research Directions

This section highlights under-explored intersections of capabilities that emerge from the surveyed literature. These are not exhaustive; concurrent or unpublished work may partially address some of these directions.

### 19.1 Capability Matrix

The following table maps representative systems against properties relevant to contact-rich dexterous manipulation. "Simulation" refers to publicly available simulation environments for training or evaluation.

|  | Multi-finger Hand | Tool Use | Force/Impedance Output | VLA/Language | Simulation |
|---|---|---|---|---|---|
| **pi0~0.7** | ✗ (gripper only) | ✗ | ✗ | ✅ | ✗ |
| **GR00T N1~1.7** | Humanoid-integrated only | ✗ | ✗ | ✅ | ✅ Isaac Lab |
| **GR00T-Dexterity** | ✅ Allegro | ✗ (grasp only) | ✗ | ✗ (RL only) | ✅ Isaac Lab |
| **UniDex-VLA** | ✅ 8 hands | ✅ | ✗ | ✅ | Partial (retargeting env) |
| **DexVLA** | ✅ | ✗ | ✗ | ✅ | ✗ |
| **SimToolReal** | ✅ Sharpa 22-DoF | ✅ 24 tasks | ✗ | ✗ | ✅ IsaacGym |
| **CompliantVLA-adaptor** | ✗ (gripper) | ✗ | ✅ K, D | ✅ (frozen VLA) | ✅ LIBERO |
| **CHIP** | Humanoid 35-DoF | ✗ | ✅ EE stiffness | ✗ (RL) | ✅ |
| **TacDiffusion** | ✗ (gripper) | ✗ | ✅ 6D wrench | ✗ | ✗ |
| **DexForce** | ✅ Allegro | ✗ | Fixed k_f (hand-tuned) | ✗ | ✗ |

### 19.2 Observations

Contact-rich manipulation with multi-finger hands — such as tool use, assembly, or handling fragile objects — requires regulating interaction forces, not just tracking position targets. Inadequate force control leads to object slip, tool breakage, or damage to the environment. While grippers can often compensate via mechanical compliance, high-DoF dexterous hands distribute contact across many fingertips, making per-contact force regulation both more critical and more challenging. This motivates examining whether existing systems combine dexterous control with force/impedance awareness.

The capability matrix and the broader survey reveal several patterns:

**Dexterous VLAs and force-aware policies have developed largely in isolation.** The dexterous VLA literature (§2) focuses on position-target generation across diverse hands, while the force/impedance literature (§3-5) focuses on contact-rich control for grippers and robot arms. UniDex-VLA, DexVLA, and DexGraspVLA all output position targets only. Conversely, systems that output impedance parameters (CompliantVLA-adaptor, CHIP, Comp-ACT, VICES) operate on grippers or arms. DexForce is the only dexterous-hand work incorporating force awareness, using hand-tuned fixed scaling on Allegro Hand.

**Cross-embodiment action representations remain fragmented.** Multiple approaches compete for representing dexterous hand actions across embodiments: FAAS (UniDex-VLA), eigengrasps (CrossDex), universal codebooks (UniAct), heterogeneous stems (HPT), and per-embodiment MLPs (GR00T). There is no consensus on which representation best supports cross-hand generalization, and direct comparisons across these approaches are scarce.

**Dexterous data collection is a recognized bottleneck.** The proliferation of low-cost teleoperation systems (§10) — DexCap, DOGlove, DEXOP, DEX-Mouse, all published 2024-2026 — signals that the community views data collection as a primary obstacle. Despite this effort, most dexterous datasets (§8.1) still capture only joint positions and visual data, with force/torque modality almost exclusively available for gripper-based systems (§8.2).

**Sim-to-real transfer for dexterous RL is maturing.** Multiple recent papers demonstrate zero-shot or near-zero-shot sim-to-real transfer for dexterous hands: CrossDex (LEAP), RobustDexGrasp (Allegro, 94.6%), DeXtreme (Allegro), DQ-RISE (LEAP+Franka, 85.8%), and HandelBot (bimanual LEAP). This suggests that simulation-trained dexterous policies are becoming practically deployable, lowering the barrier to sim-based research in this space.

**VLA model families remain gripper-centric.** Across all surveyed versions of pi (pi0 through pi0.7) and GR00T (N1 through N1.7), no version natively supports standalone multi-finger dexterous hands (§6.1-6.2). GR00T-Dexterity adds Allegro support but as a separate RL workflow, not as part of the VLA itself. The open-source VLA ecosystem (openpi, Isaac-GR00T, OpenVLA) has not yet been extended to dexterous hand embodiments by the community.

**Model-based contact control is a complementary axis.** Contact-implicit MPC and differentiable contact models (Contact Trust Region, Complementarity-Free, ComFree-Sim) offer an alternative to learned impedance for contact-rich dexterous manipulation. Recent work achieves real-time MPC at 50-100 Hz for Allegro and LEAP hands. These approaches provide formal guarantees (e.g., complementarity constraints, passivity) that learned policies typically lack, but require accurate dynamics models and struggle with soft/deformable contacts. How model-based and learning-based force control can be combined for dexterous hands — e.g., learned impedance setpoints tracked by a model-based inner loop — remains largely unexplored.

---

## 20. Reference Links

### Key GitHub Organizations / Project Pages
- [Google DeepMind](https://deepmind.google/models/gemini-robotics/) — Gemini Robotics, Gemini Robotics-ER, RT-2
- [PKU-EPIC](https://github.com/PKU-EPIC) — DexGraspNet, UniDexGrasp, BODex, Dexonomy
- [PKU-RL](https://github.com/PKU-RL) — CrossDex, ResDex
- [NVlabs](https://github.com/NVlabs) — DextrAH, DexMimicGen, IndustReal, CHIP
- [UniDex-AI](https://github.com/unidex-ai) — UniDex-VLA
- [Physical-Intelligence](https://github.com/Physical-Intelligence) — openpi (pi0, pi0-FAST, pi0.5); pi0.6, pi0.7 not publicly released
- [NVIDIA Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) — GR00T N1~N1.7
- [ForceMimic](https://github.com/ForceMimic) — ForceMimic, ForceCapture
- [Meta FAIR](https://github.com/facebookresearch) — SPIDER, TCDM, Sparsh, NeuralFeels
