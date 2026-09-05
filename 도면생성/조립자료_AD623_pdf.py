# -*- coding: utf-8 -*-
"""TL072 계측증폭기 조립 자료 PDF — 지금 쓰는 회로의 참조.
AD623 판인 「조립자료_pdf.py」와 **같은 형식**이다 — 표지 · 도면 4쪽 · 본문.
읽어들이는 문서와 도면만 다르다."""
import io, os, re, base64, subprocess, markdown

ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
def md2html(path, drop_before=None, drop_after=None, cuts=()):
    s=io.open(os.path.join(ROOT,path),encoding='utf-8').read()
    if drop_before: s=s[s.index(drop_before):]
    if drop_after:  s=s[:s.index(drop_after)]
    # (시작표시, 끝표시, 대신 넣을 것) — AD623 전용 절을 들어내는 데 쓴다
    for beg,end,rep in cuts:
        i=s.index(beg); j=s.index(end,i); s=s[:i]+rep+s[j:]
    # .md / 그림 링크는 PDF에서 쓸모없다 → 글자만 남긴다
    s=re.sub(r'\[([^\]]+)\]\((?!https?:)[^)]+\)', r'\1', s)
    s=re.sub(r'!\[[^\]]*\]\([^)]+\)', '', s)
    return markdown.markdown(s, extensions=['tables'])

def img(path):
    b=base64.b64encode(open(os.path.join(ROOT,path),'rb').read()).decode()
    return f'data:image/png;base64,{b}'

FIGS=[('2채널 전체 연결도 — 실험실에 들고 가는 한 장','이번주/장치/그림/전체연결도_2채널.png',
       '보드 두 장 · 챔버 · 건전지 · 오디오 인터페이스까지 한 장에. 번호 ①–⑨ 가 보드 바깥으로 나가는 자리다.'),
      ('브레드보드 배치도 — 1번 보드 (채널 1)','이번주/장치/그림/브레드보드_배치도_1번보드.png',
       '★ 꽂을 값이 부품마다 적혀 있다. 색띠도 그 값의 띠로 그렸다. 전원부(R1·R2·가상접지 버퍼)가 여기 있다.'),
      ('브레드보드 배치도 — 2번 보드 (채널 2)','이번주/장치/그림/브레드보드_배치도_2번보드.png',
       '1번 보드와 자리가 같다. 없는 것은 R1·R2 와 가상접지 배선뿐이고, 대신 6열 C행에 10 kΩ 이 하나 더 들어간다.'),
      ('기호표','이번주/장치/그림/기호표.png',
       '그림의 기호가 실물의 무엇인지. 선 색은 역할이 아니라 실물의 종류를 나타낸다.'),
      ]

