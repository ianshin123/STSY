# -*- coding: utf-8 -*-
import io, math
P=32.0; X0=205.0; CA,CB=0,37
SPLIT=30
ROWS=['A','B','C','D','E','F','G','H','I','J']
RY={}; y=372.0
for r in ROWS[:5]: RY[r]=y; y+=P
GUT_T=y-P*0.5; GUT_B=GUT_T+P*2.3; y=GUT_B+P*0.5
for r in ROWS[5:]: RY[r]=y; y+=P
RAIL={'TV':240.0,'TG':280.0,'BG':RY['J']+64,'BV':RY['J']+104}
def cx(c): return X0+(c-CA)*P
W=cx(CB)+300; H=RAIL['BV']+220
o=[]; a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" font-family="Noto Sans CJK KR, sans-serif"><rect width="{W:.0f}" height="{H:.0f}" fill="#fff"/>')
BL=X0-84; BR=cx(CB)+58
a(f'<rect x="{BL:.0f}" y="{RAIL["TV"]-42:.0f}" width="{BR-BL:.0f}" height="{RAIL["BV"]-RAIL["TV"]+84:.0f}" rx="10" fill="#fcfcfa" stroke="#c2c2ba" stroke-width="2"/>')
a(f'<rect x="{BL:.0f}" y="{GUT_T:.0f}" width="{BR-BL:.0f}" height="{GUT_B-GUT_T:.0f}" fill="#ebebe5"/>')
a(f'<text x="{BL+12:.0f}" y="{(GUT_T+GUT_B)/2+6:.0f}" font-size="15" fill="#8a8a8a">홈</text>')
JMP='#1a5fb4'; ALG='#0f9b8e'; SNP='#8e44ad'; PRB='#2f2f2f'
RAILR='#e2a8a8'; RAILB='#aab8dd'; GRY='#9a9a9a'
RED=JMP;BLU=JMP;BLK=JMP;GRN=JMP
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
def Y(r): return RAIL[r] if r in RAIL else RY[r]
def wire(p1,p2,col):
    (c1,r1),(c2,r2)=p1,p2
    a(f'<path d="M {cx(c1):.0f} {Y(r1):.0f} L {cx(c2):.0f} {Y(r2):.0f}" stroke="{col}" stroke-width="6.5" fill="none" stroke-linecap="round" opacity="0.9"/>')
    a(f'<circle cx="{cx(c1):.0f}" cy="{Y(r1):.0f}" r="6" fill="{col}"/><circle cx="{cx(c2):.0f}" cy="{Y(r2):.0f}" r="6" fill="{col}"/>')
def twidth(s,fs):
    """글자 폭 어림 — 한글은 fs 한 칸, 라틴·숫자는 0.60 칸."""
    return sum(fs*(1.0 if ord(ch)>0x2000 else 0.60) for ch in s)
def tlabel(x,y,s,fs=17,anc='middle',fill='#111'):
    """구멍 격자 위에 얹혀도 읽히도록 흰 바탕을 깔고 쓴다."""
    w=twidth(s,fs); h=fs*1.15
    x0={'middle':x-w/2,'end':x-w}.get(anc,x)
    a(f'<rect x="{x0-5:.0f}" y="{y-h*0.80:.0f}" width="{w+10:.0f}" height="{h:.0f}" rx="4" fill="#fff" opacity="0.9"/>')
    a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="700" text-anchor="{anc}" fill="{fill}">{s}</text>')
def leader(pts):
    """이름표 → 부품 지시선. 흰 테두리를 깔아 다른 선 위로 지나간다."""
    d='M '+' L '.join(f'{px:.0f} {py:.0f}' for px,py in pts)
    a(f'<path d="{d}" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<path d="{d}" stroke="#6a6a6a" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<circle cx="{pts[-1][0]:.0f}" cy="{pts[-1][1]:.0f}" r="3.5" fill="#6a6a6a"/>')
