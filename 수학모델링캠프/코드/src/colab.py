"""구글 코랩에서 이 코드를 돌리기 위한 잡일.

코랩에서 걸리는 것은 두 가지뿐이다.
1. 저장소를 받아 경로를 잡는 일
2. matplotlib 이 한글을 못 그려 네모(두부)로 나오는 일

둘 다 여기서 처리한다. 노트북 첫 칸에서:

    !git clone -q https://github.com/ianshin123/STSY.git
    import sys; sys.path.insert(0, '/content/STSY/수학모델링캠프/코드/src')
    import colab; colab.setup()
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/ianshin123/STSY.git"


def add_paths(repo_root: str | Path = "/content/STSY") -> Path:
    """이 프로젝트의 src 와 저장소의 분석/src 를 둘 다 import 가능하게 만든다."""
    root = Path(repo_root)
    if not root.exists():
        raise FileNotFoundError(f"{root} 가 없다. 먼저 저장소를 clone 해라")
    for p in (root / "수학모델링캠프" / "코드" / "src", root / "분석" / "src"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    return root


def korean_font(quiet: bool = True) -> bool:
    """한글 폰트를 깔고 matplotlib 에 물린다.

    코랩 기본 이미지에는 한글 폰트가 없어서 축 이름이 전부 네모로 나온다.
    나눔고딕을 설치하고 폰트 캐시를 다시 만든다. 성공하면 True.
    설치가 안 되면 그래프 이름을 영문으로 쓰면 된다 — 계산에는 영향이 없다.
    """
    import matplotlib

    try:
        from matplotlib import font_manager

        if not any("Nanum" in f.name for f in font_manager.fontManager.ttflist):
            out = subprocess.DEVNULL if quiet else None
            subprocess.run(["apt-get", "-qq", "install", "-y", "fonts-nanum"],
                           check=True, stdout=out, stderr=out)
            for path in font_manager.findSystemFonts(fontpaths=["/usr/share/fonts"]):
                if "Nanum" in path:
                    font_manager.fontManager.addfont(path)
        matplotlib.rc("font", family="NanumGothic")
        matplotlib.rc("axes", unicode_minus=False)   # 음수 기호가 깨지는 것 방지
        return True
    except Exception:
        matplotlib.rc("axes", unicode_minus=False)
        return False


def setup(repo_root: str | Path = "/content/STSY") -> Path:
    """경로 + 폰트를 한 번에. 노트북 첫 칸에서 이것만 부르면 된다."""
    root = add_paths(repo_root)
    if not korean_font():
        print("한글 폰트 설치 실패 — 그래프 이름은 영문으로 써라 (계산은 정상)")
    return root
