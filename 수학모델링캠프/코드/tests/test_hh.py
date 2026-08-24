"""hh.py 검증 — 교과서 값과 대조한다.

이 파일이 존재하는 이유: 속도상수 계수에서 10배를 놓치는 실수를 실제로 했고,
증상이 '정지전위가 -65 가 아니라 -54 mV' 라는 조용한 형태로만 나타났다.
스파이크는 그대로 났기 때문에 눈으로는 알 수 없었다.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import hh  # noqa: E402


def test_정상상태가_교과서값과_같다():
    """V = -65 mV 에서 m, h, n. HH 1952 의 널리 인용되는 값이다."""
    m, h, n = (float(x) for x in hh.steady_state(-65.0))
    assert m == pytest.approx(0.0529, abs=5e-4)
    assert h == pytest.approx(0.5961, abs=5e-4)
    assert n == pytest.approx(0.3177, abs=5e-4)


def test_정지전위가_65mV_근처다():
    """이온 전류의 합이 0이 되는 곳. 계수를 틀리면 여기서 잡힌다."""
    assert hh.resting_potential(hh.Membrane()) == pytest.approx(-65.0, abs=0.1)


def test_속도상수_특이점에서_nan이_안_난다():
    """alpha_m 은 -40 mV, alpha_n 은 -55 mV 에서 분모가 0이 된다."""
    v = np.array([-40.0, -55.0, -40.0 + 1e-12, -55.0 - 1e-12])
    for r in hh.rates(v):
        assert np.isfinite(r).all()
    # 극한값이 이웃과 매끄럽게 이어지는가
    a_m = hh.rates(np.array([-40.001, -40.0, -39.999]))[0]
    assert a_m[1] == pytest.approx(0.5 * (a_m[0] + a_m[2]), rel=1e-6)


def test_온도계수():
    assert hh.phi(hh.T_REF_C) == pytest.approx(1.0)
    assert hh.phi(hh.T_REF_C + 10.0) == pytest.approx(hh.Q10_GATE)


def test_게이팅_이동이_흥분성을_낮춘다():
    """shift 가 양수면 같은 전압에서 m 이 덜 열려야 한다 — 표면전하 효과."""
    m0 = hh.steady_state(-65.0, 0.0)[0]
    m1 = hh.steady_state(-65.0, 10.0)[0]
    assert m1 < m0


def test_금속효과가_원본을_안_건드린다():
    base = hh.Membrane()
    got = base.with_metal(shift_mv=5.0, na_scale=0.8, leak_scale=2.0)
    assert base.shift_mv == 0.0 and base.na_scale == 1.0 and base.leak_scale == 1.0
    assert got.shift_mv == 5.0 and got.na_scale == 0.8 and got.leak_scale == 2.0
    # 누적된다 — 두 번 얹으면 곱해지고 더해진다
    twice = got.with_metal(shift_mv=5.0, na_scale=0.5)
    assert twice.shift_mv == 10.0 and twice.na_scale == pytest.approx(0.4)


def test_정지전위를_못_찾으면_에러():
    with pytest.raises(ValueError):
        hh.resting_potential(hh.Membrane(), lo=-70.0, hi=-68.0)
