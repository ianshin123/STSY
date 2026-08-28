# -*- coding: utf-8 -*-
"""예비예비실험(TL072 계측증폭기) 조립 자료 PDF.
AD623 판인 「조립자료_pdf.py」와 같은 형식이고, 읽어들이는 문서와 도면만 다르다."""
import io, os, re, base64, subprocess, markdown

ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
def md2html(path, drop_before=None, drop_after=None):
    s=io.open(os.path.join(ROOT,path),encoding='utf-8').read()
    if drop_before: s=s[s.index(drop_before):]
    if drop_after:  s=s[:s.index(drop_after)]
    s=re.sub(r'\[([^\]]+)\]\((?!https?:)[^)]+\)', r'\1', s)   # 링크는 글자만 남긴다
    s=re.sub(r'!\[[^\]]*\]\([^)]+\)', '', s)
    return markdown.markdown(s, extensions=['tables'])
def img(path):
    b=base64.b64encode(open(os.path.join(ROOT,path),'rb').read()).decode()
    return f'data:image/png;base64,{b}'

parts=[]
parts.append('''
<section class="cover">
  <h1>예비예비실험 조립 자료 — TL072 계측증폭기</h1>
  <p class="sub">2026년 8월 28일 · 측정장치팀 신이안 · 북일고등학교</p>
  <p class="lead"><b>AD623 이 해외배송으로 도착하지 않았다.</b> 보유한 TL072 세 개로 계측증폭기를 만들어
  조립과 측정을 연습한다. 이 묶음 하나로 끝나게 정리했다.</p>
  <h2>이 묶음에 있는 것</h2>
  <ol class="toc">
    <li>예비예비실험 — 무엇을 얻는가 · 순서 10단계 · 소신호 · 안전 · 기록표</li>
    <li>브레드보드 배치도 — 조립할 때 펴 놓는 도면</li>
    <li>기호표 — 그림의 기호가 실물의 무엇인가</li>
    <li>회로와 결선표 40항목 · 부품표 · 조립 순서</li>
  </ol>
  <div class="warn">
    <h3>손대기 전에 확인할 것</h3>
    <ol>
      <li><b>LM741CN 을 이 회로에 꽂지 않는다.</b> 권장 최소 공급전압이 ±10 V 인데
          이 회로는 ±4.5 V 다. 바이어스 전류도 TL072 의 1,200 배다.</li>
      <li><b>오실로스코프 상자에 프로브가 있는가.</b> 없으면 측정 자체가 안 된다 — BNC 어댑터가 없다.</li>
      <li><b>프로브 감쇠를 1X 로.</b> 10X 면 감도가 10 분의 1 이 된다.</li>
      <li><b>시침핀이 9개 이상 있는가.</b> 보드 기둥 6 개 + 여분. 지렁이를 쓰지 않으므로 3 개가 남는다.</li>
      <li><b>레일 양끝 도통을 멀티미터로 확인한다.</b> 네 줄 모두 30 열 부근에서 끊겨 있다.
          레일에 붙는 것은 전부 28 열 왼쪽에 두었다.</li>
      <li><b>조립 전에 10 kΩ 40 개를 재어 값이 가장 비슷한 네 개를 고른다.</b>
          차동단에 쓸 것이고, <b>여기서 CMRR 이 정해진다.</b></li>
      <li><b>전원부(결선 1–10)만 먼저 조립하고 V+ · V− 를 잰다.</b>
          각각 건전지 전압의 절반쯤 나와야 한다. 안 나오면 다음으로 넘어가지 않는다.</li>
      <li><b>건전지는 1 개다.</b> 두 개를 직렬로 이으면 18 V 가 되어, 나중에 도착할
          AD623 의 절대최대 12 V 를 넘긴다.</li>
      <li><b>TL072 는 반원 표시를 왼쪽으로 두고 홈을 걸쳐 꽂는다.</b>
          그러면 A–E 쪽이 8·7·6·5 번 핀, F–J 쪽이 1·2·3·4 번 핀이다.</li>
      <li><b>IC 를 꽂거나 뺄 때는 반드시 건전지를 분리한다.</b></li>
    </ol>
  </div>
</section>''')

parts.append('<section class="text"><h2>1. 예비예비실험 — 그날 무엇을 하는가</h2>'
             + md2html('예비예비실험.md', drop_before='## 1. 이 실험에서 무엇을 얻는가') + '</section>')

for i,(t,p,cap) in enumerate([
    ('브레드보드 배치도','장치/그림/브레드보드_배치도_TL072IA.png',
     '조립할 때 펴 놓는 도면이다. 번호 ①–⑧ 은 시침핀 기둥 자리이고 결선표와 짝이다.'),
    ('기호표','장치/그림/기호표.png',
     '그림의 기호가 실물의 무엇인지. 선 색은 역할이 아니라 실물의 종류를 나타낸다.')],2):
    parts.append(f'''<section class="fig">
      <h2>{i}. {t}</h2><p class="cap">{cap}</p>
      <img src="{img(p)}"/>
    </section>''')

parts.append('<section class="text"><h2>4. 회로 · 결선표 40항목 · 부품표</h2>'
             + md2html('장치/TL072계측증폭기.md', drop_before='## 1. 왜 이렇게 하는가') + '</section>')

html=f'''<!doctype html><html><head><meta charset="utf-8"><title>예비예비실험 조립 자료 — TL072</title>
<style>
@page {{ size: A4 landscape; margin: 12mm 14mm; }}
body {{ font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif; font-size:9.5pt; line-height:1.55; color:#111; margin:0; }}
section {{ page-break-after: always; }}
section:last-child {{ page-break-after: auto; }}
h1 {{ font-size:26pt; margin:0 0 6pt; }}
h2 {{ font-size:15pt; margin:0 0 6pt; border-bottom:2px solid #333; padding-bottom:3pt; }}
h3 {{ font-size:11.5pt; margin:10pt 0 4pt; break-after:avoid; }}
h4 {{ font-size:10.5pt; margin:8pt 0 3pt; break-after:avoid; }}
p,ul,ol,blockquote {{ orphans:3; widows:3; }}
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
TMP=os.path.join(HERE,'_bundle_tl072.html')
PDF=os.path.normpath(os.path.join(HERE,'..','예비예비실험_조립자료_TL072.pdf'))
io.open(TMP,'w',encoding='utf-8').write(html)
print('html', len(html)//1024, 'KB')
CHROME=os.environ.get('CHROME','/opt/pw-browsers/chromium')
subprocess.run([CHROME,'--headless','--disable-gpu','--no-sandbox',
                '--no-pdf-header-footer', f'--print-to-pdf={PDF}',
                '--virtual-time-budget=25000', 'file://'+TMP], check=True)
os.remove(TMP)
print('저장:', PDF)
