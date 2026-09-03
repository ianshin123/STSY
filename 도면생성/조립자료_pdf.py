# -*- coding: utf-8 -*-
import io, os, re, base64, subprocess, markdown

ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
def md2html(path, drop_before=None, drop_after=None):
    s=io.open(os.path.join(ROOT,path),encoding='utf-8').read()
    if drop_before: s=s[s.index(drop_before):]
    if drop_after:  s=s[:s.index(drop_after)]
    # .md / 그림 링크는 PDF에서 쓸모없다 → 글자만 남긴다
    s=re.sub(r'\[([^\]]+)\]\((?!https?:)[^)]+\)', r'\1', s)
    s=re.sub(r'!\[[^\]]*\]\([^)]+\)', '', s)
    return markdown.markdown(s, extensions=['tables'])

def img(path):
    b=base64.b64encode(open(os.path.join(ROOT,path),'rb').read()).decode()
    return f'data:image/png;base64,{b}'

FIGS=[('전체연결도','보관/그림/전체연결도.png','조립할 때 펴 놓는 도면이다. 번호 ①–⑧ 은 아래 표와 짝이다.'),
      ('기호표','이번주/장치/그림/기호표.png','그림의 기호가 실물의 무엇인지. 선 색은 실물의 종류를 나타낸다.'),
      ('브레드보드 배치도','보관/그림/브레드보드_배치도.png','보드 안쪽만 크게 본 것.'),
      ('회로 원리도','보관/그림/회로도.png','전기 기호로 그린 회로. 실제로 꽂는 자리는 위 두 도면을 본다.')]

parts=[]
parts.append(f'''
<section class="cover">
  <h1>STSY 예비실험 조립 자료</h1>
  <p class="sub">2026년 8월 28일 · 측정장치팀 신이안 · 북일고등학교</p>
  <p class="lead">지렁이 거대신경섬유의 표면 신호(20–100 µV)를 오실로스코프로 볼 수 있게
  증폭하는 장치를 만든다. 이 묶음 하나로 조립이 끝나게 정리했다.</p>
  <h2>이 묶음에 있는 것</h2>
  <ol class="toc">
    <li>전체 연결도 — 지렁이 · 건전지 · 오실로스코프까지</li>
    <li>기호표 — 그림의 기호가 실물의 무엇인가</li>
    <li>브레드보드 배치도</li>
    <li>회로 원리도</li>
    <li>결선표 37항목 · 부품값 정하는 법 · 조립 순서</li>
    <li>장치 설명 — 부품이 하는 일과 용어</li>
  </ol>
  <div class="warn">
    <h3>조립 전에 확인할 것</h3>
    <ol>
      <li><b>오실로스코프 상자에 프로브가 있는가.</b> 부품 목록에 없고 스코프에 딸려 온다.
          없으면 오늘 측정이 안 된다 — BNC 어댑터가 없어 대체 불가.</li>
      <li><b>프로브 감쇠를 1X 로.</b> 10X 면 감도가 10분의 1이 되어 20–100 µV 를 볼 수 없다.</li>
      <li><b>AD623 모듈 봉지에 핀 헤더가 있는가.</b> 납땜해야 보드에 꽂힌다.</li>
      <li><b>시침핀이 9개 이상 있는가.</b> 지렁이 3개 + 보드 기둥 6개.</li>
      <li><b>모듈 두 핀 줄 사이 간격을 자로 잰다.</b> 0.3인치 → E·F행, 0.5인치 → D·G행,
          0.7인치 → C·H행. 셋 다 아니면 모듈을 보드 옆에 두고 암–수 점퍼선으로 잇는다.</li>
      <li><b>레일 양끝 도통을 멀티미터로 확인한다.</b> 네 줄 모두 30열 부근에서 끊겨 있다.</li>
      <li><b>전원부(결선표 1–14)만 먼저 조립하고 V+ · V− 를 잰다.</b>
          각각 건전지 전압의 절반쯤 나와야 한다. 안 나오면 다음으로 넘어가지 않는다.</li>
      <li><b>건전지는 1개다.</b> 2개를 직렬로 이으면 18 V 가 되어 AD623 절대최대 12 V 를 넘긴다.</li>
    </ol>
  </div>
</section>''')

for i,(t,p,cap) in enumerate(FIGS,1):
    parts.append(f'''<section class="fig">
      <h2>{i}. {t}</h2><p class="cap">{cap}</p>
      <img src="{img(p)}"/>
    </section>''')

