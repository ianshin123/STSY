# -*- coding: utf-8 -*-
"""TL072 계측증폭기 회로 원리도 — 전기 기호로 그린 것.
실제로 꽂는 자리는 「브레드보드 배치도」와 「전체 연결도」를 본다."""
import io, os, math
W,H=2460,1600
o=[]; a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'font-family="Noto Sans CJK KR, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>')
ORG='#c0392b'; GRY='#9a9a9a'; SIG='#1a5fb4'
def T(x,y,s,fs=18,fill='#111',w='400',anc='start'):
    a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="{w}" fill="{fill}" text-anchor="{anc}">{s}</text>')
def panel(x,y,w,h,title,fill='#fbfbf9'):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#c9c9c2" stroke-width="2"/>')
    T(x+16,y-12,title,24,'#111','700')
def w_(pts,col='#333',wd=3):
    d='M '+' L '.join(f'{p[0]:.0f} {p[1]:.0f}' for p in pts)
    a(f'<path d="{d}" stroke="{col}" stroke-width="{wd}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
def dot(x,y,c='#333'): a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="{c}"/>')
def gnd(x,y,lab=None):
    w_([(x,y),(x,y+16)]);
    for i,ww in enumerate((26,17,9)):
        a(f'<line x1="{x-ww/2:.0f}" y1="{y+16+i*8}" x2="{x+ww/2:.0f}" y2="{y+16+i*8}" stroke="#333" stroke-width="3"/>')
    if lab: T(x+22,y+34,lab,15,'#666')
def res(x1,y1,x2,y2,lab,sub=None,lp=None):
    mx,my=(x1+x2)/2,(y1+y2)/2; ang=math.degrees(math.atan2(y2-y1,x2-x1))
    w_([(x1,y1),(x2,y2)],'#333',3)
    a(f'<g transform="translate({mx:.0f},{my:.0f}) rotate({ang:.1f})">'
      f'<rect x="-34" y="-15" width="68" height="30" rx="4" fill="#e3cba2" stroke="#8a7a60" stroke-width="2"/></g>')
    vert=abs(y2-y1)>=abs(x2-x1)
    if lp:      lx,ly,sy,anc=lp[0],lp[1],lp[1]+21,'middle'
    elif vert:  lx,ly,sy,anc=mx+42,my+6,my+27,'start'
    else:       lx,ly,sy,anc=mx,my-30,my+34,'middle'
    T(lx,ly,lab,19,'#111','700',anc)
    if sub: T(lx,sy,sub,16,'#555','400',anc)
def cap(x1,y1,x2,y2,lab,sub=None):
    mx,my=(x1+x2)/2,(y1+y2)/2
    if abs(x2-x1)>abs(y2-y1):
        w_([(x1,y1),(mx-9,my)]); w_([(mx+9,my),(x2,y2)])
        a(f'<line x1="{mx-9}" y1="{my-24}" x2="{mx-9}" y2="{my+24}" stroke="#333" stroke-width="4"/>')
        a(f'<line x1="{mx+9}" y1="{my-24}" x2="{mx+9}" y2="{my+24}" stroke="#333" stroke-width="4"/>')
        T(mx,my-58,lab,19,'#111','700','middle')
        if sub: T(mx,my-37,sub,16,'#555','400','middle')
    else:
        w_([(x1,y1),(mx,my-9)]); w_([(mx,my+9),(x2,y2)])
        a(f'<line x1="{mx-24}" y1="{my-9}" x2="{mx+24}" y2="{my-9}" stroke="#333" stroke-width="4"/>')
        a(f'<line x1="{mx-24}" y1="{my+9}" x2="{mx+24}" y2="{my+9}" stroke="#333" stroke-width="4"/>')
        T(mx+34,my+6,lab,19,'#111','700')
        if sub: T(mx+34,my+27,sub,16,'#555')
def amp(x,y,name,sub='',minus_top=True,h=150,w=130):
    """왼쪽이 입력, 오른쪽 꼭짓점이 출력. 반환: (−입력, +입력, 출력) 좌표"""
    a(f'<polygon points="{x},{y-h/2} {x},{y+h/2} {x+w},{y}" fill="#eef2f7" stroke="#33506e" stroke-width="3"/>')
    T(x+30,y-6,name,19,'#111','700'); T(x+30,y+16,sub,14,'#555')
    yt,yb=y-h/4,y+h/4
    T(x+11,yt+7,'−' if minus_top else '+',24,'#111','700')
    T(x+11,yb+7,'+' if minus_top else '−',24,'#111','700')
    return ((x,yt),(x,yb),(x+w,y)) if minus_top else ((x,yb),(x,yt),(x+w,y))

# ═══ ① 전원부 ═══
panel(40,132,880,408,'① 전원부 — 9 V 하나를 ±4.5 V 로 나눈다')   # 위 여백은 머리글 부제와 겹치지 않을 만큼
BX,BY=90,200
a(f'<rect x="{BX}" y="{BY}" width="66" height="150" rx="8" fill="#4a4a4a" stroke="#2a2a2a" stroke-width="2"/>')
T(BX+33,BY+82,'9 V',20,'#fff','700','middle')
# 레일을 R1·R2 갈림점(x=360) 오른쪽까지 늘리고 이름표는 그 끝에 붙인다 — 갈림 도선이 글자를 뚫지 않게
w_([(BX+33,BY),(BX+33,170),(470,170)]); T(480,176,'V+   (+4.5 V)',19,'#c0392b','700')
w_([(BX+33,BY+150),(BX+33,500),(470,500)]); T(480,506,'V−   (−4.5 V)',19,SIG,'700')
res(360,200,360,290,'R1','10 kΩ'); res(360,380,360,470,'R2','10 kΩ')
w_([(360,170),(360,200)]); w_([(360,470),(360,500)]); dot(360,170); dot(360,500)
w_([(360,290),(360,380)]); dot(360,335)
(m1,p1,o1)=amp(560,335,'U1b','',minus_top=True,h=130,w=110)   # 이름은 삼각형 밖에 — 안에 넣으면 꼭짓점을 넘는다
T(615,428,'TL072 U1b — 가상접지 버퍼',16,'#555','400','middle')
w_([(360,335),(500,335),(500,p1[1]),(p1[0],p1[1])])
w_([(o1[0],o1[1]),(730,335)]); dot(730,335)
w_([(730,335),(730,250),(m1[0]-40,250),(m1[0]-40,m1[1]),(m1[0],m1[1])])
res(575,250,705,250,'1 Ω','점퍼 대신',lp=(640,204))
T(752,342,'GND   (0 V)',19,'#111','700'); gnd(880,335)
T(70,566,'★ 이 GND 는 대지가 아니라 분압과 버퍼가 만든 가상접지다. 회로도의 모든 접지 기호는 같은 한 점이다.',17,ORG,'700')

# ═══ ② 1단 · 차동단 ═══
panel(40,650,1560,760,'② 계측증폭기 — TL072 세 반쪽으로 만든 3-op-amp 구성')
# 입력 버퍼 A (위)
(mA,pA,oA)=amp(430,790,'U1a','입력 버퍼 A',minus_top=True)
(mB,pB,oB)=amp(430,1230,'U2a','입력 버퍼 B',minus_top=False)
for (px,py),lab,rb in ((pA,'전극 B','Rb2'),(pB,'전극 A','Rb1')):
    w_([(120,py),(px,py)],SIG,4)
    a(f'<polygon points="112,{py-13} 128,{py} 112,{py+13}" fill="#9fd8e8" stroke="#5a94a8" stroke-width="2"/>')
    T(104,py+7,lab,20,'#111','700','end')
    end=950 if lab=='전극 B' else 1070
    dot(210,py,SIG); res(210,py,210,end,rb,'1 MΩ'); gnd(210,end)
# 되먹임 Ra / Rb 와 이득저항 Rg
w_([(oA[0],oA[1]),(760,790)]); dot(760,790)
w_([(oB[0],oB[1]),(760,1230)]); dot(760,1230)
res(760,860,mA[0]-60,860,'Ra','10 kΩ')
w_([(760,790),(760,860)]); w_([(mA[0]-60,860),(mA[0]-60,mA[1]),(mA[0],mA[1])]); dot(mA[0]-60,mA[1])
res(760,1160,mB[0]-60,1160,'Rb','10 kΩ')
w_([(760,1230),(760,1160)]); w_([(mB[0]-60,1160),(mB[0]-60,mB[1]),(mB[0],mB[1])]); dot(mB[0]-60,mB[1])
res(mA[0]-60,960,mA[0]-60,1060,'Rg','220 Ω')
w_([(mA[0]-60,mA[1]),(mA[0]-60,960)]); w_([(mA[0]-60,1060),(mA[0]-60,mB[1])])
T(mA[0]-60,1352,'Rg 하나가 1단 이득을 정한다',17,ORG,'700','middle')
# 차동단
(mD,pD,oD)=amp(1240,1010,'U3a','차동단',minus_top=True,h=170,w=140)
res(880,790,1120,790,'R3','10 kΩ')
w_([(1120,790),(mD[0]-70,790),(mD[0]-70,mD[1]),(mD[0],mD[1])]); dot(mD[0]-70,mD[1])
res(880,1230,1120,1230,'R3′','10 kΩ')
w_([(1120,1230),(pD[0]-70,1230),(pD[0]-70,pD[1]),(pD[0],pD[1])]); dot(pD[0]-70,pD[1])
res(mD[0]-70,880,1440,880,'R4','10 kΩ')
w_([(mD[0]-70,mD[1]),(mD[0]-70,880)]); w_([(1440,880),(1440,1010)]); dot(1440,1010)
w_([(oD[0],oD[1]),(1500,1010)]); dot(1500,1010)
w_([(pD[0]-70,pD[1]),(pD[0]-70,1160)])
res(pD[0]-70,1160,pD[0]-70,1250,'R4′','10 kΩ'); gnd(pD[0]-70,1250)
T(70,1444,'★ 차동단의 R3 · R3′ · R4 · R4′ 는 10 kΩ 40개 중에서 멀티미터로 재어 가장 비슷한 네 개를 고른다. 여기서 CMRR 이 정해진다.',18,ORG,'700')
T(70,1472,'   AD623 은 이 네 저항이 칩 안에서 트리밍돼 나온다. 우리는 손으로 맞춘다 — 키트 그대로면 총 CMRR 73 dB, 0.2 % 로 고르면 87 dB.',17,'#555')

# ═══ ③ 2단 ═══
panel(1660,650,760,530,'③ 2단 — 더 키우고 통과대역을 자른다')
w_([(1500,1010),(1560,1010),(1560,900),(1700,900)],SIG,4)
cap(1700,900,1810,900,'C1','474 마일러 0.47 µF')
res(1810,900,1960,900,'Rin','3.3 kΩ')
(m2,p2,o2)=amp(2060,960,'U3b','2단',minus_top=True,h=140,w=120)
w_([(1960,900),(m2[0]-40,900),(m2[0]-40,m2[1]),(m2[0],m2[1])]); dot(m2[0]-40,m2[1])
w_([(p2[0],p2[1]),(p2[0]-40,p2[1])]); gnd(p2[0]-40,p2[1])
w_([(o2[0],o2[1]),(2300,960)]); dot(2300,960)
res(m2[0]-40,820,2300,820,'Rf','10 kΩ')
w_([(m2[0]-40,m2[1]),(m2[0]-40,820)]); w_([(2300,820),(2300,960)])
cap(m2[0]-40,752,2300,752,'Cf','472  4.7 nF')
w_([(m2[0]-40,820),(m2[0]-40,752)]); w_([(2300,752),(2300,820)])
T(1690,1152,'고역차단 103 Hz  ·  저역차단 3.39 kHz  ·  2단 이득 3.03',18,'#111','700')

# 오실로스코프
panel(1660,1240,760,270,'오실로스코프로')
w_([(2300,960),(2360,960),(2360,1350),(1980,1350)],'#2f2f2f',4)
a('<rect x="1720" y="1280" width="250" height="150" rx="10" fill="#4b4b4b" stroke="#333" stroke-width="2"/>')
a('<rect x="1740" y="1300" width="210" height="110" rx="5" fill="#101a10"/>')
a('<path d="M 1752 1370 L 1810 1370 L 1822 1326 L 1836 1398 L 1850 1362 L 1940 1362" stroke="#7ee08a" stroke-width="3" fill="none"/>')
gnd(1845,1450,'프로브 접지 클립')
w_([(1845,1430),(1845,1450)])
T(1690,1524,'프로브 1X · AC 결합 · 5 mV/div · 반드시 배터리 구동',17,'#111','700')

# 머리말
T(40,48,'회로 원리도 — TL072 계측증폭기 (AD623 대체)',34,'#111','700')
T(40,78,'전기 기호로 그린 회로다. 실제로 꽂는 자리는 「브레드보드 배치도」와 「전체 연결도」를 본다. · 2026년 8월 28일',18,'#555')
T(960,566,'★ 남는 반쪽 U2b 는 +입력을 10 kΩ 으로 GND 에 묶고 출력을 −입력에 이어 버퍼로 만들어 둔다.',17,ORG,'700')
T(960,594,'   입력이 뜬 채로 두면 발진하거나 잡음을 낸다.',17,'#555')
T(960,140,'TL072 한 개에 증폭기가 두 개다. 세 개를 쓰면 여섯 반쪽 중 다섯을 쓴다:',18,'#111','700')
for i,t0 in enumerate(['U1a = 입력 버퍼 A          U1b = 가상접지 버퍼',
                       'U2a = 입력 버퍼 B          U2b = 남는다 (묶어 둔다)',
                       'U3a = 차동단               U3b = 2단']):
    T(980,176+i*30,'· '+t0,18,'#444')
T(960,300,'AD623 안에 든 것이 바로 이 3-op-amp 구성이다.',18,'#111','700')
T(960,330,'입력 버퍼 두 개가 전극을 물지 않고 받고(입력저항 1 TΩ),',17,'#555')
T(960,356,'차동단이 두 출력의 차이만 남긴다.',17,'#555')
a('</svg>')
import cairosvg
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','이번주','장치','그림')
SVG=os.path.normpath(os.path.join(OUT,'회로도_TL072IA.svg'))
PNG=os.path.normpath(os.path.join(OUT,'회로도_TL072IA.png'))
io.open(SVG,'w',encoding='utf-8').write('\n'.join(o))
cairosvg.svg2png(url=SVG, write_to=PNG, output_width=2460)
print('저장:', SVG, '·', PNG)
