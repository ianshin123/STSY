"""recording.py 검증 — 모델과 실험을 잇는 다리가 성립하는가.

가장 중요한 시험은 test_분석코드가_참값을_되찾는다 이다.
저장소의 분석/src/velocity.py 는 지금까지 가우시안 미분으로 만든 가짜 파형으로만
검증돼 있었다. 이제 케이블 방정식이 만든 파형으로 검증한다.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(ROOT / "분석" / "src"))

import axon as A  # noqa: E402
import recording as R  # noqa: E402
import velocity as V  # noqa: E402

FS = 192_000.0
STIM = dict(stim_ua_cm2=300.0, stim_dur_ms=0.5, stim_comps=20)


def spike_run(**kw):
    ax = A.Axon(dx_um=100.0, length_mm=60.0, **kw)
    return A.simulate(ax, 20.0, t_end_ms=20.0, record_every=2, **STIM)


def test_진폭이_문헌_자릿수에_들어온다():
    """Yoshida 2009 Fig. 8 실측 MGF 29.4 µV · 잡음 19.3 µV (원문 확인).

    무한 균질 매질 근사라 절대값은 못 믿는다. 자릿수만 본다 —
    10 µV 대도 1 mV 대도 아니어야 한다.
    """
    r = spike_run()
    y = R.bipolar(r, 2.0, 3.25)
    pp = float(y.max() - y.min())
    assert 10.0 < pp < 500.0


def test_이극_기록이_먼_신호를_지운다():
    """차동 기록의 존재 이유. 멀수록 두 접점 차가 작아진다."""
    r = spike_run()
    near = float(np.ptp(R.bipolar(r, 2.0, 3.25, depth_cm=0.05)))
    far = float(np.ptp(R.bipolar(r, 2.0, 3.25, depth_cm=0.60)))
    assert far < near / 5.0


def test_뒤쪽_채널이_늦게_뜬다():
    r = spike_run()
    t, a, b, d = R.channel_pair(r, span_mm=25.0, x_start_cm=1.5)
    assert d == pytest.approx(25.0)
    assert t[int(b.argmin())] > t[int(a.argmin())]


def test_분석코드가_참값을_되찾는다():
    """★ 전 구간 시험 — 이온 통로부터 추정 속도까지.

    시뮬레이션이 아는 참값과, 세포외 파형을 192 kHz 로 다시 찍어
    분석/src/velocity.py 에 넣어 얻은 값이 일치해야 한다.
    """
    r = spike_run()
    truth = r.conduction_velocity(2.125, 4.625)
    t, a, b, d = R.channel_pair(r, span_mm=25.0, x_start_cm=1.5)
    _, aa = R.resample(t, a, FS)
    _, bb = R.resample(t, b, FS)
    est = V.estimate_dt(V.bandpass(aa, FS), V.bandpass(bb, FS), FS)
    got = V.velocity(d, est.dt_s)
    assert got == pytest.approx(truth, rel=0.01)
    assert est.peak_correlation > 0.95


def test_문헌_잡음에서도_되찾는다():
    """Yoshida 실측 잡음 19.3 µV 를 단발로 얹어도 1 % 안에 들어오는가."""
    r = spike_run()
    truth = r.conduction_velocity(2.125, 4.625)
    t, a, b, d = R.channel_pair(r, span_mm=25.0, x_start_cm=1.5)
    _, aa = R.resample(t, a, FS)
    _, bb = R.resample(t, b, FS)
    errs = []
    for seed in range(5):
        na = R.add_noise(aa, 19.3, seed)
        nb = R.add_noise(bb, 19.3, 100 + seed)
        est = V.estimate_dt(V.bandpass(na, FS), V.bandpass(nb, FS), FS)
        errs.append(abs(V.velocity(d, est.dt_s) - truth) / truth)
    assert max(errs) < 0.01


def test_거리를_틀리면_그대로_오차가_된다():
    """d 를 1 mm 잘못 재면 25 mm 기준 4 % — 목표 효과보다 크다.

    저장소가 반복해서 강조하는 사실을 코드로 고정한다.
    """
    v_true = V.velocity(25.0, 833.33e-6)
    v_wrong = V.velocity(26.0, 833.33e-6)
    assert (v_wrong - v_true) / v_true == pytest.approx(0.04, abs=1e-3)
