# Shannon 등 — 사운드카드로 전도속도 재기

서지: Shannon KM, Gage GJ, Jankovic A, Wilson WJ, Marzullo TC ·
"Portable conduction velocity experiments using earthworms for the college and high school
neuroscience teaching laboratory" ·
*Advances in Physiology Education* · 38(1):62–70 · 2014
접근: **무료 전문 (PMC)** | 원문: [`원문/Shannon_휴대형전도속도_PMC전문.html`](원문/Shannon_휴대형전도속도_PMC전문.html) ✅ **확보·확인 완료**
URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC4116350/

형식 주의: **PMC 전문 HTML**이다. 그림은 없다.
초안의 불완전한 서지(저자·연도 미상)는 이것으로 채웠다.
**Marzullo가 공저자다** — SpikerBox 논문과 같은 계보.

---

## 이 논문이 한 것 (원문 확인)

**SpikerBox 2채널 + 노트북 사운드카드 + Audacity**만으로 전도속도를 측정.

### 마취 (직접 인용) ★

> "**All experiments in this report were performed on worms under a 10% by volume ethanol
> anesthetic solution.** The 10% ethanol solution was prepared by mixing 30 ml of tap water
> with 10 ml of 80 proof (40% ethanol) vodka. We placed the earthworms in the alcohol
> anesthetic for ~5 min…"

> "**Carbonated water can also be used as an anesthetic if ethanol is not available.**
> Carbonated water (60%) can be prepared by mixing **30 ml of sugar-free seltzer water**
> (also called "club soda" or "sparkling water" at grocery stores) **with 20 ml of tap water**."

> "The typical time in the **alcohol or carbonated water** solution for sufficient anesthesia
> is ∼5 min."

**즉 시간은 두 마취제가 같다고 적혀 있다.** 다만 아래 경고를 함께 본다.

### ★ 절차에서 빠뜨리기 쉬운 두 줄 (원문 · 2026-08-29 확인)

> "We placed the earthworms in the alcohol anesthetic for ∼5 min, **briefly rinsed them off in
> tap water**, and then began the experiments."

> "**The effects of the anesthetic typically last 5–10 min.**"

> "It is important to **not leave the worms in the anesthetic solution excessively**,
> as the worms **will not produce action potentials** and can also perish."

**헹구지 않으면 몸에 남은 마취제가 계속 작용한다.** 헹군 뒤 **5–10분**이 실험 창이다.
**과마취하면 활동전위가 아예 안 나온다** — 같은 경고가
[`Kladt2010_프로토콜9종.md`](Kladt2010_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C9%EC%A2%85.md)에도 있다
(«muscles and skin sensory cells are inactive, but the giant fibers … are still responding»).

**10 % 에탄올 조제법도 원문에 있다**: 수돗물 30 ml + **80 proof(40 %) 보드카 10 ml** = 40 ml
→ 에탄올 4 ml / 40 ml = 10 % v/v.

마취 확인법: **탐침으로 머리·꼬리를 건드려 도피반사(수축)가 사라지면 된 것.**

> ### ⚠ 보고된 속도값은 **에탄올** 마취 조건이다
> 탄산수는 "에탄올이 없을 때의 대안"으로 제시됐을 뿐,
> **탄산수 조건에서 잰 속도는 이 논문에 없다.**
> **"탄산수가 에탄올과 비슷하다"는 근거 없는 가정이다.**

### 결과 (직접 인용) ★★

> "**seven worms.** In each worm, we took **five measurements** from different spikes in both
> the LGF and MGF… **Across all worms**, the average speed of the LGF was **7.6 ± 1.2 m/s
> (mean ± SD)** and the MGF was **22.8 ± 4.5 m/s (mean ± SD)**."

> ### ✅ ± 4.5 m/s 는 **개체 간(across worms) SD** 다
> 같은 개체 반복 측정의 SD가 아니다.
> **우리 개체 내 전후 비교 설계가 이 변동을 상쇄한다** — 열려 있던 위험 하나가 닫혔다.
> (CV 약 20 %. 개체 간 변동이 이만큼 크다는 것이 개체 내 비교를 택한 이유를 뒷받침한다.)

### 측정 절차

