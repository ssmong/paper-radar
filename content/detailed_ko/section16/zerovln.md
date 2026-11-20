### ZeroVLN

**전체 제목:** ZeroVLN: Learning to Navigate without Supervised Fine-Tuning of the VLM Brain

**저자:** Zixuan Huang 외

**학회/연도:** — / 2026

**arXiv:** [2611.26414v1](https://arxiv.org/abs/2611.26414v1)

**아키텍처:** Qwen3.6-35B-A3B VLM brain이 의미 기반 도구 호출로 자연어 이동 요청을 전달한다. 12층 flow-matching action expert가 Qwen3.5-4B 시각 인코더를 사용해 요청을 실행한다. 느린 brain은 이동을 결정하고, 빠른 action expert는 새 RGB 관측에 따라 연속 행동을 갱신한다.

**핵심 방법론:** 먼저 planner가 장면 mesh 기반 의미 지도와 학습 전용 기하 정보로 고정된 brain의 요청을 도달 가능한 지역 목표와 기준 궤적에 grounding한다. Action expert는 예측한 행동 시퀀스 중 실제 실행하는 prefix에 대해서만 지도학습한다. 이후 closed-loop RL로 brain과 action expert를 공동 학습한다. 두 policy는 궤적 단위 advantage를 공유하되 gradient 경로는 분리한다. 보상은 최종 성공, 첫 도달, 목표까지의 거리 감소, 정보 발견을 반영한다. Brain에 탐색 영역 SFT를 적용하지 않지만 RL 과정에서는 가중치가 바뀐다.

**로봇 / 과제:** SAGE-Bench (SAGE-3D), R2R-CE, RxR-CE의 시뮬레이션 시각·언어 탐색. 실제 로봇: —. R2R-CE와 RxR-CE는 목표 영역에서 정지해야 성공이며, SAGE-Bench는 도달을 요구한다.

**주요 contribution:**

- Brain의 탐색 영역 SFT 없이 기하 목표 예측을 의미 기반 도구 요청으로 대체한다.
- Action expert의 학습을 brain의 실제 요청과 실행에 사용하는 행동 prefix에 맞춘다.
- RL로 이동 결정과 연속 실행을 공동 개선하면서 일반 시각 능력을 대부분 보존한다.

**정량적 결과:**

| Benchmark / 과제 | 지표 | 값 | 조건 |
|---|---|---|---|
| SAGE-3D 탐색 | SR | 51.3%; NaVILA 23.5% | 동일 backbone·학습 에피소드 |
| R2R-CE 탐색 | SR | 52.7%; NaVILA 46.5% | 동일 backbone·학습 에피소드; 정지 필요 |
| RxR-CE 탐색 | SR | 51.4%; NaVILA 48.7% | 동일 backbone·학습 에피소드; 정지 필요 |
| R2R-CE / RxR-CE 탐색 | SPL | 29.2% / 28.1%; NaVILA 41.8% / 43.0% | 동일 backbone·학습 에피소드; OSR은 높지만 경로 효율은 낮다 |
| 일반 시각 benchmark 12개 | Mean accuracy | 59.16%; 기본 brain 59.47% | 탐색 학습 후 능력 보존을 평가한다 |

**AI 연구 평가:** 세 검토자의 평균 점수이며, 10점 척도이다.

| 항목 | 점수 /10 | 근거 |
|---|---|---|
| 중요도 | 8.0 | 일반 시각 능력을 유지하며 탐색을 학습하는 문제는 공유 로봇 brain 연구에 중요하다. 다른 물리 기술과 실제 로봇은 평가 범위 밖이다. |
| 추가 contribution | 8.0 | 의미 기반 요청과 slow–fast policy 공동 RL이 DualVLN의 기하 인터페이스를 확장한다. 기존 방법을 결합한 설계이며 다른 backbone으로의 전이는 미검증이다. |
| 방법 품질 | 8.0 | 요청 grounding과 실행 prefix 지도학습이 학습·실행 불일치를 줄인다. 학습에는 의미 지도와 학습 전용 기하 정보를 쓰는 planner가 필요하다. |
| 효과성 | 7.0 | 동일 backbone·에피소드 비교가 높은 SR과 능력 보존을 뒷받침한다. R2R/RxR의 낮은 SPL은 경로 효율 측면의 이점을 제한한다. |
| gap 해소 근거 | 8.0 | 통제된 탐색 비교와 답 형식을 우회한 시각 평가가 능력 보존을 지지한다. 근거는 하나의 brain backbone과 VLN-CE에 한정된다. |

**종합 점수:** 7.8/10.

**한계점:**

- R2R-CE와 RxR-CE에서 NaVILA보다 OSR은 높지만 SPL은 낮다. 추가 탐색이 경로를 늘릴 수 있다.
- Action expert의 초기 학습에는 장면 mesh 기반 의미 지도와 학습 전용 기하 정보를 쓰는 planner가 필요하다.
- 평가는 VLN-CE benchmark 3개와 하나의 brain backbone을 다룬다. 실제 로봇과 다른 backbone에서의 효과는 미검증이다.
- 목표 도달성과 일반 시각 능력을 유지하면서 불필요한 탐색을 줄이는 gap이 남는다.

**공개 가중치/코드:** — / —.

## 추론 / 배포

- **추론 지연 시간:** —.
- **배포 하드웨어:** —.

## 데이터셋 / 데이터 수집

- **학습 데이터:** 탐색 에피소드 34,445개의 공통 집합을 action expert 적응과 RL에 사용한다. 고정된 brain의 이동 요청으로 기준 궤적을 생성한다.
- **평가 데이터:** SAGE-Bench, R2R-CE, RxR-CE의 공식 평가 집합과 능력 보존 평가용 일반 시각 benchmark 12개.

**출처:** [논문 본문](https://arxiv.org/html/2611.26414v1)의 2–5절.
