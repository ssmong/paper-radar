# 10.12 HALO

- **전체 제목:** HALO: Human-Aligned Data Collection for WhoLe-body MObile Manipulation
- **저자:** Shuai Yang, Fangyi Xu, Yishu Shen, Kecheng Zheng, Yinghao Xu (HKUST / Robbyant)
- **학회/연도:** arXiv preprint, 2026년 11월
- **arXiv:** [2611.16439v1](https://arxiv.org/abs/2611.16439v1)
- **입력 모달리티:** 직접 교시와 저저항 수동 플랫폼에서의 자연스러운 조작자 이동
- **대상 hand:** 재설계한 양팔 gripper
- **Force feedback:** 직접 교시를 통한 물리적 힘 피드백
- **비용:** —

## 핵심 방법론/설계

조작자는 로봇의 말단장치를 직접 움직이고 수동 플랫폼을 이동시키며 양팔 조작을 시연한다. 수집 중에는 구동 베이스를 제거한다. 플랫폼은 배포에 사용하는 AgileX Tracer AGV 2 차동 구동 베이스의 비홀로노믹 운동 제약을 유지한다.

CaRE-Ego, SAM2, DiffuEraser로 기록 영상에서 시연자의 손을 분할·추적·제거한다. 베이스 속도를 보정하고 응답 지연에 맞춰 시간을 정렬하여 플랫폼 움직임을 배포 명령에 맞춘다. 처리한 시연으로 π0.5 policy를 fine-tuning하고, 비동기 real-time action chunking (RTC)으로 실행한다.

## 주요 contribution

- 직접 조작에 따른 힘 피드백과 자연스러운 이동을 결합하여 전신 시연을 수집한다.
- 영상과 베이스 동작을 처리하여 수집과 자율 실행 사이의 gap을 줄인다.
- Mobile ALOHA 및 VR teleoperation과 수집 효율 및 학습한 policy를 비교한다.

## 정량 결과

과제마다 초기화와 물체 준비를 포함한 수집 시간을 1시간으로 제한한다. 수집 비교는 평가 대상 인터페이스에 사전 경험이 없는 조작자 한 명으로 수행한다.

| 과제 / 조건 | 지표 | 결과 | 맥락 |
|---|---|---|---|
| Push Chair 시연 수집 | 수집 속도 향상 | 2.9× | 동일한 수집 조건에서 Mobile ALOHA와 비교 |
| Disassemble Lego | Policy 성공률 | 75.0% | 30/40 trials |
| 6단계 이동 상자 조작 | Policy 성공률 | 73.3% | 11/15 trials |
| Zip-Tie Fastening | Succ. Rate | 30.0% | 10 trials |
| Push Chair 손 제거 ablation | Success Rate | 55% → 85% | 동일 시연, 비동기 추론, execution horizon 8 |

## AI 연구 평가

AI 검토자 세 명의 평균 점수이며, 10점 척도를 사용한다.

| 항목 | 점수 | 근거 |
|---|---|---|
| 중요도 | 8.0 | 이동과 양팔 조작을 함께 담는 시연 수집 문제를 다룬다. 평가한 과제와 플랫폼 밖에서의 효과는 불확실하다. |
| 추가 contribution | 7.0 | 분리된 leader–follower 제어를 직접 교시와 수동 플랫폼으로 바꾼다. Policy와 영상 처리는 기존 방법을 사용한다. |
| 방법의 타당성 | 7.7 | 운동 제약을 맞추고 시각·제어 차이를 보정한다. 베이스 보정만의 효과는 분리하여 검증하지 않았다. |
| 효과성 | 6.7 | Policy 결과와 손 제거 ablation이 실용성을 뒷받침한다. Zip-Tie Fastening 성공률은 10 trials에서 30.0%에 그친다. |
| Gap 해소 근거 | 7.0 | 동일한 수집 조건의 비교와 시각 처리 ablation이 정렬 효과를 뒷받침한다. 조작자가 한 명이므로 사용자 전반의 효과는 불확실하다. |

**종합 점수:** 7.2/10.

## 한계점

- 수집 효율 비교는 조작자 한 명으로 수행하여 조작자 간 일반화는 검증하지 않았다.
- Zip-Tie Fastening 성공률은 10 trials에서 30.0%이다. Sub-millimeter 정확도는 과제 요구사항이며, 별도로 측정한 정확도 결과가 아니다.
- 하드웨어 평가는 하나의 차동 구동 베이스와 운동 제약을 맞춘 플랫폼에 한정된다.
- Push Chair 수집 중 목표 테이블은 고정되어 있다. Active perception은 향후 연구로 제시한다.

## 데이터 품질 영향

손 제거는 시연과 자율 실행 사이의 시각적 gap을 줄인다. 베이스 보정과 시간 정렬은 수동 플랫폼에서의 수집과 구동 베이스에서의 배포 사이의 차이를 처리한다. Push Chair ablation은 손 제거의 효과를 뒷받침하지만, 베이스 보정만의 효과는 분리하여 검증하지 않았다.

## 오픈소스 현황

코드 / weights: — / — (보고되지 않음). [프로젝트 페이지](https://robbyant-research.github.io/Lingbot-ALOHA/).

**출처:** [논문 본문](https://arxiv.org/html/2611.16439v1), 3–5절 및 부록 B.
