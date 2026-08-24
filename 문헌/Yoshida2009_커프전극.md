# Yoshida 등 2009 — 다접점 커프 전극의 전도속도 선택적 기록 검증

서지: Yoshida K, Kurstjens GAM, Hennings K ·
"Experimental validation of the nerve conduction velocity selective recording technique
using a multi-contact cuff electrode" ·
*Medical Engineering & Physics* · **31(2009):1261–1270**
접근: 유료 | 원문: `원문/Yoshida2009_커프전극.pdf` ✅ **확보·확인 완료** (신이안 제공)

**종이 *Lumbricus terrestris* 로 우리와 일치한다.**

---

## 이 논문이 한 것 (원문 확인)

지렁이를 **"섬유가 둘뿐인 말초신경"** 으로 삼아, 다접점 커프 전극의
**속도 선택적 기록 기법**(지연가산 필터 · 매치드 필터)을 실험으로 검증했다.

### 실험 조건 (§2.1)

| 항목 | 값 |
|---|---|
| 개체 | 성체 **12마리** |
| 사육 | **4 °C** 보관 → 실험 24시간 전 **실온 21 °C** 로 이동 |
| 마취 | **10 % 에탄올 10분** (공기 폭기) |
| 전극 | **11접점 백금 포일 링 커프** · 내경 4 mm · 접점 폭 0.5 mm · **간격 3 mm** |
| 자세 | 꼬리쪽을 커프에 실로 꿰어 통과시킨다 |
| **환경** | **0.9 % 생리식염수로 채운 페트리 접시에 잠긴 상태** |
| 고정 | 머리·꼬리를 Sylgard 블록에 **바늘 전극으로 핀 고정** (자극 겸용) |
| 증폭 | 이득 **1000×** · **고역통과 0.1 Hz** (저역통과 없음) |
| 샘플링 | **50 kHz** |
| 기준 전극 | 바깥쪽 두 접점을 단락해 사용 |
| 자극 | **100 µs 구형파 전류 제어** · 역치의 **2배**(supramaximal) |
| **자극 간격** | **2초** |
| 평균 | **최소 50회** 자극에 대한 응답 기록 |

> **우리 프로토콜의 「자극 간격 2초」와 「50회 평균」이 이 논문에서 나왔다.**

### §2.3.1 접점 공유 — 우리 4채널 구성의 근거 (원문 확인)

8채널 증폭기를 **인접 링 쌍(3 mm)의 차동 이극 기록**으로 설정해 기록한 뒤,
**디지털 후처리로** 6 · 12 · 18 · 24 mm 간격의 이극·삼극 신호를 합성했다.

> "the bipolar channel number n with an electrode spacing of 3 mm (b3mm,n) can be written as
> mn − mn−1 … Consequently, **the bipolar channel b6mm,n can be found as bn + bn−1 =
> mn − mn−1 + mn−1 − mn−2 = mn − mn−2**."

**즉 인접 이극 채널을 더하면 두 배 간격의 이극 신호가 된다.**
11접점에서 안쪽 9극(m1–m9)으로 이극 8채널(b1–b8)을 뽑았으므로,
**인접 채널끼리 접점을 물리적으로 공유한다.**

> ⚠ **주의**: 초안은 이 방법의 근거로 "계측증폭기는 입력 임피던스가 높아 한 접점에
> 둘이 붙어도 무방하다"를 적었다. **그 설명은 이 논문에 없다 — 우리 추론이다.**
> 논문은 그냥 그렇게 하고 설명하지 않는다. (다만 12마리에서 실제로 작동했다는 것이
> 실증이기는 하다.)

### §3.1 전도속도 결과

| | 값 |
|---|---|
| **MGF** | **15.6 ± 0.87 m/s** (mean ± **SEM**, n = 12) → SD ≈ 3.0 m/s, **CV 약 19 %** |
| **LGF** | **7.7 ± 0.48 m/s** (mean ± SEM, n = 12) → SD ≈ 1.7 m/s, **CV 약 22 %** |

