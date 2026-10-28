# Contact-Rich Dexterous Manipulation: 종합 서베이

> 최종 업데이트: 2026-05-14
> 범위: dexterous manipulation, Force-aware VLA, impedance 학습, RL 정책 및 관련 benchmark에 관한 Paper, 리포지토리, 데이터셋 (2018-2026).
> GitHub 링크 및 Weights 가용 여부는 서베이 작성일 기준으로 확인되었으며, 이후 변경될 수 있음.
>
> **표기법:** ✅ = 사용 가능/지원됨, ✗ = 사용 불가/미지원, — = 보고되지 않음 또는 해당 없음.

**목적.** 본 서베이는 세 가지 연구 흐름의 교차점을 중심으로 구성됨: (1) dexterous 다중 손가락 manipulation, (2) Vision-Language-Action(VLA) 모델, (3) 힘/impedance 인식 제어. 기존 시스템이 어떤 능력을 제공하는지, 그리고 어떤 조합이 아직 탐구되지 않았는지를 매핑하여 이러한 교차점에서의 미개척 연구 방향을 식별하는 것을 목표로 함. 범위는 이 세 영역에 의도적으로 집중되어 있으며, 보행, 이동 manipulation, 산업 자동화 등 인접 주제는 서베이의 핵심 주제와 교차하는 경우에만 다룸.

---

## 1. Dexterous 도구 사용 및 Manipulation

Parallel-jaw gripper를 넘어 grasping, 도구 사용, 또는 Objects manipulation을 수행하는 다중 손가락 핸드 시스템.

