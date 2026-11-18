## 3.21 ForceHarness

- **전체 제목:** ForceHarness: Turning Force into Action and Physics for Frozen Frontier Models
- **저자:** Ke Sun, Kevin Yuchen Ma, Yike Zhang, Yanzhe Chen, Mike Zheng Shou
- **연구 그룹:** Show Lab, National University of Singapore
- **학회/연도:** arXiv preprint, 2026
- **arXiv:** [2611.21099v1](https://arxiv.org/abs/2611.21099v1)

**힘/촉각 입력 유형:** 손목 F/T 센서 또는 외부 관절 토크로부터 보정된 힘을 얻는다. 실제 로봇에서는 손목 F/T 센서 없이 관절 토크를 사용한다.

**힘/임피던스 출력:** 모델이 force primitive와 매개변수를 선택한다. 각 primitive는 목표 자세와 로봇의 기존 임피던스 제어기를 통해 힘을 조절한다. 모델의 하위 계층에서 능동적인 힘 제어를 수행한다.

**로봇 플랫폼:** 평행 gripper, 손목 RGB-D 카메라, 외부 RGB 카메라를 갖춘 Franka FR3.

**과제:** 실제 과제는 화이트보드 닦기, 나사 조이기, 가지 껍질 벗기기, USB 삽입, 병의 무게별 분류, 부드러운 물체와 단단한 물체 구분의 6개다. 시뮬레이션에서는 ForceBench 과제 8개와 HiddenPhys 과제 7개를 사용한다.

**핵심 방법론:** 세 계층이 시연이나 fine-tuning 없이 frozen model과 로봇을 연결한다. 힘 보정 계층은 영점 오차를 제거하고 정지 상태에서 측정한다. 자체 종료 force primitive는 admittance control을 사용하며 접촉 사건, 목표 달성, 힘 상한 또는 시간 제한에 따라 종료된다. 물리량 변환 계층은 각 힘 기록에서 물리량, 불확실성 추정치, 상태 정보를 반환한다. 모델은 결과를 읽고 다음 동작을 선택한다.

**아키텍처/파라미터:** API로만 접근하는 frozen model이 힘 제어 루프의 상위에서 도구를 호출한다. force primitive 12개와 기타 도구 10개로 구성된다. 모델 내부 구조와 파라미터 수: —.

**주요 contribution:**

- 모델 학습 없이 힘 보정, 자체 종료 제어, 물리량 피드백을 결합한다.
- 숨겨진 물리 변수를 포함하는 MuJoCo benchmark인 HiddenPhys를 제시한다. 과제 7개, 전문가 힘 제어기, 학습된 policy를 포함한다.
- 손목 F/T 센서가 없는 실제 로봇 팔과 시뮬레이션 benchmark 2개에서 평가한다.

**정량적 결과:** ForceHarness를 사용하는 GPT-6 Astra와 힘을 사용하지 않는 동일 모델을 비교한다.

| Benchmark / 과제 | 지표 | 힘 미사용 | ForceHarness | 조건 |
|---|---|---|---|---|
| Franka FR3, 과제 6개 | Success rate | 3.3% (2/60) | 90.0% (54/60) | 동일 지시문; 과제별·조건별 10회 |
| ForceBench, 과제 8개 | Mean success rate | 70.0% | 87.5% | 첫 10개 seed 사용; 이 중 8개에서 도구와 임계값 조정 |
| HiddenPhys, 과제 7개 | Successful episodes | 87/140 | 135/140 | 과제별 동일한 test seed 20개; ForceHarness의 손잡이 손상은 0회 |

**AI 연구 평가:** AI 검토자 3명의 평균 점수이며, 10점 척도를 사용한다.

| 항목 | 점수 /10 | 근거 |
|---|---|---|
| 중요도 | 8.0 | fine-tuning 없이 frozen model을 접촉 제어에 연결하고 손목 센서 없는 실제 로봇에서도 작동한다. 모델 호출 지연은 빠른 협응을 제한한다. |
| 추가 contribution | 7.0 | 원시 힘 값 전달이나 제어 코드 생성을 넘어 힘 제어와 보정된 물리량 피드백을 통합한다. 구성요소는 기존 방법에 기반하며 FORCA와의 직접 비교는 보고되지 않았다. |
| 방법 품질 | 8.0 | 빠른 접촉 제어와 느린 모델 판단을 분리한다. 피드백 ablation이 설계를 뒷받침하지만 시뮬레이션에 한정된다. |
| 효과성 | 7.7 | 실제 로봇과 HiddenPhys 비교에서 뚜렷한 개선을 보인다. ForceBench 평가 seed를 사용한 조정과 학습 baseline의 평가 조건 차이는 일반화 해석을 제한한다. |
| gap 해소 근거 | 7.3 | 성공 결과와 ablation은 학습 없는 힘 활용을 뒷받침한다. 물리량 피드백의 효과는 모델에 따라 다르며 빠른 반응적 협응은 해결되지 않았다. |

**종합 점수:** 7.6/10.

**한계점/gap:**

- primitive 사이의 모델 호출에 수초가 걸린다. 고정된 primitive 목록은 새로운 운동 법칙과 반응적 협응을 제한한다.
- ablation은 시뮬레이션에서만 수행했다. 실제 로봇 평가는 과제별·조건별 10회다.
- ForceBench 평가 seed 10개 중 8개에서 도구와 지각 임계값을 조정했다. Stove Press와 Nut Thread는 초기 실행 뒤 수정했다. 일부 공개 성공 판정은 물체 놓기나 충분한 이격을 확인하지 않는다.
- ForceBench의 학습 baseline 결과는 재현하지 않고 인용했다. 시연, 입력, 지시문, 평가 횟수가 다르므로 성능 gap을 힘의 효과만으로 해석할 수 없다.
- HiddenPhys는 frozen model에 이미지 대신 잡음이 포함된 물체 자세를 제공한다. OOD 변화에서는 frozen model에만 변경된 범위의 지시문을 제공한다.
- 물리량 피드백은 작은 모델에 더 도움이 된다. GPT-6.1 Sol은 원시 힘 값으로도 좋은 성능을 보인다.

**공개 가중치/코드:** — / —.

## 추론 / 배포

- **추론 지연 시간:** 모델 판단에 수초가 걸린다. 정확한 지연 시간: —.
- **배포 하드웨어:** 위에 명시한 Franka FR3와 카메라. 연산 하드웨어: —.
- **실시간 가능 여부:** primitive가 모델의 하위 계층에서 접촉을 제어한다. 모델 호출 때문에 primitive 사이의 빠른 반응적 협응은 어렵다.

## 데이터셋 / 데이터 수집

- **학습 데이터:** ForceHarness는 시연이나 fine-tuning이 필요 없다. HiddenPhys의 학습 baseline은 과제별 약 200개 시연을 사용한다.
- **평가 데이터:** 실제 과제 6개, ForceBench 과제 8개, 숨겨진 물리 변수를 포함하는 HiddenPhys 과제 7개.
- **데이터 형식 / 공개 여부:** — / —.

**출처:** [논문 본문](https://arxiv.org/html/2611.21099v1), 1–5절과 한계점.