저자 본인의 해명 (§4.2):

> "These values are **about half of the values reported by [26]** but closer to measured by
> others. **The difference may be due to the ethanol used to anesthetize the animals**,
> but does not pose a major problem since the conduction velocity of the fibers are still
> different enough…"

**[26] = Drewes, Landa & McFall (1978), *J Exp Biol* 72:217–227**,
비마취·자유이동 *L. terrestris*. → 아래 「새로 나온 확보 대상」

### §1 문헌 속도 범위 ★

> "have a nerve conduction velocity ranging **15–45 m/s** and **7.5–15 m/s** respectively"
> (MGF / LGF, 인용 [23–25])

> ⚠ **우리 저장소가 쓰는 MGF 15–30 m/s · LGF 7–8 m/s 보다 넓다.**
> 단계 0 게이트가 30 m/s에서 끊기는데, **더 높은 값이 나와도 실패가 아니다.**

### §3.2 전극 간격과 진폭 (원문 확인)

| 관찰 | 값 |
|---|---|
| 3극이 2극을 넘어서는 **교차점** | **LGF ~6 mm · MGF ~8 mm** |
| **삼극 LGF 진폭 최대** | **12 mm** |
| **삼극 MGF** | **24 mm에서도 아직 증가 중** |
| 이극 LGF가 보강되기를 멈추는 지점 | 약 18 mm |
| 시험한 최대 간격 | **24 mm** |

**기전 (원문)**: 간격을 넓히면 진폭이 커지지만,
**"until the spacing approaches the wavelength of the action potential and the action
potential no longer adds constructively."**

즉 **최적 간격은 활동전위의 파장(≈ 전도속도 × 지속시간)에 비례한다.**
MGF가 빠르니 파장이 길고, 그래서 최적 간격이 크다. **이것이 25 mm가 MGF에 유리하고
LGF에 불리한 이유다.**

### §3.3 진폭과 잡음 (Fig. 8, grand mean ± SEM, n = 12, 6 mm 삼극)

| 항목 | 값 |
|---|---|
| **MGF 원신호** | **29.4 ± 4.1 µV** |
| **LGF 원신호** | **37.1 ± 4.4 µV** |
| **배경 잡음** | **19.3 ± 0.4 µV** |
| 자극 아티팩트 | 58.7 µV (DA 필터 후 38.7) |
| → SNR | **MGF 1.52 · LGF 1.92** |

> ⚠ **LGF가 MGF보다 크다.** 초안은 MGF를 주신호로 가정했으나 진폭은 LGF가 더 크다.
> 원문 설명: LGF는 **간극연접으로 이어진 두 섬유가 하나로 작동**하기 때문이다.

**필터 효과** (같은 Fig. 8):

| 필터 | 신호 | 잡음 | 자극 아티팩트 |
|---|---|---|---|
| 원신호 | MGF 29.4 · LGF 37.1 | 19.3 | 58.7 |
| **지연가산(DA)** | MGF **62.4** · LGF **68.4** (약 2배) | — | 38.7 |
| DA (튜닝 안 맞음) | MGF 34 · LGF 26 (변화 없음) | — | — |
| **매치드(MF)** | MGF 21.0 · LGF 43.6 | **2.4 / 2.8** | **1.4 / 0** |

**지연가산은 맞는 속도의 신호만 약 2배 키우고 안 맞는 것은 그대로 둔다.**
**매치드 필터는 잡음을 19.3 → 2.4 µV로 죽인다** (SNR 약 8.8) —
다만 저자 결론은 **"선택도(selectivity)는 개선하지 못했다"**.

필터 튜닝 폭 (§4.3): MGF는 FWHH 약 10–15 m/s, LGF는 약 5 m/s.
**커프가 길수록 속도 선택도가 올라간다.**

### 수초 서술 — 정확한 문장 (§4.1)

