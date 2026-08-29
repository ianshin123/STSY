# -*- coding: utf-8 -*-
"""TL072 3-op-amp 계측증폭기 배치도 — AD623 미도착 시의 대체 회로.
좌표계·색 체계·기호는 「브레드보드_배치도.py」와 같다."""
import io, math
P=32.0; X0=205.0; CA,CB=0,32
SPLIT=30
ROWS=['A','B','C','D','E','F','G','H','I','J']
RY={}; y=468.0            # 머리글이 7줄이라 보드를 그만큼 내렸다
for r in ROWS[:5]: RY[r]=y; y+=P
GUT_T=y-P*0.5; GUT_B=GUT_T+P*2.3; y=GUT_B+P*0.5
for r in ROWS[5:]: RY[r]=y; y+=P
RAIL={'TV':336.0,'TG':376.0,'BG':RY['J']+64,'BV':RY['J']+104}
def cx(c): return X0+(c-CA)*P
def Y(r): return RAIL[r] if r in RAIL else RY[r]
W=cx(CB)+300; H=RAIL['BV']+250
o=[]; a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" font-family="Noto Sans CJK KR, sans-serif"><rect width="{W:.0f}" height="{H:.0f}" fill="#fff"/>')
BL=X0-84; BR=cx(CB)+58
a(f'<rect x="{BL:.0f}" y="{RAIL["TV"]-42:.0f}" width="{BR-BL:.0f}" height="{RAIL["BV"]-RAIL["TV"]+84:.0f}" rx="10" fill="#fcfcfa" stroke="#c2c2ba" stroke-width="2"/>')
a(f'<rect x="{BL:.0f}" y="{GUT_T:.0f}" width="{BR-BL:.0f}" height="{GUT_B-GUT_T:.0f}" fill="#ebebe5"/>')
a(f'<text x="{BL+12:.0f}" y="{(GUT_T+GUT_B)/2+6:.0f}" font-size="15" fill="#8a8a8a">홈</text>')
JMP='#1a5fb4'; ALG='#0f9b8e'; SNP='#8e44ad'; PRB='#2f2f2f'
RAILR='#e2a8a8'; RAILB='#aab8dd'
def hole(x,yy,s=10): a(f'<rect x="{x-s/2:.1f}" y="{yy-s/2:.1f}" width="{s}" height="{s}" rx="1.5" fill="#3a3a3a"/>')
for key,col,lab in [('TV',RAILR,'V+'),('TG',RAILB,'GND'),('BG',RAILR,'GND'),('BV',RAILB,'V−')]:
    yy=RAIL[key]
    a(f'<line x1="{cx(CA)-30:.0f}" y1="{yy-18:.0f}" x2="{cx(SPLIT-2)+8:.0f}" y2="{yy-18:.0f}" stroke="{col}" stroke-width="3"/>')
    a(f'<line x1="{cx(SPLIT+1)-8:.0f}" y1="{yy-18:.0f}" x2="{cx(CB)+28:.0f}" y2="{yy-18:.0f}" stroke="{col}" stroke-width="3"/>')
    for c in range(CA,CB+1):
        if c%6!=0 and not (SPLIT-1<=c<=SPLIT): hole(cx(c),yy,9)
    a(f'<text x="{BR+12:.0f}" y="{yy+6:.0f}" font-size="21" font-weight="700" fill="#111">{lab}</text>')
for yy0,yy1 in [(RAIL['TV'],RAIL['TG']),(RAIL['BG'],RAIL['BV'])]:
    a(f'<rect x="{cx(SPLIT-1)-8:.0f}" y="{yy0-34:.0f}" width="{2*P+16:.0f}" height="{yy1-yy0+44:.0f}" fill="none" stroke="#c0392b" stroke-width="2.5" stroke-dasharray="6 4"/>')
