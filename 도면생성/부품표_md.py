# -*- coding: utf-8 -*-
"""「보드자료_AD623.py」에서 부품 수량을 세어 「장치/부품.md」를 만든다.

**손으로 표를 옮겨 적지 않는다** — 도면과 문서가 어긋나는 것을 막으려는 것이다.
부품값이나 개수가 바뀌면 「보드자료_AD623.py」만 고치고 이것을 다시 돌린다.

그림을 만들지 않고 **어떤 수치도 만들어내지 않는다** — 정본에 있는 것을 세어 옮길 뿐이다.
표 밖의 글(몸통 표기 읽는 법 · 모듈 실물 · 보드 밖 장비)은 이 파일 아래쪽 DOC 에 있다.
"""
import io
import os

import 보드자료_AD623 as D


def 표기(name, val):
    """몸통에 실제로 적혀 있거나 그려져 있는 것."""
    if val in D.BAND:
        return '색띠 ' + ' '.join(D.BAND[val])
    if name == 'Cd':
        return '`104`'
    if val.startswith('474'):
        return '`474`'
    if val.startswith('472'):
        return '`472`'
    if '전해' in val:
        return '`10µF 50V` · **극성 있음**'
    return '—'


def 수량표():
    """(이름, 값, 하는 일) 마다 1번·2번 보드의 개수를 센다."""
    order, count = [], {}

    def put(key, board):
        if key not in count:
            order.append(key)
            count[key] = [0, 0]
        count[key][board] += 1

    for board, parts in ((0, D.B1_PARTS), (1, D.B2_PARTS)):
        for p in parts:
            put((p['name'], p['val'], p['role']), board)
    for board in (0, 1):
        for _ in range(2 * len(D.CD_COLS)):
            put(('Cd', D.CAPVAL['Cd'], 'IC 전원핀 가까이 — ' +
                 ' · '.join(f'{c}열' for c in D.CD_COLS)), board)

    rows = ['| 이름 | 값 | 몸통에 적힌 것 | 1번 | 2번 | 합계 | 하는 일 |',
            '|---|---|---|---|---|---|---|']
    for (name, val, role) in order:
        a, b = count[(name, val, role)]
        label = val if name == val else f'**{name}**'
        rows.append(f'| {label} | {val} | {표기(name, val)} | {a or "—"} | {b or "—"} '
                    f'| **{a + b}** | {role or ""} |')
    for ic in D.B1_IC:
        rows.append(f'| **{ic[1]}** | — | — | 1 | 1 | **2** | {ic[2]} |')
    rows.append('| 잭 브레이크아웃 | 4극 TRRS | `T` `R1` `R2` `S` | 1 | 1 | **2** '
                '| 보드 옆에 두고 암–수 점퍼선 4개로 잇는다 |')
    rows.append(f'| 수–수 점퍼선 | — | 파란 선 | {len(D.B1_WIRES)} | {len(D.B2_WIRES)} '
                f'| **{len(D.B1_WIRES) + len(D.B2_WIRES)}** | 도면의 파란 선 전부 |')
    rows.append(f'| 암–수 점퍼선 | — | — | {len(D.JACK_PINS)} | {len(D.JACK_PINS)} '
                f'| **{2 * len(D.JACK_PINS)}** | 잭 브레이크아웃 ↔ 보드 J행 |')
    return '\n'.join(rows)


def 값별합계():
    """사거나 셀 때 필요한 것 — 값 하나에 몇 개인가."""
    tot = {}
    for parts in (D.B1_PARTS, D.B2_PARTS):
        for p in parts:
            tot[p['val']] = tot.get(p['val'], 0) + 1
    tot[D.CAPVAL['Cd']] = tot.get(D.CAPVAL['Cd'], 0) + 4 * len(D.CD_COLS)
    rows = ['| 값 | 두 보드 합계 |', '|---|---|']
    for val, k in sorted(tot.items(), key=lambda x: -x[1]):
        rows.append(f'| {val} | **{k}개** |')
    return '\n'.join(rows)


