# -*- coding: utf-8 -*-
import io
W,H=2420,1570
o=[];a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'font-family="Noto Sans CJK KR, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>')
RED='#d62828';BLU='#2a6ecb';BLK='#2f2f2f';GRN='#178a46';ORG='#c0392b';GRY='#6a6a6a'
def T(x,y,s,fs=18,fill='#111',w='400',anc='start'):
    a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="{w}" fill="{fill}" text-anchor="{anc}">{s}</text>')
def panel(x,y,w,h,title,fill='#fbfbf9'):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#c9c9c2" stroke-width="2"/>')
    T(x+16,y-14,title,25,'#111','700')
def female(x,y,rot=0,c='#262626'):
    a(f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot})">'
      f'<rect x="-10" y="-19" width="20" height="38" rx="3" fill="{c}"/>'
      f'<rect x="-4.5" y="-15" width="9" height="10" rx="1.5" fill="#8f8f8f"/>'
      f'<rect x="-10" y="8" width="20" height="5" fill="#4a4a4a"/></g>')
def male(x,y,rot=0,c='#262626'):
    a(f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot})">'
      f'<rect x="-10" y="-19" width="20" height="30" rx="3" fill="{c}"/>'
      f'<line x1="0" y1="11" x2="0" y2="37" stroke="#c9c9c9" stroke-width="5"/></g>')
def gator(x,y,rot=0,c='#333'):
    a(f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot})">'
      f'<path d="M -34 -13 L 9 -6 L 30 -2 L 9 2 L -34 9 Z" fill="{c}" opacity="0.9"/>'
      f'<path d="M -34 13 L 9 6 L 30 2 L 9 -2 L -34 -9 Z" fill="{c}" opacity="0.9"/>'
      f'<rect x="-40" y="-15" width="15" height="30" rx="4" fill="{c}"/></g>')
def hole(x,y,s=13): a(f'<rect x="{x-s/2:.1f}" y="{y-s/2:.1f}" width="{s}" height="{s}" rx="2" fill="#3a3a3a"/>')

T(50,66,'전체 연결도 기호표 — 그림의 무엇이 실물의 무엇인가',36,'#111','700')
T(50,104,'2026년 8월 28일 · [`그림/전체연결도.png`] 와 같이 본다.'.replace('[`','「').replace('`]','」'),19,'#555')

# ══════════ A. 선 색 ══════════
LX,LY,LW=50,170,1130
panel(LX,LY,LW,360,'A.  선 색 = 실물의 종류 (역할이 아니다)')
T(LX+20,LY+34,'색은 「무엇으로 만든 연결인가」를 나타낸다. 역할(V+ · V− · GND · 신호)은 색이 아니라 이름표와 결선표에 적었다.',17,ORG,'700')
for i,(c,nm,mean) in enumerate([('#1a5fb4','수–수 점퍼선','보드 구멍 ↔ 보드 구멍. 회로 안쪽 배선 전부 · 19개'),
                                ('#0f9b8e','악어클립 테스트 리드선','양끝이 악어입. 전극 3개 + 케이지 1개'),
                                ('#8e44ad','건전지 스냅 연선','실물의 두 선은 빨강·검정이다. 빨강 → V+, 검정 → V−'),
                                ('#2f2f2f','오실로스코프 프로브','동축 케이블과 접지선. 프로브에 붙어 있다'),
                                ('#9a9a9a','회색 = 부품 다리 · 시침핀','저항 · 커패시터의 다리, 그리고 강선')]):
    y=LY+76+i*48
    a(f'<line x1="{LX+30}" y1="{y}" x2="{LX+130}" y2="{y}" stroke="{c}" stroke-width="9" stroke-linecap="round"/>')
    T(LX+152,y+7,nm,19,'#111','700'); T(LX+420,y+7,mean,17,'#333')