| 항목 | 값 |
|---|---|
| 전극 | **금속 핀 3개 — 기록 1 · 기록 2 · 기준(접지).** 아래 ★ |
| 삽입 깊이 | **몸을 관통해 나무/스티로폼 받침까지** |
| 자극 | 유리 또는 플라스틱 탐침으로 **가볍게 톡** — 탭당 보통 **1–3개 스파이크** |
| LGF | **꼬리쪽** 자극 · 전극도 꼬리쪽 |
| MGF | **전극을 앞쪽으로 옮겨 다시 꽂고** 머리 자극 |
| 거리 | **자를 대거나 스티로폼의 눈금**으로 매번 실측 (d_LGF, d_MGF 따로) |
| Δt | **두 채널 첫 번째 큰 음의 편향** 사이 간격 |
| 케이지 | 패러데이 케이지, 악어클립으로 SpikerBox에 접지 |
| 보관 | 젖은 흙 통에 담아 **냉장고** |

**LGF와 MGF를 동시에 재지 않는다 — 전극을 옮겨 두 번 잰다.**

### ★ 전극 3개가 어떻게 붙는가 — 원문 §Materials and Methods, *Equipment and software* (2026-08-29 확인)

> "The recording electrodes [**electrode 1, electrode 2, and reference (sometimes also called
> "ground"）**] inserted into the worm connected to our two-channel SpikerBox…"

**즉 채널마다 기록 전극이 하나씩이고, 두 채널이 기준(접지) 전극 하나를 함께 쓴다.**
지렁이에 꽂는 핀은 모두 **3개**다. 채널당 두 개짜리 「기록 쌍」이 아니다.
지렁이를 등쪽이 위로 놓고 중심선에서 살짝 벗어나게, **몸을 관통해 받침까지** 꽂는다.

전극 실물은 **«map pins soldered to speaker wire»** — 압정을 스피커선에 납땜한 것.
받침은 **2.5 cm 눈금을 그은 스티로폼**이고 여기서 전극 간 거리를 읽는다.

### ★ SpikerBox 증폭기의 실제 수치 (같은 절 · 원문 확인)

| 항목 | 값 |
|---|---|
| 총 이득 | **880 ×** |
| 1단 | **AD623** · 이득 **4 ×** · 입력 임피던스 **2 GΩ** |
| 2단 | **TLC2272** · 이득 **220 ×** · **대역통과 300–1,300 Hz** |
| 오디오단 | LM386 |
| 출력 | **3.5 mm 스테레오 잭 → 노트북 line in** (배터리 구동 권장) |
| 노트북에 스테레오 line-in 이 없으면 | **USB 사운드카드** (본문 예: iMic · US$40). «USB sound cards can sometimes generate a 1-kHz ringing noise artifact» |
| 녹음 | **Audacity** · 입력을 "line in" 으로 |

> **우리 회로와 다른 두 가지 (우리 비교).**
> ① **1단 이득이 4 배뿐이다.** 우리 1단은 직류결합 **92 배**라 전극 오프셋 32.6 mV 에서 포화한다.
> Shannon 은 4 배라 같은 자리에서 750 mV 까지 견딘다.
> ② **대역이 300–1,300 Hz 로 우리(103 Hz–3.39 kHz)보다 훨씬 좁다.**
> **둘 다 회로를 고치는 일이므로 신이안이 정한다. 아직 하지 않았다.**

---

## 이 논문이 말하지 않은 것 ★

- **중금속에 대해 말하지 않는다.** 교육용 측정 방법 논문이다.
- **탄산수 마취 조건의 전도속도를 재지 않았다** (위 경고).
- **같은 개체 반복 측정의 SD를 보고하지 않는다.**
  개체당 5회 측정을 했지만 **개체 내 SD를 따로 제시하지 않았다.**
  개체 내 반복 측정의 SD는 어느 논문에도 없다.
- **사운드카드의 채널 간 시간 스큐를 검증하지 않았다.**
  µs 단위 시간차를 재려면 그냥 넘길 수 없는 항목이다.
- **며칠에 걸친 반복 측정 · 개체 생존**을 다루지 않는다 (관통 삽입 + 마취라 불가능하다).
- 온도를 통제하거나 기록하지 않았다.

### 우리와 다른 선택 하나 — 관통 삽입

Shannon은 핀을 **몸을 관통시켜** 받침에 박는다.
Kladt는 반대로 **피부에 닿기만** 한다.
**관통은 개체를 살려 두지 못한다** — 같은 개체를 며칠 반복 측정하려면 쓸 수 없다.

---

[`../문헌/색인.md`](../문헌/색인.md) ·
[`Marzullo2012_SpikerBox.md`](Marzullo2012_SpikerBox.md)