parts=[]
parts.append('''
<section class="cover">
  <h1>AD623 계측증폭기 — 조립 자료</h1>
  <p class="sub">2026년 8월 29일 조립·검증 완료 · 측정장치팀 신이안 · 북일고등학교</p>
  <p class="lead"><b>지금 쓰는 회로다.</b> AD623 이 오지 않아 보유한 TL072 세 개로 같은
  3-op-amp 계측증폭기를 밖에서 만들었고, <b>2026-08-29 실험에서 작동을 확인했다</b>
  (양쪽 전극 상쇄 0 V · 비마취 지렁이에서 자극 반응). <b>AD623 으로 다시 만들지 않는다.</b></p>
  <div class="warn" style="border-color:#8e44ad;background:#faf6fd">
    <h3 style="color:#8e44ad">★ 이 묶음의 도면 4쪽은 「1채널 · 오실로스코프」 판이다</h3>
    <p><b>2026-08-29 저녁에 두 가지가 바뀌었다.</b> ① 채널을 2개로 만든다 —
    보드를 한 벌 더 만들고 레일 3줄을 끌어온다. ② 오실로스코프를 안 쓰고
    <b>오디오 인터페이스로 컴퓨터에 녹음한다.</b> 그리고 <b>전극이 3개다</b> —
    채널마다 기록 하나 + 두 채널이 기준(접지) 하나를 함께 쓴다
    (그래서 <b>결선 24번이 1 MΩ 이 아니라 1 Ω 이다</b>).</p>
    <p><b>실험실에는 「2채널 전체 연결도」한 장을 들고 간다</b>
    (<code>이번주/장치/전체연결도_2채널.pdf</code>). <b>이 묶음은 보드 한 장을 조립할 때의
    결선표·부품표 참조로 쓴다</b> — 5절과 6절이 그것이다.</p>
  </div>
  <h2>이 묶음에 있는 것</h2>
  <ol class="toc">
    <li>전체 연결도 — <b>1채널 · 오실로스코프 판</b> (지난 판)</li>
    <li>기호표 — 그림의 기호가 실물의 무엇인가</li>
    <li>브레드보드 배치도</li>
    <li>회로 원리도</li>
    <li>결선표 48항목 · 부품표 · 조립 순서</li>
    <li>장치 설명 — 부품이 하는 일과 용어</li>
  </ol>
  <div class="warn">
    <h3>손대기 전에 확인할 것</h3>
    <ol>
      <li><b>LM741CN 을 이 회로에 꽂지 않는다.</b> 권장 최소 공급전압이 ±10 V 인데
          이 회로는 ±4.5 V 다. 바이어스 전류도 TL072 의 1,200 배다.</li>
      <li><b>멀티미터가 있는가.</b> 오실로스코프를 안 쓰므로 이것이 없으면 아무것도 확인할 수 없다.</li>
      <li><b>시침핀이 15개 이상 있는가.</b> 보드 기둥 12 개(보드마다 6 개) + 지렁이 전극 3 개.</li>
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

for i,(t,p,cap) in enumerate(FIGS,1):
    parts.append(f'''<section class="fig">
      <h2>{i}. {t}</h2><p class="cap">{cap}</p>
      <img src="{img(p)}"/>
    </section>''')

parts.append('<section class="text"><h2>5. 결선표 48항목 · 부품표 · 조립 순서</h2>'
             + md2html('이번주/장치/AD623계측증폭기.md', drop_before='## 1. 왜 갈아탔나') + '</section>')

# 7절은 AD623 판과 공통 문서다. 다만 4-2·4-3절은 AD623 소자 전용이라 6절 2-1 로 보낸다.
parts.append('<section class="text"><h2>6. 장치 설명 — 부품이 하는 일과 용어</h2>'
             + '<blockquote><b>이 절은 AD623 판 조립 자료와 같은 문서다.</b> '
               '전원부 · 브레드보드 · 전극 · 색띠 · 케이지는 두 회로가 같다. '
               '<b>증폭 부분만 소자가 다르고, 그것은 위 5절 2-1 절에 있다.</b></blockquote>'
             + md2html('이번주/장치/장치설명.md',
                       drop_before='## 1. 이 장치가 하는 일을 한 문장으로',
                       cuts=[('### 4-2. 1단 — AD623 계측증폭기',
                              '### 4-4. 전극 — 왜 세 개인가',
                              '### 4-2 · 4-3. 1단 · 2단 — **이 판에서는 5절 2-1 절을 본다**\n\n'
                              'AD623 판은 계측증폭기 칩 하나가 1단을 맡는다. '
                              '**이 회로는 그것을 TL072 세 개로 밖에서 만들었으므로 1단과 차동단이 나뉘어 있다.**\n\n'
                              '2단(C1 · Rin · Rf · Cf)은 두 판이 부품도 값도 같다.\n\n')])
             + '</section>')

html=f'''<!doctype html><html><head><meta charset="utf-8"><title>TL072 계측증폭기 조립 자료</title>
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
PDF=os.path.normpath(os.path.join(HERE,'..','이번주','장치','조립자료_AD623.pdf'))
io.open(TMP,'w',encoding='utf-8').write(html)
print('html', len(html)//1024, 'KB')
CHROME=os.environ.get('CHROME','/opt/pw-browsers/chromium')
subprocess.run([CHROME,'--headless','--disable-gpu','--no-sandbox',
                '--no-pdf-header-footer', f'--print-to-pdf={PDF}',
                '--virtual-time-budget=25000', 'file://'+TMP], check=True)
os.remove(TMP)
print('저장:', PDF)