a(f'<line x1="{LX+30}" y1="{LY+318}" x2="{LX+130}" y2="{LY+318}" stroke="#e2a8a8" stroke-width="4"/>')
a(f'<line x1="{LX+30}" y1="{LY+330}" x2="{LX+130}" y2="{LY+330}" stroke="#aab8dd" stroke-width="4"/>')
T(LX+152,LY+330,'연한 빨강·파랑 줄',19,'#111','700'); T(LX+420,LY+330,'보드에 인쇄된 레일 표시. 전선이 아니다',17,'#333')

# ══════════ B. 무엇으로 잇나 ══════════
BX,BY,BW=1230,170,1140
panel(BX,BY,BW,1010,'B.  무엇으로 잇나  —  실물과 짝짓기')
T(BX+80,BY+34,'그림',16,'#999','700'); T(BX+240,BY+34,'쓰는 곳',16,'#999','700'); T(BX+240,BY+52,'우리 목록의 무엇인가',16,'#999','700')
rowY=BY+62
def brow(h,draw,use,item,have=True):
    global rowY
    a(f'<rect x="{BX+18}" y="{rowY}" width="{BW-36}" height="{h}" rx="8" fill="#fff" stroke="#e2e2e2"/>')
    draw(BX+120,rowY+h/2)
    T(BX+240,rowY+h/2-6,use,18,'#111','700')
    T(BX+240,rowY+h/2+20,item,17,'#2a7a45' if have else ORG)
    rowY+=h+10

def d_mm(x,y):
    male(x-62,y,90); a(f'<line x1="{x-50}" y1="{y}" x2="{x+50}" y2="{y}" stroke="#1a5fb4" stroke-width="8" stroke-linecap="round"/>'); male(x+62,y,-90)
def d_fm(x,y):
    female(x-62,y,90); a(f'<line x1="{x-50}" y1="{y}" x2="{x+50}" y2="{y}" stroke="#9a9a9a" stroke-width="8" stroke-linecap="round"/>'); male(x+62,y,-90)
def d_ff(x,y):
    female(x-62,y,90); a(f'<line x1="{x-50}" y1="{y}" x2="{x+50}" y2="{y}" stroke="#9a9a9a" stroke-width="8" stroke-linecap="round"/>'); female(x+62,y,90)
def d_post(x,y):
    a(f'<rect x="{x-58}" y="{y+10}" width="116" height="26" rx="4" fill="#fcfcfa" stroke="#b8b8b0" stroke-width="1.5"/>')
    for k in range(3): a(f'<rect x="{x-24+k*24}" y="{y+18}" width="8" height="8" rx="1.5" fill="#3a3a3a"/>')
    a(f'<line x1="{x}" y1="{y+30}" x2="{x}" y2="{y-30}" stroke="#9a9a9a" stroke-width="4"/>')
    a(f'<polygon points="{x},{y-42} {x+9},{y-31} {x},{y-20} {x-9},{y-31}" fill="#9fd8e8" stroke="#5a94a8" stroke-width="1.3"/>')
    gator(x+28,y-6,180,'#0f9b8e')
    a(f'<line x1="{x+66}" y1="{y-6}" x2="{x+96}" y2="{y-6}" stroke="#0f9b8e" stroke-width="6" stroke-linecap="round"/>')
def d_gator(x,y):
    gator(x-20,y,0,'#0f9b8e'); a(f'<line x1="{x+12}" y1="{y}" x2="{x+70}" y2="{y}" stroke="#0f9b8e" stroke-width="7" stroke-linecap="round"/>')
def d_snap(x,y):
    a(f'<rect x="{x-70}" y="{y-24}" width="46" height="48" rx="6" fill="#1e1e1e"/>')
    a(f'<circle cx="{x-56}" cy="{y-10}" r="7" fill="#9a9a9a"/><circle cx="{x-56}" cy="{y+12}" r="7" fill="#9a9a9a"/>')
    a(f'<line x1="{x-24}" y1="{y-10}" x2="{x+48}" y2="{y-10}" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>')
    a(f'<line x1="{x-24}" y1="{y+12}" x2="{x+48}" y2="{y+12}" stroke="{BLU}" stroke-width="7" stroke-linecap="round"/>')
    male(x+60,y-10,-90); male(x+60,y+12,-90)