a(f'<text x="{cx(SPLIT)+4:.0f}" y="{RAIL["TV"]-48:.0f}" font-size="16" font-weight="700" text-anchor="middle" fill="#c0392b">레일만 여기서 끊긴다</text>')
for r in ROWS:
    for c in range(CA,CB+1): hole(cx(c),RY[r])
    a(f'<text x="{BL-16:.0f}" y="{RY[r]+6:.0f}" font-size="17" text-anchor="end" fill="#444">{r}</text>')
    a(f'<text x="{BR+14:.0f}" y="{RY[r]+6:.0f}" font-size="17" fill="#444">{r}</text>')
for c in range(CA,CB+1):
    if c%5==0:
        a(f'<text x="{cx(c):.0f}" y="{RY["A"]-16:.0f}" font-size="15" text-anchor="middle" fill="#444">{c}</text>')
        a(f'<text x="{cx(c):.0f}" y="{RY["J"]+26:.0f}" font-size="15" text-anchor="middle" fill="#444">{c}</text>')

def twidth(s,fs): return sum(fs*(1.0 if ord(ch)>0x2000 else 0.60) for ch in s)
def tlabel(x,y,s,fs=17,anc='middle',fill='#111'):
    w=twidth(s,fs); h=fs*1.15
    x0={'middle':x-w/2,'end':x-w}.get(anc,x)
    a(f'<rect x="{x0-5:.0f}" y="{y-h*0.80:.0f}" width="{w+10:.0f}" height="{h:.0f}" rx="4" fill="#fff" opacity="0.9"/>')
    a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="700" text-anchor="{anc}" fill="{fill}">{s}</text>')
def leader(pts):
    d='M '+' L '.join(f'{px:.0f} {py:.0f}' for px,py in pts)
    a(f'<path d="{d}" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<path d="{d}" stroke="#6a6a6a" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<circle cx="{pts[-1][0]:.0f}" cy="{pts[-1][1]:.0f}" r="3.5" fill="#6a6a6a"/>')
def wire(p1,p2,col=JMP):
    (c1,r1),(c2,r2)=p1,p2
    a(f'<path d="M {cx(c1):.0f} {Y(r1):.0f} L {cx(c2):.0f} {Y(r2):.0f}" stroke="{col}" stroke-width="6.5" fill="none" stroke-linecap="round" opacity="0.9"/>')
    a(f'<circle cx="{cx(c1):.0f}" cy="{Y(r1):.0f}" r="6" fill="{col}"/><circle cx="{cx(c2):.0f}" cy="{Y(r2):.0f}" r="6" fill="{col}"/>')
