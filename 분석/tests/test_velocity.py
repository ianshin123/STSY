"""velocity.py 검증.

핵심 질문 하나 — 3 % 변화(Δt 약 25 µs)를 실제로 구별하는가.
알려진 지연을 넣은 합성 파형으로 확인한다.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import velocity as V  # noqa: E402

FS = 192_000.0          # UMC404HD 최대 샘플레이트
D_MM = 25.0             # 기록 지점 간 거리


def biphasic(t, t0, width=1.5e-4):
    """이상성 파형 흉내 — 가우시안의 1차 미분."""
    u = (t - t0) / width
    return -u * np.exp(-0.5 * u * u)


def pair(dt_s, noise=0.0, seed=0, fs=FS, dur=0.006):
    """dt_s 만큼 벌어진 두 채널을 만든다."""
    t = np.arange(0, dur, 1 / fs)
    rng = np.random.default_rng(seed)
    a = biphasic(t, 0.002)
    b = biphasic(t, 0.002 + dt_s)
    if noise:
        a = a + noise * rng.standard_normal(t.size)
        b = b + noise * rng.standard_normal(t.size)
    return a, b


def test_잡음_없으면_거의_정확하다():
    dt_true = 833.33e-6
    a, b = pair(dt_true)
    est = V.estimate_dt(a, b, FS)
    assert est.dt_s == pytest.approx(dt_true, abs=2e-6)


def test_포물선_보간이_샘플간격보다_잘_본다():
    """샘플 간격 5.21 µs 의 절반이 안 되는 오차로 들어와야 한다."""
    dt_true = 833.33e-6                       # 정수 샘플에 안 떨어지는 값
    a, b = pair(dt_true)
    naive = V.estimate_dt(a, b, FS)
    assert abs(naive.subsample_shift) > 0     # 보간이 실제로 작동했다
    assert abs(naive.dt_s - dt_true) < (1 / FS) / 2


def test_음의_지연도_잡는다():
    a, b = pair(-400e-6)
    assert V.estimate_dt(a, b, FS).dt_s == pytest.approx(-400e-6, abs=2e-6)


def test_채널간_고정지연_보정():
    """캘리브레이션으로 잰 지연을 빼면 참값이 나와야 한다."""
    dt_true, skew = 833.33e-6, 40e-6
    a, b = pair(dt_true + skew)
    est = V.estimate_dt(a, b, FS, lag_offset_s=skew)
    assert est.dt_s == pytest.approx(dt_true, abs=2e-6)
    assert est.dt_raw_s == pytest.approx(dt_true + skew, abs=2e-6)


def averaged_estimate(dt_s, n_trials=50, noise=0.30, seed=0):
    """실제 프로토콜대로 — 시간 잠금 평균화 후 Δt 추정."""
    rng = np.random.default_rng(seed)
    acc_a = acc_b = 0.0
    for _ in range(n_trials):
        a, b = pair(dt_s, noise=noise, seed=int(rng.integers(1 << 31)))
        acc_a = acc_a + a
        acc_b = acc_b + b
    a, b = acc_a / n_trials, acc_b / n_trials
    return V.estimate_dt(V.bandpass(a, FS), V.bandpass(b, FS), FS).dt_s


def test_3퍼센트_변화를_구별한다():
    """설계 전체가 걸린 시험 — 30 m/s 와 29.1 m/s 를 갈라야 한다.

    50회 평균화(연구설계.md 근전위 5중 방어 3번)를 거친 뒤의 성능이다.
    """
    dts = [(D_MM * 1e-3) / v for v in (30.0, 30.0 * 0.97)]
    got = [averaged_estimate(dt, seed=i) for i, dt in enumerate(dts)]

    # 참 간격은 약 25.8 µs. 그 1/10 안으로 들어와야 한다.
    assert (got[1] - got[0]) == pytest.approx(dts[1] - dts[0], abs=2.6e-6)
    for est_dt, true_dt in zip(got, dts):
        assert abs(est_dt - true_dt) < 2e-6

    # 속도로 되돌렸을 때 두 조건이 실제로 갈라지는지
    v0, v1 = V.velocity(D_MM, got[0]), V.velocity(D_MM, got[1])
    assert (v0 - v1) / v0 == pytest.approx(0.03, abs=0.003)


def test_평균화가_필요한_이유():
    """단발 추정의 오차는 목표(25 µs) 대비 무시할 수 없다.

    평균화를 하면 그 오차가 확실히 줄어든다는 것을 수치로 남긴다.
    이 값이 나빠지면 단계 1의 SD_rep 목표가 위태로워진다.
    """
    dt_true = (D_MM * 1e-3) / 30.0

    single = []
    for seed in range(20):
        a, b = pair(dt_true, noise=0.30, seed=seed)
        single.append(V.estimate_dt(V.bandpass(a, FS), V.bandpass(b, FS), FS).dt_s)
    single_rms = float(np.sqrt(np.mean((np.array(single) - dt_true) ** 2)))

    avg = [averaged_estimate(dt_true, seed=100 + s) for s in range(5)]
    avg_rms = float(np.sqrt(np.mean((np.array(avg) - dt_true) ** 2)))

    assert single_rms < 25e-6        # 단발도 목표 효과보다는 작다
    assert avg_rms < single_rms / 3  # 평균화가 확실히 이긴다


def test_대역통과가_저주파_표류를_지운다():
    dt_true = 833.33e-6
    a, b = pair(dt_true)
    t = np.arange(a.size) / FS
    drift = 5.0 * np.sin(2 * np.pi * 3.0 * t)      # 3 Hz, 스파이크의 5배 크기
    est = V.estimate_dt(V.bandpass(a + drift, FS), V.bandpass(b + drift, FS), FS)
    assert est.dt_s == pytest.approx(dt_true, abs=3e-6)


def test_속도_계산():
    assert V.velocity(25.0, 833.33e-6) == pytest.approx(30.0, abs=0.01)
    with pytest.raises(ValueError):
        V.velocity(25.0, 0.0)


def test_섬유_판별():
    assert V.classify(22.0) == "MGF"
    assert V.classify(7.5) == "LGF"
    assert V.classify(1.0) == "범위 밖"        # 근전위 등
    assert V.classify(60.0) == "범위 밖"


def test_거리_오차가_지배한다():
    """d 1 mm 오차만으로 4 % — 목표 효과 3 % 보다 크다."""
    dt = 833.33e-6
    only_d = V.velocity_uncertainty(25.0, dt, sigma_d_mm=1.0, sigma_dt_s=0.0)
    only_t = V.velocity_uncertainty(25.0, dt, sigma_d_mm=0.0, sigma_dt_s=5.2e-6)
    assert only_d == pytest.approx(0.04, abs=1e-3)
    assert only_d > 6 * only_t                 # 거리 쪽이 압도적이다


def test_잘못된_입력():
    with pytest.raises(ValueError):
        V.estimate_dt([1, 2, 3], [1, 2], FS)
    with pytest.raises(ValueError):
        V.estimate_dt(np.ones(100), np.ones(100), FS)     # 상수 신호
    with pytest.raises(ValueError):
        V.bandpass(np.zeros(1000), 1000.0, low=300, high=3000)   # fs 부족
