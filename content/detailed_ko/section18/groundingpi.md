### GroundingPI

**전체 제목:** GroundingPI: A Grounding Foundation Model towards Physical Intelligence with Visual Primitives

**저자:** Qize Yu 외

**학회/연도:** — / 2026

**arXiv:** [2609.39601v1](https://arxiv.org/abs/2609.39601v1)

**아키텍처:** MoonViT-V2 시각 인코더와 Qwen3-4B 언어 디코더를 결합한 4B grounding 파운데이션 모델. 점과 bounding box를 공유 어휘의 양자화 좌표 토큰으로 생성함.

**핵심 방법론:** 다중 모달·공간 사전학습, 지도 미세조정(SFT), GRPO로 정밀 지각을 학습함. 조작에서는 중간 특징을 Action DiT의 각 층 cross-attention에 주입함. 각 benchmark의 백본 비교에서 행동 expert, 행동 데이터, 학습 예산, 행동 표현, 추론 절차를 고정함.

**로봇 / 과제:** RoboTwin 2.0은 고정 베이스 양손 테이블탑 조작을 평가함. RoboCasa-GR1은 humanoid dexterous-hand 조작을 평가함. nuScenes는 open-loop 주행 궤적 예측을 평가함.

**주요 기여:**
- 생성형 좌표 grounding을 폭넓은 지각 사전학습과 행동 학습 전이로 확장함.
- 장면·개체 변화에 대한 OOD 조작 4개 설정 모두에서 1위를 기록함.
- RoboCasa-GR1에서 시연의 50%로 학습하여 75%로 학습한 비교 백본들을 능가함.

**정량적 결과:**

| Benchmark / 과제 | 지표 | 값 | 조건 |
|---|---|---|---|
| RoboTwin2.0 Full | 과제 성공률 | 66.20% | 동일 downstream 구조·학습 조건 |
| RoboTwin2.0-Clean2Random | 과제 성공률 | 17.60% | Rex-Omni: 14.10%; Clean 학습 후 Randomized 장면 평가 |
| RoboCasa-GR1 Full | 과제 성공률 | 37.75% | RynnBrain: 39.00%; ID 평가 |
| nuScenes | 평균 open-loop L2 오차 | 0.296 m | 궤적 예측; 폐루프 성능은 입증하지 않음 |

**연구 점수:** 제공된 `verification.mean_scores`를 사용함. 근거는 제공된 평가를 요약함.

| 항목 | 점수 | 근거 |
|---|---|---|
| 중요도 (importance) | 8.0 | 정밀 지각은 희소한 행동 데이터의 부담을 줄일 수 있음. 보고된 평가를 넘어선 실제 효과는 불확실함. |
| 추가 기여 (delta_contribution) | 7.0 | 폭넓은 지각 사전학습과 행동 전이가 기존 grounding 모델을 확장함. 양자화 좌표 생성은 기존 방식임. |
| 방법 품질 (method_quality) | 8.0 | GRPO가 위치·누락·중복을 다루며 Action DiT를 고정해 비교함. 백본 구조·사전학습 차이는 남음. |
| 효과성 (effectiveness) | 7.0 | OOD 조작 4개 설정 모두 선두임. Clean2Random 성공률은 낮고 주행 개선은 작음. |
| 공백 해소 근거 (gap_support) | 7.3 | Grounding과 통제된 행동 전이가 지각 병목 주장을 지지함. Open-loop 주행으로 폐루프 성능을 입증하지는 않음. |

**종합 점수:** 7.4. 제공된 `verification.overall`을 사용함.

**한계점:**
- RoboCasa-GR1 Full 성공률은 RynnBrain보다 낮으며 Clean2Random 성공률도 낮음.
- nuScenes 결과는 폐루프 성능, 지연시간, 표지판 읽기의 개별 효과를 입증하지 않음.
- 백본 구조와 사전학습이 달라 grounding 학습 자체의 기여를 완전히 분리할 수 없음.
- VisDrone은 여전히 어려우며 일부 공간·GUI benchmark에서는 GPT-6 Astra가 우세함.

**공개 가중치/코드:** — / — (제공된 출처에 보고되지 않음).

## 추론 / 배포

- **추론 지연 시간:** —
- **배포 하드웨어:** —

## 데이터셋 / 데이터 수집

- **훈련 데이터:** 공개 데이터셋과 다중 teacher·과제별 검증을 사용하는 전용 데이터 엔진.
- **평가 데이터:** RoboTwin 2.0, RoboCasa-GR1, nuScenes 및 11개 지각 능력을 다루는 34개 grounding benchmark.

**출처:** [제공된 논문 본문](https://arxiv.org/html/2609.39601v1)의 3–5.2.2절. 연구 점수는 제공된 verification을 사용함.
