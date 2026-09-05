# -*- coding: utf-8 -*-
"""브레드보드 배치도 두 장 — 1번 보드(채널 1) · 2번 보드(채널 2).

**꽂을 값이 도면 위에 그대로 적혀 있게 하는 것이 이 도면의 목적이다.**
저항마다 이름 · 값 · 색띠를 함께 그리고, 아래 표에 다시 한 번 값과 하는 일을 적는다.
결선과 값은 「보드자료_AD623.py」 한 곳에서 읽는다 — 여기서 정하지 않는다.
"""
import io, math, os
import 보드자료_AD623 as D
_STEM = '브레드보드_배치도_%s보드'
_OUTDIR = ('장치', '그림')

P = 32.0; X0 = 300.0; CA, CB = 0, 36
SPLIT = 30
ROWS = D.ROWS
JMP = '#1a5fb4'; ALG = '#0f9b8e'; SNP = '#8e44ad'; USB = '#2f2f2f'
RAILR = '#e2a8a8'; RAILB = '#aab8dd'; ORG = '#c0392b'; GRY = '#9a9a9a'
VALC = '#a33'
BODY_R = '#e3cba2'; BODY_C = '#93b7dd'


def twidth(s, fs):
    return sum(fs * (1.0 if ord(ch) > 0x2000 else 0.60) for ch in s)