> "Each of the giant fibers is wrapped in myelin sheaths that **resemble** the myelin sheaths
> of vertebrate nerve fibers, **with some structural differences**. Despite these differences,
> the myelin sheaths of MGF fibers and vertebrate myelinated nerve fibers **share the same
> functional role and have saltatory conduction** [21]."

**[21] = Günther 1976, *J Comp Neurol* 168(4):505–531** — 우리 저장소의 그 논문이다.

**즉 이 논문은 기능적 유사성만 말하고 분자적 동일성은 말하지 않는다.**
오히려 "구조적 차이가 있다"고 명시한다.
→ [`../결정기록.md`](../결정기록.md) 「철회된 주장」의 판단이 옳았음이 원문으로 확인됐다.

---

## 우리가 가져오는 것

| 가져오는 것 | 우리 적용 |
|---|---|
| **접점 공유 다채널 합성** (§2.3.1) | 5접점 12.5 mm → 25/37.5/50 mm 합성 → [`../장치/전극.md`](../장치/전극.md) |
| **간격–진폭 곡선** | 25 mm 채택의 근거 |
| **파장 = CV × 지속시간** 기전 | MGF는 넓게, LGF는 좁게 봐야 하는 이유 |
| **자극 간격 2초 · 50회 평균** | 프로토콜의 직접 출처 |
| **지연가산 필터가 약 2배 증폭** | 단계 2 4채널의 목표 → [`../정리/신호처리_전도속도추정.md`](../정리/신호처리_전도속도추정.md) |
| 진폭 29.4 / 37.1 µV · 잡음 19.3 µV | 필요 이득과 평균 횟수 산정 |
| 에탄올이 속도를 절반으로 만든다는 **저자 본인 해명** | 마취 전환의 근거 |

---

## 이 논문이 말하지 않은 것 ★

- **중금속·독성물질에 대해 아무것도 말하지 않는다.** 전극 공학 논문이다.
- **비침습이 아니다.** 지렁이가 **생리식염수에 잠겨** 있고 머리·꼬리는 **바늘로 핀 고정**돼 있다.
  §4.1 제목이 "an animal model of **in vitro** peripheral nerve"인 이유다.
  **우리 챔버(젖은 막만 유지, 물이 고이면 안 됨)와 조건이 크게 다르다.**
  식염수가 세포외 신호를 단락시켰을 가능성이 있다(우리 추론) —
  SNR 1.5–2가 Mazzia의 5–10보다 낮은 이유일 수 있다.
- **25 mm를 권하지 않았다.** 이 논문의 접점 간격은 **3 mm**이고,
  합성으로 시험한 최대치가 **24 mm**다. **25 mm는 데이터 밖의 외삽이다**(아주 조금이지만).
- **"입력 임피던스가 높아 접점 공유가 무방하다"는 설명이 없다.** 우리 추론이다.
- **비마취 조건을 다루지 않았다.** 전부 10 % 에탄올이다.
- **며칠 반복 측정 · 개체 생존을 다루지 않는다.**
- **반복 측정 변동(SD_rep)을 보고하지 않는다.** ±0.87은 12마리에 걸친 SEM이다.
- **매치드 필터는 SNR을 올리지만 선택도는 못 올린다** — 저자 결론.

## 이 논문이 알려준 새 확보 대상

**Drewes CD, Landa KB, McFall JL (1978)**
"Giant nerve fibre activity in intact, freely moving earthworms" · *J Exp Biol* 72:217–227
→ **비마취·자유이동 *L. terrestris***. Yoshida가 "내 값의 2배"라고 한 그 논문이다.
비마취 기준선의 1차 출처가 될 수 있다.

---

링크: [`../문헌/색인.md`](../문헌/색인.md) ·
[`../정리/세포외기록_원리.md`](../정리/세포외기록_원리.md) ·
[`../정리/신호처리_전도속도추정.md`](../정리/신호처리_전도속도추정.md) ·
[`../장치/전극.md`](../장치/전극.md) · [`Gunther1976_등쪽결절.md`](Gunther1976_등쪽결절.md)
