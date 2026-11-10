### ODE Policy

**전체 제목:** ODE Policy: Robot Learning via Action Dynamics, Not Actions

**저자:** Jindou Jia 외

**학회/연도:** — / 2026

**arXiv:** [2611.01729v1](https://arxiv.org/abs/2611.01729v1)

**아키텍처:** Neural ODE가 FiLM-MLP vector field로 action dynamics를 모델링한다. 영상과 지시문이 vector field의 조건이 되며, 고유감각 정보는 vector field에 직접 입력한다. Diversity head는 표본 추출한 속도 편차를 더해 multi-modal behavior를 표현한다. 같은 구조를 visuomotor policy, VLA·WAM의 action head, RL의 actor로 사용한다.

**핵심 방법론:** 모방 학습(IL)에서는 짧은 chunk의 적분 경로를 시연과 맞추는 path loss를 사용하며, velocity label은 사용하지 않는다. Contractive perturbation은 학습 중 시작 action을 바꾸고 경로가 시연으로 돌아오도록 한다. 추론에서는 이전 chunk의 마지막 action부터 적분을 이어간다. 각 chunk 안에서는 관측과 고유감각 정보를 고정한다. 강화 학습(RL)에서는 제어 단계마다 이전 action에서 Euler step을 한 번 수행한다.

**로봇 / 과제:** LIBERO에서 조작을, LIBERO-plus에서 일반화를 평가한다. 실제 로봇 과제 14개에는 Franka Research 3, Galaxea R1 Lite, Sharpa 다지 손을 장착한 Sharpa North, Inspire DFX 다지 손을 장착한 Unitree G1을 사용한다. 정밀·장기·변형 물체·multi-modal·다지 손 조작과 이동을 결합한 조작 과제를 포함한다. RL에서는 SuperMimic과 시뮬레이션 Unitree G1으로 LAFAN1 동작 clip 40개를 추적한다.

**주요 contribution:**

- Velocity label 없이 물리 시간에 따라 적분한 경로로 action vector field를 학습한다.
- 이전 action부터 적분을 이어 chunk를 연결하고, diversity head로 서로 다른 행동 mode를 유지한다.
- 같은 action dynamics 구조를 IL, VLA·WAM의 action head, model-based RL에 적용한다.

**정량적 결과:**

| Benchmark / 과제 | 지표 | 값 | 조건 |
|---|---|---|---|
| LIBERO, visuomotor IL | success rate | 79.2% | 1 epoch 후; 비교 baseline의 최고값 43.2%; 4개 suite와 3개 seed |
| LIBERO, π0.5 | success rate | 96.0% | 1 epoch 후; FM-R 75.5%; 단일 seed; 두 action head 모두 무작위 초기화하며 구조와 parameter 수는 다름 |
| LIBERO, ImageWAM | success rate | 82.6% | 1 epoch 후; 기존 flow matching head 24.6%; 단일 seed |
| LIBERO, visuomotor IL | success rate | 87.7% | Epoch 100; 과제당 시연 20개; FM-DiT는 시연 50개로 85.4%; 데이터 조건이 다름 |

**AI 연구 평가:** 세 검토자의 평균 점수이며, 10점 척도이다.

| 항목 | 점수 /10 | 근거 |
|---|---|---|
| 중요도 | 8.0 | 데이터 비용, 추론 비용, action 연속성은 여러 robot policy의 공통 문제이다. VLA·WAM·RL에 폭넓게 적용하지만 장기 운용은 검증되지 않았다. |
| 추가 contribution | 8.0 | Velocity label 없이 적분 경로를 학습하고 chunk를 연결해 Streaming flow policy를 확장한다. 시간 정렬과 dynamical policy 자체에는 선행 연구가 있다. |
| 방법 품질 | 8.0 | 짧은 경로 적분과 contractive perturbation이 연속성과 오차 누적 문제에 적합하다. Chunk 안에서 관측을 고정하므로 새 사건에 대한 반응은 제한된다. |
| 효과성 | 7.3 | 동일 backbone·데이터·학습 일정이 비교를 뒷받침하며 visuomotor 실험은 seed 3개를 사용한다. 대형 모델은 단일 seed이며 baseline이 이후 따라잡거나 수렴한다. |
| gap 해소 근거 | 7.0 | 적분 구조와 학습 결과가 연속성 및 비용 gap의 개선을 뒷받침한다. 본문 발췌에는 실제 로봇·smoothness·ablation의 상세 결과가 없어 판단이 제한된다. |

**종합 점수:** 7.7/10.

**한계점:**

- Action을 순차 실행해도 관측을 연속 갱신하는 것은 아니다. Chunk 안에서는 관측과 고유감각 정보를 고정한다.
- π0.5와 ImageWAM의 학습 곡선은 단일 seed 결과이다. 사전 학습한 π0.5 expert는 epoch 2부터 따라잡고, ImageWAM head들은 epoch 6부터 수렴한다.
- 실행 품질은 성공한 episode에서만 측정한다. 실패 rollout의 품질은 이 평가에 포함되지 않는다.
- LIBERO의 이진 gripper 명령은 별도 classification head로 예측한다. 이 명령에는 다른 action과 같은 연속 적분을 적용하지 않는다.
- LIBERO에서 대형 모델의 초기 학습이 개선되어도 다른 과제나 분포 변화에서 같은 효과가 유지되는지는 확인되지 않았다.

**공개 가중치/코드:** — / —.

## 추론 / 배포

- **추론 지연 시간:** — (본문 발췌에 절대 지연 시간은 보고되지 않음).
- **배포 하드웨어:** —.
- **적분:** 표준 visuomotor IL은 8-step chunk와 RK4를 사용한다. ImageWAM은 12-step chunk와 Euler를, GR00T N1.7은 16-step chunk와 Euler를 사용한다.

## 데이터셋 / 데이터 수집

- **학습 데이터:** LIBERO 시연을 사용한다. π0.5는 과제당 episode 10개, ImageWAM은 25개를 사용한다. 실제 로봇 과제 3개는 다른 연구실의 데이터를 사용한다.
- **평가 데이터:** LIBERO의 4개 suite에서 visuomotor checkpoint마다 과제당 episode 20개로 평가하며 학습 seed는 3개이다. 대형 모델 학습 곡선은 단일 seed이다. 실제 로봇은 과제·방법별로 20회 평가한다. RL은 LAFAN1 clip 40개 전체를 평가한다.

**출처:** [논문 본문](https://arxiv.org/html/2611.01729v1)의 초록 및 1–6.1.2절.
