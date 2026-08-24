"""axon.py 검증 — 케이블 방정식이 물리적으로 옳게 행동하는가.

수치해가 수렴했는지를 먼저 확인하지 않으면, 나중에 나오는 모든 결론이
'물리'인지 '이산화 오차'인지 구별할 수 없다.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import axon as A  # noqa: E402
import hh  # noqa: E402

STIM = dict(stim_ua_cm2=300.0, stim_dur_ms=0.5, stim_comps=20)


def fire(ax, temp_c=20.0, t_end_ms=12.0, **kw):
    return A.simulate(ax, temp_c, t_end_ms=t_end_ms, record_every=4, **{**STIM, **kw})


def test_스파이크가_전파한다():
    r = fire(A.Axon(length_mm=40.0))
    assert r.propagated()
    assert 30.0 < float(r.v.max()) < 55.0          # HH 정점은 +40 mV 근처
    pk = r.peak_times_ms()
    good = np.isfinite(pk)
    # 정점 시각이 위치에 따라 뒤로 가지 않는다 = 한 방향으로 달린다.
    # record_every 때문에 이웃 구획이 같은 표본에 걸려 0 이 나올 수 있으므로
    # 뒤로 가는 것만 금지하고, 전체 추세는 따로 본다.
    assert np.all(np.diff(pk[good]) >= 0)
    assert np.all(np.diff(pk[good][::20]) > 0)


def test_dx를_줄여도_속도가_안_바뀐다():
    """공간 수렴 검사. dx=100 um 를 표준으로 쓰는 근거다."""
    vs = [fire(A.Axon(dx_um=dx, length_mm=40.0)).conduction_velocity(1.0, 3.0)
          for dx in (200.0, 100.0, 50.0)]
    assert abs(vs[1] - vs[2]) / vs[2] < 0.01       # 100 과 50 의 차이가 1 % 미만


def test_속도가_지름의_제곱근에_비례한다():
    """무수축삭 케이블 이론의 기본 결과. 코드가 맞는지 보는 가장 강한 시험이다."""
    v1 = fire(A.Axon(diameter_um=70.0, length_mm=40.0)).conduction_velocity(1.0, 3.0)
    v4 = fire(A.Axon(diameter_um=280.0, length_mm=40.0)).conduction_velocity(1.0, 3.0)
    assert v4 / v1 == pytest.approx(2.0, rel=0.05)  # 지름 4배 -> 속도 2배


def test_무수축삭은_MGF_속도에_못_닿는다():
    """★ 이 프로젝트의 첫 번째 결론을 고정하는 시험이다.

    지렁이 MGF 는 지름 70 um 에 15-45 m/s 다
    (정리/지렁이_해부와생리.md · Yoshida 2009 §1 인용 범위).
    가장 유리한 조건(오징어 축삭의 낮은 세로저항)을 줘도 무수 모델은
    그 하한의 절반에 그친다. 그래서 수초가 선택이 아니다.
    """
    v = fire(A.Axon(diameter_um=70.0, r_a=35.4, length_mm=40.0)).conduction_velocity(1.0, 3.0)
    assert v < 15.0 * 0.75                          # MGF 하한에 한참 못 미친다


def test_온도가_속도를_올린다():
    vs = [fire(A.Axon(length_mm=40.0), temp_c=T, t_end_ms=20.0).conduction_velocity(1.0, 3.0)
          for T in (10.0, 25.0)]
    assert vs[1] > vs[0]
    # 게이팅 Q10=3 이 속도 Q10 으로는 훨씬 작아진다 — 속도가 속도상수의
    # 제곱근 쪽으로 붙기 때문이다. 정리/온도와_Q10.md 의 근거.
    q10 = (vs[1] / vs[0]) ** (10.0 / 15.0)
    assert 1.2 < q10 < 1.6


def test_불안정한_dt는_거부한다():
    """명시적 오일러의 안정 한계. 넘으면 nan 대신 설명이 나와야 한다."""
    ax = A.Axon(length_mm=10.0)
    with pytest.raises(ValueError, match="안정 한계"):
        A.simulate(ax, 20.0, dt_ms=ax.max_stable_dt() * 3.0, t_end_ms=1.0)


def test_dx를_키우면_dt_한계가_완화된다():
    """느리면 dx 를 키우라는 조언의 근거.

    결합항만 보면 dt 한계가 dx^2 로 늘어야 하지만, 이온 전도도 항이
    dx 에 무관하게 남아 있어 실제 이득은 그보다 작다. dx 2배에 약 2.6배다.
    """
    a1 = A.Axon(dx_um=100.0)
    a2 = A.Axon(dx_um=200.0)
    ratio = a2.max_stable_dt() / a1.max_stable_dt()
    assert 2.0 < ratio < 4.0


def test_강한_차단은_전도를_막는다():
    """발화 확률 계산이 성립하려면 전파/실패 전이가 실제로 있어야 한다."""
    base = hh.Membrane()
    assert fire(A.Axon(length_mm=40.0, membrane=base.with_metal(na_scale=0.6)),
                t_end_ms=25.0).propagated()
    assert not fire(A.Axon(length_mm=40.0, membrane=base.with_metal(na_scale=0.3)),
                    t_end_ms=25.0).propagated()


def test_전파_실패시_속도가_nan이다():
    r = fire(A.Axon(length_mm=40.0, membrane=hh.Membrane().with_metal(na_scale=0.3)),
             t_end_ms=25.0)
    assert np.isnan(r.conduction_velocity(1.0, 3.0))
