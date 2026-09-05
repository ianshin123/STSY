# -*- coding: utf-8 -*-
"""「보드자료_AD623.py」에서 결선표·부품표를 뽑아 「이번주/장치/AD623계측증폭기.md」를 만든다.

**손으로 표를 옮겨 적지 않는다** — 도면과 문서가 어긋나는 것을 막으려는 것이다.
결선을 고치면 「보드자료_AD623.py」만 고치고 이 스크립트를 다시 돌린다.
"""
import io, os
import 보드자료_AD623 as D

RAILNAME = {'TV': '위 V+ 레일', 'TG': '위 GND 레일', 'BG': '아래 GND 레일', 'BV': '아래 V− 레일'}


def 자리(p):
    c, r = p
    return f'{RAILNAME[r]} ({c}열)' if r in RAILNAME else f'({c}, {r})'


def 표(wires, parts, ics, 이름):
    설명 = {}
    src = io.open('보드자료_AD623.py', encoding='utf-8').read().split('\n')
    for ln in src:                                   # 결선 옆 주석을 그대로 가져온다
        if ln.strip().startswith('((') and '#' in ln:
            설명[ln.split('#')[0].strip().rstrip(',')] = ln.split('#', 1)[1].strip()
    out = [f'### {이름} — 결선', '', '| # | 무엇 | 어디에서 | 어디로 | 비고 |', '|---|---|---|---|---|']
    n = 0
    for ic in [i for i in ics if len(i) > 4]:
        c0, nm, s1, s2, top, bot = ic[:6]
        top_row = ic[6] if len(ic) > 6 else 'E'
        bot_row = ic[7] if len(ic) > 7 else 'F'
        n += 1
        out.append(f'| {n} | **{nm}** | {c0}–{c0+3}열 · 윗핀 {top_row}행 / 아랫핀 {bot_row}행 | '
                   f'위 `{" · ".join(top)}` / 아래 `{" · ".join(bot)}` | 왼쪽이 GND 쪽 |')
    for ic in [i for i in ics if len(i) <= 4]:
        n += 1
        out.append(f'| {n} | **{ic[1]}** | {ic[0]}–{ic[0]+3}열 · 홈을 걸친다 | 8·7·6·5 / 1·2·3·4 | 홈 자국이 왼쪽 |')
    for p in parts:
        n += 1
        val = p['val'] if p['name'] == p['val'] else f"**{p['name']}** {p['val']}"
        out.append(f'| {n} | {val} | {자리(p["p1"])} | {자리(p["p2"])} | {p["role"]} |')
    for c in D.CD_COLS:
        for r0, r1 in (('TV', 'TG'), ('BG', 'BV')):
            n += 1
            out.append(f'| {n} | **Cd** `104` | {자리((c, r0))} | {자리((c, r1))} | 디커플링 |')
    for w in wires:
        n += 1
        key = str(w).replace("'", "'")
        out.append(f'| {n} | 수–수 점퍼선 | {자리(w[0])} | {자리(w[1])} | {설명.get(str(w), "")} |')
    for (c, r), num, col, what in (D.B1_POSTS if 이름.startswith('1') else D.B2_POSTS):
        n += 1
        out.append(f'| {n} | {num} {what} | {자리((c, r))} | 보드 밖 | 악어클립 또는 스냅 |')
    for c, nm in D.JACK_PINS:
        n += 1
        out.append(f'| {n} | 잭 `{nm}` | 모듈 (보드 옆) | ({c}, J) | **암–수 점퍼선** |')
    out.append('')
    return '\n'.join(out)


def 부품표(parts, ics, 이름):
    cnt, role = {}, {}
    for p in parts:
        k = (p['name'], p['val']); cnt[k] = cnt.get(k, 0) + 1; role.setdefault(k, p['role'])
    cnt[('Cd', D.CAPVAL['Cd'])] = 2 * len(D.CD_COLS)
    role[('Cd', D.CAPVAL['Cd'])] = 'IC 전원핀 가까이 — ' + ' · '.join(f'{c}열' for c in D.CD_COLS)
    out = [f'### {이름} — 무엇을 몇 개', '', '| 이름 | 값 | 색띠 | 개수 | 하는 일 |', '|---|---|---|---|---|']
    for (nm, val), k in cnt.items():
        band = ' '.join(D.BAND[val]) if val in D.BAND else '—'
        out.append(f'| **{nm}** | {val} | {band} | {k}개 | {role[(nm, val)]} |')
    out.append(f'| IC | {" · ".join(i[1] for i in ics)} | — | {len(ics)}개 | '
               f'{" · ".join(str(i[0]) + "열" for i in ics)} |')
    out.append('| 잭 브레이크아웃 | TRRS · 보드 옆에 | — | 1개 | 암–수 점퍼선 4개로 30–33열 J행에 |')
    out.append('')
    return '\n'.join(out)