def d_probe(x,y):
    yy=y-24
    a(f'<path d="M {x-62} {yy} m -20 0 a 20 20 0 1 0 20 -20" stroke="#cfcfcf" stroke-width="6" fill="none" stroke-linecap="round"/>')
    a(f'<rect x="{x-60}" y="{yy-12}" width="74" height="24" rx="11" fill="#d2d2d2" stroke="#8a8a8a"/>')
    a(f'<rect x="{x+14}" y="{yy-14}" width="14" height="28" rx="4" fill="#e8c33a" stroke="#a88f20"/>')
    a(f'<rect x="{x+28}" y="{yy-12}" width="30" height="24" rx="8" fill="#9a9a9a" stroke="#6a6a6a"/>')
    a(f'<path d="M {x+58} {yy} L {x+100} {yy}" stroke="#333" stroke-width="7" fill="none" stroke-linecap="round"/>')
    a(f'<path d="M {x-10} {yy+12} L {x-10} {y+22} L {x-56} {y+22}" stroke="#333" stroke-width="5" fill="none" stroke-linecap="round"/>')
    gator(x-64,y+22,180,'#333')
    T(x-88,yy-22,'훅',12,'#666','700','middle')
    T(x+80,yy-16,'동축',12,'#666','700','middle')
    T(x+14,y+44,'접지선 + 악어클립',12,'#666','700','middle')
def d_pin(x,y):
    a(f'<line x1="{x-40}" y1="{y-40}" x2="{x-40}" y2="{y+40}" stroke="#a0a0a0" stroke-width="5"/>')
    a(f'<polygon points="{x-40},{y-52} {x-30},{y-41} {x-40},{y-30} {x-50},{y-41}" fill="#9fd8e8" stroke="#5a94a8" stroke-width="1.3"/>')
    gator(x-12,{}.get(0,y-16),180,'#333')
    a(f'<line x1="{x+26}" y1="{y-16}" x2="{x+60}" y2="{y-16}" stroke="#0f9b8e" stroke-width="6" stroke-linecap="round"/>')

brow(88,d_mm,'수–수 점퍼선 — 보드 구멍 ↔ 보드 구멍','안쪽 17개 + 전극 끌어오기 2개 = 19개 (20개 보유)')
brow(88,d_fm,'암–수 점퍼선 — 이번 회로에서는 쓰지 않는다','시침핀에는 암 커넥터가 안 물린다 (40개 보유)')
brow(88,d_ff,'암–암 점퍼선 — 수핀 ↔ 수핀','수–수가 모자랄 때 이어 늘린다 (20개 보유)')
brow(96,d_pin,'시침핀 + 악어클립 — 지렁이에 꽂는 전극','장식 머리는 절연체다. 머리 아래 금속 축을 문다')
brow(88,d_snap,'건전지 스냅 — 9 V 건전지 ↔ 레일','9 V 건전지 스냅 홀더 (점퍼선 타입) 2개')
brow(88,d_gator,'악어클립 리드 — 호일 ↔ GND 레일','악어클립 테스트 리드선 50 cm · 5색')
brow(126,d_probe,'오실로스코프 프로브 한 벌 — 훅 · 동축 케이블 · 접지선 · 악어클립','네 가지가 하나로 붙어 나온다. 스코프 상자에 있는지 확인할 것', False)
brow(110,d_post,'시침핀 기둥 — 보드 구멍에 세워 꽂는다','훅·악어클립이 물 자리 6곳. 래핑와이어는 연선이라 못 쓴다')
T(BX+24,BY+980,'초록 글씨 = 이미 있다   ·   주황 글씨 = 확인이 필요하다',17,'#555','700')

