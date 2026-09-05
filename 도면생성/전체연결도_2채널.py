# -*- coding: utf-8 -*-
"""2채널 전체 연결도 — 그림 한 장. 실험실에는 이것만 들고 간다.
1번 보드는 이미 만든 것, 2번 보드가 새로 만들 것. 전원은 1번에서 끌어온다.
결선·부품값·번호는 「보드자료_AD623.py」 한 곳에서 읽는다 — 배치도 두 장과 같은 자료다."""
import io, math
import 보드자료_AD623 as D
_STEM = '전체연결도_2채널'
_OUTDIR = ('장치', '그림')

W, H = 3700, 2800
o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'font-family="Noto Sans CJK KR, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>')

JMP = '#1a5fb4'; ALG = '#0f9b8e'; SNP = '#8e44ad'; USB = '#2f2f2f'
RAILR = '#e2a8a8'; RAILB = '#aab8dd'; ORG = '#c0392b'; GRY = '#9a9a9a'; VALC = '#a33'
P = 32.0; CA, CB = 0, 36
SPLIT = 30


def T(x, y, s, fs=18, fill='#111', w='400', anc='start'):
    a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="{w}" fill="{fill}" text-anchor="{anc}">{s}</text>')


def panel(x, y, w, h, title, fill='#fbfbf9', tc='#111'):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#c9c9c2" stroke-width="2"/>')
    if title: T(x + 16, y - 14, title, 26, tc, '700')


def wirepath(d, col, w=8, halo=True):
    if halo: a(f'<path d="{d}" stroke="#fff" stroke-width="{w+10}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def dot(x, y, col, r=8): a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}"/>')


def Rp(pts, rad=20):
    d = f'M {pts[0][0]:.0f} {pts[0][1]:.0f}'
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i-1]; x, y = pts[i]; x1, y1 = pts[i+1]
        v0 = (x - x0, y - y0); v1 = (x1 - x, y1 - y)
        l0 = math.hypot(*v0) or 1; l1 = math.hypot(*v1) or 1
        r = min(rad, l0 / 2, l1 / 2)
        d += (f' L {x-v0[0]/l0*r:.0f} {y-v0[1]/l0*r:.0f} Q {x:.0f} {y:.0f}'
              f' {x+v1[0]/l1*r:.0f} {y+v1[1]/l1*r:.0f}')
    return d + f' L {pts[-1][0]:.0f} {pts[-1][1]:.0f}'


def postmark(x, y, lab, col):
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="#fff" stroke="{col}" stroke-width="4"/>')
    T(x, y + 7, lab, 17, '#222', '700', 'middle')


def twidth(s, fs): return sum(fs * (1.0 if ord(ch) > 0x2000 else 0.60) for ch in s)


# ───────── 브레드보드 한 장 ─────────
ROWS = D.ROWS