DOC = f'''# AD623 계측증폭기 — 지금 쓰는 회로

<sub>2026년 9월 5일 · AD623 모듈 2개가 도착해 TL072 3개 판에서 갈아탄 것</sub>

> **조립할 때 펴 놓는 것은 보드마다 한 장씩이다** —
> [`그림/브레드보드_배치도_1번보드.png`](%EA%B7%B8%EB%A6%BC/%EB%B8%8C%EB%A0%88%EB%93%9C%EB%B3%B4%EB%93%9C_%EB%B0%B0%EC%B9%98%EB%8F%84_1%EB%B2%88%EB%B3%B4%EB%93%9C.png) ·
> [`그림/브레드보드_배치도_2번보드.png`](%EA%B7%B8%EB%A6%BC/%EB%B8%8C%EB%A0%88%EB%93%9C%EB%B3%B4%EB%93%9C_%EB%B0%B0%EC%B9%98%EB%8F%84_2%EB%B2%88%EB%B3%B4%EB%93%9C.png).
> **부품마다 꽂을 값과 색띠가 그림 위에 적혀 있다.**
> 챔버 · 건전지 · 오디오 인터페이스까지 한 장에 있는 것은
> [`그림/전체연결도_2채널.png`](%EA%B7%B8%EB%A6%BC/%EC%A0%84%EC%B2%B4%EC%97%B0%EA%B2%B0%EB%8F%84_2%EC%B1%84%EB%84%90.png).
> **아래 표는 [`도면생성/보드자료_AD623.py`](../../%EB%8F%84%EB%A9%B4%EC%83%9D%EC%84%B1/%EB%B3%B4%EB%93%9C%EC%9E%90%EB%A3%8C_AD623.py) 에서 뽑은 것이다** —
> 손으로 옮겨 적지 않는다. 결선을 고치면 그 파일을 고치고 `결선표_AD623_md.py` 를 다시 돌린다.
>
> **TL072 판(지난 판)은 [`보관/TL072_회로도.md`](../../%EB%B3%B4%EA%B4%80/TL072_%ED%9A%8C%EB%A1%9C%EB%8F%84.md) 에 그대로 있다.**

---

## 1. 왜 갈아탔나

AD623 안에 든 것이 3-op-amp 계측증폭기다. TL072 판은 그것을 칩 세 개로 밖에서 만든 것이었다.

| | TL072 판 | **AD623 판** |
|---|---|---|
| IC | 3개 | **2개** (AD623 모듈 + TL072 하나) |
| 저항 (1번 / 2번 보드) | 16 / 15개 | **9 / 8개** |
| 수–수 점퍼선 (1번 / 2번) | 20 / 16개 | **{len(D.B1_WIRES)} / {len(D.B2_WIRES)}개** |
| 차동단 저항 네 개 짝맞춤 | 10 kΩ 40개를 재서 고른다 | **없다** — 칩 안에서 공장 트리밍 |
| 이득 저항 Rg | 220 Ω | **없다** — 모듈의 트리머 |
| 입력환산 잡음 | 37 nV/√Hz × √2 = 52 | **35 nV/√Hz** |
| 출력 스윙 (±4.5 V 에서) | 약 ±3.0 V | **−4.3 ~ +4.0 V** |

## 2. ★ 바꾸면서 반드시 같이 고쳐야 하는 것 — Rb1 과 Rb2

**AD623 입력 바이어스 전류는 17 nA typ · 25 nA max** (데이터시트 Rev. G p.6 DUAL SUPPLIES).
TL072 의 **65 pA** 보다 **260배**다.

- 08-29 에 전극을 채널당 하나로 바꾸면서 TL072 판은 IN− 를 **1 Ω** 으로 GND 에 묶었다.
  TL072 에서는 65 pA × 1 MΩ = 65 µV 라 아무 문제가 없었다
- **AD623 에서 그대로 두면** 17 nA × 1 MΩ = **17 mV** 가 한쪽에만 생겨
  **그대로 차동 오프셋**이 된다. 이득 100 이면 1.7 V
- **양쪽 다 1 MΩ 으로 균형을 맞추면** 남는 것은 오프셋 전류(0.25 nA typ)뿐이라
  0.25 nA × 1 MΩ = **0.25 mV**. **68배 줄어든다**

**그래서 Rb1 · Rb2 를 둘 다 1 MΩ 으로 되돌렸다.** IN− 에는 전극을 붙이지 않고
1 MΩ 으로만 GND 에 묶는다 — 신호적으로는 여전히 0 V 기준이다.

## 3. 이득은 트리머로 맞춘다

`G = 1 + 100 kΩ / R_G` 이고 **모듈 위의 트리머가 R_G 자리를 대신한다** — 저항을 꽂지 않는다.

> **★ 이득을 100 이하로 둔다.** 데이터시트 Table 3 의 −3 dB 대역폭이
> G=100 에서 10 kHz, G=1000 에서 2 kHz 로 떨어진다. 목표 통과대역 상한이 3 kHz 이므로
> 1단에서 대역을 다 써 버리면 안 된다.

**총 이득 = 트리머(100 이하) × 2단 3.03.** 조립 뒤 크기를 아는 소신호를 넣어 실측으로 확인한다.

---

## 4. 결선표

표기는 `(열, 행)` 이다. **AD623은 윗핀 E행·아랫핀 I행, TL072는 E행·F행이며 왼쪽이 GND(또는 1번) 쪽이다.**

> ### ★ AD623 실물은 처음 도면보다 세로로 3칸 길다
> 윗핀은 E행, 아랫핀은 I행에 꽂는다. **윗줄은 `GND·OUT·REF·−VS`,
> 아랫줄은 `GND·IN+·IN−·+VS`**다. IN+는 9열로 빼서 전극과 Rb1을 나눠 꽂는다.

> ### ★ 레일 구멍은 5개마다 한 칸씩 비어 있다 — 5 · 11 · 17 · 23 · 29 열에 구멍이 없다
> 레일은 30열 부근에서 끊기므로 **레일에 무는 것은 전부 28열 왼쪽**이다.

{표(D.B1_WIRES, D.B1_PARTS, D.B1_IC, '1번 보드 (채널 1 · 전원부가 여기 있다)')}
{표(D.B2_WIRES, D.B2_PARTS, D.B2_IC, '2번 보드 (채널 2 · 전원부가 없다)')}

---

## 5. 부품

{부품표(D.B1_PARTS, D.B1_IC, '1번 보드')}
{부품표(D.B2_PARTS, D.B2_IC, '2번 보드')}

> **1 Ω 은 옆 열끼리(2.54 mm) 잇는다.** 1/4 W 저항 몸통이 6.3 mm 라 눕힐 수 없다 —
> 다리를 몸통 양 끝에서 아래로 꺾어 ㄷ자로 만들어 세운다. 도면에는 자리를 보이려고 눕혀 그렸다.

> **잭 브레이크아웃은 보드에 직접 못 꽂는다** (2026-09-05 실물 확인) —
> 핀 4개가 한 레일 안에서 전부 단락된다. **보드 옆에 두고 암–수 점퍼선 4개로 뺀다.**
> TIP 이 33열에 가게만 맞추면 되고, 나머지 셋은 어차피 전부 GND 로 묶인다.

---

## 6. 조립 순서

1. **레일 도통 확인** — 네 줄 모두 30열 부근에서 끊겨 있다
2. **전원부만 조립** (1번 보드의 R1 · R2 · 가상접지 버퍼) → 멀티미터로 V+ · V− 확인.
   **여기서 안 나오면 멈춘다**
3. **AD623 모듈에 핀 헤더를 납땜**하고 4–7열, **윗핀 E행·아랫핀 I행**에 꽂는다. **왼쪽이 GND 쪽**
4. TL072 를 19–22열에 꽂는다. **꽂고 뺄 때는 건전지를 분리한다**
5. **전원·디커플링 배선** → 다시 전압 확인
6. **Rb1 · Rb2 를 둘 다 1 MΩ 으로** 꽂는다 (2절)
7. **2단** (C1 · Rin · Rf · Cf)
8. **출력과 잭** — 10 µF · 암–수 점퍼선 4개
9. **두 입력을 GND 에 단락**하고 무신호 잡음 관찰 → 발진·포화 여부
10. 크기를 아는 소신호를 넣어 **트리머로 이득을 맞춘다** (100 이하)
11. 전극 연결, 측정

---

[`부품값.md`](%EB%B6%80%ED%92%88%EA%B0%92.md) · [`장치설명.md`](%EC%9E%A5%EC%B9%98%EC%84%A4%EB%AA%85.md) ·
[`장비.md`](%EC%9E%A5%EB%B9%84.md)
'''

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '이번주', '장치', 'AD623계측증폭기.md'))
io.open(OUT, 'w', encoding='utf-8').write(DOC)
print('저장:', OUT)
