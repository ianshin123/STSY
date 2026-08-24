"""power.py 검증.

핵심은 '교과서에 실린 기준값과 맞는가'다.
이 계산이 틀리면 단계 1의 합격선과 필요 개체 수가 통째로 틀린다.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import power  # noqa: E402


def test_교과서_기준값_d1_n10():
    """Cohen's d = 1.0, n = 10 의 대응표본 검정력은 약 0.80.

    가장 널리 인용되는 기준점이다. 여기가 맞으면 나머지도 맞다.
    """
    assert power.power_paired(10, 1.0) == pytest.approx(0.803, abs=0.005)


def test_교과서_기준값_d05_n34():
    """중간 효과 d = 0.5 에 검정력 0.80 이면 n ≈ 34."""
    assert power.power_paired(34, 0.5) == pytest.approx(0.80, abs=0.02)
    assert power.required_n(1.0, 0.5) == 34


def test_mde가_검정력을_되돌려준다():
    """mde 가 낸 값을 power_paired 에 넣으면 정확히 0.80 이 나와야 한다."""
    for n in (5, 10, 15, 20, 30):
        assert power.power_paired(n, power.mde(n)) == pytest.approx(0.80, abs=1e-6)


def test_문서에_실린_표와_일치():
    """정리/통계_검출력.md 의 계수. 문서를 고치면 여기도 고쳐야 한다."""
    expected = {5: 1.6820, 10: 0.9960, 15: 0.7780, 20: 0.6604, 30: 0.5292}
    for n, coeff in expected.items():
        assert power.mde(n) == pytest.approx(coeff, abs=5e-4)


def test_3퍼센트_검출에_필요한_개체수():
    """연구설계.md 의 표."""
    assert power.required_n(1.0, 3.0) == 4
    assert power.required_n(2.0, 3.0) == 6
    assert power.required_n(3.0, 3.0) == 10
    assert power.required_n(5.0, 3.0) == 24


def test_SD3에_n10은_여유가_없다():
    """설계상 가장 중요한 한 줄 — 목표 3 % 에 딱 걸린다."""
    got = power.mde(10, sd_pct=3.0)
    assert got <= 3.0            # 목표를 만족은 한다
    assert got > 2.9             # 그러나 여유가 0.01 %p 뿐이다


def test_정규근사는_낙관적이다():
    """근사가 항상 정확값보다 작고, n 이 작을수록 차이가 크다."""
    ratios = []
    for n in (5, 10, 15, 20, 30):
        exact, approx = power.mde(n), power.mde_normal_approx(n)
        assert approx < exact
        ratios.append(approx / exact)
    assert ratios == sorted(ratios)          # n 이 커질수록 1에 가까워진다
    assert ratios[0] < 0.76                  # n=5 에서 25 % 넘게 과소평가


def test_n이_커지면_MDE가_작아진다():
    values = [power.mde(n) for n in range(5, 40)]
    assert all(b < a for a, b in zip(values, values[1:]))


def test_SD에_비례한다():
    """MDE 는 SD 의 선형 함수다 — % 단위 약속이 성립하는지 확인."""
    assert power.mde(10, 6.0) == pytest.approx(2 * power.mde(10, 3.0))


def test_잘못된_입력():
    with pytest.raises(ValueError):
        power.power_paired(1, 1.0)
    with pytest.raises(ValueError):
        power.required_n(50.0, 3.0, n_max=30)