def sheet(which):
    b1 = which == 'B1'
    wires = D.B1_WIRES if b1 else D.B2_WIRES
    parts = D.B1_PARTS if b1 else D.B2_PARTS
    posts = D.B1_POSTS if b1 else D.B2_POSTS
    ics = D.B1_IC if b1 else D.B2_IC

    notes = getattr(D, 'NOTES', {}).get(which) or [
        ('★ 저항마다 이름 아래 붉은 글씨가 실제로 꽂는 값이다. 몸통의 색띠도 그 값의 띠다. 그래도 꽂기 전에 멀티미터로 잰다 — 색은 헷갈린다.', 1),
        ('★ 차동단 R3 · R3′ · R4 · R4′ 는 10 kΩ 40개를 재서 값이 가장 비슷한 네 개를 골라 쓴다. 여기서 CMRR 이 정해진다.', 1),
        ('★ 5열 J행의 1 Ω 은 예전 Rb2(1 MΩ) 자리다. 전극을 채널마다 하나만 쓰기로 해서 차동단 −쪽을 GND 에 묶는다.', 1),
        ('★ 잭 브레이크아웃은 30–33열 J행에 걸쳐 꽂는다 — 잭 몸통이 핀과 같은 면에 붙어 있어 보드 위에 얹히지 않는다. 몸통이 보드 밖으로 나가야 꽂힌다.', 1),
        ('★ 레일 구멍은 5개마다 한 칸씩 비어 있다 — 5 · 11 · 17 · 23 · 29 열에 구멍이 없다. 레일은 30열 부근에서 끊기므로 레일에 무는 것은 전부 28열 왼쪽이다.', 1),
        ('신호는 아래쪽(F–J)으로 지나가고 위쪽(A–E)은 전원 · 가상접지 · 2단을 쓴다. 2단 출력만 26열에서 아래로 넘어가 잭으로 간다.', 0),
        ('보드는 열 0–60 · 행 A–E / F–J 다. 여기는 0–36 만 그렸다. 선 색 = 실물의 종류 (파랑 점퍼선 · 청록 악어클립 · 보라 건전지 스냅 · 검정 오디오).', 0),
        (('2번 보드는 1번 보드와 자리가 같다. 없는 것은 R1 · R2 와 가상접지 배선뿐이고, 대신 6열 C행에 10 kΩ 이 하나 더 들어간다.'
          if not b1 else
          '1번 보드에만 전원부(R1 · R2 · 가상접지 버퍼)가 있다. 2번 보드는 레일 3줄로 여기서 전원을 받는다.'), 1),
    ]
    HEAD = len(notes)
    RY = {}; y = 122.0 + HEAD * 27 + 196
    for r in ROWS[:5]: RY[r] = y; y += P
    GUT_T = y - P * 0.5; GUT_B = GUT_T + P * 2.3; y = GUT_B + P * 0.5
    for r in ROWS[5:]: RY[r] = y; y += P
    RAIL = {'TV': RY['A'] - 132, 'TG': RY['A'] - 92, 'BG': RY['J'] + 64, 'BV': RY['J'] + 104}
    EDGE = RAIL['BV'] + 42                      # 보드의 물리적 아래 모서리

    def cx(c): return X0 + (c - CA) * P
    def Y(r):
        if r == 'gut': return (GUT_T + GUT_B) / 2 + 6
        return RAIL[r] if r in RAIL else RY[r]

    o = []; a = o.append
    BL = X0 - 84; BR = cx(CB) + 58

    def label2(x, yy, l1, l2, anc, fs1=17, fs2=15):
        w = max(twidth(l1, fs1), twidth(l2, fs2))
        x0 = {'middle': x - w / 2, 'end': x - w}.get(anc, x)
        a(f'<rect x="{x0-6:.0f}" y="{yy-22:.0f}" width="{w+12:.0f}" height="38" rx="4" fill="#fff" opacity="0.92"/>')
        a(f'<text x="{x:.0f}" y="{yy-6:.0f}" font-size="{fs1}" font-weight="700" text-anchor="{anc}" fill="#111">{l1}</text>')
        a(f'<text x="{x:.0f}" y="{yy+11:.0f}" font-size="{fs2}" font-weight="700" text-anchor="{anc}" fill="{VALC}">{l2}</text>')

    def part(p):
        (c1, r1), (c2, r2) = p['p1'], p['p2']
        x1, y1, x2, y2 = cx(c1), Y(r1), cx(c2), Y(r2)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1)); bw = p['bw']
        a(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{GRY}" stroke-width="2.5"/>')
        fill = BODY_C if p['cap'] else BODY_R
        g = [f'<rect x="{-bw/2:.0f}" y="-12" width="{bw:.0f}" height="24" rx="4" fill="{fill}" stroke="#8a7a60" stroke-width="1.5"/>']
        bands = D.BAND.get(p['val'])
        if bands:                                     # 저항 몸통에 그 값의 색띠를 그린다
            span = bw - 12; step = span / 4; bwid = 2.8 if bw > 32 else 2.4
            for k, nm in enumerate(bands):
                g.append(f'<rect x="{-span/2 + k*step - bwid/2:.1f}" y="-11" width="{bwid}" height="22" '
                         f'fill="{D.BANDCOL[nm]}" stroke="#5a5a5a" stroke-width="0.4"/>')
        a(f'<g transform="translate({mx:.0f},{my:.0f}) rotate({ang:.1f})">' + ''.join(g) + '</g>')
        lx, ly = p['lp'](cx, Y) if p['lp'] else (mx, my - 30)
        l1, l2 = (p['short'], p['role']) if p['name'] == p['val'] else (p['name'], p['short'])
        label2(lx, ly, l1, l2, p['anc'])

    # ═══ 머리글 ═══
    ttl = getattr(D, 'TITLE', {}).get(which) or (
        '브레드보드 배치도 — 1번 보드 · 채널 1  (전원부가 여기 있다)' if b1 else
        '브레드보드 배치도 — 2번 보드 · 채널 2  (전원부가 없다 — 레일 3줄을 1번에서 끌어온다)')

    # ═══ 보드 바탕 ═══
    a(f'<rect x="{BL:.0f}" y="{RAIL["TV"]-42:.0f}" width="{BR-BL:.0f}" '
      f'height="{EDGE-(RAIL["TV"]-42):.0f}" rx="10" fill="#fcfcfa" stroke="#c2c2ba" stroke-width="2"/>')
    a(f'<rect x="{BL:.0f}" y="{GUT_T:.0f}" width="{BR-BL:.0f}" height="{GUT_B-GUT_T:.0f}" fill="#ebebe5"/>')
    a(f'<text x="{BL+12:.0f}" y="{(GUT_T+GUT_B)/2+6:.0f}" font-size="15" fill="#8a8a8a">홈</text>')

    def hole(x, yy, s=10):
        a(f'<rect x="{x-s/2:.1f}" y="{yy-s/2:.1f}" width="{s}" height="{s}" rx="1.5" fill="#3a3a3a"/>')
    for key, col, lab in [('TV', RAILR, 'V+'), ('TG', RAILB, 'GND'), ('BG', RAILR, 'GND'), ('BV', RAILB, 'V−')]:
        yy = RAIL[key]
        a(f'<line x1="{cx(CA)-30:.0f}" y1="{yy-18:.0f}" x2="{cx(SPLIT-2)+8:.0f}" y2="{yy-18:.0f}" stroke="{col}" stroke-width="3"/>')
        a(f'<line x1="{cx(SPLIT+1)-8:.0f}" y1="{yy-18:.0f}" x2="{cx(CB)+28:.0f}" y2="{yy-18:.0f}" stroke="{col}" stroke-width="3"/>')
        for c in range(CA, CB + 1):
            if c % 6 != D.RAILGAP and not (SPLIT - 1 <= c <= SPLIT): hole(cx(c), yy, 9)
        a(f'<text x="{BR+12:.0f}" y="{yy+6:.0f}" font-size="21" font-weight="700" fill="#111">{lab}</text>')
    for yy0, yy1 in [(RAIL['TV'], RAIL['TG']), (RAIL['BG'], RAIL['BV'])]:
        a(f'<rect x="{cx(SPLIT-1)-8:.0f}" y="{yy0-34:.0f}" width="{2*P+16:.0f}" height="{yy1-yy0+44:.0f}" '
          f'fill="none" stroke="{ORG}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    a(f'<text x="{cx(SPLIT)+4:.0f}" y="{RAIL["TV"]-48:.0f}" font-size="16" font-weight="700" '
      f'text-anchor="middle" fill="{ORG}">레일만 여기서 끊긴다</text>')
    for r in ROWS:
        for c in range(CA, CB + 1): hole(cx(c), RY[r])
        a(f'<text x="{BL-16:.0f}" y="{RY[r]+6:.0f}" font-size="17" text-anchor="end" fill="#444">{r}</text>')
        a(f'<text x="{BR+14:.0f}" y="{RY[r]+6:.0f}" font-size="17" fill="#444">{r}</text>')

    jspan = range(min(c for c, _ in D.JACK_PINS) - 1, max(c for c, _ in D.JACK_PINS) + 2)
    def colnums():
        for c in range(CA, CB + 1):
            if c % 5 == 0:
                for ty in ([RY['A'] - 16] if c in jspan else [RY['A'] - 16, RY['J'] + 26]):
                    a(f'<rect x="{cx(c)-11:.0f}" y="{ty-13:.0f}" width="22" height="17" rx="3" fill="#fff" opacity="0.92"/>')
                    a(f'<text x="{cx(c):.0f}" y="{ty:.0f}" font-size="15" text-anchor="middle" fill="#444">{c}</text>')
    colnums()

    # ═══ IC ═══
    for ic in ics:
        c0, name, sub1, sub2 = ic[:4]
        top = ic[4] if len(ic) > 4 else [str(8 - i) for i in range(4)]
        bot = ic[5] if len(ic) > 5 else [str(1 + i) for i in range(4)]
        top_row = ic[6] if len(ic) > 6 else 'E'
        bot_row = ic[7] if len(ic) > 7 else 'F'
        fsp = 14 if max(len(x) for x in top + bot) < 3 else 11
        is_module = len(ic) > 7
        body_top = Y(top_row) - (18 if is_module else Y(top_row) - GUT_T - 4)
        body_bottom = Y(bot_row) + (18 if is_module else GUT_B - Y(bot_row) - 4)
        a(f'<rect x="{cx(c0)-P*0.45:.0f}" y="{body_top:.0f}" width="{3*P+P*0.9:.0f}" '
          f'height="{body_bottom-body_top:.0f}" rx="5" fill="#3b3b3b"/>')
        cy = (body_top + body_bottom) / 2
        a(f'<circle cx="{cx(c0)-P*0.45+14:.0f}" cy="{cy:.0f}" r="8" fill="#606060"/>')
        for i in range(4):
            a(f'<line x1="{cx(c0+i):.0f}" y1="{Y(top_row):.0f}" x2="{cx(c0+i):.0f}" y2="{body_top:.0f}" stroke="{GRY}" stroke-width="5"/>')
            a(f'<line x1="{cx(c0+i):.0f}" y1="{body_bottom:.0f}" x2="{cx(c0+i):.0f}" y2="{Y(bot_row):.0f}" stroke="{GRY}" stroke-width="5"/>')
            a(f'<rect x="{cx(c0+i)-18:.0f}" y="{Y(top_row)-27:.0f}" width="36" height="17" rx="3" fill="#fff" opacity="0.92"/>')
            a(f'<text x="{cx(c0+i):.0f}" y="{Y(top_row)-14:.0f}" font-size="{fsp}" font-weight="700" text-anchor="middle" fill="#111">{top[i]}</text>')
            bot_box_y = Y(bot_row) - 27 if is_module else Y(bot_row) + 13
            bot_text_y = Y(bot_row) - 14 if is_module else Y(bot_row) + 26
            a(f'<rect x="{cx(c0+i)-18:.0f}" y="{bot_box_y:.0f}" width="36" height="17" rx="3" fill="#fff" opacity="0.92"/>')
            a(f'<text x="{cx(c0+i):.0f}" y="{bot_text_y:.0f}" font-size="{fsp}" font-weight="700" text-anchor="middle" fill="#111">{bot[i]}</text>')
        a(f'<text x="{cx(c0+1.6):.0f}" y="{cy-8:.0f}" font-size="16" font-weight="700" text-anchor="middle" fill="#fff">{name}</text>')
        a(f'<text x="{cx(c0+1.6):.0f}" y="{cy+9:.0f}" font-size="11" text-anchor="middle" fill="#d8d8d0">{sub1}</text>')
        a(f'<text x="{cx(c0+1.6):.0f}" y="{cy+24:.0f}" font-size="11" text-anchor="middle" fill="#d8d8d0">{sub2}</text>')

    # ═══ 배선 ═══
    def wire(p1, p2, col=JMP):
        (c1, r1), (c2, r2) = p1, p2
        a(f'<path d="M {cx(c1):.0f} {Y(r1):.0f} L {cx(c2):.0f} {Y(r2):.0f}" stroke="{col}" '
          f'stroke-width="6.5" fill="none" stroke-linecap="round" opacity="0.9"/>')
        a(f'<circle cx="{cx(c1):.0f}" cy="{Y(r1):.0f}" r="6" fill="{col}"/>'
          f'<circle cx="{cx(c2):.0f}" cy="{Y(r2):.0f}" r="6" fill="{col}"/>')
    for w in wires: wire(*w)

    # ═══ 부품 ═══
    for p in parts: part(p)
    for c in D.CD_COLS:                       # 디커플링 — 이름표는 한 줄로 짧게
        for r0, r1 in (('TV', 'TG'), ('BG', 'BV')):
            x, ym = cx(c), (Y(r0) + Y(r1)) / 2
            a(f'<line x1="{x:.0f}" y1="{Y(r0):.0f}" x2="{x:.0f}" y2="{Y(r1):.0f}" stroke="{GRY}" stroke-width="2.5"/>')
            a(f'<rect x="{x-14:.0f}" y="{ym-11:.0f}" width="28" height="22" rx="4" fill="{BODY_C}" stroke="#8a7a60" stroke-width="1.5"/>')
            a(f'<rect x="{x+16:.0f}" y="{ym-11:.0f}" width="44" height="20" rx="3" fill="#fff" opacity="0.92"/>')
            a(f'<text x="{x+18:.0f}" y="{ym+5:.0f}" font-size="15" font-weight="700" fill="{VALC}">104</text>')

    # ═══ 잭 브레이크아웃 — 보드에 못 꽂는다. 암–수 점퍼선 4개로 잇는다 ═══
    a(f'<line x1="{BL:.0f}" y1="{EDGE:.0f}" x2="{BR:.0f}" y2="{EDGE:.0f}" '
      f'stroke="#8a8a8a" stroke-width="2" stroke-dasharray="8 5"/>')
    a(f'<text x="{BL+10:.0f}" y="{EDGE+22:.0f}" font-size="15" fill="#666">'
      f'← 여기까지가 브레드보드. 아래는 책상 위다 →</text>')
    jc = [c for c, _ in D.JACK_PINS]
    MX0 = cx(max(jc)) + 150          # 모듈은 보드 오른쪽 아래 책상에 놓는다
    MY0 = EDGE + 92
    MW, MH = 150, 190
    a(f'<rect x="{MX0:.0f}" y="{MY0:.0f}" width="{MW}" height="{MH}" rx="6" '
      f'fill="#8f2b2b" stroke="#5e1616" stroke-width="2"/>')
    a(f'<text x="{MX0+MW/2:.0f}" y="{MY0+MH-16:.0f}" font-size="13" font-weight="700" '
      f'text-anchor="middle" fill="#fff">TRRS Breakout</text>')
    # 잭 몸통 — 구멍이 왼쪽을 본다
    sy = MY0 + MH - 62
    a(f'<rect x="{MX0+8:.0f}" y="{sy-26:.0f}" width="{MW-16}" height="52" rx="5" fill="#242424"/>')
    a(f'<rect x="{MX0-26:.0f}" y="{sy-15:.0f}" width="34" height="30" rx="6" fill="#2b2b2b"/>')
    a(f'<circle cx="{MX0-14:.0f}" cy="{sy:.0f}" r="9" fill="#0b0d10" stroke="#8d939c" stroke-width="2"/>')
    a(f'<text x="{MX0+MW/2+6:.0f}" y="{sy+5:.0f}" font-size="12" text-anchor="middle" fill="#bbb">3.5 mm 암</text>')
    # 핀 4개와 암–수 점퍼선
    for k, (c, nm) in enumerate(D.JACK_PINS):
        short = {'TIP': 'T', 'RING1': 'R1', 'RING2': 'R2', 'SLEEVE': 'S'}[nm]
        px = MX0 + 26 + k * 33; py = MY0 + 16
        a(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="7" fill="#d9b34a" stroke="#7a5f18" stroke-width="2"/>')
        a(f'<text x="{px:.0f}" y="{py-14:.0f}" font-size="13" font-weight="700" '
          f'text-anchor="middle" fill="#8f2b2b">{short}</text>')
        # 점퍼선 — 보드 J행 구멍까지
        bx, by = cx(c), RY['J']
        mid = EDGE + 40 + k * 11
        a(f'<path d="M {bx:.0f} {by:.0f} L {bx:.0f} {mid:.0f} L {px:.0f} {mid:.0f} L {px:.0f} {py:.0f}" '
          f'stroke="#0f9b8e" stroke-width="4" fill="none" stroke-linejoin="round" opacity="0.9"/>')
        a(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="6" fill="#0f9b8e"/>')
        a(f'<rect x="{bx-14:.0f}" y="{by+11:.0f}" width="28" height="18" rx="3" fill="#fff" opacity="0.95"/>')
        a(f'<text x="{bx:.0f}" y="{by+25:.0f}" font-size="13" font-weight="700" '
          f'text-anchor="middle" fill="#0f9b8e">{short}</text>')
    jn, jt = D.JACK_POST[which]
    a(f'<path d="M {MX0-52:.0f} {sy:.0f} L {MX0-26:.0f} {sy:.0f}" stroke="{USB}" stroke-width="7" stroke-linecap="round"/>')
    a(f'<rect x="{MX0-88:.0f}" y="{sy-6:.0f}" width="40" height="12" rx="3" fill="#b9bcc2"/>')
    a(f'<path d="M {MX0-88:.0f} {sy:.0f} L {cx(3):.0f} {sy:.0f}" stroke="{USB}" stroke-width="7" stroke-linecap="round"/>')
    a(f'<circle cx="{cx(3):.0f}" cy="{sy:.0f}" r="16" fill="#fff" stroke="{USB}" stroke-width="3.5"/>')
    a(f'<text x="{cx(3):.0f}" y="{sy+6:.0f}" font-size="16" font-weight="700" text-anchor="middle" fill="#222">{jn}</text>')
    a(f'<text x="{cx(3)+26:.0f}" y="{sy+32:.0f}" font-size="16" fill="#111">{jt}</text>')
    a(f'<text x="{MX0+MW+18:.0f}" y="{MY0+24:.0f}" font-size="16" font-weight="700" fill="{ORG}">암–수 점퍼선 4개</text>')
    a(f'<text x="{MX0+MW+18:.0f}" y="{MY0+46:.0f}" font-size="15" fill="#444">암 쪽 → 모듈의 수핀</text>')
    a(f'<text x="{MX0+MW+18:.0f}" y="{MY0+66:.0f}" font-size="15" fill="#444">수 쪽 → 보드 J행</text>')
    jy1 = MY0 + MH
    ny = jy1 + 34
    for k, (t, warn) in enumerate(getattr(D, 'JACKNOTE', None) or [
            ('★ 브레이크아웃은 브레드보드에 꽂을 수 없다 — 잭 몸통이 걸려 레일 줄에만 닿는데, 레일 한 줄은 통째로 한 노드라 핀 4개가 전부 단락된다 (2026-09-05 실물 확인).', 1),
            ('★ 그래서 모듈은 보드 옆 책상에 두고 암–수 점퍼선 4개로 잇는다. 암 쪽을 모듈의 수핀에 끼우고 수 쪽을 보드 J행에 꽂는다. 채널마다 4개, 두 채널 8개.', 1),
            ('★ 실물 인쇄를 보고 TIP 이 33열에 가게만 맞추면 된다. 나머지 셋(RING1 · RING2 · SLEEVE)은 어차피 전부 GND 로 묶인다.', 1),
            ('점퍼선이 길면 케이블타이로 묶는다 — 벌어지면 그 사이가 고리가 되어 60 Hz 를 줍는다.', 0)]):
        a(f'<text x="{BL:.0f}" y="{ny + k*24:.0f}" font-size="16" fill="{ORG if warn else "#444"}" '
          f'font-weight="{700 if warn else 400}">{t}</text>')
    return_y = ny + 4 * 24

    # ═══ 보드 밖으로 나가는 자리 ═══
    for (c, r), num, col, what in posts:
        if c == 0:
            x2 = cx(0) - 96
            a(f'<line x1="{x2:.0f}" y1="{Y(r):.0f}" x2="{cx(0):.0f}" y2="{Y(r):.0f}" stroke="{col}" stroke-width="6.5" stroke-linecap="round"/>')
        a(f'<circle cx="{cx(c):.0f}" cy="{Y(r):.0f}" r="15" fill="#fff" stroke="{col}" stroke-width="3.5"/>')
        a(f'<text x="{cx(c):.0f}" y="{Y(r)+6:.0f}" font-size="16" font-weight="700" text-anchor="middle" fill="#333">{num}</text>')
    for (c, r), num, col, what in posts:
        if c == 1:      # 건전지 스냅 — 레일 밖으로 짧게 뺀다
            a(f'<line x1="{cx(1):.0f}" y1="{Y(r):.0f}" x2="{cx(1)-60:.0f}" y2="{Y(r):.0f}" stroke="{col}" stroke-width="6.5" stroke-linecap="round"/>')
            a(f'<circle cx="{cx(c):.0f}" cy="{Y(r):.0f}" r="15" fill="#fff" stroke="{col}" stroke-width="3.5"/>')
            a(f'<text x="{cx(c):.0f}" y="{Y(r)+6:.0f}" font-size="16" font-weight="700" text-anchor="middle" fill="#333">{num}</text>')
    colnums()

    # ═══ 번호 · 부품표 ═══
    ly = return_y + 40
    a(f'<text x="{BL:.0f}" y="{ly:.0f}" font-size="21" font-weight="700" fill="#111">보드 밖으로 나가는 자리</text>')
    seen_n = []
    for (c, r), num, col, what in posts:
        if not any(n == num for n, _, _ in seen_n): seen_n.append((num, col, what))
    seen_n.append((jn, USB, jt))
    for i, (num, col, what) in enumerate(seen_n):
        x = BL + 250 + (i % 2) * 800; yy = ly + (i // 2) * 32
        a(f'<circle cx="{x:.0f}" cy="{yy-6:.0f}" r="14" fill="#fff" stroke="{col}" stroke-width="3"/>')
        a(f'<text x="{x:.0f}" y="{yy:.0f}" font-size="15" font-weight="700" text-anchor="middle" fill="#222">{num}</text>')
        a(f'<text x="{x+24:.0f}" y="{yy:.0f}" font-size="16" fill="#333">{what}</text>')
    ty = ly + ((len(seen_n) + 1) // 2) * 32 + 64

    a(f'<text x="{BL:.0f}" y="{ty-34:.0f}" font-size="24" font-weight="700" fill="#111">'
      f'무엇을 몇 개 꽂나 — {"1번 보드" if b1 else "2번 보드"}</text>')
    cols = [BL, BL + 132, BL + 300, BL + 470, BL + 560]
    for x, t in zip(cols, ['이름', '값', '색띠', '개수', '하는 일 · 어디에']):
        a(f'<text x="{x:.0f}" y="{ty:.0f}" font-size="18" font-weight="700" fill="#111">{t}</text>')
    a(f'<line x1="{BL:.0f}" y1="{ty+10:.0f}" x2="{BR:.0f}" y2="{ty+10:.0f}" stroke="#c9c9c2" stroke-width="2"/>')

    seen = []
    for p in parts:
        key = (p['name'], p['val'])
        for s in seen:
            if s['key'] == key:
                s['n'] += 1; s['where'].append(p['p1']); break
        else:
            seen.append(dict(key=key, n=1, role=p['role'], where=[p['p1']]))
    for s in seen:                       # 여러 군데 들어가는 것은 자리를 적는다
        if s['n'] > 1:
            s['role'] = s['role'].lstrip('★ ') + ' — ' + ' · '.join(f'{c}열 {r}행' for c, r in s['where'])
    seen.append(dict(key=('Cd', D.CAPVAL['Cd']), n=2 * len(D.CD_COLS),
                     role='IC 전원핀 가까이 — ' + ' · '.join(f'{c}열' for c in D.CD_COLS)))
    rows = [(k[0], k[1], s['n'], s['role']) for s in seen for k in [s['key']]]
    rows += [('IC', ' · '.join(i[1] for i in ics), len(ics),
              '홈에 걸쳐 꽂는다 — ' + ' · '.join(f'{i[0]}열' for i in ics)),
             ('잭 브레이크아웃', 'TRRS · 보드 옆에', 1, '★ 암–수 점퍼선 4개로 30–33열 J행에 · TIP 이 33열'),
             ('수–수 점퍼선', '—', len(wires), '파란 선 · 위 표에 없는 연결은 전부 점퍼선이다')]
    for i, (nm, val, n, role) in enumerate(rows):
        yy = ty + 40 + i * 30
        a(f'<text x="{cols[0]:.0f}" y="{yy:.0f}" font-size="17" font-weight="700" fill="#111">{nm}</text>')
        a(f'<text x="{cols[1]:.0f}" y="{yy:.0f}" font-size="17" font-weight="700" fill="{VALC}">{val}</text>')
        bands = D.BAND.get(val)
        if bands:
            a(f'<rect x="{cols[2]:.0f}" y="{yy-15:.0f}" width="76" height="20" rx="3" fill="{BODY_R}" stroke="#8a7a60" stroke-width="1"/>')
            for k, cn in enumerate(bands):
                a(f'<rect x="{cols[2]+8+k*13:.0f}" y="{yy-14:.0f}" width="4.5" height="18" fill="{D.BANDCOL[cn]}" stroke="#5a5a5a" stroke-width="0.4"/>')
            a(f'<text x="{cols[2]+84:.0f}" y="{yy:.0f}" font-size="14" fill="#555">{" ".join(bands)}</text>')
        a(f'<text x="{cols[3]:.0f}" y="{yy:.0f}" font-size="17" fill="#111">{n}개</text>')
        a(f'<text x="{cols[4]:.0f}" y="{yy:.0f}" font-size="16" fill="{ORG if role.startswith("★") else "#444"}" '
          f'font-weight="{700 if role.startswith("★") else 400}">{role}</text>')
    fy = ty + 40 + len(rows) * 30 + 18
    for k, t in enumerate([
        '★ 1 Ω 은 옆 열끼리(2.54 mm) 잇는다. 몸통이 6.3 mm 라 눕지 않으니 다리를 ㄷ자로 꺾어 세워 꽂는다. 그림은 자리를 보이려고 눕혀 그렸다.',
        '★ 링 두 개(R1 · R2)를 SLEEVE 에 묶는 것은 3극 케이블을 꽂아도 링이 뜨지 않게 하려는 것이다. 1 Ω 은 점퍼선 대신이고 전기적으로 같다.']):
        a(f'<text x="{BL:.0f}" y="{fy + k*26:.0f}" font-size="16" fill="{ORG}" font-weight="700">{t}</text>')

    H = fy + 2 * 26 + 40; W = max(cx(CB) + 320, MX0 + MW + 320)
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
            f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="Noto Sans CJK KR, sans-serif">'
            f'<rect width="{W:.0f}" height="{H:.0f}" fill="#fff"/>',
            f'<text x="{BL:.0f}" y="72" font-size="31" font-weight="700" fill="#111">{ttl}</text>']
    for i, (t, warn) in enumerate(notes):
        head.append(f'<text x="{BL:.0f}" y="{106 + i*27:.0f}" font-size="17" '
                    f'fill="{ORG if warn else "#444"}" font-weight="{700 if warn else 400}">{t}</text>')
    return '\n'.join(head + o + ['</svg>'])


import cairosvg
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', *_OUTDIR))
for which, stem in (('B1', _STEM % '1번'), ('B2', _STEM % '2번')):
    svg = sheet(which)
    s = os.path.join(OUT, stem + '.svg'); p = os.path.join(OUT, stem + '.png')
    io.open(s, 'w', encoding='utf-8').write(svg)
    cairosvg.svg2png(url=s, write_to=p, output_width=2000)
    print('저장:', s, '·', p)
