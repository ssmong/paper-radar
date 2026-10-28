### λ_0

**전체 제목:** $λ_0$: Scaling Open-World Egocentric Human Data for Humanoid Loco-Manipulation

**저자:** Lambda-humanoid Team

**학회/연도:** — / 2026

**arXiv:** [2610.18950v1](https://arxiv.org/abs/2610.18950v1)

**아키텍처:** Qwen3.5-2B 시각·언어 backbone이 생성형 action expert에 조건 정보를 전달한다. policy는 자기중심 영상, 언어 지시, 로봇 상태를 입력받아 50-step action chunk를 예측한다. G1의 각 action은 64차원 SONIC motion latent와 양손의 6차원 Revo2 명령으로 구성된다.

**핵심 방법론:** 카메라 시점과 팔 외형을 정렬한다. 인간 동작 참조, 로봇 동작 참조, 제어기 입력을 오프라인에서 보정한다. 학습은 손 동작 사전 학습, 정렬된 HumanVerse를 이용한 인간 전신 동작 mid-training, 로봇 post-training의 세 단계로 진행된다. Stage II와 III는 flow matching을 사용한다.

**로봇 / 과제:** Revo2 손을 장착한 Unitree G1이 전신 loco-manipulation을 수행한다. 실제 평가 과제는 Bottle Disposal, Toy Storage, Box Transport, Chair Placement이다. 별도의 전이 실험은 대상 과제의 로봇 시연 없이 과제별 인간 시연을 사용한다. 전체 λ_0 policy는 로봇 post-training을 거친다.

**주요 contribution:**

- 자기중심 영상과 동기화된 신체·손 동작으로 구성된 HumanVerse를 제안한다. 500시간은 변환과 유효성 필터링 이전의 수집량이다.
- 인간 관측과 action을 G1 제어기 인터페이스에 정렬한다.
- 로봇 시연을 고정한 상태에서 인간 데이터 규모와 학습 단계의 효과를 분석한다.

**정량적 결과:**

| Benchmark / 과제 | 지표 | 값 | 조건 |
|---|---|---|---|
| SIMPLE | Success rate | 90.0% | 과제 6개, Levels 0–2; 과제·수준별 10회; 과제별 설정 선택 |
| 실제 G1 과제 4개 | Average success rate | 62.5% | 과제와 policy마다 고정된 초기 구성 10개 |
| 실제 G1 과제 4개 | Average weighted progress | 80.4% | 과제별 동일 가중치; 같은 초기 구성과 채점 기준에서 StarVLA는 54.6% |
| Stage II를 제외한 실제 G1 과제 4개 | Average success rate | 22.5% | 아키텍처, action 표현, 시각·언어 초기화, Stage III 로봇 post-training을 동일하게 유지 |
| 오프라인 action 정렬 | 평균 end-effector 위치 / 방향 오차 | 17.03 → 3.83 cm / 36.06° → 10.85° | 로봇 참조 보정과 동역학 기반 단계를 과제 50개, 약 1 h 데이터에서 평가 |

**AI 연구 평가:** 세 검토자의 평균 점수이며, 10점 척도이다.

| 항목 | 점수 /10 | 근거 |
|---|---|---|
| 중요도 | 8.0 | 비용이 큰 humanoid 시연 수집과 이동·조작의 공동 학습을 다룬다. 수집 효율 검증은 대표 과제에 한정된다. |
| 추가 contribution | 7.3 | HumanVerse, G1 정렬, 로봇 데이터를 고정한 규모화 검증을 결합한다. HALOMI와 EMMA에 관련 정렬·인간 데이터 학습 방법이 있다. |
| 방법 품질 | 8.0 | 기하 오차와 제어기 오차를 분리하고 공통 action 인터페이스를 사용한다. 통제된 ablation이 설계를 뒷받침하지만 정렬 검증 범위는 제한적이다. |
| 효과성 | 8.0 | 실제 G1 결과와 Stage II ablation이 인간 전신 데이터의 효과를 뒷받침한다. 실제 평가는 과제 4개와 과제당 10회에 한정된다. |
| gap 해소 근거 | 8.0 | 정렬, 수집 노동 측정, 규모화 결과가 인간 경험을 humanoid 학습 신호로 전환하는 gap의 축소를 뒷받침한다. 다른 embodiment로의 전이와 측정 범위 밖 규모 외삽은 입증되지 않았다. |

**종합 점수:** 7.8/10.

**한계점:**

- 실제 λ_0 평가는 G1, 과제 4개, 과제당 초기 구성 10개에 한정된다.
- SIMPLE 결과는 과제별 설정 선택을 사용한다. 공개 baseline은 원래 평가 절차를 유지한다.
- 규모화 loss fit은 단일 실행 결과이다. 여러 seed에서의 재현성이나 측정 범위 밖 외삽은 입증하지 않는다.
- HumanVerse의 500시간은 변환과 유효성 필터링 이전의 수집량이다. 손 동작은 RGB에서 복원한다.
- 전체 policy는 로봇 post-training이 필요하다. 대상 과제의 로봇 시연 없는 전이는 별도 실험이다.

**공개 가중치/코드:** — / [코드](https://github.com/LambdaHumanoid/openlambda).

## 추론 / 배포

- **추론 지연 시간:** —.
- **배포 하드웨어:** Revo2 손과 머리에 GoPro HERO13을 장착한 Unitree G1이다. SONIC이 motion token을 실행한다. 배포 시 인간 동작 스트림 없이 로봇 영상과 상태를 사용한다.

## 데이터셋 / 데이터 수집

- **HumanVerse:** 수집량은 500시간이며, 시연 32,993개, 자세 프레임 8,700만 개, 과제 유형 827개를 포함한다. 착용형 신체 추적 데이터를 자기중심 영상과 동기화하고, 손 동작은 영상에서 복원한다.
- **학습 데이터:** Stage I는 공개 자기중심 손·물체 데이터셋, Stage II는 정렬된 HumanVerse, Stage III는 로봇 시연을 사용한다.
- **데이터 분할:** 시간 구간을 추출하기 전에 수집 세션별로 분할한다. 후속 post-training용 과제별 인간 시연은 HumanVerse와 분리한다.

**출처:** [논문 본문](https://arxiv.org/html/2610.18950v1)의 초록 및 3–5절.
