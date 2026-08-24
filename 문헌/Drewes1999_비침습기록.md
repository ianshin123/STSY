# Drewes 1999 — 자유롭게 움직이는 빈모류에서 비침습 기록

서지: Drewes CD · "Non-invasive Recording of Giant Nerve Fiber Action Potentials from
Freely Moving Oligochaetes" · *Tested Studies for Laboratory Teaching* (ABLE) · 20:45–62 · 1999
접근: **무료 PDF** | 원문: `원문/Drewes1999_비침습기록.pdf` ✅ **확보·확인 완료**
URL: https://www.ableweb.org/biologylabs/wp-content/uploads/volumes/vol-20/2-drewes.pdf

> ## ⚠ 이 논문의 실험체는 지렁이가 아니다
>
> 원문 확인 결과 실험 대상은 ***Lumbriculus variegatus*** (California blackworm,
> **담수 빈모류**)다. *Lumbricus terrestris* 가 아니다.
> 제목의 "Oligochaetes"가 그 뜻이다 — 초안이 "지렁이"로 잘못 읽었다.
>
> 원리(굵은 축삭 · 얇은 체벽)와 장비 사양은 그대로 가져올 수 있으나,
> **속도값이나 신호 크기를 *L. terrestris* 로 옮길 때는 종이 다르다는 것을 명시해야 한다.**

---

## 이 논문이 한 것 (원문 확인)

해부 · 마취 · 구속 없이 거대섬유 스파이크를 기록한다.

> "electrical recordings of giant fiber spikes may be made **without dissecting,
> anesthetizing or restraining worms**."

### 비침습이 가능한 이유 — 두 가지 (직접 인용)

> "**Two factors make this possible.** First, giant fiber spikes produce **large electrical
> currents due to their large diameter**. Second, these currents easily pass through the
> worm's body wall and skin because **these tissues have a low resistance** to electrical
> current flow."

### 장비 (Materials 절)

| 항목 | 값 |
|---|---|
| 전극 | **인쇄회로기판 기록 그리드** (Iowa State University에서 실비 공급) |
| 전치증폭기 | 2대 · **capacity-coupled, differential inputs** · ×100 및 ×1000 |
| 전원 | **±9 V DC 배터리팩** (또는 ±15 V DC 전원공급기) |
| 오디오 모니터 | Grass AM7 · **저역 300 Hz · 고역 3 kHz** · noise clipper ON |
| 오실로스코프 | **Tektronix TDS 210 디지털 스토리지** ($995) |
| 패러데이 케이지 | 알루미늄 호일을 안에 댄 접이식 골판지 상자 |
| 스위프 속도 | 2.5 ms/div |

**전원공급기를 쓸 경우 반드시 패러데이 상자 밖에 둔다** — 60 Hz 유입 방지.

### 오실로스코프 요구 사양 (직접 인용) ★

> "**Non-storage oscilloscopes are not well suited for this exercise** because they provide
> no means for capture and fixed display of transient, touch-evoked spikes."

> "At a sweep speed of 2 msec/division, **a minimum of 12 digital sampling points/msec/channel**
> (i.e., one sample point per 0.08 msec) is needed for spike analysis, along with a
> **total capture time of at least 20 msec/channel**. … it is imperative that the recording
> system have **internal triggering capabilities**."

**즉 필요조건은 ① 디지털 스토리지 ② 12 kHz/채널 이상 ③ 채널당 20 ms 이상 캡처
④ 내부 트리거 기능.**

### 단발 자극과 근수축 (직접 인용)

> "it works best if the Widgeteer touches the worm **so lightly that just one spike (pop)
> occurs**, rather than a burst of spikes. Bursts of spikes may cause the worm to rapidly
> shorten and crawl away… **When just one spike is evoked by very light touch,
> no body shortening occurs.**"

### 파형 검증 요령

> "The spike should have **the same polarity sequence in both traces** and should be
> **detected first by the electrode pair closest to the point of touch**."

우리 4채널 판별 논리와 같은 검사다.

---

## 우리가 가져오는 것

| 가져오는 것 | 우리 적용 |
|---|---|
| 비침습 기록의 이론적 정당화 | 연구 전체의 전제 → [`../정리/세포외기록_원리.md`](../정리/세포외기록_원리.md) |
| **±9 V 배터리 구성** | 전원 설계 → [`../장치/증폭기/회로설계.md`](../장치/증폭기/회로설계.md) |
| **디지털 스토리지 + 12 kHz + 20 ms + 내부 트리거** | 학교 스코프 확인 조건 |
| 통과대역 300 Hz – 3 kHz | 우리 339–3390 Hz와 일치 |
| 패러데이 케이지 = 호일 댄 골판지 상자 | 단계 0 구성 그대로 |
| **단발 자극 → 근수축 없음** | 근전위 5중 방어의 2번 |
| 극성 순서 · 도달 순서 검증 | 스파이크 진위 판별 |

---

## 이 논문이 말하지 않은 것 ★

- **중금속에 대해 말하지 않는다.**
- ***Lumbricus terrestris* 를 쓰지 않았다.** *Lumbriculus variegatus* 다 (위 경고 참조).
- **"표면 신호 0.1 mV 이하"라는 문장을 찾지 못했다.**
  초안이 이 논문에 귀속시켰던 수치인데 **본문에서 확인되지 않는다.**
  Yoshida 2009의 30 µV가 우리가 가진 유일한 실측 진폭이다.
- **"MGF 2개 이상 / LGF 3개 이상부터 수축"이라는 숫자는 이 논문에 없다.**
  있는 것은 "**단발이면 수축 없음, 버스트면 수축**"뿐이다.
  초안의 구체적 개수는 **출처 미상**이므로 그렇게 표기해야 한다.
- **전극 간 거리 d를 고정하는 방법을 다루지 않는다.** 자유 이동이라 d가 시행마다 달라진다.
  **우리가 챔버를 쓰는 이유가 이것이다.**
- **정량적 검출 한계나 반복 측정 변동을 제시하지 않는다.** 교육용 실습 논문이다.
- **채널 간 시간정렬** 문제를 다루지 않는다.

---

링크: [`../정리/세포외기록_원리.md`](../정리/세포외기록_원리.md) ·
[`../문헌/색인.md`](../문헌/색인.md) ·
[`../장치/증폭기/회로설계.md`](../장치/증폭기/회로설계.md)