# ══════════ C. 부품 기호 ══════════
CX0,CY0,CW=50,580,1130
panel(CX0,CY0,CW,330,'C.  부품 기호')
def prow(i,draw,nm,desc):
    y=CY0+50+i*68
    draw(CX0+110,y)
    T(CX0+210,y+7,nm,19,'#111','700'); T(CX0+400,y+7,desc,17,'#444')
def d_res(x,y):
    a(f'<line x1="{x-70}" y1="{y}" x2="{x+70}" y2="{y}" stroke="#9a9a9a" stroke-width="3"/>')
    a(f'<rect x="{x-26}" y="{y-14}" width="52" height="28" rx="5" fill="#e3cba2" stroke="#8a7a60" stroke-width="1.5"/>')
    for k,c in enumerate(['#8a5a2a','#111','#c33','#c9a227','#8a4a8a']):
        a(f'<rect x="{x-20+k*9}" y="{y-14}" width="4" height="28" fill="{c}"/>')
def d_cap(x,y):
    a(f'<line x1="{x-70}" y1="{y}" x2="{x+70}" y2="{y}" stroke="#9a9a9a" stroke-width="3"/>')
    a(f'<rect x="{x-24}" y="{y-14}" width="48" height="28" rx="5" fill="#93b7dd" stroke="#5a7a9a" stroke-width="1.5"/>')
    T(x,y+6,'104',13,'#123','700','middle')
def d_ic(x,y):
    a(f'<rect x="{x-70}" y="{y-20}" width="140" height="40" rx="5" fill="#3b3b3b"/>')
    a(f'<circle cx="{x-54}" cy="{y}" r="8" fill="#606060"/>')
    T(x+12,y+7,'TL072',17,'#fff','700','middle')
def d_mod(x,y):
    a(f'<rect x="{x-70}" y="{y-22}" width="140" height="44" rx="5" fill="#2f2f2f"/>')
    for k in range(4):
        a(f'<circle cx="{x-48+k*32}" cy="{y-22}" r="6" fill="#c9a227"/>')
        a(f'<circle cx="{x-48+k*32}" cy="{y+22}" r="6" fill="#c9a227"/>')
    T(x,y+6,'AD623',15,'#fff','700','middle')
prow(0,d_res,'저항  R','R1 · R2 · Rb1 · Rb2 · Rin · Rf — 몸통에 색띠 5개가 있다')
prow(1,d_cap,'커패시터  C','C1 · Cf · Cd — 몸통에 숫자가 인쇄돼 있다')
prow(2,d_ic,'IC (DIP-8)','TL072 — 홈을 걸치고 왼쪽이 1번 쪽')
prow(3,d_mod,'모듈 (기판)','AD623 — 위아래 금색 점이 납땜할 핀 자리다')
T(CX0+20,CY0+318,'★ 도면 색은 도면 안에서만 통하는 약속이다. 우리 저항은 1 % 금속피막이라 실물은 파란 몸통일 수 있다.',17,ORG,'700')

# ══════════ D. 브레드보드 기호 ══════════
DX,DY,DW=50,960,1130
panel(DX,DY,DW,470,'D.  브레드보드 기호')
def drow(i,draw,nm,desc,h=76):
    y=DY+52+i*h
    draw(DX+110,y)
    T(DX+220,y+7,nm,19,'#111','700'); T(DX+430,y+7,desc,17,'#444')
def d_hole(x,y):
    for k in range(3):
        for j in range(2): hole(x-30+k*30,y-16+j*32)
def d_node(x,y):
    for k in range(3): hole(x-30+k*30,y)
    a(f'<circle cx="{x}" cy="{y}" r="9" fill="#1a5fb4"/>')
def d_rail(x,y):
    a(f'<line x1="{x-70}" y1="{y-14}" x2="{x+70}" y2="{y-14}" stroke="#e2a8a8" stroke-width="4"/>')
    a(f'<line x1="{x-70}" y1="{y+18}" x2="{x+70}" y2="{y+18}" stroke="#aab8dd" stroke-width="4"/>')
    for k in range(5): hole(x-60+k*30,y+2,10)
