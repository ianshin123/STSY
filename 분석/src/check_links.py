"""저장소 무결성 검사 — 깨진 링크와 망가진 표를 잡는다.

    python3 분석/src/check_links.py

파일 이름을 바꿨는데 가리키는 링크를 안 고쳤거나, 편집하다 표가 깨졌을 때
커밋 전에 잡으려고 만들었다. CLAUDE.md 커밋 규칙
("이름을 바꾸면 그 파일을 가리키는 링크를 같은 커밋에서 고친다")의 자동 점검판이다.

문제를 찾으면 종료코드 1.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
WIKILINK = re.compile(r"(?<!\[)\[\[([^\]]+)\]\]")
EXTERNAL = ("http://", "https://", "#", "mailto:")


SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", ".venv", "venv"}


def md_files() -> list[Path]:
    return sorted(
        p for p in REPO.rglob("*.md") if not SKIP_DIRS.intersection(p.parts)
    )


def check_links(path: Path, text: str) -> list[str]:
    """상대 경로 링크가 실제 파일을 가리키는지."""
    bad = []
    for m in LINK.finditer(text):
        target = m.group(2).strip()
        if target.startswith(EXTERNAL):
            continue
        resolved = (path.parent / target.split("#")[0]).resolve()
        if not resolved.exists():
            line = text[: m.start()].count("\n") + 1
            bad.append(f"{path.relative_to(REPO)}:{line}  깨진 링크 → {target}")
    return bad


def strip_code(text: str) -> str:
    """코드 블록과 인라인 코드를 같은 길이의 공백으로 지운다.

    줄 번호와 위치를 보존해야 하므로 삭제하지 않고 치환한다.
    문서가 규칙 자체를 예시로 보여줄 때(``[[위키링크]]``) 오탐을 막는다.
    """
    def blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))

    text = re.sub(r"(?ms)^```.*?^```", blank, text)
    text = re.sub(r"`[^`\n]*`", blank, text)
    return text


def check_wikilinks(path: Path, text: str) -> list[str]:
    """[[위키링크]]는 GitHub에서 글자 그대로 나온다 — 쓰지 않는다."""
    out = []
    for m in WIKILINK.finditer(strip_code(text)):
        line = text[: m.start()].count("\n") + 1
        out.append(
            f"{path.relative_to(REPO)}:{line}  위키링크 [[{m.group(1)}]] "
            f"— GitHub에서 렌더링되지 않는다. [텍스트](경로.md) 로 쓸 것"
        )
    return out


def check_tables(path: Path, text: str) -> list[str]:
    """표 구분선(|---|)이 헤더 없이 떠 있거나 열 수가 안 맞는 경우.

    편집하다 표 한 조각만 남는 사고를 잡는다.
    """
    bad = []
    lines = text.split("\n")
    in_code = False
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # 표 구분선처럼 보이는가 — 앞에 | 가 없어도 잡아야 한다.
        # 지난 사고가 정확히 이 형태였다: 줄 첫머리가 `---|---|---|`
        if "|" not in s or "-" not in s:
            continue
        if not re.fullmatch(r"\|?[\s:|-]+\|?", s):
            continue
        if s.strip("-") == "":  # 그냥 수평선(---)
            continue
        prev = lines[i - 1].strip() if i else ""
        if not prev.startswith("|"):
            bad.append(f"{path.relative_to(REPO)}:{i + 1}  헤더 없는 표 구분선 → {s[:40]}")
            continue
        if prev.count("|") != s.count("|"):
            bad.append(
                f"{path.relative_to(REPO)}:{i + 1}  헤더와 구분선의 열 수가 다르다 "
                f"({prev.count('|')} vs {s.count('|')})"
            )
    return bad


def check_orphans(files: list[Path], texts: dict[Path, str]) -> list[str]:
    """어디서도 링크되지 않는 노트. 오류는 아니고 알림이다."""
    linked: set[Path] = set()
    for path, text in texts.items():
        for m in LINK.finditer(text):
            t = m.group(2).strip()
            if t.startswith(EXTERNAL):
                continue
            resolved = (path.parent / t.split("#")[0]).resolve()
            if resolved.exists():
                linked.add(resolved)
    roots = {REPO / n for n in ("README.md", "현재.md", "CLAUDE.md")}
    return [
        f"{f.relative_to(REPO)}  어디서도 링크되지 않는다"
        for f in files
        if f.resolve() not in linked and f.resolve() not in roots
    ]


def main() -> int:
    files = md_files()
    texts = {f: f.read_text(encoding="utf-8") for f in files}

    errors: list[str] = []
    for f, t in texts.items():
        errors += check_links(f, t)
        errors += check_wikilinks(f, t)
        errors += check_tables(f, t)

    warnings = check_orphans(files, texts)

    n_links = sum(
        1
        for t in texts.values()
        for m in LINK.finditer(t)
        if not m.group(2).strip().startswith(EXTERNAL)
    )
    print(f"문서 {len(files)}개 · 내부 링크 {n_links}개")

    if warnings:
        print(f"\n알림 {len(warnings)}건 (오류 아님)")
        for w in warnings:
            print("  ·", w)

    if errors:
        print(f"\n오류 {len(errors)}건")
        for e in errors:
            print("  ✗", e)
        return 1

    print("\n문제 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
