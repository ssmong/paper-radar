### Ropedia W0

**전체 제목:** Ropedia W0: Scaling Loco-Manipulation World Models across Embodiments with Human Experience

**저자:** Tianqi Liu 외

**학회/연도:** — / 2026

**arXiv:** [2610.26855v1](https://arxiv.org/abs/2610.26855v1)

**아키텍처:** 영상 diffusion transformer가 초기 이미지, 텍스트, 카메라 자세, 투영된 조작기 skeleton을 조건으로 미래 1인칭 프레임을 예측함. 카메라 자세는 이동을 나타내며 skeleton은 인간 또는 로봇 조작기의 고유 구조를 유지함.

**핵심 방법론:** Xp-Data로 인간 사전학습 후 인간·로봇 혼합 학습을 수행하며 같은 카메라·skeleton 인터페이스를 사용함. 로봇 skeleton은 사용 가능한 순기구학과 광범위한 수동 keypoint 주석·보정을 결합함. 증류로 장기 영상 생성과 실시간 VR 상호작용을 위한 인과적 생성기를 만듦.

**로봇 / 과제:** 인간, gripper 로봇, dexterous humanoid의 이동·조작 영상 예측. DreamDojo, Ψ0, ω-HOME, Xp-Teleop, AgiBot과 학습에 사용하지 않은 인간 영상으로 평가함. Xp-Teleop은 6자유도 dexterous hand 두 개를 장착한 Unitree G1을 사용함.

**주요 기여:**

- 공통 카메라·skeleton 인터페이스로 인간과 로봇의 동작을 함께 학습함.
- 통합 다중모달 주석이 있는 인간 영상 약 10,000시간과 로봇 영상 약 3,000시간으로 Xp-Data를 구축함.
- 장기 humanoid 이동·dexterous 조작 평가용 Xp-Teleop을 추가함. 인간 사전학습 데이터 증가가 인간·로봇 예측을 개선함.

**정량적 결과:**

| Benchmark / 과제 | 지표 | 값 | 조건 |
|---|---|---|---|
| EgoSuite + OpenAoE 인간 영상 예측 | 절대 궤적 오차 | 1.542 cm | A14B 인간 사전학습 모델; 미학습 영상 200개; Cosmos3-Nano 16B: 1.931 cm |
| DreamDojo In-lab 영상 예측 | PSNR | 20.854 dB | Ropedia W0 5B; post-training 데이터 1%; DreamDojo 14B: 18.983 dB |
| Ψ0 dexterous humanoid 영상 예측 | PSNR | 19.07 dB | A14B 혼합 학습 모델; 전체 데이터 post-training; Cosmos3-Nano 16B: 16.55 dB |

**AI 연구 평가:** 세 검토자의 평균 점수, 10점 척도.

| 항목 | 점수 /10 | 근거 |
|---|---|---|
| 중요도 | 8.0 | 인간 경험 재사용은 고비용 로봇 데이터 수집과 적응 부담을 줄일 수 있음. 실제 의사결정에 대한 효과의 크기는 불확실함. |
| 추가 기여 | 8.0 | 공통 카메라·skeleton 인터페이스와 통합 데이터로 embodiment 간 전이를 확장함. 렌더링 조건은 선행연구에도 있음. |
| 방법 품질 | 8.0 | 카메라와 조작기 조건을 분리해 이질적 행동 공간을 연결함. 정확한 로봇 skeleton에 광범위한 수동 보정이 필요함. |
| 효과성 | 7.0 | 인간 동작 추종과 저자료 로봇 예측이 전이를 지지함. 상세 결과는 계획·제어보다 영상 품질을 주로 측정함. |
| 공백 해소 근거 | 7.0 | 여러 embodiment의 예측이 이동·조작 통합 모델링을 부분적으로 지지함. Zero-shot 평가가 미학습 embodiment로의 전이를 입증하지는 않음. |

**종합 점수:** 7.6/10.

**한계점:**

- 로봇 skeleton의 부정확한 투영을 보정하기 위해 광범위한 수동 주석 작업이 필요함.
- Zero-shot은 평가 데이터셋을 학습에 사용하지 않았다는 뜻임. 같은 embodiment가 다른 학습 데이터에 포함될 수 있음.
- 상세 수치 근거는 영상 품질과 동작 추종에 집중함. 계획·제어 효과의 크기는 불확실함.
- Xp-Teleop은 하나의 humanoid 플랫폼에서 수집한 장기 시연 27개, 약 한 시간을 다룸.

**공개 가중치/코드:** — / —.

## 추론 / 배포

- **추론 지연 시간:** —. 증류 모델은 640×480 해상도에서 초당 21.3프레임을 생성하며 분 단위 상호작용 영상을 지원함.
- **배포 하드웨어:** —.

## 데이터셋 / 데이터 수집

- **훈련 데이터:** Xp-Data는 인간 영상 약 10,000시간과 로봇 영상 약 3,000시간으로 구성됨. 공개 인간 데이터셋 14개, 공개 로봇 데이터셋 13개, 자체 수집 인간 영상을 포함함.
- **평가 데이터:** 로봇 benchmark 5개와 EgoSuite·OpenAoE의 미학습 인간 영상 200개. Xp-Teleop은 시연 27개에 30개 기술 유형의 수동 주석 원자 행동 구간 543개를 포함함.

**출처:** [논문 본문](https://arxiv.org/html/2610.26855v1)의 3–6.2절; [프로젝트](https://ropedia.github.io/ropedia-w0/).