| Paper | Group | Venue | Year | Hand (DoF) | Tasks | Sim Platform | Sim2Real | Code | Weights | VLA/Lang |
|---|---|---|---|---|---|---|---|---|---|---|
| [**SimToolReal**](https://arxiv.org/abs/2602.16863) | Stanford IPRL | arXiv | 2026 | Sharpa (22) + KUKA | 24가지 도구 사용 Tasks (해머, 드라이버, 주걱) | IsaacGym | Yes | [GitHub](https://github.com/tylerlum/simtoolreal) ✅ | ✅ ckpt | ✗ |
| [**Grasp-to-Act**](https://arxiv.org/abs/2602.20466) | UIUC RoboTouch | arXiv | 2026 | LEAP (16) | 5가지 동적 도구 사용 (해머, 톱, 자르기, 젓기, 뜨기) | Sim + real | Yes | ✗ | ✗ | ✗ |
| [**DexMachina**](https://arxiv.org/abs/2505.24853) | Stanford/NVIDIA | arXiv | 2025 | Inspire, Allegro, Xhand, Schunk | bimanual 관절 Objects manipulation | Genesis | ✗ | [GitHub](https://github.com/MandiZhao/dexmachina) ✅ | ✗ (eval TODO) | ✗ |
| [**ManipTrans**](https://arxiv.org/abs/2503.21860) | BIGAI/Tsinghua/PKU | CVPR | 2025 | 4종 핸드 (Shadow, MANO, Inspire, Allegro) | bimanual Tasks (펜 캡, 병뚜껑 열기) | IsaacGym P4 | ✗ | [GitHub](https://github.com/ManipTrans/ManipTrans) ✅ | ✅ imitator ckpt + HF | ✗ |
| [**SPIDER**](https://arxiv.org/abs/2511.09484) | Meta FAIR / Berkeley | arXiv | 2025 | 9종 humanoid | retargeted human demos | MuJoCo | ✅ (Franka+Allegro) | [GitHub](https://github.com/facebookresearch/spider) ✅ | ✗ | ✗ |
| **Scaffolding+VLM** | Stanford / KIT | NeurIPS | 2025 | Allegro (16) + KUKA | 관절 Objects (사과, 병, 서랍) | Sim + real | Yes | [GitHub](https://github.com/vdebakker/vlm-scaffolding) ✅ | ✗ | ✅ Gemini VLM |
| [**DexUMI**](https://arxiv.org/abs/2505.21864) | Stanford | CoRL Best Paper Finalist | 2025 | XHand, Inspire | 실세계 dexterous manipulation | Real only | N/A | [GitHub](https://github.com/real-stanford/DexUMI) ✅ | ✗ | ✗ |
| [**DexterityGen**](https://arxiv.org/abs/2502.04307) | Berkeley/Meta | RSS | 2025 | Allegro (16) + arm | 도구 사용 (펜, 드라이버, 주사기) | IsaacGym | ✅ | ✗ | ✗ | ✗ |
| [**ArtiGrasp**](https://arxiv.org/abs/2309.03891) | ETH Zurich | 3DV | 2024 | MANO (인간 프록시) | bimanual grasping + articulated manipulation (8개 Objects) | RaiSim | ✗ | [GitHub](https://github.com/zdchan/artigrasp) ✅ | ✅ pretrained | ✗ |
| [**DexDeform**](https://arxiv.org/abs/2304.03223) | MIT-IBM | ICLR | 2023 | Multi-finger (sim) | 6가지 deformable Objects Tasks (점토) | PlasticineLab | ✗ | [GitHub](https://github.com/sizhe-li/DexDeform) ✅ | ✗ | ✗ |

---

## 2. Dexterous VLA / Vision-Language-Action

dexterous 핸드 지원 또는 언어 조건부 dexterous manipulation을 갖춘 VLA 모델.

| Paper | Group | Venue | Year | Hand (DoF) | Tasks | Code | Weights | Key Method |
|---|---|---|---|---|---|---|---|---|
| [**UniDex-VLA**](https://arxiv.org/abs/2603.22264) | UniDex-AI | CVPR | 2026 | FAAS를 통한 8종 핸드 (Allegro, LEAP, Shadow, Inspire, Wuji, Oymotion, Ability, Xhand) | 도구 사용, 81% Tasks 진행률 | [GitHub](https://github.com/unidex-ai/UniDex) ✅ | ✅ 3-epoch + 32-epoch on HF | 3D VLA + flow matching, FAAS 통합 행동 |
| [**DexGraspVLA**](https://arxiv.org/abs/2502.08142) | Psi-Robot | AAAI | 2026 | Custom dexterous | 복잡 환경 grasp, 90%+ 성공률 | [GitHub](https://github.com/Psi-Robot/DexGraspVLA) ✅ | ✅ controller ckpt (GDrive) | Qwen2.5-VL-72B 플래너 + diffusion 컨트롤러 |
| [**DexVLA**](https://arxiv.org/abs/2502.05855) | Multi-inst. | CoRL | 2025 | Yes (커리큘럼) | dexterous 스킬 학습 | [GitHub](https://github.com/juruobenruo/DexVLA) ✅ | ✅ ScaleDP-H/L on HF | fixed VLM 위 1B diffusion expert 플러그인 |
| **Dexora** | Multi-inst. | ICRA | 2025 | bimanual 36-DoF | 픽앤플레이스, dexterous manipulation, 조립, 도구 사용 | [GitHub](https://github.com/ZZongzheng0918/Dexora) ✅ | ✅ real data on HF | 12.2K 실제 + 100K sim 에피소드 |
| [**Grasp as You Say**](https://arxiv.org/abs/2405.19291) | Sun Yat-sen | NeurIPS | 2024 | Shadow (24) | 언어 안내 grasp ("손잡이로 머그잔 잡기") | [GitHub](https://github.com/iSEE-Laboratory/Grasp-as-You-Say) ✅ | ✗ | 언어 조건부 dexterous grasp 생성 |
| [**HumanoidGen**](https://arxiv.org/abs/2507.00833) | TeleHuman | NeurIPS | 2025 | Unitree H1_2 + Inspire (6 DoF/hand) | 20가지 테이블탑 Tasks (bimanual, 장기 Tasks) | [GitHub](https://github.com/TeleHuman/HumanoidGen) ✅ | ✅ HF (model + data) | LLM 플래너 + MCTS + diffusion policy |
| [**VLA+Diffusion Switch**](https://arxiv.org/abs/2410.14022) | — | arXiv | 2024 | ADAPT Hand (13) | VLA 전환을 통한 픽앤플레이스 | ✗ | ✗ | 직렬 탄성 다중 손가락 핸드에서 VLA + diffusion policy 전환 |

---

## 3. Force-aware VLA / Tactile VLA

Contact-rich Tasks을 위해 force/torque 또는 tactile 센싱을 통합하는 모델. VLM/VLA backbone 또는 언어 조건부를 사용하는 시스템이 여기에 포함됨; 그렇지 않으면 VLM backbone 없는 힘/impedance 중심 시스템은 §5에 수록.

| Paper | Group | Venue | Year | Force Input | Force/Impedance 출력? | Robot | Code | Weights | Tasks |
|---|---|---|---|---|---|---|---|---|---|
| [**ForceVLA**](https://arxiv.org/abs/2505.22159) | SJTU/Fudan | NeurIPS | 2025 | 6축 F/T | ✗ (position only) | Flexiv Rizon + gripper | [GitHub](https://github.com/ft-robotic/ForceVLA) ✅ | ✗ (data on HF) | 플러그 삽입, 닦기, 껍질 벗기기 (5가지 Tasks) |
| [**ForceVLA2**](https://arxiv.org/abs/2603.15169) | Shanghai AI Lab | CVPR | 2026 | 6축 F/T 300Hz | ✅ hybrid F/P + predicted force | Flexiv Rizon 4s + gripper | ✗ "coming soon" | ✗ | 누르기, 청소, 기어 조립 (5가지 Tasks) |
| [**FD-VLA**](https://arxiv.org/abs/2602.02142) | NUS | ICRA | 2026 | 증류(inference 시 센서 없음) | ✗ | UR5e + gripper | ✗ | ✗ | 닦기, 삽입, 버튼 누르기 (3가지 Tasks) |
| [**FAVLA**](https://arxiv.org/abs/2602.23648) | USTC | arXiv | 2026 | 6축 F/T 고주파 | ✗ | Monte dual-arm X-ARM | ✗ | ✗ | USB 삽입, 기어, 닦기 (4가지 Tasks) |
| [**HapticVLA**](https://arxiv.org/abs/2603.15257) | Skoltech | arXiv | 2026 | tactile (증류 후 제거) | ✗ | LeRobot SO-101 + tactile | Paper에서 공개 예정 주장; 2026년 5월 기준 공개 리포 not verified | not verified | 병/와플/달걀 픽앤플레이스 |
| [**DreamTacVLA**](https://arxiv.org/abs/2512.23864) | Northwestern | arXiv | 2025 | tactile (V-JEPA2) | ✗ | Dobot Xtrainer + gripper + tactile | [GitHub](https://github.com/michaelyeah7/learning-to-feel-the-future) (Code만) | ✗ | tactile world model이 미래 잠재 표현 예측 → 행동 정제; 4가지 contact-rich Tasks에서 최대 95% |
| [**OmniVTLA**](https://arxiv.org/abs/2508.08706) | - | arXiv | 2025 | 비전 기반 + 힘 기반 tactile | ✗ | gripper + Dex Hand | ✗ (dataset only) | ✗ | 픽앤플레이스 (dexterous 핸드 100%) |
| [**Tactile-VLA**](https://arxiv.org/abs/2507.09160) | Tsinghua | arXiv | 2025 | tactile | ✅ hybrid position-force | not specified | ✗ | ✗ | 충전기 삽입 90% |
| [**TaF-VLA**](https://arxiv.org/abs/2601.20321) | - | arXiv | 2026 | GelSight + 6축 F/T | ✗ | Franka FR3 + gripper | ✗ | ✗ | 8가지 contact-rich Tasks |
| [**TA-VLA**](https://arxiv.org/abs/2509.07962) | Tsinghua AIR | CoRL | 2025 | joint torque | auxiliary torque prediction | Cobot Magic ALOHA | ✗ | ✗ | 10가지 Tasks (버튼, 충전기, USB...) |
| [**CRAFT**](https://arxiv.org/abs/2602.12532) | - | arXiv | 2026 | 힘 | ✗ | teleoperation 팔 | ✗ | ✗ | deformable, 정렬 Tasks |
| [**VLA-Touch**](https://arxiv.org/abs/2507.17294) | NUS | arXiv | 2025 | GelSight tactile | ✗ (residual correction) | 팔 + gripper | [GitHub](https://github.com/jxbi1010/VLA-Touch) ✅ | ✅ ckpts + HF | contact-rich 조작 |
| [**FoAR**](https://arxiv.org/abs/2411.15753) | SJTU | RA-L/IROS 2025 | 2024 | 6축 F/T | ✗ | Flexiv Rizon + gripper | [GitHub](https://github.com/Alan-Heoooh/FoAR) ✅ | ✗ | 닦기, 껍질 벗기기 |
| [**FACTR**](https://arxiv.org/abs/2502.17432) | CMU | RSS | 2025 | joint torque (servo current) | ✗ | Franka + gripper | [GitHub](https://github.com/RaindragonD/factr) ✅ | ✗ (encoder only) | 상자 들기, 피벗, 반죽 밀기 |
| [**ForceMimic**](https://arxiv.org/abs/2410.07554) | SJTU | ICRA | 2024 | captured interaction wrench | ✅ wrench-position hybrid | Flexiv + gripper | [GitHub](https://github.com/ForceMimic/hybridil) ✅ | ✗ | 야채 껍질 벗기기 |
| [**Reactive Diffusion Policy**](https://arxiv.org/abs/2503.02881) | - | RSS | 2025 | GelSight Mini | ✗ (학습된 "impedance 유사") | Flexiv Rizon 4 + gripper | [GitHub](https://github.com/xiaoxiaoxh/reactive_diffusion_policy) ✅ | ✅ ckpts + HF | 3가지 contact-rich Tasks |
| [**ACP**](https://arxiv.org/abs/2410.09309) | Toyota/Columbia | ICRA | 2024 | 6축 F/T (ATI) | ✅ scalar stiffness | UR5e + 수동 도구 | ✗ | ✗ | 물건 뒤집기, 꽃병 닦기 |
| [**TacDiffusion**](https://arxiv.org/abs/2409.11047) | TU Munich MIRMI | ICRA | 2024 | tactile | ✅ 6D wrench | gripper + tactile | [GitHub](https://github.com/popnut123/TacDiffusion) ✅ | ✗ | force-domain diffusion, 95.7% zero-shot |
| [**FARM**](https://arxiv.org/abs/2510.13324) | TU Munich MIRMI | arXiv | 2025 | GelSight Mini | ✅ grip force | 개조된 UMI gripper | ✗ | ✗ | joint position + force prediction |
| [**T-Dex**](https://arxiv.org/abs/2303.12076) | NYU (Pinto) | ICRA | 2024 | tactile (DIGIT) | ✗ (position only) | **Allegro (16) + DIGIT** + Kinova arm | [GitHub](https://github.com/irmakguzey/tdex) ✅ | ✗ | 5가지 dexterous Tasks (조이스틱, 책, 그릇, 페그, 점토); vs vision-only 1.7배. §3 항목 중 dexterous 핸드를 사용한 극소수 사례 중 하나. |

---

## 4. VLM-guided Impedance Control

VLM/LLM이 하위 수준 컨트롤러를 위한 impedance 매개변수 (K, D)를 생성하거나 검색하는 시스템.

| Paper | Group | Venue | Year | K/D 적응 방법 | Stiffness (K) | Damping (D) | Robot | Dex Hand? | Code | Weights |
|---|---|---|---|---|---|---|---|---|---|---|
| [**CompliantVLA-adaptor**](https://arxiv.org/abs/2601.15541) | IIT Genoa / TU Darmstadt | arXiv | 2026 | VLM (GPT-4o-mini) zero-shot | ✅ (Kx,Ky,Kz) | ✅ (Dx,Dy,Dz) | Franka Panda + gripper | ✗ | project page (pending) | ✗ (training-free) |
| [**OmniVIC**](https://arxiv.org/abs/2510.17150) | IIT Genoa / Georgia Tech | arXiv | 2025 | VLM + RAG 자기 개선 | ✅ | ✅ | Franka Panda + F/T 센서 | ✗ | ✗ | ✗ (GPT-4o-mini API 사용) |
| [**HumanoidVLM**](https://arxiv.org/abs/2601.14874) | - | HRI | 2026 | VLM (Molmo-7B) + FAISS RAG | ✅ (검색) | ✅ (검색) | Unitree G1 humanoid | ✗ | ✗ | ✗ |
| **SafeHumanoid** | 동일 그룹 | HRI | 2026 | VLM + RAG 검색 | ✅ | ✅ | Unitree G1 | ✗ | ✗ | ✗ |
| [**ImpedanceGPT**](https://arxiv.org/abs/2503.02723) | - | IROS | 2025 | VLM (Molmo) + RAG | ✅ | ✅ | 드론 군집 (조작 아님) | N/A | [GitHub](https://github.com/Faryal-Batool/ImpedanceGPT) ✅ | ✗ |

---

## 5. Learned Impedance / Variable Compliance Control

VLM backbone 없이 impedance/stiffness/damping 매개변수를 학습하거나 최적화하는 시스템. VLM 기반 impedance 접근법은 §4 참조. 힘을 Input으로 사용하지만 position only 출력하는 Paper(예: FoAR, FACTR)은 §3에 수록.

| Paper | Group | Venue | Year | Stiffness (K) | Damping (D) | Learning Method | Robot | Dex Hand? | Sim | Code | Weights |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [**Comp-ACT**](https://arxiv.org/abs/2406.14990) | OMRON SINIC X / UTokyo | IROS | 2024 | ✅ (12D Cholesky) | ✗ | IL (VR 시연 기반 ACT) | 2x UR5e + gripper | ✗ | Robosuite (MuJoCo) | [GitHub](https://github.com/omron-sinicx/CompACT) ✅ | ✗ |
| [**Diff-Impedance**](https://arxiv.org/abs/2509.19696) | KIT / MIT | arXiv | 2025 | ✅ | ✅ | Diffusion + energy-based | KUKA LBR iiwa | ✗ | Sim + real | [GitHub](https://github.com/StrokeAIRobotics/DiffusionBasedImpedanceLearning) ✅ | ✗ |
| [**VICES**](https://arxiv.org/abs/1906.08880) | Stanford / NVIDIA | IROS | 2019 | ✅ | ✅ | RL (policy gradient) | Franka/Sawyer + gripper | ✗ | Robosuite (MuJoCo) | [robosuite/vices](https://github.com/ARISE-Initiative/robosuite/tree/vices_iros19) ✅ | ✗ |
| [**CHIP**](https://arxiv.org/abs/2512.14689) | NVIDIA NVLabs | ICRA | 2025 | ✅ (EE stiffness) | ✗ | RL (hindsight perturbation) | humanoid 35-DoF | ✗ | Isaac Sim | [Page](https://nvlabs.github.io/CHIP/) | ✗ |
| [**FILIC**](https://arxiv.org/abs/2509.17053) | Tsinghua/HKUST | arXiv | 2025 | fixed K | fixed B | IL (transformer, 25Hz) | AIRBOT Play | ✗ | MuJoCo + real | [GitHub](https://github.com/OpenGHz/FILIC) ✅ | ✗ |
| [**CHEQ**](https://arxiv.org/abs/2501.07985) | RWTH Aachen | arXiv | 2025 | ✅ | ✅ | RL (hybrid 적응) | 팔 (연마) | ✗ | real hardware | ✗ | ✗ |
| [**DA-VIL**](https://arxiv.org/abs/2410.19712) | IIIT/Brown | ICRA | 2024 | ✅ | not reported | RL + QP 최적화 | 양팔 | ✗ | Sim | project page only | ✗ |
| [**DexForce**](https://arxiv.org/abs/2501.10356) | Stanford | RA-L | 2025 | fixed k_f | ✗ | hand-tuned | Allegro (16) | **✅** | ✗ (real only) | ✗ | ✗ |
| [**Force Policy**](https://arxiv.org/abs/2602.22088) | SJTU/Flexiv | RSS | 2026 | force targets | ✗ | IL (teleoperation 시연) | Flexiv + gripper | ✗ | ✗ (real only) | ✗ | ✗ |
| [**IndustReal**](https://arxiv.org/abs/2305.17110) | NVIDIA | RSS | 2023 | fixed | fixed | RL (PPO) 포즈 학습 | Franka + gripper | ✗ | IsaacGym | [GitHub](https://github.com/NVlabs/industreallib) ✅ | ✅ RL policies |
| [**Divide et Impera**](https://arxiv.org/abs/2410.01054) | MIT/KIT | arXiv | 2024 | ✅ (군집) | ✅ | NN success predictor | 실제 팔 | ✗ | Real | ✗ | ✗ |
| [**DCM**](https://arxiv.org/abs/2403.13221) | Omron SINIC X | IROS | 2024 | VIC Input | ✗ | Diffusion contact model | 팔 + gripper | ✗ | ✗ | ✗ | ✗ |

---

## 6. VLA Foundation Models: Version History

### 6.1 Physical Intelligence pi 시리즈

| Version | Date | Params | VLM Backbone | Action Head | Dex Hand | Force/Impedance | 오픈 Weights |
|---|---|---|---|---|---|---|---|
| **pi0** | 2024년 10월 | 3.3B | PaliGemma 3B | Flow matching (300M) | ✗ (gripper) | ✗ | ✅ Apache 2.0 ([openpi](https://github.com/Physical-Intelligence/openpi), [HF](https://huggingface.co/lerobot/pi0_base)) |
| **pi0-FAST** | 2025년 1월 | 3.3B | PaliGemma 3B | autoregressive (FAST tokenizer) | ✗ | ✗ | ✅ Apache 2.0 (openpi) |
| **pi0.5** | 2025년 4월 | 3.3B | PaliGemma 3B | 2단계: FAST pretraining → flow matching | ✗ | ✗ | ✅ Apache 2.0 ([HF](https://huggingface.co/lerobot/pi05_base)) |
| **pi0.6 / pi\*0.6** | 2025년 11월 | ~5B | Gemma3 4B | Flow + token dual | ✗ | ✗ | not officially released; third-party reimplementations exist |
| **pi0.7** | 2026년 4월 | ~5B | Gemma3 4B + 400M 비전 | Flow matching (860M DiT) | ✗ | ✗ | 2026년 5월 기준 not released |

모든 pi Version은 parallel-jaw gripper만 사용. action space은 18-19D (양팔 6-DoF + gripper + 베이스). 어떤 Version에서도 힘 또는 impedance 출력 없음.

### 6.2 NVIDIA GR00T 시리즈

| Version | Date | Params | VLM Backbone | DiT 레이어 | Dex Hand | Force/Impedance | 오픈 Weights |
|---|---|---|---|---|---|---|---|
| **GR00T N1** | 2025년 3월 | 2.2B | Eagle-2 | 16 | Fourier 핸드 (humanoid 통합) | ✗ | ✅ non-commercial ([HF](https://huggingface.co/nvidia/GR00T-N1-2B)) |
| **GR00T N1.5** | 2025년 중반 | 3B | Eagle 2.5 (fixed) | 16 | not documented | ✗ | ✅ non-commercial ([HF](https://huggingface.co/nvidia/GR00T-N1.5-3B)) |
| **GR00T N1.6** | 2025년 후반 | 3B | Cosmos-2B | 32 | not documented | ✗ | ✅ ([HF](https://huggingface.co/nvidia/GR00T-N1.6-3B)) |
| **GR00T N1.7** | 2026년 5월 | 3B | Cosmos-Reason2-2B (Qwen3-VL) | 32 | 22-DoF (EgoScale/Sharpa 표현) | ✗ | ✅ commercial OK ([HF](https://huggingface.co/nvidia/GR00T-N1.7-3B)) |

**GR00T-Dexterity**는 별도의 RL 워크플로우(VLA 모델이 아님)로 DextrAH-G 기반. Isaac Lab에서 geometric fabrics를 사용하여 Allegro Hand (16 DoF) + Kuka를 지원함. GR00T N1.x VLA 모델은 다중 손가락 핸드 행동을 직접 출력하지 않음.

모든 GR00T VLA Version은 위치 목표만 출력. N1.7의 "22 DoF 핸드"는 인간 손 동작을 22-DoF Sharpa 핸드 관절 각도로 표현하는 EgoScale pretraining framework에서 유래. Unitree G1의 물리적 핸드(Dex3-1)는 핸드당 7 DoF만 보유. 22-DoF 능력은 인간 비디오 pretraining 시 사용된 행동 표현을 의미하며 deploy된 핸드가 아님.

### 6.3 기타 주요 VLA

| Paper | Group | Venue | Year | Dex Hand? | Force 출력? | 오픈 Code | 오픈 Weights | Key Feature |
|---|---|---|---|---|---|---|---|---|
| [**Gemini Robotics**](https://arxiv.org/abs/2503.20020) | Google DeepMind | arXiv | 2025 | ✗ (gripper) | ✗ | ✗ | ✗ (비공개, 신뢰 테스터) | Gemini 2.0 기반 VLA; 일반화 benchmark에서 SOTA 2배; ALOHA/Franka/Apollo |
| **Gemini Robotics 1.5** | Google DeepMind | Blog | 2026 | ✗ | ✗ | ✗ | ✗ (신뢰 테스터) | VLA + inference; cross-embodiment; Gemini API (ER 1.5) |
| **Gemini Robotics On-Device** | Google DeepMind | Blog | 2025 | ✗ | ✗ | SDK (제한적) | ✗ | 온디바이스 VLA; 50-100 시연으로 fine-tuning; 네트워크 의존성 없음 |
| [**RT-2**](https://arxiv.org/abs/2307.15818) | Google DeepMind | CoRL | 2023 | ✗ | ✗ | ✗ | ✗ (비공개) | 55B VLM을 Robot 행동에 공동 fine-tuning |
| [**OpenVLA**](https://arxiv.org/abs/2406.09246) | Berkeley/Stanford | CoRL | 2024 | ✗ | ✗ | [GitHub](https://github.com/openvla/openvla) ✅ | ✅ HF | 7B VLA baseline, Apache 2.0 |
| [**OpenVLA-OFT**](https://arxiv.org/abs/2502.19645) | Stanford/Berkeley | RSS | 2025 | ✗ (ALOHA) | ✗ | [GitHub](https://github.com/moojink/openvla-oft) ✅ | ✅ | 26배 빠른 inference, parallel decoding |
| [**Octo**](https://arxiv.org/abs/2405.12213) | Berkeley RAIL | RSS | 2024 | ✗ | ✗ | [GitHub](https://github.com/octo-models/octo) ✅ | ✅ HF | 93M, modular fine-tuning |
| [**RDT-1B**](https://arxiv.org/abs/2410.07864) | Tsinghua thu-ml | ICLR | 2025 | ✗ (bimanual) | ✗ | [GitHub](https://github.com/thu-ml/RoboticsDiffusionTransformer) ✅ | ✅ HF 1B | largest open diffusion model |
| [**HPT**](https://arxiv.org/abs/2409.20537) | MIT (Kaiming He) | NeurIPS | 2024 | ✗ | ✗ | [GitHub](https://github.com/liruiw/HPT) ✅ | ✗ | heterogeneous embodiment pretraining |
| [**CogACT**](https://arxiv.org/abs/2411.19650) | Microsoft | arXiv | 2024 | ✗ | ✗ | [GitHub](https://github.com/microsoft/CogACT) ✅ | ✗ | cognition-action separation |
| [**EgoScale**](https://arxiv.org/abs/2602.16710) | NVIDIA/Berkeley | arXiv | 2026 | ✅ 22-DoF | ✗ | ✗ | ✗ | 20K시간 인간 비디오, dexterous 스케일링 법칙 |
| [**SimpleVLA-RL**](https://arxiv.org/abs/2509.09674) | — | ICLR | 2025 | ✗ | ✗ | [GitHub](https://github.com/PRIME-RL/SimpleVLA-RL) ✅ | ✗ | VLA의 RL fine-tuning |
| [**SpatialVLA**](https://arxiv.org/abs/2501.15830) | Shanghai AI Lab / Multi-inst. | RSS | 2025 | ✗ | ✗ | ✅ (프로젝트 페이지) | ✅ | PaliGemma2 기반 3.5B VLA, Ego3D 위치 인코딩 + adaptive action grids |
| [**TinyVLA**](https://arxiv.org/abs/2409.12514) | ECNU / Midea | AAAI | 2025 | ✗ | ✗ | ✗ (project page only) | ✗ | 1.3B VLA + diffusion decoder; 7B OpenVLA와 동등 성능, 20배 빠름 |
| [**LLARVA**](https://arxiv.org/abs/2406.11815) | UC Berkeley | arXiv | 2024 | ✗ | ✗ | ✗ (project page only) | ✗ | 2D 시각 궤적 보조 Tasks을 통한 비전-행동 인스트럭션 튜닝 |
| [**UniAct**](https://arxiv.org/abs/2501.10105) | Multi-inst. | CVPR | 2025 | designed for diverse embodiments | ✗ | [GitHub](https://github.com/2toinf/UniAct) ✅ | ✗ | 범용 행동 Code북 |

### 6.4 Visuomotor Policies (without language conditioning)

VLM backbone을 사용하지 않지만 dexterous manipulation의 baseline 또는 구성 요소로 널리 채택되는 영향력 있는 Visuomotor Policies.

| Paper | Group | Venue | Year | Dex Hand? | Force 출력? | 오픈 Code | 오픈 Weights | Key Feature |
|---|---|---|---|---|---|---|---|---|
| [**Diffusion Policy**](https://arxiv.org/abs/2303.04137) | Columbia (Shuran Song) | RSS | 2023 | ✗ | ✗ | [GitHub](https://github.com/real-stanford/diffusion_policy) ✅ | ✗ | 기초적 diffusion policy 방법 |
| [**ACT / ALOHA**](https://arxiv.org/abs/2304.13705) | Stanford (Tony Zhao) | RSS | 2023 | ✗ (gripper) | ✗ | [GitHub](https://github.com/tonyzhaozh/act) ✅ | ✗ | action chunking transformer, bimanual teleoperation |
| [**DP3**](https://arxiv.org/abs/2403.03954) | Tsinghua (Yanjie Ze) | RSS | 2024 | ✅ (sim) | ✗ | [GitHub](https://github.com/YanjieZe/3D-Diffusion-Policy) ✅ | ✗ | 3D point cloud diffusion, 72가지 Tasks |
| [**iDP3**](https://arxiv.org/abs/2410.10803) | Stanford/Tsinghua | IROS | 2025 | ✅ Inspire (25 DoF) | ✗ | [GitHub](https://github.com/YanjieZe/Improved-3D-Diffusion-Policy) ✅ | ✗ | Fourier GR1 humanoid에서 egocentric 3D |
| [**DexWM**](https://arxiv.org/abs/2512.13644) | Meta FAIR / NYU | arXiv | 2025 | ✅ Allegro + Franka | ✗ | ✗ | ✗ | dexterous 핸드-Objects 상호작용을 위한 world model |

---

## 7. RL-based Dexterous Manipulation

### 7.1 Dexterous Grasping

| Paper | Group | Venue | Year | RL Algo | Hand (DoF) | Sim | Sim2Real | Objects | Code | Weights |
|---|---|---|---|---|---|---|---|---|---|---|
| [**CrossDex**](https://arxiv.org/abs/2410.02479) | PKU-RL | ICLR | 2025 | PPO + DAgger | 6종 핸드 (Shadow, Allegro, LEAP, ...) | IsaacGym P4 | ✅ | 100 (YCB+GRAB) | [GitHub](https://github.com/PKU-RL/CrossDex) ✅ | partial |
| [**ResDex**](https://arxiv.org/abs/2410.01481) | PKU-RL | ICLR | 2025 | PPO + MoE + DAgger | Shadow (24) | IsaacGym P4 | ✗ | 3200, 88.8% | [GitHub](https://github.com/PKU-RL/ResDex) ✅ | partial |
| [**UniDexGrasp++**](https://arxiv.org/abs/2304.00464) | PKU-EPIC | ICCV | 2023 | PPO + DAgger | Shadow (24) | IsaacGym | ✗ | 3000+, 85.4% | [GitHub](https://github.com/PKU-EPIC/UniDexGrasp2) ✅ | ✅ state ckpt |
| [**UniDexGrasp**](https://arxiv.org/abs/2303.00938) | PKU-EPIC | CVPR | 2023 | PPO (goal-conditioned) | Shadow (24) | IsaacGym | ✗ | 3000+, ~60% | [GitHub](https://github.com/PKU-EPIC/UniDexGrasp) ✅ | ✗ |
| [**BODex**](https://arxiv.org/abs/2412.16490) | PKU-EPIC | ICRA | 2025 | bilevel optimization | Shadow, Allegro, LEAP | cuRobo | ✅ 81% | 5355 | [GitHub](https://github.com/JYChen18/BODex) ✅ | HF 데이터셋 |
| [**DexGrasp Anything**](https://arxiv.org/abs/2409.11159) | ShanghaiTech | CVPR Highlight | 2025 | Diffusion | Shadow | IsaacGym | ✗ | 15K+, 340만 grasp | [GitHub](https://github.com/4DVLab/DexGrasp-Anything) ✅ | ✅ HF+GDrive |
| [**DexGraspNet 2.0**](https://arxiv.org/abs/2410.15590) | PKU-EPIC | CoRL | 2024 | Diffusion | Shadow | IsaacGym | ✅ 90.7% | 1319, 4.26억 grasp | [GitHub](https://github.com/PKU-EPIC/DexGraspNet2) ✅ | ✅ HF |
| [**RobustDexGrasp**](https://arxiv.org/abs/2501.01771) | ETH Zurich | CoRL | 2025 | PPO + teacher-student | Allegro (16) + UR5 | RaiSim | ✅ 94.6% | 시뮬 247K, 실제 512 | [GitHub](https://github.com/zdchan/RobustDexGrasp) ✅ | ✅ |
| [**Dexonomy**](https://arxiv.org/abs/2504.01301) | PKU-EPIC | RSS | 2025 | 최적화 | Shadow, Allegro, LEAP, Unitree G1 | MuJoCo + cuRobo | ✅ 82.3% | 10.7K, 31종 | [GitHub](https://github.com/JYChen18/Dexonomy) ✅ | HF |
| [**UltraDexGrasp**](https://arxiv.org/abs/2603.05312) | InternRobotics | ICRA | 2026 | multi-strategy | 다수 | BODex + cuRobo | ✅ 81.2% | 2000만 프레임 | [GitHub](https://github.com/InternRobotics/UltraDexGrasp) ✅ | ✗ |
| [**DexPoint**](https://arxiv.org/abs/2211.09423) | UCSD | CoRL | 2022 | PPO (point cloud) | Allegro (16) | IsaacGym | ✅ | category-level novel | [GitHub](https://github.com/yzqin/dexpoint-release) ✅ | ✗ |
| [**AnyGrasp**](https://arxiv.org/abs/2212.08333) | SJTU (Cewu Lu) | IEEE T-RO | 2023 | supervised (GSNet) | parallel-jaw gripper | GraspNet-1B | ✅ 93.3% | 300+ 미지 Objects, 시간당 900+ 픽 | [SDK](https://github.com/graspnet/anygrasp_sdk) (license) | ✗ | 상위 grasp 감지 (parallel-jaw). dexterous VLA pipeline의 인식 모듈로 널리 사용되어 포함. |
| [**DextrAH-G/RGB**](https://arxiv.org/abs/2407.02274) | NVIDIA | CoRL | 2024 | PPO + geometric fabrics | Allegro (16) + Kuka | Isaac Lab | ✅ | 다중 Objects | [GitHub](https://github.com/NVlabs/DEXTRAH) ✅ | ✗ |

### 7.2 In-Hand Manipulation / Reorientation

| Paper | Group | Venue | Year | Hand (DoF) | Sim | Sim2Real | Code | Weights |
|---|---|---|---|---|---|---|---|---|
| [**Dactyl**](https://arxiv.org/abs/1808.00177) | OpenAI | arXiv 2018 / IJRR 2020 | 2018 | Shadow (24) | MuJoCo | ✅ (ADR) | ✗ | ✗ |
| [**Hora**](https://arxiv.org/abs/2210.04887) | Berkeley/Meta | CoRL | 2022 | Allegro (16) | IsaacGym P4 | ✅ | [GitHub](https://github.com/HaozhiQi/hora) ✅ | ✅ |
| [**Rotating w/o Seeing**](https://arxiv.org/abs/2303.10880) | UCSD | RSS | 2023 | Allegro (16) + 이진 tactile | IsaacGym | ✅ | [Page](https://touchdexterity.github.io) | ✗ |
| [**General In-Hand Rotation**](https://arxiv.org/abs/2309.09979) | Berkeley/Meta | CoRL | 2023 | Allegro (16) + DIGIT | IsaacGym | ✅ | (hora 리포에 포함) | ✗ |
| [**RotateIt**](https://arxiv.org/abs/2309.02388) | Berkeley/Meta/CMU | CoRL | 2023 | Allegro (16) + DIGIT | IsaacGym | ✅ | (hora 리포에 포함) | ✗ |
| [**AnyRotate**](https://arxiv.org/abs/2405.07391) | U. Bristol | CoRL | 2024 | Allegro (16) + tactile | IsaacGym | ✅ | ✗ | ✗ |
| [**Visual Dexterity**](https://arxiv.org/abs/2211.11744) | MIT CSAIL | Science Robotics | 2023 | D'Claw (9/12) | IsaacGym P3 | ✅ | [GitHub](https://github.com/Improbable-AI/dexenv) ✅ | ✅ |
| [**DeXtreme**](https://arxiv.org/abs/2210.13702) | NVIDIA | ICRA | 2023 | Allegro (16) | IsaacGym | ✅ | IsaacGymEnvs 내 ✅ | ✗ |
| [**DexPBT**](https://arxiv.org/abs/2305.12127) | NVIDIA | RSS | 2023 | Allegro (16) + Kuka | IsaacGym | ✗ | IsaacGymEnvs 내 ✅ | ✗ |
| [**SAPG**](https://arxiv.org/abs/2407.04890) | CMU | ICML Oral | 2024 | Allegro/Shadow (16-46) | IsaacGym P4 | ✗ | [GitHub](https://github.com/jayeshs999/sapg) ✅ | ✗ |
| [**DexHandDiff**](https://arxiv.org/abs/2411.18562) | HKU/Berkeley | CVPR | 2025 | Shadow | Adroit (MuJoCo) | ✗ | [GitHub](https://github.com/Liang-ZX/DexHandDiff) ✅ | ✅ HF |

### 7.3 장기 / 다단계 / Contact-Rich

| Paper | Group | Venue | Year | Hand (DoF) | Tasks | Sim | Sim2Real | Code | Weights |
|---|---|---|---|---|---|---|---|---|---|
| [**SeqDex**](https://arxiv.org/abs/2309.00987) | Stanford | CoRL | 2023 | Allegro (16) | 연쇄 정책 (탐색→방향 설정→grasp→삽입) | IsaacGym | ✅ | [GitHub](https://github.com/sequential-dexterity/SeqDex) ✅ | ✅ |
| [**Bi-DexHands**](https://arxiv.org/abs/2206.08686) | PKU-MARL | NeurIPS | 2022 | 2x Shadow (48) | 16+ bimanual Tasks | IsaacGym | ✗ | [GitHub](https://github.com/PKU-MARL/DexterousHands) ✅ | ✅ |
| [**DexArt**](https://arxiv.org/abs/2305.05706) | UCSD | CVPR | 2023 | Allegro (16) | 4가지 관절 Objects Tasks | SAPIEN | ✗ | [GitHub](https://github.com/Kami-code/dexart-release) ✅ | ✅ |
| [**TCDM**](https://arxiv.org/abs/2209.11221) | Meta | ICRA | 2023 | 3종 핸드 플랫폼 | 50가지 Tasks, 34개 Objects | MuJoCo | ✗ | [GitHub](https://github.com/facebookresearch/TCDM) ✅ | ✅ |
| [**VTDexManip**](https://arxiv.org/abs/2501.01370) | - | ICLR | 2025 | Multi-finger (sim) | 6가지 Tasks (병뚜껑, 수도꼭지, reorientation) | IsaacGym | ✗ | [GitHub](https://github.com/LQTS/VTDexManip) ✅ | ✅ 18개 모델 |
| [**DexGarmentLab**](https://arxiv.org/abs/2503.18693) | Multi-inst. | NeurIPS Spotlight | 2025 | bimanual dexterous | 15가지 의류 Tasks, 2500+ 의류 | IsaacSim | ✗ | [GitHub](https://github.com/wayrise/DexGarmentLab) ✅ | ✗ |
| [**Contact Trust Region**](https://arxiv.org/abs/2505.02291) | MIT CSAIL (Tedrake) | IJRR | 2025 | Allegro (16) | contact-rich MPC | Drake | ✗ | ✗ | ✗ |
| [**Complementarity-Free**](https://arxiv.org/abs/2408.07855) | MIT CSAIL (Pang, Tedrake) | RSS | 2024 | Allegro (16) | 닫힌 형태 미분 가능 접촉, 50-100 Hz MPC | Drake | ✗ | ✗ | ✗ |
| [**ComFree-Sim**](https://arxiv.org/abs/2603.12185) | — | arXiv | 2026 | LEAP Hand | NVIDIA Warp 기반 GPU 병렬 접촉 MPC | Custom (Warp) | ✗ | ✗ | ✗ |

참고: IndustReal (NVIDIA, RSS 2023)도 RL을 통한 contact-rich 조립을 다룸; 자세한 내용은 §5 참조.

### 7.4 추가 최신 RL

| Paper | Group | Venue | Year | Hand (DoF) | Tasks | Sim2Real | Code |
|---|---|---|---|---|---|---|---|
| [**DQ-RISE**](https://arxiv.org/abs/2503.01766) | SJTU | ICRA | 2026 | OyMotion RoHand + Flexiv Rizon 4 | 6가지 실제 Tasks, 85.83% | ✅ | [GitHub](https://github.com/rise-policy/DQ-RISE) ✅ |
| [**DexTrack**](https://arxiv.org/abs/2501.15760) | PKU/Shanghai AI | ICLR | 2025 | Shadow (24), Allegro (16) | MoCap 추적 | ✗ | [GitHub](https://github.com/Meowuu7/DexTrack) partial |
| [**BiDexHD**](https://arxiv.org/abs/2501.09821) | PKU | arXiv | 2025 | 2x Shadow (48) | 141가지 bimanual Tasks (TACO) | ✗ | ✗ |
| [**DONIC**](https://arxiv.org/abs/2610.29997v1) | Ropedia | arXiv | 2026 | 2x Wuji Hand V1 (자유도 —) | 양손 참조 궤적 추적 (PPO + BC) | ✗ | — |
| [**HandelBot**](https://arxiv.org/abs/2603.12243) | Stanford | arXiv | 2026 | LEAP (16) bimanual | 실제 피아노 연주 | ✅ | [GitHub](https://github.com/amberxie88/handelbot) ✅ |
| [**DexDrummer**](https://arxiv.org/abs/2603.22263) | Stanford | arXiv | 2026 | bimanual dexterous | 드럼 연주 (contact-rich) | ✗ | [GitHub](https://github.com/hc-fang/dexdrummer) ✅ |
| [**RoboPianist**](https://arxiv.org/abs/2304.04150) | Google/Berkeley | CoRL | 2023 | 의인화 bimanual | 피아노 (150곡) | ✗ | [GitHub](https://github.com/google-research/robopianist) ✅ |
| [**DemoStart**](https://arxiv.org/abs/2409.06613) | Google DeepMind | ICRA | 2024 | DEX-EE (3-finger) | 플러그 삽입, 큐브 reorientation | ✅ | ✗ |
| **Closing Reality Gap** | - | arXiv | 2026 | 5-finger hand | 힘 제어 grasp | ✅ zero-shot | ✗ |
| [**Maniwhere**](https://arxiv.org/abs/2407.15815) | Shanghai AI Lab | CoRL | 2024 | Allegro (16) | 8가지 Tasks, 시각적 일반화 | ✅ | [GitHub](https://github.com/gemcollector/maniwhere) ✅ |
| [**Eureka**](https://arxiv.org/abs/2310.12931) | NVIDIA | ICLR | 2024 | Shadow (24, sim) | LLM 생성 보상, 펜 스피닝 | ✗ | [GitHub](https://github.com/eureka-research/Eureka) ✅ |
| [**DrEureka**](https://arxiv.org/abs/2406.01967) | NVIDIA | RSS | 2024 | Shadow (sim) + 4족 Robot | LLM 안내 DR, sim2real | ✅ | [GitHub](https://github.com/eureka-research/DrEureka) ✅ |
| [**DexMV**](https://arxiv.org/abs/2108.05877) | UCSD | ECCV | 2022 | Adroit (30, sim) | 인간 비디오로부터 IL (따르기, 놓기, 재배치) | ✗ | [GitHub](https://github.com/yzqin/dexmv-sim) ✅ |
| [**CyberDemo**](https://arxiv.org/abs/2402.14795) | UCSD | CVPR | 2024 | Allegro (16) | 증강 시뮬 시연, 밸브 회전 | ✅ | [GitHub](https://github.com/wang59695487/CyberDemo) ✅ |

---

## 8. 데이터셋

### 8.1 Robot Dexterous 핸드 데이터셋

| 데이터셋 | Year | Venue | 규모 | Hand Type | Tasks | F/T or Tactile | 다운로드 | 형식 |
|---|---|---|---|---|---|---|---|---|
| **UniDex** | 2026 | CVPR | 900만 프레임, 50K+ 궤적 | 8종 Robot 핸드 (FAAS) | 다양한 조작 | ✗ | ✅ [HF](https://huggingface.co/datasets/UniDex-ai/UniDex) | HDF5 |
| **Dexora** | 2025 | ICRA | 12.2K 에피소드, 40.5시간 실제 | bimanual 36-DoF | 픽, 조작, 조립, 도구 | ✗ | ✅ [HF](https://huggingface.co/datasets/ZZongzheng0918/Dexora) | Parquet+MP4 |
| **DexMimicGen** | 2024 | ICRA | 21K 시연 | bimanual dexterous | 9가지 Tasks | ✗ | ✅ [HF](https://huggingface.co/datasets/MimicGen/dexmimicgen_datasets) 59.9GB | HDF5 |
| **DexGraspNet 2.0** | 2024 | CoRL | 4.26억 grasp | Shadow | grasp | ✗ | ✅ [HF](https://huggingface.co/datasets/lhrlhr/DexGraspNet2.0) | WebDataset |
| **VTDexManip** | 2025 | ICLR | 56.5만 프레임, 182개 Objects | Multi-finger (sim) | 6가지 복잡 Tasks | ✅ 이진 tactile | ✅ [GitHub](https://github.com/LQTS/VTDexManip) | IsaacGym |
| **ManipTrans/DexManipNet** | 2025 | CVPR | 3.3K 에피소드 | 6종 핸드 | bimanual 조작 | ✗ | ✅ [HF](https://huggingface.co/datasets/ManipTrans/DexManipNet) | MuJoCo |
| **CEDex** | 2026 | ICRA | 2000만 grasp, 50만 Objects | Shadow, Allegro, LEAP | cross-embodiment grasp | ✗ | ✅ [GitHub](https://github.com/GeorgeWuzy/CEDex-Grasp) | Custom |
| **Dexonomy** | 2025 | RSS | 950만 grasp, 10.7K Objects | Shadow (공개; Paper에서 Allegro, LEAP 다룸) | 31종 grasp 유형 | ✗ | ✅ [HF](https://huggingface.co/datasets/JiayiChenPKU/Dexonomy) | Custom |
| **Dex1B** | 2025 | RSS | 10억 시연, 6K+ Objects | Shadow, Inspire, Ability | grasp + 관절 조작 | ✗ | 불명확 | Custom |
| **Fourier ActionNet** | 2025 | — | 30K+ 궤적, 140시간 | Fourier Dex Hands | 실제 humanoid bimanual | ✗ | ✅ [action-net.org](https://action-net.org/) | Custom |
| **RoboMIND** | 2025 | RSS | 107K 궤적, 479가지 Tasks | dexterous 포함 다중 임바디먼트 | 다양한 조작 | ✗ | ✅ [HF](https://huggingface.co/datasets/x-humanoid-robomind/RoboMIND) | Custom |
| **Bi-DexHands** | 2022 | NeurIPS | 오프라인 RL 데이터셋 | 2x Shadow | 16+ bimanual Tasks | ✗ | ✅ [GitHub](https://github.com/PKU-MARL/DexterousHands) | IsaacGym |
| **TCDM** | 2023 | ICRA | 50가지 Tasks, 34개 Objects | 3종 핸드 플랫폼 | 다양한 조작 | ✗ | ✅ [GitHub](https://github.com/facebookresearch/TCDM) | MuJoCo |
| **DAPG** | 2018 | RSS | Tasks당 25개 인간 시연 | Shadow (sim) | 펜, 문, 해머, 공 | ✗ | ✅ [GitHub](https://github.com/aravindr93/hand_dapg) | Pickle/NumPy |

### 8.2 Force / Tactile / 접촉 데이터셋

| 데이터셋 | Year | Venue | 규모 | Sensor Type | 핸드 | 다운로드 | Key Feature |
|---|---|---|---|---|---|---|---|
| **ForceVLA-Data** | 2025 | NeurIPS | 244 궤적, 14만 스텝 | 6축 F/T | gripper (Flexiv) | ✅ [HF](https://huggingface.co/datasets/qiaojunyu/ForceVLA-real-data) | contact-rich 5가지 Tasks |
| **REASSEMBLE** | 2024 | RSS | 4551 시연, 781분 | F/T + 이벤트 카메라 + 오디오 | gripper | ✅ [TUData](https://researchdata.tuwien.ac.at/records/0ewrv-8cb44) | 다중 모달 조립 |
| **RH20T** | 2023 | NeurIPS | 11만 에피소드, 5000만 프레임 | F/T + 손끝 tactile | gripper | ✅ [Site](https://rh20t.github.io/) | 140+ Tasks |
| **Touch100k** | 2025 | Info. Fusion | 10.1만 샘플 | GelSight | N/A | ✅ [GitHub](https://github.com/cocacola-lab/TLV-Link) | 대규모 tactile-언어-비전 데이터셋 |
| **Sparsh/TacBench** | 2024 | CoRL | 46만+ 이미지 | DIGIT/GelSight (교차 센서) | N/A | ✅ [GitHub](https://github.com/facebookresearch/sparsh) | 교차 센서 SSL tactile 인코더, 5가지 Tasks benchmark |
| **TVL** | 2024 | ICML | 4.4만 쌍 | DIGIT | N/A | ✅ [GitHub](https://github.com/Max-Fu/tvl) + [HF](https://huggingface.co/datasets/Max-Fu/TVL) | tactile-비전-언어 정렬 |
| **FMB** | 2025 | IJRR | 22.5K 시연 | F/T (Franka) | gripper | ✅ [HF](https://huggingface.co/datasets/charlesxu0124/functional-manipulation-benchmark) | 기능적 조작 |
| **FeelSight** | 2024 | Science Robotics | 70건 실험 | DIGIT + Allegro | Allegro (16) | ✅ [HF](https://huggingface.co/datasets/suddhu/Feelsight) | in-hand tactile-시각 추적 |
| **ContactPose** | 2020 | ECCV | 2306 grasp, 290만 이미지 | 열 접촉 | 인간 | ✅ [GitHub](https://github.com/facebookresearch/ContactPose) | 기능적 grasp |

### 8.3 인간 손 / egocentric 데이터셋

| 데이터셋 | Year | Venue | 규모 | Modality | Tasks | 언어 | 다운로드 |
|---|---|---|---|---|---|---|---|
| **EgoDex** | 2025 | ICLR | 829시간, 30Hz 1080p | egocentric RGB + 68관절 3D (AVP) | 194가지 테이블탑 | ✅ LLM 설명 | ✅ [GitHub](https://github.com/apple/ml-egodex) ~1.7TB |
| **DexCanvas** | 2025 | arXiv | 7000시간 (v0.1=1%) | 다시점 RGB-D + MANO | 21가지 조작 유형 | ✗ | ✅ [HF](https://huggingface.co/datasets/DEXROBOT/DexCanvas) v0.1 |
| **GigaHands** | 2025 | CVPR | 34시간, 14K 클립 | 다시점 RGB + 3D 손 | bimanual | ✅ 84K 주석 | ✅ [Site](https://ivl.cs.brown.edu/research/gigahands.html) |
| **DexWild** | 2025 | RSS | 9.5K 에피소드, 33시간 | 다시점 RGB + 장갑 | 5가지 Tasks | ✅ | ✅ [HF](https://huggingface.co/datasets/boardd/dexwild-dataset) 2.14TB |
| **HOI4D** | 2022 | CVPR | 240만 RGB-D, 4K 시퀀스 | egocentric RGB-D + 3D 손 | 카테고리 수준 | ✅ 행동 레이블 | ✅ [Site](https://hoi4d.github.io/) |
| **GRAB** | 2020 | ECCV | 162만 프레임 | SMPL-X + MANO + 접촉 | 전신 grasp | ✗ | ✅ [Site](https://grab.is.tue.mpg.de/) (등록 필요) |
| **ARCTIC** | 2023 | CVPR | 210만 프레임 | RGB + MANO + 접촉 | bimanual 관절 조작 | ✗ | ✅ [Site](https://arctic.is.tue.mpg.de/) ~116GB |
| **OakInk / OakInk2** | 2022/24 | CVPR | 23만+ 프레임 | RGB + MANO + Objects | 손-Objects 상호작용 | ✅ (v2) | ✅ [HF](https://huggingface.co/datasets/kelvin34501/OakInk-v2) |
| **DexYCB** | 2021 | CVPR | 58.2만 RGB-D | RGB-D + MANO + Objects | grasp (20 YCB) | ✗ | ✅ [Site](https://dex-ycb.github.io/) 119GB |
| **Ego-Exo4D** | 2024 | CVPR | 1286시간, 740명 참가자 | egocentric+외부 RGB + IMU + 시선 | 숙련 활동 | ✅ | ✅ [Site](https://ego-exo4d-data.org/) (등록 필요) |
| **Humanoid Everyday** | 2025 | arXiv | 10.3K 궤적, 300만 프레임 | RGB + 깊이 + LiDAR + tactile | 260가지 dexterous Tasks | ✅ | ✅ [HF](https://huggingface.co/datasets/USC-GVL/humanoid-everyday) |

### 8.4 Cross-Embodiment pretraining 데이터셋

| 데이터셋 | Year | Venue | 규모 | 임바디먼트 | Tasks | 형식 | 다운로드 |
|---|---|---|---|---|---|---|---|
| [**Open X-Embodiment (OXE)**](https://arxiv.org/abs/2310.08864) | 2023 | arXiv/ICRA | ~100만 에피소드 | 22종 Robot (gripper만) | 527가지 스킬, 160K+ Tasks | RLDS (TF Datasets) | ✅ [Site](https://robotics-transformer-x.github.io/) |
| [**DROID**](https://arxiv.org/abs/2403.12945) | 2024 | arXiv | 76K 시연, 350시간 | Franka Panda (1종 임바디먼트, 564 씬) | 84가지 Tasks, 50명 운영자 | 스테레오 RGB + proprioception + 언어 | ✅ [Site](https://droid-dataset.github.io/) |

---

## 9. Sim Benchmark 및 플랫폼

| Benchmark | Venue | Year | Dex Hand | Sim Platform | Key Feature | 설치 |
|---|---|---|---|---|---|---|
| [**ManiSkill3**](https://arxiv.org/abs/2410.00425) | RSS | 2025 | Allegro, DClaw | SAPIEN (GPU) | 430배 빠름, RL/IL/VLA baseline | `pip install mani-skill` |
| **MuJoCo Playground** | RSS demo | 2025 | LEAP Hand | MuJoCo | 수 분 내 학습, zero-shot sim2real | `pip install playground` |
| **MuJoCo Manipulus** | 2025 | 2025 | 도구 조작 | MuJoCo | 16가지 도구 사용 Tasks | open-source |
| **Adroit** | RSS | 2018 | Shadow (24) | MuJoCo | 표준 RL baseline | `pip install gymnasium-robotics` |
| **Genesis** | 2024년 12월 | 2024 | 모든 URDF | Genesis | 실시간 대비 430K배, 미분 가능 | `pip install genesis-world` |
| **DiffTactile** | ICLR | 2024 | Multi-finger | Custom | 미분 가능 FEM tactile Sim | [GitHub](https://github.com/Genesis-Embodied-AI/DiffTactile) |
| **TeleOpBench** | 2025 | 2025 | 3종 humanoid | Isaac Sim | 30가지 Tasks, 4가지 teleoperation Modality | [GitHub](https://github.com/cyjdlhy/TeleOpBench) |
| [**Isaac Lab**](https://isaac-sim.github.io/IsaacLab/) | RA-L / 2024 | 2024 | Allegro, Shadow, 모든 URDF | Isaac Sim (PhysX 5) | IsaacGym 후속, GPU 병렬, RTX 렌더링 | `pip install isaaclab` |
| [**TACTO**](https://github.com/facebookresearch/tacto) | RA-L | 2022 | gripper (DIGIT/GelSight sim) | PyBullet + PyRender | 비전 기반 tactile 센서 시뮬레이터 | `pip install tacto` |
| [**BiGym 2.0**](https://arxiv.org/abs/2610.07594v2) | — | 2026 | Unitree G1, Dex1 평행 그리퍼 2개 | MuJoCo | 가정용 작업 20개, 작업당 VR 시연 60개, 공통 전신 제어기 | [GitHub](https://github.com/swirl-uk/BiGym2) |

---

## 10. Teleoperation 시스템

| 시스템 | Group | Venue | Year | Input | Target Hand | Force Feedback | Cost | Code |
|---|---|---|---|---|---|---|---|---|
| [**DexCap**](https://arxiv.org/abs/2403.07788) | Stanford | RSS | 2024 | SLAM + 전자기 | LEAP Hand | ✗ | ~$2K | [GitHub](https://github.com/j96w/DexCap) ✅ |
| [**BunnyVisionPro**](https://arxiv.org/abs/2407.03162) | HKU / UCSD | arXiv | 2024 | Apple Vision Pro | bimanual dexterous | 저Cost 햅틱 | ~$3.5K+ | [GitHub](https://github.com/Dingry/BunnyVisionPro) ✅ |
| **AnyTeleop** | UCSD | RSS | 2023 | 비전 (카메라) | 다수 | ✗ | 저가 | 프로젝트 페이지 |
| [**DOGlove**](https://arxiv.org/abs/2505.14635) | TEA Lab | RSS | 2025 | 햅틱 글로브 | 모든 dexterous 핸드 | ✅ 5-DoF | <$600 | [GitHub](https://github.com/TEA-Lab/DOGlove) ✅ |
| [**DEXOP**](https://arxiv.org/abs/2509.04441) | Stanford | arXiv | 2025 | 수동 외골격 | 모든 dexterous 핸드 | ✅ proprioceptive | - | [Page](https://dex-op.github.io/) |
| [**DEX-Mouse**](https://arxiv.org/abs/2604.15013) | - | arXiv | 2026 | 핸드헬드 인터페이스 | 범용 | ✅ 근감각 | <$150 | open-source |
| [**Open TeleDex**](https://arxiv.org/abs/2510.14771) | - | arXiv | 2025 | 휴대폰 기반 | 모든 팔 + 핸드 | ✗ | 매우 저가 | [GitHub](https://github.com/omarrayyann/TeleDex) ✅ |
| [**OmniH2O**](https://arxiv.org/abs/2406.08858) | CMU LeCAR | CoRL | 2024 | VR/음성/RGB | humanoid | ✗ | - | [GitHub](https://github.com/LeCAR-Lab/human2humanoid) ✅ |
| [**Open-TeleVision**](https://arxiv.org/abs/2407.10107) | UCSD | CoRL | 2024 | 스테레오 VR | bimanual dexterous | ✗ | - | [GitHub](https://github.com/OpenTeleVision/TeleVision) ✅ |
| [**HATO**](https://arxiv.org/abs/2404.16823) | UC Berkeley | ICRA | 2024 | Meta Quest 2 VR | 2x Psyonic Ability Hand (6 DoF) + 터치 센서 | ✗ (Robot 측 터치만) | 저가 (VR + 의수 핸드) | [GitHub](https://toruowo.github.io/hato/) ✅ |
| [**DexPilot**](https://arxiv.org/abs/1910.03135) | NVIDIA | ICRA | 2020 | 비전 (맨손, 단일 RGB 카메라) | Allegro (16) + Kuka IIWA | ✗ | 매우 저가 (카메라만) | [Page](https://sites.google.com/view/dex-pilot) |

---

## 11. 저Cost Dexterous 핸드 하드웨어

| 핸드 | Group | Year | 자유도 | Cost | Sim2Real | tactile | Design Files |
|---|---|---|---|---|---|---|---|
| **LEAP Hand V2** | CMU (Pathak) | 2024 | 16 + 손바닥 | ~$3K | ✅ | ✗ | [Page](https://v2-adv.leaphand.com/) |
| **ORCA Hand** | ETH Zurich | 2025 | 17 | <$2K | ✅ (1시간 학습) | ✅ | [orcahand.com](https://www.orcahand.com/) 완전 공개 |
| **ISyHand** | MPI-IS | 2025 | 18 (12+6 손바닥) | ~$1.3K | ✅ | ✗ | [Page](https://isyhand.is.mpg.de/) |
| **RUKA Hand** | NYU (Pinto) | 2025 | 15 | <$1.3K | ✅ | ✗ | [Page](https://ruka-hand.github.io/) |
| **FAIVE Hand** | ETH Zurich (SRL) | 2024 | 11+ | ~$500-800 | ✅ | ✗ | [GitHub](https://github.com/srl-ethz/faive-hand) 완전 공개 |
| **Ability Hand** | PSYONIC Inc. | 2024 | 6 | 상용 | — | ✅ 손끝 압력 | [psyonic.io](https://www.psyonic.io/ability-hand) 비공개 |
| **XHand / Inspire Hand** | 중국 제조사 | 2023+ | 12-16 | ~$1-3K | partial | ✗ | 비공개 상용 |
| **Digit 360** | Meta FAIR | 2024 | N/A (센서) | - | N/A | ✅ 18+ Modality | open-source 예정 |

---

## 12. Tactile 표현 모델

| 모델 | Group | Venue | Year | Key Feature | Code |
|---|---|---|---|---|---|
| **Sparsh** | Meta FAIR/CMU | CoRL | 2024 | SSL 교차 센서 tactile 인코더, TacBench 5가지 Tasks benchmark | [GitHub](https://github.com/facebookresearch/sparsh) ✅, Weights ✅ |
| **UniTouch** | UCSD | CVPR | 2024 | 통합 tactile-비전-언어-소리 정렬 | [GitHub](https://github.com/cfeng16/UniTouch) ✅, Weights ✅ |
| **AnyTouch** | Renmin Univ | ICLR | 2025 | TacQuad 4센서 데이터셋을 활용한 교차 센서 SSL | [GitHub](https://github.com/GeWu-Lab/AnyTouch) ✅, Weights ✅ |
| **NeuralFeels** | Meta FAIR | Science Robotics | 2024 | Allegro+DIGIT in-hand 추적을 위한 뉴럴 필드 | [GitHub](https://github.com/facebookresearch/neuralfeels) ✅ |

---

## 13. 보행 및 휴머노이드 로봇 학습

| 논문 | 연도 | 로봇 / 과제 | 핵심 방법 | 주요 결과 | 코드 |
|---|---|---|---|---|---|
| [**Reflex**](https://arxiv.org/abs/2610.12772v1) | 2026 | Unitree G1; 사람이 던진 상자를 전신으로 받아 유지한다 | 상태 기반 PPO, 동역학 latent 학습, 고정 제어기를 위한 RGB-D 이력 회귀의 3단계로 학습한다 | 포획 성공률: 시뮬레이션 85.7%; 실제 G1은 2.5, 5, 7 m에서 각각 65%, 40%, 15% (조건당 20회) | — |

---

## 14. 학습 기반·최적·안전 제어

| 논문 | 연도 | 로봇 / 과제 | 핵심 방법 | 주요 결과 | 코드 |
|---|---|---|---|---|---|

---

## 15. 로봇 조작 및 모방 학습

| 논문 | 연도 | 로봇 / 과제 | 핵심 방법 | 주요 결과 | 코드 |
|---|---|---|---|---|---|
| [**HexaShell**](https://arxiv.org/abs/2610.23479v1) | 2026 | 시뮬레이션 양팔 ARX X5; RoboDojo 조작 과제 42개 | GPT-6-Astra coding agent가 재사용 도구를 작성·수정; 보정된 RGB의 삼각측량과 평면 제약으로 위치 측정 | seed 0의 새 배치: 성공률 39.7%, progress score 48.0; 정밀 삽입 성공률 8.3% | [코드](https://github.com/HexaFuture/HexaShell) |

---

## 16. 동작 계획 및 의사결정

| 논문 | 연도 | 로봇 / 과제 | 핵심 방법 | 주요 결과 | 코드 |
|---|---|---|---|---|---|

---

## 17. 상태 추정 및 센서 융합

| 논문 | 연도 | 로봇 / 과제 | 핵심 방법 | 주요 결과 | 코드 |
|---|---|---|---|---|---|

---

## 18. 로봇 월드 모델 및 임바디드 파운데이션 모델

| 논문 | 연도 | 로봇 / 과제 | 핵심 방법 | 주요 결과 | 코드 |
|---|---|---|---|---|---|
| [**Towards Agentic Robots: Model, Data, Environment, and Harness**](https://arxiv.org/abs/2610.20442v1) | 2026 | 실제·시뮬레이션 로봇 시스템의 과제 실행과 역량 개발을 다룬 서베이 | policy·VLA·world model·world-action model의 발전을 검토하고 에이전트 결정·도구·피드백을 비교한다 | Model·Data·Environment·Harness의 4개 영역과 중복 가능한 기능 범주 17개로 실행과 역량 개발을 연결한다 | [서베이 자료](https://github.com/chonghanqin/Awesome-Agentic-Robots) |
| [**GroundingPI**](https://arxiv.org/abs/2609.39601v1) | 2026 | 양손 조작 (RoboTwin 2.0), humanoid dexterous-hand 조작 (RoboCasa-GR1); 주행 (nuScenes) | 4B grounding 모델; 점·상자 공유 좌표 토큰; 사전학습 + SFT + GRPO; 조작용 Action DiT | OOD 조작 4개 설정 모두 1위; RoboTwin2.0-Clean2Random 성공률 17.60% vs Rex-Omni 14.10%; nuScenes open-loop L2 0.296 m | — |
| [**ScaleNav**](https://arxiv.org/abs/2610.25690v1) | 2026 | Unitree Go2; 초기 시야의 목표를 향한 언어 조건 지역 항법 | 공유 DiT로 영상·행동 청크 예측; 인터넷 영상 사전학습 + 시뮬레이션 행동 정렬 + 공동 미세조정; 초기 프레임 앵커 | 성공률: 단일 시점 Short-Horizon OVON 86.5%, HabitatGS-LN 94.9%, Go2 83.3% (60회 시행) | [프로젝트](https://zju3dv.github.io/ScaleNav/) |
| [**Ropedia W0**](https://arxiv.org/abs/2610.26855v1) | 2026 | 인간, gripper 로봇, dexterous humanoid; 이동·조작 영상 예측; Xp-Teleop의 Unitree G1 | 카메라 자세·투영 skeleton 조건 영상 diffusion 모델; Xp-Data 인간 사전학습 + 인간·로봇 혼합 학습; 증류 | DreamDojo In-lab PSNR: 20.854 dB vs DreamDojo 14B 18.983 dB (Ropedia W0 5B; post-training 데이터 1%) | — |
| [**VQ-WM**](https://arxiv.org/abs/2610.25600v1) | 2026 | WidowX AI; 네 원판 하노이 탑 (H15); 시뮬레이션 조작·Walker 이동 | 첫 도달시간 기반 상태 양자화; 이산 잠재 BFS + 연속 시각 피드백 제어 | 실제 H15: 짧은 play 데이터로 과제 진행률 100% (6개 사례, 사례별 3회); Cube-Hard 성공률: 73.3 ± 0.9% | — |
| [**RynnUnify**](https://arxiv.org/abs/2610.32965v1) | 2026 | Astribot S1; 다단계 조작; 선택된 RoboCasa365 복합 과제 20개; 시각 계획·미래 상태 추론 | Cosmos3 기반 16B MoT; 장면 기억을 이용한 영상·언어 교차 계획; RL agent 및 공동 영상·행동 확장 | Rynn-VP: Cosmos 3 Nano 대비 +9.75점; 제어 성공률: 선택된 RoboCasa365 과제 51.5%, 실제 로봇 과제 3개 평균 46.7% | [코드](https://github.com/alibaba-damo-academy/RynnUnify) |
| [**Has GPT-6-Astra Achieved Embodied Intelligence?**](https://arxiv.org/abs/2610.22471v1) | 2026 | 조작·이동; benchmark 12개; 로봇 팔, dexterous hand, 이동형 로봇, humanoid를 포함한 실제 로봇 구성 8개 | 모델 가중치 고정; 시연으로 만든 ICL 지식 패키지 동결; 행동 예산 1×/10×; π0.5 행동의 폐루프 검토 | SIMPLE 성공률: ICL 90.8% vs zero-shot 70.8% (공통 과제 4개, 표준 예산); RoboDojo: ICL + 폐루프 VLA 54.17% vs ICL 직접 제어 29.67% | — |
| [**UniWAM**](https://arxiv.org/abs/2610.02054v3) | 2026 | LIBERO·LIBERO-Plus·RoboTwin 2.0의 시뮬레이션 조작; 양손 조작 과제 | MoT 공동 attention으로 물리 추론·영상 생성·행동 예측을 연결한다; VQA·인간·로봇 데이터 사전학습 후 미래 프레임 잡음과 행동 이력 기반 flow matching을 적용한다 | 성공률: LIBERO-Plus 92.6%; RoboTwin 2.0 C2R 68.32%, C2C 75.14% | — |

---

## 19. 미개척 연구 방향

이 절에서는 서베이 문헌에서 도출되는 능력의 미탐구 교차점을 강조함. 이것이 전부는 아니며, 동시 진행 중이거나 미발표된 연구가 이러한 방향 중 일부를 partial으로 다루고 있을 수 있음.

### 19.1 능력 매트릭스

다음 표는 contact-rich dexterous manipulation과 관련된 속성에 대해 대표 시스템을 매핑함. "Sim"은 학습 또는 평가를 위해 공개적으로 사용 가능한 Sim 환경을 의미함.

|  | 다중 손가락 핸드 | 도구 사용 | Force/Impedance 출력 | VLA/Lang | Sim |
|---|---|---|---|---|---|
| **pi0~0.7** | ✗ (gripper만) | ✗ | ✗ | ✅ | ✗ |
| **GR00T N1~1.7** | humanoid 통합만 | ✗ | ✗ | ✅ | ✅ Isaac Lab |
| **GR00T-Dexterity** | ✅ Allegro | ✗ (grasp만) | ✗ | ✗ (RL만) | ✅ Isaac Lab |
| **UniDex-VLA** | ✅ 8종 핸드 | ✅ | ✗ | ✅ | partial (리타겟팅 환경) |
| **DexVLA** | ✅ | ✗ | ✗ | ✅ | ✗ |
| **SimToolReal** | ✅ Sharpa 22-DoF | ✅ 24가지 Tasks | ✗ | ✗ | ✅ IsaacGym |
| **CompliantVLA-adaptor** | ✗ (gripper) | ✗ | ✅ K, D | ✅ (fixed VLA) | ✅ LIBERO |
| **CHIP** | humanoid 35-DoF | ✗ | ✅ EE stiffness | ✗ (RL) | ✅ |
| **TacDiffusion** | ✗ (gripper) | ✗ | ✅ 6D wrench | ✗ | ✗ |
| **DexForce** | ✅ Allegro | ✗ | fixed k_f (hand-tuned) | ✗ | ✗ |

### 19.2 관찰

dexterous 핸드를 이용한 contact-rich 조작 — 도구 사용, 조립, 또는 깨지기 쉬운 물체 다루기 등 — 은 단순히 위치 목표를 추적하는 것이 아니라 상호작용 힘을 조절하는 것을 요구한다. 부적절한 힘 제어는 Objects 미끄러짐, 도구 파손, 또는 환경 손상을 초래한다. gripper는 기계적 compliance로 보상할 수 있는 경우가 많지만, 고자유도 dexterous 핸드는 여러 손끝에 걸쳐 접촉을 분산하므로 각 접촉점의 힘 조절이 더 중요하면서도 더 어렵다. 이는 기존 시스템이 dexterous 제어와 힘/impedance 인식을 결합하고 있는지를 검토하는 동기가 된다.

능력 매트릭스와 광범위한 서베이에서 여러 패턴이 드러난다:

**dexterous VLA와 force-aware 정책은 대체로 독립적으로 발전해 왔다.** dexterous VLA 문헌(§2)은 다양한 핸드에 걸친 위치 목표 생성에 초점을 맞추는 반면, 힘/impedance 문헌(§3-5)은 gripper와 Robot 팔의 contact-rich 제어에 집중한다. UniDex-VLA, DexVLA, DexGraspVLA 모두 위치 목표만을 출력한다. 반대로 impedance 매개변수를 출력하는 시스템(CompliantVLA-adaptor, CHIP, Comp-ACT, VICES)은 gripper 또는 팔에서 작동한다. DexForce만이 force-aware을 통합한 dexterous 핸드 연구로, Allegro Hand에서 hand-tuned된 fixed 스케일링을 사용한다.

**cross-embodiment 행동 표현은 여전히 단편화되어 있다.** 다양한 임바디먼트 간 dexterous 핸드 행동을 표현하기 위해 여러 접근법이 경쟁하고 있다: FAAS (UniDex-VLA), eigengrasps (CrossDex), 범용 Code북 (UniAct), 이종 스템 (HPT), 임바디먼트별 MLP (GR00T). 어떤 표현이 교차 핸드 일반화를 가장 잘 지원하는지에 대한 합의는 없으며, 이들 접근법 간의 직접 비교도 드물다.

**dexterous 데이터 수집은 공인된 병목이다.** 저Cost teleoperation 시스템(§10)의 증가 — DexCap, DOGlove, DEXOP, DEX-Mouse, 모두 2024-2026년 발표 — 는 커뮤니티가 데이터 수집을 주요 장애물로 보고 있음을 시사한다. 이러한 노력에도 불구하고, 대부분의 dexterous 데이터셋(§8.1)은 여전히 joint position와 시각 데이터만을 캡처하며, force/torque Modality는 거의 전적으로 gripper 기반 시스템(§8.2)에서만 사용 가능하다.

**dexterous RL의 Sim-to-Real 전이는 성숙해지고 있다.** 여러 최근 Paper이 dexterous 핸드에 대한 zero-shot 또는 near-zero-shot sim-to-real 전이를 시연한다: CrossDex (LEAP), RobustDexGrasp (Allegro, 94.6%), DeXtreme (Allegro), DQ-RISE (LEAP+Franka, 85.8%), HandelBot (bimanual LEAP). 이는 Sim 학습 dexterous 정책이 실용적으로 deploy 가능해지고 있음을 시사하며, 이 분야에서 Sim 기반 연구의 진입 장벽을 낮추고 있다.

**VLA 모델 계열은 여전히 gripper 중심이다.** 서베이된 pi(pi0~pi0.7)와 GR00T(N1~N1.7)의 모든 Version에서 독립형 다중 손가락 dexterous 핸드를 네이티브로 지원하는 Version은 없다(§6.1-6.2). GR00T-Dexterity는 Allegro 지원을 추가하지만, VLA 자체의 일부가 아닌 별도의 RL 워크플로우로서이다. open-source VLA 생태계(openpi, Isaac-GR00T, OpenVLA)는 아직 커뮤니티에 의해 dexterous 핸드 임바디먼트로 확장되지 않았다.

**모델 기반 접촉 제어는 상보적 축이다.** 접촉 내재 MPC와 미분 가능 contact model(Contact Trust Region, Complementarity-Free, ComFree-Sim)은 contact-rich dexterous manipulation을 위한 학습된 impedance의 대안을 제공한다. 최근 연구는 Allegro 및 LEAP 핸드에 대해 50-100 Hz의 실시간 MPC를 달성한다. 이러한 접근법은 학습된 정책이 일반적으로 결여하는 형식적 보장(예: 상보성 제약, 수동성)을 제공하지만, 정확한 동역학 모델을 요구하며 연성/deformable 접촉에서 어려움을 겪는다. dexterous 핸드를 위해 모델 기반과 학습 기반 힘 제어를 어떻게 결합할 수 있는지 — 예: 모델 기반 내부 루프가 추적하는 학습된 impedance 설정값 — 는 대체로 미탐구 상태이다.

---

## 20. 참고 링크

### 주요 GitHub 조직 / 프로젝트 페이지
- [Google DeepMind](https://deepmind.google/models/gemini-robotics/) — Gemini Robotics, Gemini Robotics-ER, RT-2
- [PKU-EPIC](https://github.com/PKU-EPIC) — DexGraspNet, UniDexGrasp, BODex, Dexonomy
- [PKU-RL](https://github.com/PKU-RL) — CrossDex, ResDex
- [NVlabs](https://github.com/NVlabs) — DextrAH, DexMimicGen, IndustReal, CHIP
- [UniDex-AI](https://github.com/unidex-ai) — UniDex-VLA
- [Physical-Intelligence](https://github.com/Physical-Intelligence) — openpi (pi0, pi0-FAST, pi0.5); pi0.6, pi0.7은 not released
- [NVIDIA Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) — GR00T N1~N1.7
- [ForceMimic](https://github.com/ForceMimic) — ForceMimic, ForceCapture
- [Meta FAIR](https://github.com/facebookresearch) — SPIDER, TCDM, Sparsh, NeuralFeels
