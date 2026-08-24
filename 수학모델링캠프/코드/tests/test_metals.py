"""metals.py 검증 — 세 금속의 구조가 실제로 다른 결과를 내는가.

이 프로젝트의 주장은 "세 금속에 서로 다른 모델 구조를 준다"는 것이다.
그 주장이 성립하려면 구조 차이가 관측 가능한 지문 차이로 나와야 한다.
안 나오면 구조를 나눈 의미가 없다.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import axon as A  # noqa: E402
import hh  # noqa: E402
import metals as M  # noqa: E402
import recording as R  # noqa: E402

STIM = dict(stim_ua_cm2=300.0, stim_dur_ms=0.5, stim_comps=20)


def measure(mem):
    """대조군과 같은 조건에서 속도와 진폭을 잰다."""
    ax = A.Axon(dx_um=100.0, length_mm=60.0, membrane=mem)
    r = A.simulate(ax, 20.0, t_end_ms=22.0, record_every=4, **STIM)
    v = r.conduction_velocity(2.125, 4.625)
    amp = float(np.ptp(R.bipolar(r, 2.0, 3.25)))
    return v, amp


def test_점유율_곡선():
    assert M.occupancy(0.0, 1.0) == pytest.approx(0.0)
    assert M.occupancy(1.0, 1.0) == pytest.approx(0.5)       # 정의상 반효과
    assert M.occupancy(1e6, 1.0) == pytest.approx(1.0, abs=1e-5)
    assert np.all(np.diff(M.occupancy(np.linspace(0, 10, 50), 2.0)) > 0)
    with pytest.raises(ValueError):
        M.occupancy(1.0, 0.0)


def test_누적손상은_농도와_시간_둘_다에_의존한다():
    assert M.cumulative_damage(2.0, 0.0, 0.25) == pytest.approx(0.0)
    # 농도 2 로 1일 = 농도 1 로 2일 (농도x시간이 같으면 같다)
    assert M.cumulative_damage(2.0, 1.0, 0.25) == pytest.approx(
        M.cumulative_damage(1.0, 2.0, 0.25))
    assert M.cumulative_damage(2.0, 7.0, 0.25) > M.cumulative_damage(2.0, 1.0, 0.25)


def test_차단형은_시간에_무관하고_손상형은_자란다():
    """★ 첫 번째 지문 — 시간 경과.

    납·카드뮴은 농도에 평형이므로 날짜가 지나도 그대로여야 한다.
    철은 손상이 쌓이므로 자라야 한다. 이것이 실험으로 두 기전을 가르는 방법이다.
    """
    base = hh.Membrane()
    for m in (M.LEAD, M.CADMIUM):
        d1 = m.membrane(base, 2.0, days=1.0)
        d7 = m.membrane(base, 2.0, days=7.0)
        assert d1 == d7
    fe1 = M.IRON.membrane(base, 2.0, days=1.0)
    fe7 = M.IRON.membrane(base, 2.0, days=7.0)
    assert fe7.leak_scale > fe1.leak_scale * 1.5


def test_철만_진폭을_같이_떨어뜨린다():
    """★ 두 번째 지문 — 속도와 진폭의 결합.

    차단형은 속도를 떨어뜨리면서 진폭은 거의 그대로 둔다.
    손상형은 막이 새므로 속도와 진폭이 같이 떨어진다.
    이 대비가 이 프로젝트가 제안하는 판별 지표의 근거다.
    """
    base = hh.Membrane()
    v0, a0 = measure(base)
    out = {m.name: measure(m.membrane(base, 2.0, days=7.0)) for m in M.ALL}

    for name in ("납", "카드뮴", "철"):
        assert out[name][0] < v0                       # 셋 다 속도는 떨어진다

    def d_amp(name):
        return (out[name][1] - a0) / a0

    assert d_amp("철") < -0.10                          # 철은 진폭이 10 % 넘게 떨어진다
    assert abs(d_amp("납")) < 0.05                      # 납은 거의 안 변한다
    assert abs(d_amp("카드뮴")) < 0.05
    assert d_amp("철") < d_amp("납") - 0.10             # 확실히 갈린다


def test_용량반응이_단조롭다():
    """차단형은 농도가 높을수록 느려져야 한다 — 뒤집히면 모델이 틀린 것이다."""
    base = hh.Membrane()
    vs = [measure(M.LEAD.membrane(base, c, days=7.0))[0] for c in (0.5, 1.0, 2.0, 4.0)]
    assert np.all(np.diff(vs) < 0)


def test_철의_U자곡선():
    """필수 원소라 결핍 쪽에도 손상이 있다. 납·카드뮴에는 없는 성질이다."""
    c = np.linspace(0.01, 20.0, 400)
    u = M.iron_u_curve(c)
    i = int(np.argmin(u))
    assert 0 < i < len(c) - 1                          # 최적점이 안쪽에 있다 = U자
    assert u[0] > u[i] and u[-1] > u[i]
    # 오른쪽 가지만 쓰면 단조 증가 = 납·카드뮴과 같은 모양
    only_tox = M.iron_u_curve(c, include_deficiency=False)
    assert np.all(np.diff(only_tox) > 0)


def test_금속이_없으면_대조군과_같다():
    base = hh.Membrane()
    for m in M.ALL:
        assert m.membrane(base, 0.0, days=7.0) == base