def d_split(x,y):
    a(f'<line x1="{x-70}" y1="{y}" x2="{x-16}" y2="{y}" stroke="#e2a8a8" stroke-width="4"/>')
    a(f'<line x1="{x+16}" y1="{y}" x2="{x+70}" y2="{y}" stroke="#e2a8a8" stroke-width="4"/>')
    a(f'<rect x="{x-24}" y="{y-22}" width="48" height="44" rx="4" fill="none" stroke="{ORG}" stroke-width="2.5" stroke-dasharray="6 4"/>')
def d_gut(x,y):
    a(f'<rect x="{x-70}" y="{y-16}" width="140" height="32" fill="#e9e9e3" stroke="#d0d0c8"/>')
    for k in range(4): hole(x-52+k*30,y-30,10)
    for k in range(4): hole(x-52+k*30,y+30,10)
drow(0,d_hole,'검은 네모','브레드보드 구멍. 한 열의 A–E 다섯 개가 속에서 이어져 있다')
drow(1,d_node,'색 있는 동그라미','선이나 부품 다리를 그 구멍에 꽂는다는 표시')
drow(2,d_rail,'연한 빨강·파랑 줄','보드에 인쇄된 전원 레일 표시. 한 줄 전체가 속에서 이어져 있다')
drow(3,d_split,'빨간 점선 네모','레일이 여기서 물리적으로 끊겨 있다 (30열 부근)')
drow(4,d_gut,'가운데 회색 띠','홈. 위(A–E)와 아래(F–J)는 홈을 건너 이어지지 않는다')

# ══════════ E. 도면 표시 ══════════
EX,EY,EW=1230,1230,1140
panel(EX,EY,EW,240,'E.  도면에만 있는 표시 (전선이 아니다)')
def erow(i,draw,nm):
    y=EY+50+i*58
    draw(EX+110,y); T(EX+230,y+7,nm,18,'#333')
def d_lead(x,y):
    a(f'<path d="M {x-70} {y} L {x+20} {y} L {x+20} {y+22}" stroke="#888" stroke-width="1.6" stroke-dasharray="7 5" fill="none"/>')
    a(f'<circle cx="{x+20}" cy="{y+22}" r="11" fill="none" stroke="#888" stroke-width="2"/>')
def d_sold(x,y):
    a(f'<rect x="{x-70}" y="{y-14}" width="140" height="28" rx="4" fill="none" stroke="{ORG}" stroke-width="2.5" stroke-dasharray="6 4"/>')
def d_over(x,y):
    a(f'<line x1="{x}" y1="{y-22}" x2="{x}" y2="{y+22}" stroke="#1a5fb4" stroke-width="8" stroke-linecap="round"/>')
    a(f'<line x1="{x-70}" y1="{y}" x2="{x+70}" y2="{y}" stroke="#fff" stroke-width="17" stroke-linecap="round"/>')
    a(f'<line x1="{x-70}" y1="{y}" x2="{x+70}" y2="{y}" stroke="#0f9b8e" stroke-width="8" stroke-linecap="round"/>')
erow(0,d_lead,'회색 점선 + 동그라미 = 이름표가 가리키는 자리')
erow(1,d_sold,'주황 점선 네모 = 여기를 납땜한다')
erow(2,d_over,'흰 테두리가 있는 선 = 위로 지나간다 (닿지 않는다)')

a('</svg>')
# ── 저장: SVG 와 PNG 를 같이 만든다 ──
import os, cairosvg
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','이번주','장치','그림')
SVG=os.path.normpath(os.path.join(OUT,'기호표.svg'))
PNG=os.path.normpath(os.path.join(OUT,'기호표.png'))
io.open(SVG,'w',encoding='utf-8').write('\n'.join(o))
cairosvg.svg2png(url=SVG, write_to=PNG, output_width=2420)
print('저장:', SVG, '·', PNG)
print('ok')
