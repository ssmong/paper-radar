### TCP4D

**전체 제목:** TCP4D: A Unified Tool-Center-Point Tracking and Generation Model for Robot Manipulation

**저자:** Haosong Peng 외

**학회/연도:** — / 2026

**arXiv:** [2611.23143v1](https://arxiv.org/abs/2611.23143v1)

**아키텍처:** DINOv2 기반 Transformer backbone이 4RC 구조를 따라 공유 4D 장면 표현을 만든다. 초기 2D TCP query로 SE(3)의 TCP 자세, gripper 상태, 장면 기하, 카메라 매개변수를 직접 추정한다. DiT는 추적 경로 주변 특징, 로봇 상태, 손목 영상, 언어 지시로 미래 TCP 상태를 생성한다. 고정된 DINOv2와 T5-base가 손목 영상과 언어 지시를 인코딩한다.

**핵심 방법론:** 먼저 장면 기하와 TCP 복원을 함께 학습한다. 이후 flow matching으로 backbone, tracker, generator를 공동 fine-tuning한다. Cross-embodiment 증강은 RGB 영상에서 동작을 복원하고 IK로 대상 로봇에 맞춘다. 원본 로봇을 제거하고 배경을 복원한 뒤 대상 로봇을 렌더링한다. 기록된 원본 로봇 상태 없이도 수행할 수 있다. 대상 로봇은 복원된 동작에 도달할 수 있어야 한다.

**로봇 / 과제:** TCP 추적은 DROID와 RoboLab에서 평가한다. 조작 평가는 RoboTwin 과제 48개와 CoBoT Magic의 펜 놓기·그릇 쌓기 두 과제를 포함한다. Cross-embodiment policy 평가는 네 과제에서 Aloha-AgileX의 원본 시연과 ARX-X5·UR5-WSG 대상 로봇을 사용한다.

**주요 contribution:**

- 표면점에 강체 동작을 맞추는 과정 없이 가상 TCP 자세와 gripper 상태를 직접 복원한다.
- 공유 4D 장면 표현으로 TCP 추적과 미래 행동 생성을 연결한다.
- 기록된 원본 로봇 상태 없이 RGB 영상을 대상 로봇 시연으로 변환한다.

**정량적 결과:**

| Benchmark / 과제 | 지표 | 값 | 조건 |
|---|---|---|---|
| DROID / RoboLab | ATE | 7.60 / 16.07 mm | Sim(3) 정렬 후 측정 |
| RoboLab Unseen | RRE | 6.80° | MoSE3: 0.99°; TCP4D의 회전 오차가 더 큼 |
| RoboTwin 과제 48개 | 평균 성공률 | clean2clean 69.19% / clean2random 10.94% | 과제별 100회 시행; TCP4D는 third view, 비교 baseline은 head view 사용 |
| CoBoT Magic 두 과제 | 평균 성공률 | 78.33% | 과제·방법별 30회 시행; DP3: 63.33%; DP3는 depth point cloud, TCP4D는 RGB 사용 |
| ARX-X5 네 과제 | 평균 성공률 | 72.0% vs 30.5% | DP의 원본 + 증강 데이터 학습과 증강 데이터만 사용한 학습 비교; 동일 학습 예산; 과제별 50회 실행 |

**AI 연구 평가:** 세 검토자의 평균 점수이며, 10점 척도이다.

| 항목 | 점수 /10 | 근거 |
|---|---|---|
| 중요도 | 8.0 | 행동 주석이 없는 영상의 재사용은 로봇 학습 데이터를 늘릴 수 있다. 대상 로봇의 도달 가능 범위가 전이 가능한 동작을 제한한다. |
| 추가 contribution | 8.0 | 가상 TCP를 직접 복원해 표면점 맞춤과 기록된 원본 로봇 상태에 대한 의존을 줄인다. Backbone과 생성 방법은 기존 설계를 확장한다. |
| 방법 품질 | 7.7 | 직접 자세 복원과 추적 경로를 조건으로 한 flow matching이 행동 복원과 생성을 연결한다. 공유 표현과 추적 경로 조건화 각각의 효과는 분리되지 않는다. |
| 효과성 | 7.0 | 추적, 실제 로봇 과제, 증강 데이터로 학습한 policy 결과가 활용 가능성을 뒷받침한다. 낮은 clean2random 성공률과 더 큰 RoboLab 회전 오차가 성능의 한계를 보인다. |
| gap 해소 근거 | 7.0 | 추적과 대상 policy 결과는 행동 주석 복원과 원본 로봇 상태 없는 증강을 뒷받침한다. 도달 가능 범위와 제한된 과제 범위가 남은 gap이다. |

**종합 점수:** 7.5/10.

**한계점:**

- Generator는 clean 시연만으로 학습한다. RoboTwin clean2random 성공률은 10.94%로 낮아진다.
- 실제 로봇 generator 평가는 CoBoT Magic 두 과제에 한정되며, 과제·방법별 30회 시행한다.
- RoboTwin에서 TCP4D와 비교 baseline의 카메라 시점이 다르다. 실제 로봇 비교에서 DP3는 depth point cloud를 사용한다.
- ATE는 Sim(3) 정렬 후 측정한다. 이 값만으로 정렬 전의 실제 단위 자세 정확도를 판단할 수 없다.
- 대상 로봇은 복원된 동작에 도달할 수 있어야 한다. 공유 표현과 추적 경로 조건화 각각의 효과는 분리해 측정하지 않았다.

**공개 가중치/코드:** — / —.

## 추론 / 배포

- **추론 지연 시간:** —.
- **배포 하드웨어:** —.
- **통합:** Euler 갱신 4회로 미래 행동 시퀀스를 생성한다. CoBoT Magic은 IK에 cuRobo를 사용하며, 추론 시 실측 depth가 필요하지 않다.

## 데이터셋 / 데이터 수집

- **학습 데이터:** Tracker 학습에 DROID와 RoboTwin을 사용한다. CoBoT Magic은 과제별 시연 60개를 사용한다. 증강에는 과제별 Aloha-AgileX 원본 시연 50개를 사용하며, 네 과제 전체에서 ARX-X5 시연 199개와 UR5-WSG 시연 198개를 생성한다.
- **평가 데이터:** DROID·RoboLab 추적; RoboTwin 과제 48개에서 과제별 100회 시행; CoBoT Magic 두 과제에서 과제·방법별 30회 시행; cross-embodiment policy는 과제별 policy–embodiment 조합당 50회 실행한다.

**출처:** [논문 본문](https://arxiv.org/html/2611.23143v1)의 초록 및 1–5절. [프로젝트](https://livioni.github.io/TCP4D/).