def board(OX, OY, which, name, sub, note):
    wires = D.B1_WIRES if which == 'B1' else D.B2_WIRES
    parts = D.B1_PARTS if which == 'B1' else D.B2_PARTS
    posts = D.B1_POSTS if which == 'B1' else D.B2_POSTS
    RY = {}; y = OY + 108.0
    for r in ROWS[:5]: RY[r] = y; y += P
    GT = y - P * 0.5; GB = GT + P * 2.3; y = GB + P * 0.5
    for r in ROWS[5:]: RY[r] = y; y += P
    RAIL = {'TV': OY + 16.0, 'TG': OY + 56.0, 'BG': RY['J'] + 64, 'BV': RY['J'] + 104}
    EDGE = RAIL['BV'] + 42

    def cx(c): return OX + c * P
    def Y(r):
        if r == 'gut': return (GT + GB) / 2 + 6
        return RAIL[r] if r in RAIL else RY[r]
    BL = OX - 84; BR = cx(CB) + 58
    a(f'<rect x="{BL:.0f}" y="{RAIL["TV"]-42:.0f}" width="{BR-BL:.0f}" '
      f'height="{EDGE-(RAIL["TV"]-42):.0f}" rx="10" fill="#fcfcfa" stroke="#c2c2ba" stroke-width="2"/>')
    a(f'<rect x="{BL:.0f}" y="{GT:.0f}" width="{BR-BL:.0f}" height="{GB-GT:.0f}" fill="#ebebe5"/>')

    def hole(x, yy, s=10): a(f'<rect x="{x-s/2:.1f}" y="{yy-s/2:.1f}" width="{s}" height="{s}" rx="1.5" fill="#3a3a3a"/>')
    for key, col, lab in [('TV', RAILR, 'V+'), ('TG', RAILB, 'GND'), ('BG', RAILR, 'GND'), ('BV', RAILB, 'V−')]:
        yy = RAIL[key]
        a(f'<line x1="{cx(CA)-30:.0f}" y1="{yy-18:.0f}" x2="{cx(SPLIT-2)+8:.0f}" y2="{yy-18:.0f}" stroke="{col}" stroke-width="3"/>')
        a(f'<line x1="{cx(SPLIT+1)-8:.0f}" y1="{yy-18:.0f}" x2="{cx(CB)+28:.0f}" y2="{yy-18:.0f}" stroke="{col}" stroke-width="3"/>')
        for c in range(CA, CB + 1):
            if c % 6 != D.RAILGAP and not (SPLIT - 1 <= c <= SPLIT): hole(cx(c), yy, 9)
        T(BR + 12, yy + 7, lab, 21, '#111', '700')
    for yy0, yy1 in [(RAIL['TV'], RAIL['TG']), (RAIL['BG'], RAIL['BV'])]:
        a(f'<rect x="{cx(SPLIT-1)-8:.0f}" y="{yy0-30:.0f}" width="{2*P+16:.0f}" height="{yy1-yy0+40:.0f}" '
          f'fill="none" stroke="{ORG}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    for r in ROWS:
        for c in range(CA, CB + 1): hole(cx(c), RY[r])
        T(BL - 14, RY[r] + 6, r, 17, '#444', '400', 'end'); T(BR + 12, RY[r] + 6, r, 17, '#444')

    def wire(p1, p2, col=JMP):
        x1, y1 = cx(p1[0]), Y(p1[1]); x2, y2 = cx(p2[0]), Y(p2[1])
        wirepath(f'M {x1:.0f} {y1:.0f} L {x2:.0f} {y2:.0f}', col, 7)
        dot(x1, y1, col, 7); dot(x2, y2, col, 7)

    def label2(x, yy, l1, l2, anc):
        w = max(twidth(l1, 16), twidth(l2, 14))
        x0 = {'middle': x - w / 2, 'end': x - w}.get(anc, x)
        a(f'<rect x="{x0-5:.0f}" y="{yy-21:.0f}" width="{w+10:.0f}" height="36" rx="4" fill="#fff" opacity="0.93"/>')
        T(x, yy - 6, l1, 16, '#111', '700', anc); T(x, yy + 10, l2, 14, VALC, '700', anc)

    def part(p, bwx=1.0):
        (c1, r1), (c2, r2) = p['p1'], p['p2']
        x1, y1 = cx(c1), Y(r1); x2, y2 = cx(c2), Y(r2)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2; ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        bw = p['bw'] * bwx
        wirepath(f'M {x1:.0f} {y1:.0f} L {x2:.0f} {y2:.0f}', GRY, 3, False)
        fill = '#93b7dd' if p['cap'] else '#e3cba2'
        g = [f'<rect x="{-bw/2:.0f}" y="-13" width="{bw:.0f}" height="26" rx="4" fill="{fill}" stroke="#8a7a60" stroke-width="2"/>']
        bands = D.BAND.get(p['val'])
        if bands:
            span = bw - 12; step = span / 4; bwid = 2.8 if bw > 32 else 2.4
            for k, nm in enumerate(bands):
                g.append(f'<rect x="{-span/2 + k*step - bwid/2:.1f}" y="-12" width="{bwid}" height="24" '
                         f'fill="{D.BANDCOL[nm]}" stroke="#5a5a5a" stroke-width="0.4"/>')
        a(f'<g transform="translate({mx:.0f},{my:.0f}) rotate({ang:.1f})">' + ''.join(g) + '</g>')
        lx, ly = p['lp'](cx, Y)
        l1, l2 = (p['short'], p['role']) if p['name'] == p['val'] else (p['name'], p['short'])
        label2(lx, ly, l1, l2, p['anc'])

    for ic in (D.B1_IC if which == 'B1' else D.B2_IC):
        c0, nm, s1, s2 = ic[:4]
        top = ic[4] if len(ic) > 4 else [str(8 - k) for k in range(4)]
        bot = ic[5] if len(ic) > 5 else [str(1 + k) for k in range(4)]
        top_row = ic[6] if len(ic) > 6 else 'E'
        bot_row = ic[7] if len(ic) > 7 else 'F'
        fsp = 15 if max(len(x) for x in top + bot) < 3 else 11
        x0, x1 = cx(c0) - 15, cx(c0 + 3) + 15
        is_module = len(ic) > 7
        body_top = Y(top_row) - (18 if is_module else Y(top_row) - GT + 6)
        body_bottom = Y(bot_row) + (18 if is_module else GB - Y(bot_row) + 6)
        a(f'<rect x="{x0:.0f}" y="{body_top:.0f}" width="{x1-x0:.0f}" height="{body_bottom-body_top:.0f}" rx="7" fill="#3a3a3a"/>')
        cy = (body_top + body_bottom) / 2
        a(f'<circle cx="{x0+13:.0f}" cy="{cy:.0f}" r="6" fill="#777"/>')
        for k in range(4):
            a(f'<line x1="{cx(c0+k):.0f}" y1="{Y(top_row):.0f}" x2="{cx(c0+k):.0f}" y2="{body_top:.0f}" stroke="{GRY}" stroke-width="4"/>')
            a(f'<line x1="{cx(c0+k):.0f}" y1="{body_bottom:.0f}" x2="{cx(c0+k):.0f}" y2="{Y(bot_row):.0f}" stroke="{GRY}" stroke-width="4"/>')
            a(f'<rect x="{cx(c0+k)-19:.0f}" y="{Y(bot_row)-21:.0f}" width="38" height="17" rx="3" fill="#fff" opacity="0.92"/>')
            T(cx(c0 + k), Y(bot_row) - 8, bot[k], fsp, '#111', '700', 'middle')
            a(f'<rect x="{cx(c0+k)-19:.0f}" y="{Y(top_row)+9:.0f}" width="38" height="17" rx="3" fill="#fff" opacity="0.92"/>')
            T(cx(c0 + k), Y(top_row) + 22, top[k], fsp, '#111', '700', 'middle')
        T(cx(c0) + 50, cy - 4, nm, 19, '#fff', '700', 'middle')
        T(cx(c0) + 50, cy + 18, s1, 12, '#ccc', '400', 'middle')
        T(cx(c0) + 50, cy + 34, s2, 12, '#ccc', '400', 'middle')
    for w in wires: wire(*w)
    for p in parts: part(p)
    for c in D.CD_COLS:
        for r0, r1 in (('TV', 'TG'), ('BG', 'BV')):
            x, ym = cx(c), (Y(r0) + Y(r1)) / 2
            a(f'<line x1="{x:.0f}" y1="{Y(r0):.0f}" x2="{x:.0f}" y2="{Y(r1):.0f}" stroke="{GRY}" stroke-width="2.5"/>')
            a(f'<rect x="{x-13:.0f}" y="{ym-11:.0f}" width="26" height="22" rx="4" fill="#93b7dd" stroke="#8a7a60" stroke-width="1.5"/>')
            a(f'<rect x="{x+15:.0f}" y="{ym-11:.0f}" width="42" height="20" rx="3" fill="#fff" opacity="0.93"/>')
            T(x + 17, ym + 5, '104', 15, VALC, '700')

    # ── 잭 브레이크아웃 — 보드에 못 꽂는다. 암–수 점퍼선 4개로 보드 옆 모듈에 잇는다 ──
    jc = [c for c, _ in D.JACK_PINS]
    a(f'<line x1="{BL:.0f}" y1="{EDGE:.0f}" x2="{BR:.0f}" y2="{EDGE:.0f}" '
      f'stroke="#8a8a8a" stroke-width="2" stroke-dasharray="8 5"/>')
    MX0, MY0, MW, MH = cx(max(jc)) + 128, EDGE + 76, 140, 170
    a(f'<rect x="{MX0:.0f}" y="{MY0:.0f}" width="{MW}" height="{MH}" rx="6" fill="#8f2b2b" stroke="#5e1616" stroke-width="2"/>')
    T(MX0 + MW / 2, MY0 + MH - 14, 'TRRS Breakout', 13, '#fff', '700', 'middle')
    sy = MY0 + MH - 56
    a(f'<rect x="{MX0+8:.0f}" y="{sy-24:.0f}" width="{MW-16}" height="48" rx="5" fill="#242424"/>')
    a(f'<rect x="{MX0-26:.0f}" y="{sy-15:.0f}" width="34" height="30" rx="6" fill="#2b2b2b"/>')
    a(f'<circle cx="{MX0-14:.0f}" cy="{sy:.0f}" r="9" fill="#0b0d10" stroke="#8d939c" stroke-width="2"/>')
    T(MX0 + MW / 2 + 6, sy + 5, '3.5 mm 암', 12, '#bbb', '400', 'middle')
    for k, (c, nm) in enumerate(D.JACK_PINS):
        short = {'TIP': 'T', 'RING1': 'R1', 'RING2': 'R2', 'SLEEVE': 'S'}[nm]
        px, py = MX0 + 24 + k * 31, MY0 + 15
        bx, by = cx(c), RY['J']
        mid = EDGE + 30 + k * 10
        a(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="6" fill="#d9b34a" stroke="#7a5f18" stroke-width="2"/>')
        a(f'<path d="M {bx:.0f} {by:.0f} L {bx:.0f} {mid:.0f} L {px:.0f} {mid:.0f} L {px:.0f} {py:.0f}" '
          f'stroke="{ALG}" stroke-width="4" fill="none" stroke-linejoin="round" opacity="0.9"/>')
        dot(bx, by, ALG, 6)
        a(f'<rect x="{bx-14:.0f}" y="{by+11:.0f}" width="28" height="18" rx="3" fill="#fff" opacity="0.95"/>')
        T(bx, by + 25, short, 13, ALG, '700', 'middle')
    T(MX0 + MW + 14, MY0 + 22, '암–수 점퍼선 4개', 16, ORG, '700')
    T(MX0 + MW + 14, MY0 + 44, '보드에 직접 못 꽂는다', 14, '#555')

    out = {lab: (cx(c), Y(r)) for (c, r), lab, _, _ in posts}
    out['posts'] = [(cx(c), Y(r), lab, col) for (c, r), lab, col, _ in posts]
    out['plug'] = (MX0 - 40, sy)
    out['cx'] = cx; out['Y'] = Y; out['BL'] = BL; out['BR'] = BR; out['EDGE'] = EDGE
    T(BL, RAIL['TV'] - 58, note, 25, '#111', '700')
    return out


# ═══════════ 머리글 ═══════════
T(50, 62, '2채널 전체 연결도 — AD623 계측증폭기 × 2 · 컴퓨터 녹음 · 실물 방향 최종 연결본',
  40, '#111', '700')
T(50, 100, '전극은 3개다 — 채널마다 기록 전극 하나 + 두 채널이 기준(접지) 전극 하나를 함께 쓴다.  '
           '2번 보드는 1번을 그대로 한 벌 더 만든 것이고 전원부만 없다 — 레일 3줄을 1번에서 끌어온다.  '
           '저항의 붉은 글씨가 꽂는 값이다.'
           '  AD623: 위 GND·OUT·REF·−VS / 아래 GND·IN+·IN−·+VS.', 21, '#555')

OX = 900
_b1_note = '1번 보드 — 채널 1 (완성된 개별 배치 · 전원부가 여기 있다)'
_b2_note = '2번 보드 — 채널 2 (완성된 개별 배치 · 전원부는 없다)'
b1 = board(OX, 300, 'B1', None, None, _b1_note)
b2 = board(OX, 1320, 'B2', None, None, _b2_note)
cx = b1['cx']

# ═══════════ 배선이 지나는 세로 길 ═══════════
L1, L3, L5 = 526, 574, 622                # ① ② ③ 전극
LVN = 676                                 # 건전지 검정
J1, J2, J3 = 712, 742, 772                # 레일 3줄 (V+ · GND · V−)
AUD1, AUD2 = 2170, 2214                   # 오디오 케이블 두 가닥

# ═══════════ 레일 3줄 — 1번 → 2번 ═══════════
for lane, k1, k2, lab in [(J1, 'TV', 'TV', 'V+'), (J2, 'BG', 'TG', 'GND'), (J3, 'BV', 'BV', 'V−')]:
    y1 = b1['Y'](k1); y2 = b2['Y'](k2)
    wirepath(Rp([(cx(0), y1), (lane, y1), (lane, y2), (cx(0), y2)], 18), JMP, 7)
    dot(cx(0), y1, JMP, 7); dot(cx(0), y2, JMP, 7)
a('<rect x="960" y="1062" width="700" height="92" rx="8" fill="#fff" opacity="0.95"/>')
T(980, 1094, '④ 레일 3줄 — 1번 보드 0열 → 2번 보드 0열', 22, ORG, '700')
T(980, 1128, '위 V+ → 위 V+ · 아래 GND → 위 GND · 아래 V− → 아래 V−', 19, '#555')

# ═══════════ 건전지 ═══════════
panel(90, 250, 380, 270, '전원')
a('<rect x="180" y="300" width="130" height="180" rx="12" fill="#3a3a3a"/>')
T(245, 398, '9 V', 31, '#fff', '700', 'middle'); T(245, 432, '건전지 1개', 16, '#bbb', '400', 'middle')
T(390, 352, '빨강', 18, SNP, '700', 'middle'); T(390, 462, '검정', 18, SNP, '700', 'middle')
wirepath(Rp([(340, 330), (600, 330), (600, 296), (880, 296), (cx(1), b1['Y']('TV'))], 18), SNP, 8)
wirepath(Rp([(340, 440), (LVN, 440), (LVN, 950), (cx(1), 950), (cx(1), b1['Y']('BV'))], 18), SNP, 8)
T(250, 556, '★ 1개만 쓴다 — 2개를 직렬로 이으면 18 V 가 된다', 19, ORG, '700', 'middle')

# ═══════════ 챔버 ═══════════
panel(90, 640, 410, 740, '챔버 — 챔버팀이 만든다', '#f7fbfa')
a('<rect x="110" y="900" width="370" height="150" rx="18" fill="#d9b38c" stroke="#a8845c" stroke-width="3"/>')
a('<path d="M 130 985 Q 220 945 300 985 Q 380 1025 465 985" stroke="#8f5f3f" stroke-width="26" fill="none" stroke-linecap="round"/>')
PINS = [(170, '①', '기록 전극 1', L1, 680), (280, '②', '기록 전극 2', L3, 725), (400, '③', '기준(접지)', L5, 770)]
for px, nm, lab, lane, ey in PINS:
    wirepath(Rp([(px, 960), (px, ey), (lane, ey)], 14), ALG, 7)
    a(f'<line x1="{px}" y1="{960}" x2="{px}" y2="{860}" stroke="#8a8a8a" stroke-width="5"/>')
    a(f'<g transform="translate({px},{866}) rotate(-90)">'
      f'<path d="M -26 -10 L 7 -4 L 22 -2 L 7 2 L -26 7 Z" fill="{ALG}" opacity="0.92"/>'
      f'<path d="M -26 10 L 7 4 L 22 2 L 7 -2 L -26 -7 Z" fill="{ALG}" opacity="0.92"/>'
      f'<rect x="-31" y="-11" width="12" height="22" rx="4" fill="{ALG}"/></g>')
for i, (px, nm, lab, lane, ey) in enumerate(PINS):
    T(px, 1096, nm, 20, ALG, '700', 'middle'); T(px, 1120, lab, 15, '#555', '400', 'middle')
a(f'<path d="M 170 1146 L 280 1146" stroke="{ORG}" stroke-width="3"/>')
a(f'<path d="M 170 1140 L 170 1152 M 280 1140 L 280 1152" stroke="{ORG}" stroke-width="3"/>')
T(225, 1138, 'Δs', 19, ORG, '700', 'middle')
T(112, 1196, '비마취 · 전극 3개가 나온다', 21, '#111', '700')
T(112, 1224, '기록 2개 + 기준(접지) 1개', 18, '#555')
T(112, 1250, '두 채널이 기준 하나를 함께 쓴다', 18, '#555')
T(112, 1284, '★ ①②사이 거리 Δs 를 자로 잰다', 18, ORG, '700')
T(112, 1310, '전도속도 = Δs ÷ Δt 다', 18, ORG, '700')
T(112, 1346, '전극 실물은 챔버팀이 정한다. 커터칼날은 임시였다.', 17, '#777')


def lead(lane, ey, pts): wirepath(Rp([(lane, ey)] + pts, 20), ALG, 7)


# 전극선 끝은 보드 자료의 번호 좌표를 직접 읽는다.
# 배치를 옮겨도 전체 연결도만 예전 좌표에 남는 일이 없다.
e1x, e1y = b1['①']
e2x, e2y = b2['②']
egx, egy = b1['③']
lead(L1, 680, [(L1, 150), (e1x, 150), (e1x, e1y - 28), (e1x, e1y)])
lead(L3, 725, [(L3, 1215), (e2x, 1215), (e2x, e2y - 28), (e2x, e2y)])
lead(L5, 770, [(L5, 985), (egx, 985), (egx, egy)])

# ═══════════ 잭 → 오디오 인터페이스 → 컴퓨터 ═══════════
IX = 2400; IN1, IN2 = 470, 566
for bd, lane, ty, drop, lab in [(b1, AUD1, IN1, 1022, '채널 1'), (b2, AUD2, IN2, 2002, '채널 2')]:
    px, py = bd['plug']
    wirepath(Rp([(px, py), (px - 46, py), (px - 46, drop), (lane, drop), (lane, ty), (IX + 86, ty)], 22), USB, 7)
T(AUD1 - 10, 1250, '★ 두 오디오 케이블은 여기서부터 끝까지 나란히 붙여 묶는다', 18, ORG, '700', 'end')

panel(IX, 340, 1120, 400, '오디오 인터페이스 · M-Audio M-Track Duo → 컴퓨터', '#f7f8fb')
a(f'<rect x="{IX+40}" y="392" width="560" height="300" rx="14" fill="#3f4550"/>')
T(IX + 320, 428, 'M-Track Duo — 앞면', 20, '#fff', '700', 'middle')
for cy, lab in [(IN1, '콤보 입력 1  ← 채널 1'), (IN2, '콤보 입력 2  ← 채널 2')]:
    a(f'<circle cx="{IX+86}" cy="{cy}" r="20" fill="#1c1f24" stroke="#8d939c" stroke-width="3"/>')
    a(f'<circle cx="{IX+86}" cy="{cy}" r="8" fill="#0b0d10"/>')
    T(IX + 124, cy + 1, lab, 18, '#eee', '700')
    T(IX + 124, cy + 26, 'Line/Inst 스위치 → Inst · 6.35 mm 로 꽂는다', 15, '#a8bccd')
T(IX + 56, 660, '★ +48 V 팬텀 스위치는 끈다 (두 입력에 함께 걸린다)', 17, '#f4b8b0', '700')
T(IX + 56, 684, '모니터 스위치 → USB', 16, '#a8bccd')
a(f'<rect x="{IX+740}" y="392" width="340" height="196" rx="14" fill="#2b2b2b"/>')
a(f'<rect x="{IX+760}" y="410" width="300" height="146" rx="6" fill="#12161c"/>')
T(IX + 910, 458, '컴퓨터', 25, '#fff', '700', 'middle')
T(IX + 910, 490, 'Yoga Slim 7 Pro 14ARH5', 15, '#9ab', '400', 'middle')
T(IX + 910, 514, '★ 윈도우는 드라이버를 미리 깐다', 15, '#f4b8b0', '400', 'middle')
T(IX + 910, 540, 'Audacity · 48 kHz · 16 bit · 2채널', 15, '#9ab', '400', 'middle')
wirepath(f'M {IX+600} 470 L {IX+740} 470', USB, 9)
T(IX + 670, 452, 'USB-B', 16, USB, '700', 'middle'); T(IX + 670, 494, '동봉', 15, '#666', '400', 'middle')
T(IX + 660, 616, '뒷면 USB-B → 동봉 케이블 → 노트북 USB-A', 16, '#555')
T(IX + 660, 640, '상자에 오는 것은 이 케이블 하나뿐이다', 16, ORG, '700')
T(IX + 40, 718, '★ 컴퓨터는 배터리로 돌린다 — 충전기를 꽂으면 60 Hz 가 실린다', 18, ORG, '700')

# ═══════════ 번호를 맨 위에 다시 ═══════════
for bd in (b1, b2):
    for x, y, lab, col in bd['posts']: postmark(x, y, lab, col)
    px, py = bd['plug']
    postmark(px - 46, py, D.JACK_POST['B1' if bd is b1 else 'B2'][0], USB)

# ═══════════ 잭 브레이크아웃 상세 ═══════════
JX, JY = 90, 1470
panel(JX, JY, 720, 400, '잭 브레이크아웃 — 보드에 직접 꽂지 않는다', '#fdf8f3')
a(f'<rect x="{JX+40}" y="{JY+40}" width="230" height="200" rx="8" fill="#8f2b2b"/>')
for k, nm in enumerate(['TIP', 'RING1', 'RING2', 'SLEEVE']):
    x = JX + 74 + k * 54
    a(f'<circle cx="{x}" cy="{JY+62}" r="9" fill="#d9b34a" stroke="#7a5f18" stroke-width="2"/>')
    a(f'<g transform="translate({x+5},{JY+80}) rotate(90)"><text font-size="12" fill="#fff">{nm}</text></g>')
    wirepath(Rp([(x, JY + 62), (x, JY - 6), (JX + 330 + k * 30, JY - 6), (JX + 330 + k * 30, JY + 150)], 12), USB, 5)
a(f'<rect x="{JX+56}" y="{JY+156}" width="180" height="66" rx="5" fill="#242424"/>')
a(f'<rect x="{JX+230}" y="{JY+172}" width="46" height="34" rx="8" fill="#2b2b2b"/>')
a(f'<circle cx="{JX+262}" cy="{JY+189}" r="10" fill="#0b0d10" stroke="#8d939c" stroke-width="2"/>')
T(JX + 146, JY + 196, '3.5 mm 잭', 13, '#bbb', '400', 'middle')
T(JX + 155, JY + 262, '보드 옆 책상에 둔다', 16, '#111', '700', 'middle')
a(f'<rect x="{JX+318}" y="{JY+150}" width="126" height="90" rx="6" fill="#fcfcfa" stroke="#c2c2ba" stroke-width="2"/>')
T(JX + 381, JY + 174, '브레드보드', 14, '#555', '700', 'middle')
for k, col in enumerate((33, 32, 31, 30)):
    T(JX + 330 + k * 30, JY + 200, str(col), 15, '#111', '700', 'middle')
    T(JX + 330 + k * 30, JY + 222, 'J', 13, '#666', '400', 'middle')
T(JX + 470, JY + 176, '암–수 점퍼선 4개', 17, ORG, '700')
T(JX + 470, JY + 200, '암 쪽 → 모듈의 수핀', 15, '#444')
T(JX + 470, JY + 222, '수 쪽 → 보드 J행', 15, '#444')
for k, t in enumerate([
        '★ 레일 두 줄에만 걸려서 보드에 직접 못 꽂는다 — 핀 4개가 한 레일 안에서 전부 단락된다 (2026-09-05 실물 확인).',
        '★ TIP 이 33열에 가게만 맞추면 된다. RING1 · RING2 · SLEEVE 는 어차피 전부 GND 로 묶인다.',
        '★ 이 한 벌을 채널마다 하나씩 — 점퍼선 8개. 케이블은 3.5 mm 수 → 6.35 mm 수(국내 표기 「5.5」).']):
    T(JX + 20, JY + 300 + k * 28, t, 16, ORG if k < 2 else '#333', '700' if k < 2 else '400')

# ═══════════ 선 색 ═══════════
panel(90, 2100, 410, 200, '선 색 = 실물의 종류')
for i, (c, lab) in enumerate([(JMP, '수–수 점퍼선'), (ALG, '악어클립 리드선'), (SNP, '건전지 스냅 연선'), (USB, '오디오 케이블')]):
    yy = 2150 + i * 38
    a(f'<line x1="130" y1="{yy}" x2="188" y2="{yy}" stroke="{c}" stroke-width="9" stroke-linecap="round"/>')
    T(204, yy + 6, lab, 19, '#333')

# ═══════════ 이름표 ═══════════
KY = 840
# 부품 줄은 보드자료에서 만든다 — 손으로 적지 않는다
_seen, _role = [], {}
for _p in D.B1_PARTS + D.B2_PARTS:
    k = (_p['name'], _p['val'])
    if k not in _role:
        _seen.append(k); _role[k] = _p['role']
_n1 = {k: sum(1 for q in D.B1_PARTS if (q['name'], q['val']) == k) for k in _seen}
_n2 = {k: sum(1 for q in D.B2_PARTS if (q['name'], q['val']) == k) for k in _seen}
rows = []
for k in _seen:
    cnt = f'보드마다 {_n1[k]}개' if _n1[k] == _n2[k] else f'1번 {_n1[k]}개 · 2번 {_n2[k]}개'
    rows.append((k[0], k[1], f'{_role[k]} — {cnt}' if _role[k] else cnt))
rows += [('Cd', D.CAPVAL['Cd'], '전원 흔들림 흡수. IC 전원핀 가까이 — 보드마다 4개'),
         (' · '.join(i[1] for i in D.B1_IC), 'AD623 데이터시트 Rev. G', '보드마다 2개 — '
          + ' · '.join(f'{i[0]}열' for i in D.B1_IC)),
         ('', '', '★ 이득 저항 Rg 를 안 꽂는다 — AD623 모듈 위의 트리머로 맞춘다 (100 이하)'),
         ('', '', '★ 차동단 저항 네 개가 없다 — CMRR 이 칩 안에서 공장 트리밍돼 있다'),
         ('잭 브레이크아웃', 'TRRS · 보드 옆 책상에', '★ 보드에 못 꽂는다 — 암–수 점퍼선 4개로 30–33열 J행에'),
         ('멀티미터', '학교에서 빌린다', '회로의 부품이 아니다. 도통 · V+/V− 확인'),
         ('오디오 인터페이스', 'M-Audio M-Track Duo', '6.35 mm 쪽에 Inst 로. ★ 48 V 팬텀은 끈다'),
         ('시침핀', '0.6 mm 강선', '지렁이 전극 3개. ★ 출력 쪽에는 기둥이 없다'),
         ('건전지', '9 V 1개', '★ 2개를 직렬로 이으면 18 V 가 된다. 1개만 쓴다'),
         ('', '', '—'),
         ('①②', '기록 전극 2개', '채널마다 하나 (AD623 IN+). ★ 둘 사이 거리 Δs 를 자로 잰다'),
         ('③', '기준(접지) 전극', '지렁이 몸을 회로의 0 V 에 묶는다. 두 채널이 함께 쓴다'),
         ('④', '레일 3줄', '2번 보드는 전원부가 없다. 1번에서 끌어온다'),
         ('⑤⑥', '오디오 케이블 2개', '보드 옆 잭 → 인터페이스 콤보 입력 1 · 2'),
         ('⑦⑧', '건전지 스냅', '빨강 V+ · 검정 V−. 1번 보드 1열'),
         ('⑨', '호일 케이지 (선택)', '알루미늄 호일로 덮고 위 GND 레일 15열에 문다'),
         ('', '', '★ 채널마다 (그 전극 − 기준) 을 잰다. 두 채널을 빼면 이극 신호다')]

panel(IX, KY, 1120, 96 + len(rows) * 36 + 30, '이름표가 무엇인가', '#fbfbf9')
T(IX + 30, KY + 52, '부품', 20, '#111', '700'); T(IX + 280, KY + 52, '값 / 규격', 20, '#111', '700')
T(IX + 570, KY + 52, '하는 일', 20, '#111', '700')
a(f'<line x1="{IX+24}" y1="{KY+66}" x2="{IX+1096}" y2="{KY+66}" stroke="#c9c9c2" stroke-width="2"/>')
for i, (n1, n2, n3) in enumerate(rows):
    yy = KY + 96 + i * 36
    T(IX + 30, yy, n1, 19, '#111', '700'); T(IX + 280, yy, n2, 19, VALC if n2 else '#444', '700' if n2 else '400')
    T(IX + 570, yy, n3, 18, ORG if n3.startswith('★') else '#444', '700' if n3.startswith('★') else '400')

# ═══════════ 보드 바깥에서 들어오는 연결 ═══════════
CYT = 2360
panel(90, CYT, 3520, 380, '보드 바깥에서 들어오는 연결 — 그림의 번호와 같다')
CONN = [('①', ALG, '기록 전극 1 → 1번 보드 9열 H행', '시침핀을 몸에 대고 악어클립으로 문다. 채널 1'),
        ('②', ALG, '기록 전극 2 → 2번 보드 9열 H행', '채널 2. ★ ①과의 거리 Δs 를 자로 재서 적는다'),
        ('③', ALG, '기준(접지) 전극 → 1번 보드 아래 GND 레일 12열', '두 채널이 함께 쓴다. 지렁이 몸을 회로의 0 V 에 묶는다'),
        ('④', JMP, '레일 3줄 → 1번 보드 0열에서 2번 보드 0열로', '위 V+→위 V+ · 아래 GND→위 GND · 아래 V−→아래 V−'),
        ('⑤', USB, '채널 1 오디오 케이블 → 인터페이스 콤보 입력 1', '1번 보드에 꽂힌 잭에서 나온다. 6.35 mm 쪽을 Inst 로'),
        ('⑥', USB, '채널 2 오디오 케이블 → 인터페이스 콤보 입력 2', '2번 보드에 꽂힌 잭에서 나온다'),
        ('⑦', SNP, '건전지 빨강 → 1번 보드 위 V+ 레일 1열', '스냅 끝의 수핀을 그대로 꽂는다'),
        ('⑧', SNP, '건전지 검정 → 1번 보드 아래 V− 레일 1열', 'GND 가 아니다 — 건전지에 GND 단자는 없다'),
        ('⑨', ALG, '알루미늄 호일 케이지 → 위 GND 레일 15열', '선택. 60 Hz 가 크면 지렁이를 호일로 덮고 문다'),
        ('', ORG, '출력·접지에는 시침핀 기둥이 없다', '잭 브레이크아웃은 암–수 점퍼선으로 30–33열 J행에 잇는다'),
        ('', ORG, 'AD623 방향을 실물 표기와 맞춘다', '윗 E행 GND·OUT·REF·−VS / 아래 I행 GND·IN+·IN−·+VS'),
        ('', ORG, '2번 보드에는 건전지를 따로 달지 않는다', '전원은 ④ 로만 들어온다. 두 채널의 0 V 가 같아야 한다'),
        ('', ORG, '상자에 오는 것은 USB 케이블 하나뿐', '오디오 케이블·잭 브레이크아웃은 전부 따로 산다'),
        ('', ORG, '두 케이블을 케이블타이로 나란히 묶는다', '벌어지면 그 사이가 고리가 되어 60 Hz 를 줍는다'),
        ('', ORG, '2번 보드의 남는 TL072 출력을 GND에 묶지 않는다', '두 버퍼 출력을 병렬 연결하면 서로 맞서므로 금지한다')]
for i, (n, c, t1, t2) in enumerate(CONN):
    col = i // 5; row = i % 5
    x = 130 + col * 1170; y = CYT + 56 + row * 66
    if n:
        a(f'<circle cx="{x+18}" cy="{y-6}" r="17" fill="#fff" stroke="{c}" stroke-width="3.5"/>')
        T(x + 18, y + 1, n, 17, '#222', '700', 'middle')
    else:
        T(x + 18, y + 1, '★', 22, ORG, '700', 'middle')
    T(x + 52, y, t1, 19, '#111', '700'); T(x + 52, y + 25, t2, 16, '#666')

# ═══════════ 선을 왜, 어떻게 묶나 ═══════════
a('</svg>')
svg = '\n'.join(o)
import os, cairosvg
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', *_OUTDIR)
SVG = os.path.normpath(os.path.join(OUT, _STEM + '.svg'))
PNG = os.path.normpath(os.path.join(OUT, _STEM + '.png'))
io.open(SVG, 'w', encoding='utf-8').write(svg)
PDF = os.path.normpath(os.path.join(OUT, '..', _STEM + '.pdf'))
cairosvg.svg2png(url=SVG, write_to=PNG, output_width=W, output_height=H)
# 실험실에 들고 갈 한 장 — A3 가로(420×297 mm) 안에 들어가게 맞춘 1쪽 PDF.
_pw = min(1190.0 / W, 842.0 / H) * W / 0.75
cairosvg.svg2pdf(url=SVG, write_to=PDF, output_width=_pw, output_height=_pw * H / W)
print('저장:', SVG, '·', PNG, '·', PDF)