def part(p1,p2,label,body="#e3cba2",bw=38,lp=None,anc='middle',ldr=None):
    (c1,r1),(c2,r2)=p1,p2
    x1,y1,x2,y2=cx(c1),Y(r1),cx(c2),Y(r2); mx,my=(x1+x2)/2,(y1+y2)/2
    ang=math.degrees(math.atan2(y2-y1,x2-x1))
    a(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#9a9a9a" stroke-width="2.5"/>')
    a(f'<g transform="translate({mx:.0f},{my:.0f}) rotate({ang:.1f})"><rect x="{-bw/2:.0f}" y="-12" width="{bw:.0f}" height="24" rx="4" fill="{body}" stroke="#8a7a60" stroke-width="1.5"/></g>')
    if ldr: leader(ldr)
    lx,ly=lp if lp else (mx,my-26)
    tlabel(lx,ly,label,17,anc)
# ── AD623 모듈 (핀 확정) ──
mt=['GND','IN+','IN−','+VS']; mb=['GND','OUT','REF','−VS']
for i in range(4):
    a(f'<line x1="{cx(4+i):.0f}" y1="{RY["E"]:.0f}" x2="{cx(4+i):.0f}" y2="{GUT_T+6:.0f}" stroke="#9a9a9a" stroke-width="5"/>')
    a(f'<line x1="{cx(4+i):.0f}" y1="{RY["F"]:.0f}" x2="{cx(4+i):.0f}" y2="{GUT_B-6:.0f}" stroke="#9a9a9a" stroke-width="5"/>')
    a(f'<text x="{cx(4+i):.0f}" y="{RY["E"]-14:.0f}" font-size="13" text-anchor="middle" fill="#111">{mt[i]}</text>')
    a(f'<text x="{cx(4+i):.0f}" y="{RY["F"]+26:.0f}" font-size="13" text-anchor="middle" fill="#111">{mb[i]}</text>')
MOX0,MOX1=cx(1)-14,cx(7)+26; MOY0,MOY1=RY['E']-46,RY['F']+46
a(f'<rect x="{MOX0:.0f}" y="{MOY0:.0f}" width="{MOX1-MOX0:.0f}" height="{MOY1-MOY0:.0f}" rx="6" fill="#2f2f2f" opacity="0.12" stroke="#c0392b" stroke-width="2.5" stroke-dasharray="8 5"/>')
for _r in ('E','F'):
    a(f'<circle cx="{cx(2):.0f}" cy="{Y(_r):.0f}" r="13" fill="none" stroke="#c0392b" stroke-width="3"/>')
    a(f'<circle cx="{cx(2):.0f}" cy="{Y(_r):.0f}" r="5" fill="none" stroke="#c0392b" stroke-width="2"/>')
tlabel(MOX0+6,MOY0-30,'모듈 바닥 면적',15,'start','#c0392b')
a(f'<rect x="{cx(4)-P*0.5:.0f}" y="{GUT_T+4:.0f}" width="{3*P+P:.0f}" height="{GUT_B-GUT_T-8:.0f}" rx="5" fill="#2f2f2f"/>')
a(f'<text x="{cx(5.5):.0f}" y="{(GUT_T+GUT_B)/2+7:.0f}" font-size="17" font-weight="700" text-anchor="middle" fill="#fff">AD623 모듈</text>')
# ── TL072 ──
for i in range(4):
    a(f'<line x1="{cx(21+i):.0f}" y1="{RY["E"]:.0f}" x2="{cx(21+i):.0f}" y2="{GUT_T+6:.0f}" stroke="#9a9a9a" stroke-width="5"/>')
    a(f'<line x1="{cx(21+i):.0f}" y1="{RY["F"]:.0f}" x2="{cx(21+i):.0f}" y2="{GUT_B-6:.0f}" stroke="#9a9a9a" stroke-width="5"/>')
    a(f'<text x="{cx(21+i):.0f}" y="{RY["E"]-14:.0f}" font-size="14" text-anchor="middle" fill="#111">{8-i}</text>')
    a(f'<text x="{cx(21+i):.0f}" y="{RY["F"]+26:.0f}" font-size="14" text-anchor="middle" fill="#111">{1+i}</text>')
a(f'<rect x="{cx(21)-P*0.45:.0f}" y="{GUT_T+4:.0f}" width="{3*P+P*0.9:.0f}" height="{GUT_B-GUT_T-8:.0f}" rx="5" fill="#3b3b3b"/>')
a(f'<circle cx="{cx(21)-P*0.45+15:.0f}" cy="{(GUT_T+GUT_B)/2:.0f}" r="9" fill="#606060"/>')
a(f'<text x="{cx(22.6):.0f}" y="{(GUT_T+GUT_B)/2+7:.0f}" font-size="19" font-weight="700" text-anchor="middle" fill="#fff">TL072</text>')
# ── 배선 ──
wire((14,'TG'),(14,'BG'),JMP)                     # GND 위아래
wire((7,'B'),(7,'TV'),JMP)                       # +VS
wire((7,'I'),(7,'BV'),JMP)                       # −VS
wire((4,'B'),(4,'TG'),JMP)                       # 모듈 GND
wire((6,'I'),(5,'BG'),JMP)                       # REF → GND · 레일 6열은 구멍이 없다
# Rb1·Rb2 는 5열·6열로 한 칸 차이라 옆에 이름을 쓸 자리가 없다 → 지시선으로 빼낸다
_RBY=(RY['B']+RAIL['TG'])/2                       # 두 저항 몸통의 높이
part((5,'B'),(5,'TG'),'Rb1',lp=(cx(12),RAIL['TG']+24),anc='start',
     ldr=[(cx(11.8),RAIL['TG']+18),(cx(5),RAIL['TG']+18),(cx(5),_RBY-19)])
part((6,'B'),(7,'TG'),'Rb2',lp=(cx(12),_RBY+6),anc='start',
     ldr=[(cx(11.8),_RBY),(cx(6)+13,_RBY)])
wire((5,'J'),(10,'F'),JMP)                       # OUT →
part((10,'G'),(13,'G'),'C1',"#93b7dd",32,lp=(cx(11.5),RY['G']-12))
part((13,'H'),(22,'H'),'Rin',lp=(cx(17),RY['H']-14))
wire((21,'J'),(26,'J'),JMP); wire((22,'I'),(30,'I'),JMP)
part((26,'H'),(30,'H'),'Rf',lp=(cx(28),RY['H']+18)); part((26,'G'),(30,'G'),'Cf',"#93b7dd",32,lp=(cx(28),RY['G']-12))
wire((26,'F'),(34,'F'),JMP)
wire((21,'C'),(21,'TV'),JMP)                     # 8번 V+
wire((24,'G'),(23,'BV'),JMP)                     # 4번 V− · 레일 24열은 구멍이 없다
wire((23,'G'),(23,'BG'),JMP)                     # 3번 GND
wire((22,'D'),(23,'D'),JMP)                      # 7번→6번
wire((22,'C'),(22,'TG'),JMP)                     # 7번→GND
wire((18,'J'),(17,'BV'),JMP); wire((18,'I'),(18,'C'),JMP)   # V− 를 위로 · 레일 18열은 구멍이 없다
part((26,'TV'),(26,'A'),'R1',lp=(cx(26)+22,(RAIL['TV']+RY['A'])/2+6),anc='start')
part((18,'B'),(26,'B'),'R2',lp=(cx(22),RY['B']-12))
wire((26,'C'),(24,'C'),JMP)                      # 중점 → 5번
part((10,'TV'),(10,'TG'),'Cd',"#93b7dd",28,lp=(cx(10)-22,(RAIL['TV']+RAIL['TG'])/2+6),anc='end')
part((16,'BG'),(16,'BV'),'Cd',"#93b7dd",28,lp=(cx(16)+22,(RAIL['BG']+RAIL['BV'])/2+6),anc='start')
def lead(c,r,txt,col,side='L',dx=110):
    yy=Y(r); x=cx(c); x2=x-dx if side=='L' else x+dx
    a(f'<line x1="{x2:.0f}" y1="{yy:.0f}" x2="{x:.0f}" y2="{yy:.0f}" stroke="{col}" stroke-width="6.5" stroke-linecap="round" opacity="0.9"/>')
    a(f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="6" fill="{col}"/>')
    a(f'<text x="{(x2-10) if side=="L" else (x2+10):.0f}" y="{yy+6:.0f}" font-size="17" text-anchor="{"end" if side=="L" else "start"}" fill="#111">{txt}</text>')
wire((5,'A'),(11,'A'),JMP); wire((6,'A'),(20,'A'),JMP)   # 전극 마중 점퍼
for c,r,lab in [(11,'B','① 전극 A'),(20,'B','② 전극 B'),(12,'BG','③ 접지 전극'),
                (15,'TG','④ 케이지 호일'),(28,'BG','⑧ 스코프 접지'),(34,'G','⑦ 프로브 훅')]:
    a(f'<circle cx="{cx(c):.0f}" cy="{Y(r):.0f}" r="15" fill="#fff" stroke="{PRB if lab[0] in "⑦⑧" else ALG}" stroke-width="3.5"/>')
    a(f'<text x="{cx(c):.0f}" y="{Y(r)+6:.0f}" font-size="16" font-weight="700" text-anchor="middle" fill="#333">{lab[0]}</text>')
lead(0,'TV','⑤ 건전지 +',SNP,'L',100); lead(0,'BV','⑥ 건전지 −',SNP,'L',100)
a(f'<text x="{BL:.0f}" y="{RAIL["BV"]+70:.0f}" font-size="17" fill="#c0392b" font-weight="700">①–⑧ 은 시침핀 기둥 자리다. 자세한 것은 「전체 연결도」를 본다.</text>')
a(f'<text x="{BL:.0f}" y="76" font-size="30" font-weight="700" fill="#111">브레드보드 배치도 — 완성본</text>')
for i,t in enumerate([
 '보드는 열 0–60, 행 A–E / F–J. 위 그림은 0–37까지만 그렸다.',
 '★ 레일(가장자리 네 줄)만 30열 부근에서 끊겨 있다. 레일에 연결하는 것은 전부 30열 왼쪽에 두었고, 신호선만 30열을 넘어간다.',
 '★ 모듈은 큰 고정 구멍 2개가 핀 줄의 연장선상, GND 핀 바깥쪽(왼쪽)에 더 나와 있다. 모듈 발밑에는 아무것도 꽂지 않았다.',
 '선 색은 실물의 종류다 — 역할(V+ · GND …)은 이름표와 결선표에 적었다. 연한 빨강·파랑 줄은 보드에 인쇄된 레일 표시다.']):
    c='#c0392b' if i in (1,2) else '#444'; fw='700' if i in (1,2) else '400'
    a(f'<text x="{BL:.0f}" y="{110+i*26:.0f}" font-size="17" fill="{c}" font-weight="{fw}">{t}</text>')
ly=H-112
for i,(c,t) in enumerate([(JMP,'수–수 점퍼선'),(ALG,'악어클립 리드'),(SNP,'건전지 스냅 연선'),(PRB,'프로브')]):
    a(f'<line x1="{BL+i*300:.0f}" y1="{ly:.0f}" x2="{BL+44+i*300:.0f}" y2="{ly:.0f}" stroke="{c}" stroke-width="6.5" stroke-linecap="round"/>')
    a(f'<text x="{BL+56+i*300:.0f}" y="{ly+7:.0f}" font-size="18" fill="#111">{t}</text>')
a(f'<text x="{BL:.0f}" y="{ly+40:.0f}" font-size="17" fill="#444">AD623 모듈 핀은 실물 표기대로다 — 윗줄 GND · IN+ · IN− · +VS / 아랫줄 GND · OUT · REF · −VS. 이득 트리머가 달려 있으므로 RG 저항은 꽂지 않는다.</text>')
a(f'<text x="{BL:.0f}" y="{ly+68:.0f}" font-size="17" fill="#444">모듈의 두 핀 줄이 홈을 걸치지 못하면, 암–수 점퍼선으로 모듈을 보드 옆에 두고 연결한다.</text>')
a('</svg>')
# ── 저장: SVG 와 PNG 를 같이 만든다 ──
import os, cairosvg
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','그림')
SVG=os.path.normpath(os.path.join(OUT,'브레드보드_배치도.svg'))
PNG=os.path.normpath(os.path.join(OUT,'브레드보드_배치도.png'))
io.open(SVG,'w',encoding='utf-8').write('\n'.join(o))
cairosvg.svg2png(url=SVG, write_to=PNG, output_width=1600)
print('저장:', SVG, '·', PNG)
