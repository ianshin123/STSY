# Bähring & Bauer 2014 — 마취 없이 재는 챔버

서지: Bähring R, Bauer CK · "Easy method to examine single nerve fiber excitability and
conduction parameters using intact nonanesthetized earthworms" ·
*Advances in Physiology Education* · 38:253–264 · 2014
접근: **무료 전문 (PMC)** | 원문: `원문/Bahring2014_비마취챔버_PMC전문.html` ✅ **확보·확인 완료**
URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC4154267/

형식 주의: 출판사 PDF가 아니라 **PMC 전문 HTML**이다. 본문·표는 있으나 **그림은 없다.**

> ## ★ 부록 `suppdata.zip` (39.8 MB) 미확보 — 챔버 제작 도면이 여기 있다
>
> PMC가 프루프오브워크를 요구해 자동 내려받기가 안 된다. **브라우저로 받아야 한다.**
> 직접 링크: `https://pmc.ncbi.nlm.nih.gov/articles/instance/4154267/bin/suppdata.zip`
> (기사 페이지 https://pmc.ncbi.nlm.nih.gov/articles/PMC4154267/ 하단 "Supplementary Materials")
>
> **단계 2 챔버 제작에 직접 필요하다.**

**종이 *Lumbricus terrestris* 로 우리와 일치한다.**

---

## 이 논문이 한 것 (원문 확인)

Hamburg 의대 1학년 실습. **마취하지 않은 온전한 지렁이**에서 MGF 단일 활동전위를
비침습으로 유발·기록하고, **역치–자극지속시간 관계**(rheobase · chronaxie)를 재게 한다.

### 챔버 (직접 인용)

> "the nonanesthetized earthworm **enters completely unforced**. The worm resides in a
> **narrow round duct with silver electrodes on the bottom** such that individual APs of the
> MGF can be elicited and recorded superficially."

> "The earthworm chamber designed for this activity has **four different pairs of silver
> electrodes (and two electrodes for grounding)**; **two central pairs of recording electrodes
> are routinely used**… the electrode pair on the left is connected to the stimulator together
> with a grounding electrode."

전극 구성은 **기록 4쌍 + 접지 2개**다(초안은 접지를 빠뜨렸다).
앞끝이 왼쪽, 왼쪽 쌍이 자극용 — MGF가 앞→뒤로 달린다.

### 왜 챔버를 만들었나 (직접 인용)

> "We used the Heinzel recording method for several years, but with nonanesthetized
> earthworms. Our experiments were frequently unsuccessful (**~30% failure rate**) due to one
> main problem: when forced into a narrow enclosure… the worm may **vigorously twist and turn**…
> Also, due to the applied force, **often the ventral side of the worm may not face the
> electrodes**."

**즉 비마취의 진짜 난점은 자세(배쪽이 전극을 향하는가)이지 움직임 자체가 아니다.**

### 결과 (Table 1) ★★ 숫자를 정확히 읽어야 한다

| 항목 | 값 | n |
|---|---|---|
| 0.1 ms 자극에서의 역치 | **1.49 ± 0.08 V** (범위 0.6 – 4 V) | 74 |
| **전도속도 (실온)** | **30.2 ± 0.7 m/s** | **74** |
| Rheobase | 1.012 ± 0.052 V | 64 |
| Chronaxie | 0.060 ± 0.005 ms | 64 |

> "pooled data are given as **means ± SE unless stated otherwise**.
> **The number of observations (n) refers to the number of trials and not to the number of worms.**"

> "the calculated values for the conduction velocity ranged between **as low as 10.3 m/s and
> as high as 54.8 m/s** with a mean value of 30.2 ± 0.7 m/s (n = 74)."

> ### ⚠ 30.2 ± 0.7 의 0.7 은 **SD가 아니라 SE**다
>
> n = 74 이므로 **SD = 0.7 × √74 ≈ 6.0 m/s → 변동계수 약 20 %.**
> 그리고 **실측 범위가 10.3 – 54.8 m/s 로 5배 넘게 벌어진다.**
>
> **이것이 이 저장소에서 우리 SD_rep 목표(≤ 3 %)와 가장 직접 비교되는 공개 숫자다.**
> → [`../정리/통계_검출력.md`](../정리/통계_검출력.md)

### 측정 방법

- 전도속도 = **채널 1·2의 첫 번째 음의 정점 사이 잠복기 차 Δt** 와 **실측 전극 거리 Δs**
  → 우리 규약과 같다
- 자극 지속시간을 **1 ms → 0.5 → 0.2 → 0.1 → 0.08 → 0.06 → 0.04 → 0.02 ms** 로 줄여가며 역치 탐색
  (긴 쪽부터 시작하는 것이 빠르다)
- **모든 실험을 실온에서 수행했다** — 온도를 통제하지 않았다
- 한 개체가 길면 **다른 기록 지점에서 한 번 더 반복**했다

### 근육 전위 문제 (직접 인용)

> "Usually, in both recording channels, the **first biphasic AP was followed by a second AP,
> presumably fired by a motor neuron** and, frequently, a **third voltage deflection indicated
> summed muscle potentials**."

우리 근전위 5중 방어의 근거가 여기서 실측으로 확인된다.

---

## 우리가 가져오는 것

| 가져오는 것 | 우리 적용 |
|---|---|
| **자발 진입 · 비마취 · 비침습 챔버** | 단계 2 → [`../장치/챔버/설계.md`](../장치/챔버/설계.md) |
| 은전극 · 바닥 배치 · 반원 덕트 | 챔버 설계 |
| **비마취 기준선 30.2 m/s** | 단계 2 기준값 |
| **첫 음의 정점 기준 Δt** | 분석 규약 |
| 0.1 ms 펄스 · 역치 약 1.5 V | 단계 2 자극 파라미터의 출발점 |
| **자세(배쪽 방향)가 실패의 주원인** | 챔버 홈 폭 설계의 진짜 목적 |
| 근전위가 3번째 편향으로 따라온다 | 파형 해석 |

---

## 이 논문이 말하지 않은 것 ★

- **중금속·독성물질에 대해 아무것도 말하지 않는다.** 교육용 실습 장치 논문이다.
- **같은 개체를 며칠에 걸쳐 반복 측정하지 않았다.**
  n은 **시행 수이지 개체 수가 아니고**, 실습은 단회 세션이다.
  **"7일 반복 측정해도 죽지 않는다"는 이 논문이 보증한 사실이 아니라
  우리가 단계 2에서 직접 확인해야 할 가정이다.**
- **반복 측정 변동(SD_rep)을 보고하지 않는다.** ±0.7은 시행 전체의 SE다.
- **온도를 통제하지 않았다.** "room temperature"라고만 쓴다.
- **챔버 재료를 논하지 않는다**(아크릴 커버 언급뿐). **우리 PETG 선택은 이 논문이 아니라
  재료 물성에서 나온 독자 판단이다.**
- **LGF를 다루지 않는다.** MGF 전용 설계다.
- 챔버 치수는 본문에 없고 **부록 도면에 있다** — 미확보.

## 확보 시 확인할 것

1. **`suppdata.zip` 제작 도면** — 최우선 (위 링크)
2. Fig. 3의 챔버 치수 — 덕트 지름 · 전극 간격
3. Fig. 4D 전도속도 분포 히스토그램의 모양 (10.3–54.8 범위가 어떻게 퍼져 있나)
4. 실온이 몇 도였는지

---

링크: [`../정리/마취와_구속법.md`](../정리/마취와_구속법.md) ·
[`../정리/지렁이_전극연구.md`](../정리/지렁이_전극연구.md) ·
[`../정리/통계_검출력.md`](../정리/통계_검출력.md) ·
[`../장치/챔버/설계.md`](../장치/챔버/설계.md)
