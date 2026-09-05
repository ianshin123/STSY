#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AD623 2채널 브레드보드 배치의 물리·전기 일관성을 검사한다.

도면의 좌표 정본인 ``보드자료_AD623.py``를 직접 읽는다. 정상이면 검사 결과와
필터 계산값을 출력하고 0으로 끝난다.
"""
from collections import defaultdict
import math

import 보드자료_AD623 as D


RAILS = {'TV', 'TG', 'BG', 'BV'}


def ic_holes(ics):
    holes = []
    for ic in ics:
        c0, name = ic[:2]
        top_row = ic[6] if len(ic) > 6 else 'E'
        bot_row = ic[7] if len(ic) > 7 else 'F'
        for offset in range(4):
            holes.append(((c0 + offset, top_row), f'{name} 윗핀 {offset + 1}'))
            holes.append(((c0 + offset, bot_row), f'{name} 아랫핀 {offset + 1}'))
    return holes


def physical_checks(which, wires, parts, posts, ics):
    use = defaultdict(list)

    def put(hole, label, kind):
        use[hole].append((label, kind))

    for i, (p1, p2) in enumerate(wires, 1):
        put(p1, f'점퍼선 {i}', 'wire')
        put(p2, f'점퍼선 {i}', 'wire')
    for i, p in enumerate(parts, 1):
        put(p['p1'], f"{p['name']} {i}", 'part')
        put(p['p2'], f"{p['name']} {i}", 'part')
    for c in D.CD_COLS:
        for r0, r1 in (('TV', 'TG'), ('BG', 'BV')):
            put((c, r0), f'Cd {c}{r0}', 'part')
            put((c, r1), f'Cd {c}{r1}', 'part')
    for hole, number, _colour, label in posts:
        put(hole, f'보드 밖 {number} {label}', 'post')
    for hole, label in ic_holes(ics):
        put(hole, label, 'ic')
    for c, name in D.JACK_PINS:
        put((c, D.JACK_ROW), f'잭 점퍼선 {name}', 'jack')

    duplicates = {hole: items for hole, items in use.items() if len(items) > 1}
    assert not duplicates, f'{which}: 한 구멍 중복 {duplicates}'

    missing_rail_holes = [
        (hole, items) for hole, items in use.items()
        if hole[1] in RAILS and (hole[0] % 6 == D.RAILGAP or 29 <= hole[0] <= 30)
    ]
    assert not missing_rail_holes, f'{which}: 구멍 없는 레일 좌표 {missing_rail_holes}'

    # 모듈 몸통이 덮는 4–7열 F–H행은 핀이나 다른 부품이 없어야 한다.
    covered = {
        (c, r): use[(c, r)] for c in range(4, 8) for r in 'FGH' if use.get((c, r))
    }
    assert not covered, f'{which}: AD623 모듈 아래 충돌 {covered}'

    # 같은 행에 누워 놓은 부품 몸통 아래로 다른 맨 리드가 지나지 않는다.
    body_crossings = []
    for p in parts:
        (c1, r1), (c2, r2) = p['p1'], p['p2']
        if r1 != r2 or r1 in RAILS:
            continue
        lo, hi = sorted((c1, c2))
        for c in range(lo + 1, hi):
            bare = [label for label, kind in use.get((c, r1), []) if kind != 'wire']
            if bare:
                body_crossings.append((p['name'], (c, r1), bare))
    assert not body_crossings, f'{which}: 부품 몸통–리드 충돌 {body_crossings}'


class Nets:
    def __init__(self):
        self.parent = {}

    def root(self, item):
        self.parent.setdefault(item, item)
        if self.parent[item] != item:
            self.parent[item] = self.root(self.parent[item])
        return self.parent[item]

    def union(self, a, b):
        ra, rb = self.root(a), self.root(b)
        if ra != rb:
            self.parent[rb] = ra

    def same(self, a, b):
        return self.root(a) == self.root(b)


def electrical_checks(which, wires, parts):
    nets = Nets()
    for c in range(37):
        for rows in ('ABCDE', 'FGHIJ'):
            for row in rows[1:]:
                nets.union((c, rows[0]), (c, row))
    for rail in RAILS:
        for segment in (range(0, 29), range(31, 37)):
            segment = list(segment)
            for c in segment[1:]:
                nets.union((segment[0], rail), (c, rail))
    for p1, p2 in wires:
        nets.union(p1, p2)

    vplus, ground, vminus = (0, 'TV'), (0, 'TG'), (0, 'BV')
    assert len({nets.root(vplus), nets.root(ground), nets.root(vminus)}) == 3, f'{which}: 전원 레일 단락'
    assert nets.same((2, 'TG'), (2, 'BG')), f'{which}: 위·아래 GND 레일이 끊김'

    # AD623 모듈: 위 E행 GND·OUT·REF·−VS, 아래 I행 GND·IN+·IN−·+VS.
    assert nets.same((7, 'I'), vplus), f'{which}: AD623 +VS'
    assert nets.same((7, 'E'), vminus), f'{which}: AD623 −VS'
    assert ((3, 'B'), (3, 'BV')) in wires or ((3, 'BV'), (3, 'B')) in wires, f'{which}: 모듈 왼쪽 −VS 단일 점퍼'
    assert all((3, 'I') not in wire for wire in wires), f'{which}: 모듈이 가리는 3열 I행 사용'
    for pin in ((4, 'E'), (4, 'I'), (6, 'E')):
        assert nets.same(pin, ground), f'{which}: AD623 GND/REF {pin}'
    assert nets.same((5, 'I'), (9, 'H')), f'{which}: AD623 IN+ 전극'
    for name, pin in (('OUT', (5, 'E')), ('IN+', (5, 'I')), ('IN−', (6, 'I'))):
        assert not any(nets.same(pin, rail) for rail in (vplus, ground, vminus)), f'{which}: AD623 {name} 전원/GND 직결'
    assert len({nets.root((5, 'E')), nets.root((5, 'I')), nets.root((6, 'I'))}) == 3, f'{which}: AD623 OUT/IN+/IN− 단락'

    rb1 = next(p for p in parts if p['name'] == 'Rb1')
    rb2 = next(p for p in parts if p['name'] == 'Rb2')
    assert nets.same(rb1['p1'], (5, 'I')) and nets.same(rb1['p2'], ground), f'{which}: Rb1'
    assert nets.same(rb2['p1'], (6, 'I')) and nets.same(rb2['p2'], ground), f'{which}: Rb2'

    c1 = next(p for p in parts if p['name'] == 'C1')
    rin = next(p for p in parts if p['name'] == 'Rin')
    rf = next(p for p in parts if p['name'] == 'Rf')
    cf = next(p for p in parts if p['name'] == 'Cf')
    cout = next(p for p in parts if p['name'] == '10 µF')
    assert nets.same((5, 'E'), c1['p1']), f'{which}: AD623 OUT–C1'
    assert nets.same(c1['p2'], rin['p1']), f'{which}: C1–Rin'
    assert nets.same(rin['p2'], (20, 'F')), f'{which}: Rin–TL072 pin 2'
    assert nets.same((20, 'F'), rf['p2']) and nets.same((20, 'F'), cf['p2']), f'{which}: 2단 되먹임 입력'
    assert nets.same((19, 'F'), rf['p1']) and nets.same((19, 'F'), cf['p1']), f'{which}: 2단 되먹임 출력'
    assert nets.same((19, 'F'), cout['p1']), f'{which}: TL072 OUT–출력 커패시터'
    assert nets.same((21, 'F'), ground), f'{which}: TL072 2단 +입력'
    assert nets.same((19, 'E'), vplus) and nets.same((22, 'F'), vminus), f'{which}: TL072 전원'

    # 1 Ω은 회로 토폴로지 검사에서만 점퍼선처럼 취급한다.
    low_ohm = Nets()
    low_ohm.parent = dict(nets.parent)
    for p in parts:
        if p['val'] == '1 Ω':
            low_ohm.union(p['p1'], p['p2'])
    assert len({low_ohm.root(vplus), low_ohm.root(ground), low_ohm.root(vminus)}) == 3, f'{which}: 1 Ω 포함 전원 단락'

    if which == 'B1':
        r1 = next(p for p in parts if p['name'] == 'R1')
        r2 = next(p for p in parts if p['name'] == 'R2')
        midpoint = (22, 'E')  # TL072 위 반쪽 +입력(pin 5)
        assert nets.same(midpoint, r1['p2']) and nets.same(midpoint, r2['p2']), 'B1: 분압 중점'
        assert nets.same(r1['p1'], vplus) and nets.same(r2['p1'], vminus), 'B1: 분압 양끝'
        assert nets.same((20, 'E'), ground), 'B1: 가상접지 버퍼 출력'
        assert low_ohm.same((20, 'E'), (21, 'E')), 'B1: 가상접지 버퍼 되먹임'
    else:
        assert not nets.same((20, 'E'), ground), 'B2: 남는 TL072 출력이 GND에 직결됨'
        assert low_ohm.same((20, 'E'), (21, 'E')), 'B2: 남는 TL072 되먹임'
        park = next(p for p in parts if p['name'] == '10 kΩ')
        assert nets.same(park['p1'], (22, 'E')) and nets.same(park['p2'], ground), 'B2: 남는 TL072 +입력'


def filter_values():
    rin = 3_300.0
    c1 = 0.47e-6
    rf = 10_000.0
    cf = 4.7e-9
    hp = 1.0 / (2.0 * math.pi * rin * c1)
    lp = 1.0 / (2.0 * math.pi * rf * cf)
    gain = rf / rin

    def relative_gain(freq):
        highpass = freq / math.hypot(freq, hp)
        lowpass = lp / math.hypot(freq, lp)
        return highpass * lowpass

    at_60 = relative_gain(60.0)
    return hp, lp, gain, at_60, 20.0 * math.log10(at_60)


def main():
    for which, wires, parts, posts, ics in (
        ('B1', D.B1_WIRES, D.B1_PARTS, D.B1_POSTS, D.B1_IC),
        ('B2', D.B2_WIRES, D.B2_PARTS, D.B2_POSTS, D.B2_IC),
    ):
        module = ics[0]
        assert module[4] == ['GND', 'OUT', 'REF', '−VS'] and module[6] == 'E', f'{which}: AD623 윗핀 표기/방향'
        assert module[5] == ['GND', 'IN+', 'IN−', '+VS'] and module[7] == 'I', f'{which}: AD623 아랫핀 표기/방향'
        physical_checks(which, wires, parts, posts, ics)
        electrical_checks(which, wires, parts)
        print(f'✓ {which}: 구멍·레일·모듈 여유·전원·신호 결선 일관성')
    hp, lp, gain, at_60, db_60 = filter_values()
    print(f'✓ 2단: HP {hp:.3f} Hz · LP {lp:.3f} Hz · 중간대역 이득 {gain:.4f}')
    print(f'✓ 60 Hz: 중간대역 대비 {at_60:.4f} ({db_60:.2f} dB)')


if __name__ == '__main__':
    main()
