# Marzullo & Gage 2012 — SpikerBox, 저가 오픈소스 생체증폭기

서지: Marzullo TC, Gage GJ · "The SpikerBox: A Low Cost, Open-Source BioAmplifier for
Increasing Public Participation in Neuroscience Inquiry" ·
*PLOS ONE* · 7(3):e30837 · 2012 · DOI 10.1371/journal.pone.0030837
접근: **무료 전문 + 부록** | 원문: ✅ **확보·확인 완료**
- 본문 [`원문/Marzullo2012_SpikerBox.pdf`](원문/Marzullo2012_SpikerBox.pdf)
- **회로도·제작 가이드** [`원문/Marzullo2012_부록_회로도와제작가이드.docx`](원문/Marzullo2012_부록_회로도와제작가이드.docx) (File S1)
- **부품표** [`원문/Marzullo2012_부록_부품표.xlsx`](원문/Marzullo2012_부록_부품표.xlsx) (File S10)

URL: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0030837

---

## 회로 상세 (부록 File S1 원문 확인)

### 전원 ★

> "This would require 2 batteries (one each for V+ V-). **For portability, we designed our
> circuit to use a single 9 V battery**, and we therefore **split the voltage into ±4.5 V
> using a voltage divider (R1/R1)**. The virtual ground is stabilized by an op-amp (Chip 2a)
> using a voltage follower."

**SpikerBox는 9 V 하나를 ±4.5 V로 쪼갠다.** 저자가 든 이유는 휴대성이다.
결과적으로 **AD623의 공급전압 절대최대 12 V 안에 들어간다** → [`장치/장비.md`](../%EC%9E%A5%EC%B9%98/%EC%9E%A5%EB%B9%84.md).

### 1단 — AD623 계측증폭기

> "This signal is amplified **~4x** by the AD623 low-voltage instrumentation amp (Chip 1)…
> You can also use an **INA118** chip from Texas Instruments instead of the AD623.
> The gain is set by adjusting the resistor across pins 1 and 8 according to the equation:
> **Gain = 1 + (100 kΩ/R)**. In our circuit, **R6 = 33 kΩ, thus the gain is 4.03.**"

**이득 공식이 확인됐다.** AD623 데이터시트의 식과 같다.

### 2단 — TLC2272 + 대역통과

> "**R8/R7 = 220 kΩ/1 kΩ = 220** … The resistor and capacitor in series (C7 and R7) serve as
> a **high-pass filter** with a cut-off frequency determined by **f = 1/(2πRC)**.
> Our high pass cut-off is thus **338 Hz**. The resistor and capacitor in parallel (C8 and R8)
> serve as the **low-pass filter** … and thus is **1291 Hz**.
> **The total gain of the circuit is 4.03 × 220 = 886.6.**"

부품값(조립 절): **C7 = 0.47 µF · R7 = 1 kΩ · R8 = 220 kΩ · C8 = 560 pF ·
C4 = 0.047 µF · R3 = 10 Ω · C5 = 0.1 µF.**

**초안이 적은 "887배"는 886.6의 반올림으로 맞다.**
본문 초록 쪽은 "~900×"로 어림해 쓴다.

### op-amp 대체 부품 (직접 인용)

> "We used a **TLC2272** as our op-amp, but similar parts could be used from other suppliers
> (**TL074, OP291, OP293, MCP602**)."

**TL074가 저자 승인 대체 목록에 있다.** TL072는 같은 계열의 2연산 판이다
— **다만 저자가 TL072를 직접 승인한 것은 아니다.**

### 전극

> "we can use electrodes (in our case **stainless steel needles**) which have a high impedance…
> The pins we use have a **1 kHz impedance typically around 20–30 kΩ**."

### 본문에서 확인된 것

- **3단 증폭기**, 통과대역 **300–1300 Hz**, 스피커로 소리를 들려준다
- 라인 출력으로 노트북·스마트폰 녹음 가능
- **60 Hz 취약성을 저자들이 명시한 약점으로 인정한다**:
  > "our amplifier was **susceptible to line noise interference**… If a student's laptop or
  > oscilloscope is **plugged into a wall outlet, the SpikerBox can become unusable**.
  > It is therefore recommended that demonstrations be **restricted to battery-powered devices**,
  > though we have found simple **faraday cages built with hardware store components for <$20**
  > can reduce much or all of the line noise."

**"어댑터 금지 · 패러데이 케이지 필수"가 저자 자신의 권고다.**

---

## 이 논문이 말하지 않은 것 ★

- **지렁이에 대해 말하지 않는다.** 바퀴벌레 다리 신경이다.
- **전도속도 측정을 하지 않는다.** 단채널 스파이크 기록 장치다.
  **두 지점의 시간차를 어떻게 잡는가**를 다루지 않는다.
- **이 회로보다 이득을 올렸을 때의 안정성을 보증하지 않는다.**
  이득을 올리면 발진·포화 위험이 커진다. 조립 후 직접 확인해야 한다.
- **스파이크의 주파수 성분을 측정해 보고하지 않는다.**
  저자들은 "neural spike signals have frequencies of **~500–1000 Hz** in waveshape"
  라고 쓸 뿐이다. **이 문장은 파형 모양에 대한 서술이지 통과대역 설계값이 아니다.**
  (Bähring 2014가 지정한 대역은 0.1–3 kHz다 → [`Bahring2014_비마취챔버.md`](Bahring2014_비마취챔버.md))
- **TL072가 TLC2272를 대체해도 되는지 직접 검증하지 않았다** (TL074는 목록에 있다).
  입력 바이어스 전류와 잡음 특성이 다르다 — 조립 후 잡음 바닥 실측으로 확인한다.
- 실측 잡음 바닥(µV RMS)을 부록에서 확인하지 못했다.

---

[`Shannon_휴대형전도속도.md`](Shannon_휴대형전도속도.md)
