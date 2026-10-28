### SuperNav

**전체 제목:** SuperNav: An Agentic Navigation System for Any Task in Any Scene

**저자:** Jinkai Zhang 외

**학회/연도:** — / 2026

**arXiv:** [2610.12126v1](https://arxiv.org/abs/2610.12126v1)

**아키텍처:** Pretrained MLLM이 탐색 전용 fine-tuning 없이 harness를 통해 탐색 목표를 선택한다. Navigation Skills는 탐색, 복구, 완료 판단을 위한 지침을 제공한다. 도구는 네 방향 RGB 영상, 실행 상태, 진단 정보를 반환한다. 공통 이미지 좌표 인터페이스가 MLLM을 Geo-based Executor 또는 Learned Executor와 연결한다.

**핵심 방법론:** MLLM이 이미지에서 목적지를 선택하면 실행기가 이동하고 다음 판단을 위한 피드백을 반환한다. 목표 기록은 미완료 항목과 완료 항목을 관리한다. 문맥 관리는 새 관측으로 대체된 이미지 데이터를 제거하되 텍스트 이력과 이미지 경로를 유지한다. Geo-based Executor는 기하 정보와 경로 계획을 사용한다. Learned Executor는 RGB 관측과 이미지에 표시한 목표 좌표에서 국소 이동을 예측한다.

**로봇 / 과제:** Habitat-GS의 객체 인스턴스 및 순서가 있는 다중 객체 탐색, AI2-THOR의 요구 기반 탐색, HM3D의 객체 범주 탐색을 평가한다. 실제 로봇 사례에서는 Unitree Go2가 물체를 찾고 여러 목표를 차례로 방문한다.

**주요 contribution:**

- 이미지에서 선택한 목적지를 교체 가능한 운동 실행기와 연결한다.
- Navigation Skills, 목표 기록, 문맥 관리를 결합해 다양한 요청을 처리한다.
- 여러 탐색 과제 유형을 평가하고 ablation으로 harness의 효과를 분석한다.

**정량적 결과:**

| Benchmark / 과제 | 지표 | 값 | 조건 |
|---|---|---|---|
| InteriorGS 기반 Habitat-GS, 단일 객체 탐색 | SR | 78.00% | Geo-based Executor; 150개 과제; 승인된 목표 시점까지 navmesh 경로 거리 1 m 미만 및 명시적 STOP |
| InteriorGS 기반 Habitat-GS, 순서가 있는 다중 객체 탐색 | SR | 34.00% | Geo-based Executor; 목표 2–5개의 과제 150개; 순서대로 도달 및 명시적 STOP |
| AI2-THOR에서 평가를 수정한 Demand-Bench | SR | 59.50% | Geo-based Executor; 200개 과제; 객체 재사용 없이 2 m 목표 영역에 순서대로 도달 및 명시적 STOP |
| HM3D-OVON val-unseen, Navigation Skills ablation | SR | Skills 사용 68.33%; 제거 35.00% | 동일한 120개 에피소드, Geo-based Executor, GPT-5.6 Terra (high), 0.25 m 임계값 |

**AI 연구 평가:** 세 검토자의 평균 점수이며, 10점 척도이다.

| 항목 | 점수 /10 | 근거 |
|---|---|---|
| 중요도 | 8.0 | 낯선 환경에서 다양한 요청을 처리하는 능력은 서비스 로봇에 중요하다. 추론 비용, 지연 변동, 기하 정보 의존이 실제 활용을 제한한다. |
| 추가 contribution | 6.0 | 교체 가능한 실행기, Skills, 문맥 관리가 기존 harness 접근을 확장한다. 가장 가까운 harness 접근과의 직접 비교는 없다. |
| 방법 품질 | 8.0 | 이미지 좌표 목표와 실행 피드백으로 판단과 운동 실행을 분리한다. 동일 실행기의 ablation이 설계를 지지하지만 의미적 완료 판단을 독립적으로 검증하지 않는다. |
| 효과성 | 7.0 | 결과가 여러 탐색 과제 유형의 효과를 뒷받침한다. 관측·실행 조건 차이가 baseline 비교를 제한하며, 실제 로봇 근거는 정성 사례이다. |
| gap 해소 근거 | 7.0 | 고정 절차와 탐색 학습 데이터 범위를 넘어선 과제·장면 일반성을 결과가 지지한다. 실제 활동 완수와 긴 실환경 연속 과제는 검증되지 않았다. |

**종합 점수:** 7.1/10.

**한계점:**

- 의미 판단과 목표 기록은 MLLM에 의존하며, 독립적인 의미 검증이 아니다.
- Geo-based Executor는 지도 또는 장면 기하 정보가 필요하다. MLLM 추론은 비용과 지연 변동을 추가한다.
- 요구 기반 평가는 목표까지 순서대로 이동하는 능력을 측정하며, 요청된 활동 자체의 완수를 평가하지 않는다.
- Baseline은 고유 입력과 이력 관리 방식을 유지한다. SuperNav와 관측·운동 실행 조건이 다르다.
- 실제 로봇 근거는 정성 사례이다. 긴 탐색 연속 과제의 신뢰성과 더 넓은 실환경 평가는 후속 과제로 남는다.

**공개 가중치/코드:** — / —.

## 추론 / 배포

- **추론 지연 시간:** 변동이 크며, 수치: —.
- **배포 하드웨어:** 네 방향 RGB 카메라, LiDAR, odometry를 사용하는 Unitree Go2; 연산 하드웨어: —.

## 데이터셋 / 데이터 수집

- **평가 데이터:** InteriorGS 기반 Habitat-GS의 단일 객체 과제 150개와 순서가 있는 다중 객체 과제 150개. AI2-THOR에서 평가를 수정한 Demand-Bench의 과제 200개. 객체 범주 평가는 HM3D-OVON val-unseen의 120개 에피소드와 HM3Dv2 검증 에피소드 1,000개를 사용한다.

**출처:** [논문 본문](https://arxiv.org/html/2610.12126v1)의 3–5절 및 부록 A.1; [프로젝트](https://zju3dv.github.io/SuperNav/).