# 「3. 부품값을 정하는 법」은 TL072 판과 공유하므로 이번주/장치/부품값.md 로 떼어 두었다.
# AD623 판 PDF 에는 그 자리에 다시 끼워 넣는다 — 결선표와 부품값은 한 부에 같이 있어야 한다.
parts.append('<section class="text"><h2>5. 결선표 · 부품값 · 조립 순서</h2>'
             + md2html('보관/AD623_회로도.md', drop_before='## 1. 부품 배치',
                       drop_after='## 3. 부품값을 정하는 법')
             + md2html('이번주/장치/부품값.md', drop_before='### 3-1. 분압 저항')
             + md2html('보관/AD623_회로도.md', drop_before='## 4. 조립 순서') + '</section>')
parts.append('<section class="text"><h2>6. 장치 설명</h2>'
             + md2html('이번주/장치/장치설명.md', drop_before='## 1. 이 장치가 하는 일을 한 문장으로') + '</section>')

html=f'''<!doctype html><html><head><meta charset="utf-8"><title>STSY 예비실험 조립 자료</title>
<style>
@page {{ size: A4 landscape; margin: 12mm 14mm; }}
body {{ font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif; font-size:9.5pt; line-height:1.55; color:#111; margin:0; }}
section {{ page-break-after: always; }}
section:last-child {{ page-break-after: auto; }}
h1 {{ font-size:26pt; margin:0 0 6pt; }}
h2 {{ font-size:15pt; margin:0 0 6pt; border-bottom:2px solid #333; padding-bottom:3pt; }}
h3 {{ font-size:11.5pt; margin:10pt 0 4pt; break-after:avoid; }}
h4 {{ break-after:avoid; }}
p,ul,ol,blockquote {{ orphans:3; widows:3; }}
h4 {{ font-size:10.5pt; margin:8pt 0 3pt; }}
.cover .sub {{ color:#666; font-size:11pt; margin:0 0 14pt; }}
.cover .lead {{ font-size:11pt; max-width:210mm; }}
.cover .toc li {{ margin:2pt 0; }}
.warn {{ margin-top:12pt; border:1.5px solid #c0392b; border-radius:5px; padding:8pt 14pt; background:#fdf6f5; }}
.warn h3 {{ color:#c0392b; margin-top:2pt; }}
.warn li {{ margin:3pt 0; }}
.fig {{ text-align:center; }}
.fig .cap {{ color:#555; font-size:9pt; margin:0 0 6pt; }}
.fig img {{ max-width:100%; max-height:165mm; object-fit:contain; }}
.text {{ column-count:2; column-gap:10mm; }}
.text h2 {{ column-span:all; }}
table {{ border-collapse:collapse; width:100%; margin:6pt 0; font-size:8.5pt; break-inside:avoid; }}
th,td {{ border:1px solid #bbb; padding:2.5pt 4pt; text-align:left; vertical-align:top; }}
th {{ background:#f0f0ec; }}
blockquote {{ margin:6pt 0; padding:5pt 9pt; border-left:3px solid #c9c9c2; background:#fafaf7; break-inside:avoid; }}
code {{ background:#f2f2ee; padding:0 2px; border-radius:2px; font-size:8.5pt; }}
hr {{ border:0; border-top:1px solid #ddd; margin:8pt 0; }}
p,ul,ol {{ margin:4pt 0; }} li {{ margin:1.5pt 0; }}
</style></head><body>{''.join(parts)}</body></html>'''
HERE=os.path.dirname(os.path.abspath(__file__))
TMP=os.path.join(HERE,'_bundle.html')
PDF=os.path.normpath(os.path.join(HERE,'..','보관','AD623판_조립자료.pdf'))
io.open(TMP,'w',encoding='utf-8').write(html)
print('html', len(html)//1024, 'KB')

# ── Chromium 헤드리스로 인쇄 ──
# 다른 환경에서는 chromium / google-chrome 경로만 바꾸면 된다.
CHROME=os.environ.get('CHROME','/opt/pw-browsers/chromium')
subprocess.run([CHROME,'--headless','--disable-gpu','--no-sandbox',
                '--no-pdf-header-footer', f'--print-to-pdf={PDF}',
                '--virtual-time-budget=25000', 'file://'+TMP], check=True)
os.remove(TMP)
print('저장:', PDF)