DOC = f'''# 부품 — 무엇이 무엇인가

<sub>**어디에 꽂는지는 여기에 없다.** 자리와 결선의 정본은 도면이다 —
[`그림/브레드보드_배치도_1번보드.png`](%EA%B7%B8%EB%A6%BC/%EB%B8%8C%EB%A0%88%EB%93%9C%EB%B3%B4%EB%93%9C_%EB%B0%B0%EC%B9%98%EB%8F%84_1%EB%B2%88%EB%B3%B4%EB%93%9C.png) ·
[`그림/브레드보드_배치도_2번보드.png`](%EA%B7%B8%EB%A6%BC/%EB%B8%8C%EB%A0%88%EB%93%9C%EB%B3%B4%EB%93%9C_%EB%B0%B0%EC%B9%98%EB%8F%84_2%EB%B2%88%EB%B3%B4%EB%93%9C.png) ·
[`전체연결도_2채널.pdf`](%EC%A0%84%EC%B2%B4%EC%97%B0%EA%B2%B0%EB%8F%84_2%EC%B1%84%EB%84%90.pdf).
**이 문서는 「무엇을 몇 개 · 실물에서 어떻게 알아보나」만 적는다.**

아래 두 표는 [`도면생성/보드자료_AD623.py`](../%EB%8F%84%EB%A9%B4%EC%83%9D%EC%84%B1/%EB%B3%B4%EB%93%9C%EC%9E%90%EB%A3%8C_AD623.py) 에서
[`도면생성/부품표_md.py`](../%EB%8F%84%EB%A9%B4%EC%83%9D%EC%84%B1/%EB%B6%80%ED%92%88%ED%91%9C_md.py) 가 세어 뽑은 것이다.
**손으로 고치지 마라** — 값이 바뀌면 정본을 고치고 스크립트를 다시 돌린다.
값을 그 값으로 정한 근거는 [`기록.md`](../%EA%B8%B0%EB%A1%9D.md) 「부품값을 정하는 식과 제약」에 있다.</sub>

---

## 1. 보드에 꽂는 것

{수량표()}

### 사거나 셀 때 — 값별로 몇 개

{값별합계()}

---

## 2. 몸통에 적힌 것을 읽는 법

### 저항 — 색띠 다섯 줄

우리 저항은 오차 ±1 % 금속피막이라 **색띠가 5개**이고 흔한 4색띠와 읽는 법이 다르다.
읽는 법과 값별 색띠는 [`기록.md`](../%EA%B8%B0%EB%A1%9D.md) 「저항 색띠」에 있다.
**위 표의 「몸통에 적힌 것」 칸이 그 값의 띠다.**

> 색으로 읽는 것을 믿지 마라 — 오차 띠가 갈색인데 숫자 띠에도 갈색이 있어 헷갈린다.

### 세라믹·마일러 커패시터 — 세 자리 숫자

**세 자리 숫자는 pF 단위다.** 앞 두 자리가 숫자, **셋째 자리가 그 뒤에 붙는 0의 개수**다.

| 몸통 표기 | 읽으면 | 우리 이름 |
|---|---|---|
| `104` | 10 뒤에 0이 4개 = 100 000 pF = **0.1 µF** | Cd (전원 흔들림 흡수) |
| `474` | 47 뒤에 0이 4개 = 470 000 pF = **0.47 µF** | C1 (마일러 · 직류를 끊는다) |
| `472` | 47 뒤에 0이 2개 = 4 700 pF = **4.7 nF** | Cf (저역차단) |

**1 µF = 1 000 nF = 1 000 000 pF.**
세라믹은 방향이 없다 — 아무 쪽으로나 꽂아도 같다.

### 전해 커패시터 — **방향이 있다**

10 µF 짜리 하나만 전해다. 몸통에 `10µF 50V` 라고 그대로 적혀 있다.
**몸통에 세로 띠가 그려진 쪽 다리가 `−`** 이고 **다리가 긴 쪽이 `+`** 다.
도면이 지정한 방향은 **`+` 를 TIP(33열) 쪽으로** 다.

---

## 3. AD623 모듈 — 실물

**DIYMORE 제품.** 핀 4개짜리 줄이 두 개, 큰 고정 구멍 2개, 그리고 왼쪽 가장자리에
`REF` 와 `GND` 를 잇는 **납땜 점퍼**가 있다.

### ★ 글씨 면이 보드 쪽(아래)을 본다 — 그래서 좌우가 뒤집힌다

<sub>2026-09-06 신이안 실물 확인.</sub>

| | 왼쪽 → 오른쪽 |
|---|---|
| 글씨 면에 인쇄된 순서 (보드에 꽂으면 아래로 간다) | 한 줄 `GND · IN+ · IN− · +VS` / 다른 줄 `GND · OUT · REF · −VS` |
| **보드에 꽂히는 순서 (도면)** | **윗핀 E행 `GND · OUT · REF · −VS` / 아랫핀 I행 `GND · IN+ · IN− · +VS`** |

- **고정 구멍 2개와 `GND` 핀 두 개가 같은 쪽(4열 쪽)** 이다. 몸통이 왼쪽으로 나와 **3열 I행을 가린다**
- **`REF` ↔ `GND` 납땜 점퍼**: 우리 회로는 REF 를 어차피 GND 에 묶으므로 이어져 있든 아니든 같다
- **이득 저항 Rg 를 꽂지 않는다** — 모듈의 트리머가 그 자리를 대신한다

---

## 4. 보드에 안 꽂는 것

| 무엇 | 수량 | 비고 |
|---|---|---|
| **9 V 건전지** | **1개** | ★ 2개를 직렬로 이으면 18 V 가 되어 AD623 절대최대 12 V 를 넘는다 |
| 건전지 스냅 | 1개 | 빨강이 V+ · 검정이 V− |
| **M-Audio M-Track Duo** | 1개 | 6.35 mm 쪽 콤보 입력 2개에 채널 1·2 |
| 3.5 mm(수) ↔ 6.35 mm(수) TRS 케이블 | 2개 | 국내에서는 6.35 mm 를 「5.5」로 쓴다 |
| 악어클립 테스트 리드선 | 4개 | 전극 3개 + 호일 케이지 1개 |
| **전극 — 순은선 0.5 mm** | 3개 | 기록 2 + 기준(접지) 1 |
| 노트북 · USB-B 케이블 | 1벌 | 케이블은 인터페이스 상자에 들어 있다 |
| 케이블타이 · 마스킹테이프 | — | 케이블 묶기 · 채널 표시 |
| 알루미늄 호일 | — | 케이지(선택) |

**멀티미터는 회로의 부품이 아니다.** 갖고 있는 **OWON HDS1021M-N 의 내장 멀티미터는
고장으로 쓸 수 없다** (2026-09-06). 산 것과 값은 [`기록.md`](../%EA%B8%B0%EB%A1%9D.md) 「사고 구매한 것」에 있다.
'''

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '장치', '부품.md'))
io.open(OUT, 'w', encoding='utf-8').write(DOC)
print('저장:', OUT)