def part(p1,p2,label,body="#e3cba2",bw=38,lp=None,anc='middle',ldr=None):
    (c1,r1),(c2,r2)=p1,p2
    x1,y1,x2,y2=cx(c1),Y(r1),cx(c2),Y(r2); mx,my=(x1+x2)/2,(y1+y2)/2
    ang=math.degrees(math.atan2(y2-y1,x2-x1))
    a(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#9a9a9a" stroke-width="2.5"/>')
    a(f'<g transform="translate({mx:.0f},{my:.0f}) rotate({ang:.1f})"><rect x="{-bw/2:.0f}" y="-12" width="{bw:.0f}" height="24" rx="4" fill="{body}" stroke="#8a7a60" stroke-width="1.5"/></g>')
    if ldr: leader(ldr)
    lx,ly=lp if lp else (mx,my-26)
    tlabel(lx,ly,label,17,anc)

# ── TL072 3개 · 왼쪽이 1번 쪽 (A–E 가 8·7·6·5, F–J 가 1·2·3·4) ──
def ic(c0,name,sub1,sub2):
    for i in range(4):
        a(f'<line x1="{cx(c0+i):.0f}" y1="{RY["E"]:.0f}" x2="{cx(c0+i):.0f}" y2="{GUT_T+6:.0f}" stroke="#9a9a9a" stroke-width="5"/>')
        a(f'<line x1="{cx(c0+i):.0f}" y1="{RY["F"]:.0f}" x2="{cx(c0+i):.0f}" y2="{GUT_B-6:.0f}" stroke="#9a9a9a" stroke-width="5"/>')
        a(f'<text x="{cx(c0+i):.0f}" y="{RY["E"]-14:.0f}" font-size="14" text-anchor="middle" fill="#111">{8-i}</text>')
        a(f'<text x="{cx(c0+i):.0f}" y="{RY["F"]+26:.0f}" font-size="14" text-anchor="middle" fill="#111">{1+i}</text>')
    a(f'<rect x="{cx(c0)-P*0.45:.0f}" y="{GUT_T+4:.0f}" width="{3*P+P*0.9:.0f}" height="{GUT_B-GUT_T-8:.0f}" rx="5" fill="#3b3b3b"/>')
    a(f'<circle cx="{cx(c0)-P*0.45+14:.0f}" cy="{(GUT_T+GUT_B)/2:.0f}" r="8" fill="#606060"/>')
    a(f'<text x="{cx(c0+1.6):.0f}" y="{(GUT_T+GUT_B)/2-6:.0f}" font-size="16" font-weight="700" text-anchor="middle" fill="#fff">{name}</text>')
    a(f'<text x="{cx(c0+1.6):.0f}" y="{(GUT_T+GUT_B)/2+11:.0f}" font-size="11" text-anchor="middle" fill="#d8d8d0">{sub1}</text>')
    a(f'<text x="{cx(c0+1.6):.0f}" y="{(GUT_T+GUT_B)/2+25:.0f}" font-size="11" text-anchor="middle" fill="#d8d8d0">{sub2}</text>')
ic(3,'U1  TL072','A(아래) 입력버퍼 A','B(위) 가상접지')
ic(11,'U2  TL072','A(아래) 입력버퍼 B','B(위) 남는 반쪽')
ic(19,'U3  TL072','A(아래) 차동단','B(위) 2단')

# ── 배선 ── (수–수 점퍼선 18개)
wire((2,'TG'),(2,'BG'))            # 1
wire((17,'BV'),(17,'J'))           # 2  V− 를 위로
wire((17,'I'),(17,'C'))            # 3
part((9,'TV'),(9,'A'),'R1',lp=(cx(9)+20,(RAIL['TV']+RY['A'])/2+6),anc='start')
part((17,'B'),(9,'B'),'R2',lp=(cx(13),RY['B']-14))
wire((9,'C'),(6,'C'))              # 4  분압 중점 → U1b +입력
part((4,'D'),(5,'D'),'1 Ω',"#e3cba2",30,lp=(cx(3)-8,RY['D']+6),anc='end')
wire((4,'C'),(4,'TG'))             # 5  U1b 출력 = 가상접지
wire((3,'B'),(3,'TV'))             # 6
wire((6,'I'),(5,'BV'))             # 7
wire((11,'B'),(11,'TV'))           # 8
wire((14,'I'),(14,'BV'))           # 9
wire((19,'B'),(19,'TV'))           # 10
wire((22,'I'),(22,'BV'))           # 11
part((5,'J'),(5,'BG'),'Rb2',lp=(cx(4)-8,(RY['J']+Y('BG'))/2+6),anc='end')
part((13,'J'),(13,'BG'),'Rb1',lp=(cx(12)-8,(RY['J']+Y('BG'))/2+6),anc='end')
wire((3,'J'),(8,'J'))              # 12 U1a 출력 연장
part((8,'I'),(4,'I'),'Ra',lp=(cx(6),RY['I']-16))
wire((11,'J'),(16,'J'))            # 13 U2a 출력 연장
part((16,'I'),(12,'I'),'Rb',lp=(cx(12)-14,RY['I']+6),anc='end')
part((4,'G'),(12,'G'),'Rg 220 Ω',lp=(cx(8),RY['G']-16))
part((8,'H'),(20,'H'),'R3',lp=(cx(10),RY['H']+18))
part((16,'G'),(21,'G'),'R3′',lp=(cx(17.5),RY['G']-16))
wire((19,'J'),(24,'J'))            # 14 U3a 출력 연장
part((24,'I'),(20,'I'),'R4',lp=(cx(22),RY['I']-16))
part((21,'J'),(21,'BG'),'R4′',lp=(cx(20)-8,(RY['J']+Y('BG'))/2+6),anc='end')
part((24,'H'),(25,'E'),'C1',"#93b7dd",32,lp=(cx(26.2),(GUT_T+GUT_B)/2+6),anc='start')
part((25,'D'),(21,'D'),'Rin',lp=(cx(25)+16,RY['D']+6),anc='start')
wire((20,'A'),(26,'A'))            # 15 U3b 출력 연장
part((26,'B'),(21,'B'),'Rf',lp=(cx(26)+16,RY['B']+6),anc='start')
part((26,'C'),(21,'C'),'Cf',"#93b7dd",32,lp=(cx(26)+16,RY['C']+6),anc='start')
wire((22,'A'),(22,'TG'))           # 16 U3b +입력 → GND
part((12,'D'),(13,'D'),'1 Ω',"#e3cba2",30,lp=(cx(11)-8,RY['D']+6),anc='end')
wire((5,'H'),(1,'B'))            # 17 전극 B 를 위쪽으로
wire((13,'H'),(16,'B'))          # 18 전극 A 를 위쪽으로
part((14,'A'),(14,'TG'),'10 kΩ',lp=(cx(13)-8,(RY['A']+Y('TG'))/2+6),anc='end')
for c in (7,16):   # 레일 구멍은 6열마다 하나씩 비고, 0·6·12·18·24 가 빈 자리다
    part((c,'TV'),(c,'TG'),'Cd',"#93b7dd",28,lp=(cx(c)-22,(RAIL['TV']+RAIL['TG'])/2+6),anc='end')
    part((c,'BG'),(c,'BV'),'Cd',"#93b7dd",28,lp=(cx(c)-22,(RAIL['BG']+RAIL['BV'])/2+6),anc='end')

def lead(c,r,txt,col,side='L',dx=110):
    yy=Y(r); x=cx(c); x2=x-dx if side=='L' else x+dx
    a(f'<line x1="{x2:.0f}" y1="{yy:.0f}" x2="{x:.0f}" y2="{yy:.0f}" stroke="{col}" stroke-width="6.5" stroke-linecap="round" opacity="0.9"/>')
    a(f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="6" fill="{col}"/>')
    a(f'<text x="{(x2-10) if side=="L" else (x2+10):.0f}" y="{yy+6:.0f}" font-size="17" text-anchor="{"end" if side=="L" else "start"}" fill="#111">{txt}</text>')
for c,r,lab in [(16,'A','① 전극 A'),(1,'A','② 전극 B'),(10,'BG','③ 접지 전극'),
                (15,'TG','④ 케이지 호일'),(26,'E','⑦ 프로브 훅'),(28,'BG','⑧ 스코프 접지')]:
    a(f'<circle cx="{cx(c):.0f}" cy="{Y(r):.0f}" r="15" fill="#fff" stroke="{PRB if lab[0] in "⑦⑧" else ALG}" stroke-width="3.5"/>')
    a(f'<text x="{cx(c):.0f}" y="{Y(r)+6:.0f}" font-size="16" font-weight="700" text-anchor="middle" fill="#333">{lab[0]}</text>')
lead(0,'TV','⑤ 건전지 +',SNP,'L',100); lead(0,'BV','⑥ 건전지 −',SNP,'L',100)

a(f'<text x="{BL:.0f}" y="76" font-size="30" font-weight="700" fill="#111">브레드보드 배치도 — TL072 계측증폭기 (AD623 대체)</text>')
for i,t in enumerate([
 'AD623 미도착 시의 대체 회로. TL072 3개로 3-op-amp 계측증폭기를 만든다. 보드는 열 0–60 · 행 A–E / F–J, 여기는 0–32 만 그렸다.',
 '★ 신호는 전부 아래쪽(F–J)으로 지나가고, 위쪽(A–E)은 전원 · 가상접지 · 2단만 쓴다. 그래서 부품이 IC 위로 지나가지 않는다.',
 '★ 레일만 30열 부근에서 끊겨 있다. 레일에 붙는 것은 전부 28열 왼쪽에 두었다.',
 '★ 레일 구멍은 5개마다 한 칸씩 비어 있다 — 0 · 6 · 12 · 18 · 24 · 30 열에는 구멍이 없다. 레일에 붙는 것은 전부 구멍이 있는 열에 두었다.',
 '   그래도 레일은 통째로 한 덩어리라 구멍이 어긋나면 옆 구멍에 꽂아도 전기적으로 같다.',
 '★ 차동단의 R3 · R3′ · R4 · R4′ 는 10 kΩ 40개 중에서 멀티미터로 재어 가장 비슷한 4개를 고른다. 여기서 CMRR 이 정해진다.',
 '선 색은 실물의 종류다 — 파랑 = 수–수 점퍼선 · 청록 = 악어클립 리드 · 보라 = 건전지 스냅 · 검정 = 프로브.']):
    c='#c0392b' if i in (1,2,3,5) else '#444'; fw='700' if i in (1,2,3,5) else '400'
    a(f'<text x="{BL:.0f}" y="{108+i*26:.0f}" font-size="17" fill="{c}" font-weight="{fw}">{t}</text>')
a(f'<text x="{BL:.0f}" y="{RAIL["BV"]+70:.0f}" font-size="17" fill="#c0392b" font-weight="700">①–⑧ 은 시침핀 기둥 자리다. 전극 A(16열)와 전극 B(1열)는 약 38 mm 떨어져 있어 악어클립 두 개가 닿지 않는다.</text>')
ly=H-118
for i,(c,t) in enumerate([(JMP,'수–수 점퍼선 18개'),(ALG,'악어클립 리드 4개'),(SNP,'건전지 스냅 1개'),(PRB,'프로브')]):
    a(f'<line x1="{BL+i*300:.0f}" y1="{ly:.0f}" x2="{BL+44+i*300:.0f}" y2="{ly:.0f}" stroke="{c}" stroke-width="6.5" stroke-linecap="round"/>')
    a(f'<text x="{BL+56+i*300:.0f}" y="{ly+7:.0f}" font-size="18" fill="#111">{t}</text>')
for i,t in enumerate([
 '저항 16개 — 10 kΩ ×10 (R1·R2·Ra·Rb·R3·R3′·R4·R4′·Rf·U2b 접지) · 1 MΩ ×2 (Rb1·Rb2) · 3.3 kΩ (Rin) · 220 Ω (Rg) · 1 Ω ×2',
 '커패시터 6개 — 104(0.1 µF) ×4 디커플링 · 474 마일러(0.47 µF) C1 · 472(4.7 nF) Cf.    시침핀 9개 (보드 6 · 지렁이 3).',
 '1 Ω 두 개는 점퍼선 대신이다 — 되먹임에 넣는 1 Ω 은 전기적으로 점퍼와 같다.',
 '★ Ra · Rb · R3 · R4 의 몸통이 다른 열 위를 지나가는데, 그 아래는 전부 수–수 점퍼선이라 맨 리드가 닿을 곳이 없다. 맨 리드끼리 겹치던 자리는 없앴다.']):
    a(f'<text x="{BL:.0f}" y="{ly+40+i*26:.0f}" font-size="17" fill="#444">{t}</text>')
a('</svg>')
import os, cairosvg
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','그림')
SVG=os.path.normpath(os.path.join(OUT,'브레드보드_배치도_TL072IA.svg'))
PNG=os.path.normpath(os.path.join(OUT,'브레드보드_배치도_TL072IA.png'))
io.open(SVG,'w',encoding='utf-8').write('\n'.join(o))
cairosvg.svg2png(url=SVG, write_to=PNG, output_width=1700)
print('저장:', SVG, '·', PNG)
