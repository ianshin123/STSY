# Shannon 등 — 사운드카드로 전도속도 재기

서지: Shannon KM, Gage GJ, Jankovic A, Wilson WJ, Marzullo TC ·
"Portable conduction velocity experiments using earthworms for the college and high school
neuroscience teaching laboratory" ·
*Advances in Physiology Education* · 38(1):62–70 · 2014
접근: **무료 전문 (PMC)** | 원문: `원문/Shannon_휴대형전도속도_PMC전문.html` ✅ **확보·확인 완료**
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
> … **with 20 ml of tap water**."

마취 확인법: **탐침으로 머리·꼬리를 건드려 도피반사(수축)가 사라지면 된 것.**
효과 지속 **5–10분**. 마취 후 수돗물로 몇 초 헹군다.

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
| 전극 | **금속 핀 3개.** 지렁이를 **등쪽이 위로** 놓고 중심선에서 살짝 벗어나게 삽입 |
| 삽입 깊이 | **몸을 관통해 나무/스티로폼 받침까지** |
| 자극 | 유리 또는 플라스틱 탐침으로 **가볍게 톡** — 탭당 보통 **1–3개 스파이크** |
| LGF | **꼬리쪽** 자극 · 전극도 꼬리쪽 |
| MGF | **전극을 앞쪽으로 옮겨 다시 꽂고** 머리 자극 |
| 거리 | **자를 대거나 스티로폼의 눈금**으로 매번 실측 (d_LGF, d_MGF 따로) |
| Δt | **두 채널 첫 번째 큰 음의 편향** 사이 간격 |
| 케이지 | 패러데이 케이지, 악어클립으로 SpikerBox에 접지 |
| 보관 | 젖은 흙 통에 담아 **냉장고** |

**LGF와 MGF를 동시에 재지 않는다 — 전극을 옮겨 두 번 잰다.**
우리 5접점 4채널 구성은 이걸 한 번에 하려는 것이다.

---

## 우리가 가져오는 것

| 가져오는 것 | 우리 적용 |
|---|---|
| **탄산수 마취 레시피** (셀처 30 mL + 수돗물 20 mL, 5분) | 단계 0 → [`../정리/마취와_구속법.md`](../정리/마취와_구속법.md) |
| **마취 확인법 — 도피반사 소실** | 단계 0 절차 |
| **±4.5 m/s = 개체 간 SD** | 개체 내 비교 설계의 정당화 |
| 사운드카드 경로의 실증 | 스코프가 아날로그일 때의 대안 |
| **첫 번째 큰 음의 편향 기준 Δt** | 분석 규약 (Bähring과 일치) |
| 탭당 1–3 스파이크 | 기계적 자극의 현실적 기대치 |

---

## 이 논문이 말하지 않은 것 ★

- **중금속에 대해 말하지 않는다.** 교육용 측정 방법 논문이다.
- **탄산수 마취 조건의 전도속도를 재지 않았다** (위 경고).
- **같은 개체 반복 측정의 SD를 보고하지 않는다.**
  개체당 5회 측정을 했지만 **개체 내 SD를 따로 제시하지 않았다.**
  우리가 필요한 SD_rep은 여전히 어느 논문에도 없다.
- **사운드카드의 채널 간 시간 스큐를 검증하지 않았다.**
  우리 목표가 25 µs라 이건 그냥 넘길 수 없다 →
  [`../장치/캘리브레이션/색인.md`](../장치/캘리브레이션/색인.md)
- **며칠에 걸친 반복 측정 · 개체 생존**을 다루지 않는다 (관통 삽입 + 마취라 불가능하다).
- 온도를 통제하거나 기록하지 않았다.

### 우리와 다른 선택 하나 — 관통 삽입

Shannon은 핀을 **몸을 관통시켜** 받침에 박는다.
Kladt는 반대로 **피부에 닿기만** 한다.
우리 단계 0은 **1–2 mm만 삽입**으로 그 사이에 있다 — 신호를 키우되 개체를 살린다.
단계 2 이후에는 삽입 자체가 없어진다(챔버 접점).

---

링크: [`../정리/마취와_구속법.md`](../정리/마취와_구속법.md) ·
[`../정리/지렁이_전극연구.md`](../정리/지렁이_전극연구.md) ·
[`../정리/통계_검출력.md`](../정리/통계_검출력.md) ·
[`Marzullo2012_SpikerBox.md`](Marzullo2012_SpikerBox.md)
