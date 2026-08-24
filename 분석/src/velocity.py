"""두 채널의 시간차(Δt)로 전도속도를 구한다.

    v [m/s] = d [mm] / Δt [ms]

Δt 추정은 상호상관 + 포물선 보간. 원리와 대안은
정리/신호처리_전도속도추정.md 참조.

목표 정밀도가 Δt 25 µs 라서 두 가지가 중요하다.
- 샘플 간격보다 미세한 분해능이 필요하다  -> 포물선 보간
- 채널 간 고정 지연을 빼야 한다           -> lag_offset_s
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import signal

# 거대섬유 판별에 쓰는 속도 범위 (m/s).
# 출처: 정리/지렁이_해부와생리.md — 전부 원문 미확보 상태의 2차 인용.
MGF_RANGE = (15.0, 30.0)
LGF_RANGE = (7.0, 8.0)


@dataclass(frozen=True)
class Estimate:
    """Δt 추정 결과. 진단에 필요한 것을 같이 들고 다닌다."""

    dt_s: float           # 채널 간 고정 지연을 보정한 Δt
    dt_raw_s: float       # 보정 전
    peak_correlation: float   # 정규화 상호상관 최대값 (-1..1)
    subsample_shift: float    # 포물선 보간이 옮긴 양 (샘플)

    @property
    def dt_us(self) -> float:
        return self.dt_s * 1e6


def bandpass(x, fs, low=300.0, high=3000.0, order=4):
    """영위상 대역통과.

    filtfilt 를 쓰는 이유: 인과 필터는 채널마다 지연을 넣는데,
    우리가 재는 것이 바로 채널 간 지연이다.
    """
    nyq = fs / 2
    if not 0 < low < high < nyq:
        raise ValueError(f"통과대역 {low}-{high} Hz 가 fs={fs} Hz 와 맞지 않는다")
    sos = signal.butter(order, [low / nyq, high / nyq], btype="band", output="sos")
    return signal.sosfiltfilt(sos, np.asarray(x, dtype=float))


def _parabolic_vertex(y_prev: float, y_peak: float, y_next: float) -> float:
    """최대점 주변 3점에 포물선을 맞춰 꼭짓점의 샘플 단위 오프셋을 낸다."""
    denom = y_prev - 2.0 * y_peak + y_next
    if denom == 0.0:
        return 0.0
    shift = 0.5 * (y_prev - y_next) / denom
    # 3점 보간의 꼭짓점은 ±0.5 샘플 안에 있어야 정상이다.
    return float(np.clip(shift, -0.5, 0.5))


def estimate_dt(ch_a, ch_b, fs: float, lag_offset_s: float = 0.0) -> Estimate:
    """ch_a 대비 ch_b 의 지연을 상호상관으로 구한다.

    ch_b 가 ch_a 보다 나중이면 dt_s 가 양수다.
    lag_offset_s 는 캘리브레이션으로 잰 채널 간 고정 지연 (장치/캘리브레이션/).
    """
    a = np.asarray(ch_a, dtype=float)
    b = np.asarray(ch_b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("두 채널의 길이가 다르다")
    if a.size < 3:
        raise ValueError("표본이 너무 짧다")

    a = a - a.mean()
    b = b - b.mean()
    norm = np.sqrt((a * a).sum() * (b * b).sum())
    if norm == 0.0:
        raise ValueError("채널이 상수다 — 상호상관을 낼 수 없다")

    corr = signal.correlate(b, a, mode="full") / norm
    lags = signal.correlation_lags(b.size, a.size, mode="full")
    k = int(np.argmax(corr))

    shift = 0.0
    if 0 < k < corr.size - 1:
        shift = _parabolic_vertex(corr[k - 1], corr[k], corr[k + 1])

    dt_raw = (lags[k] + shift) / fs
    return Estimate(
        dt_s=dt_raw - lag_offset_s,
        dt_raw_s=dt_raw,
        peak_correlation=float(corr[k]),
        subsample_shift=shift,
    )


def velocity(distance_mm: float, dt_s: float) -> float:
    """전도속도 (m/s). distance_mm 은 두 기록 지점(전극 쌍의 중심) 사이 거리."""
    if dt_s == 0.0:
        raise ValueError("Δt 가 0이다")
    return (distance_mm * 1e-3) / dt_s


def classify(v: float) -> str:
    """속도로 섬유를 판별한다. 근전위는 어느 범위에도 안 들어온다."""
    if MGF_RANGE[0] <= v <= MGF_RANGE[1]:
        return "MGF"
    if LGF_RANGE[0] <= v <= LGF_RANGE[1]:
        return "LGF"
    return "범위 밖"


def velocity_uncertainty(distance_mm: float, dt_s: float,
                         sigma_d_mm: float, sigma_dt_s: float) -> float:
    """v 의 상대 불확도. d 와 Δt 의 상대오차가 제곱합으로 더해진다.

    d = 25 mm 에서 sigma_d = 1 mm 면 그것만으로 4 % — 목표 효과 3 % 보다 크다.
    전극 간격 실측이 전자회로 정밀도보다 훨씬 중요하다는 뜻이다.
    """
    return float(np.hypot(sigma_d_mm / distance_mm, sigma_dt_s / dt_s))


if __name__ == "__main__":
    # 25 mm 간격, MGF 30 m/s 의 3 % 저하를 192 kHz 로 분해할 수 있는지.
    fs, d_mm = 192_000.0, 25.0
    for v_true in (30.0, 30.0 * 0.97):
        dt_true = (d_mm * 1e-3) / v_true
        t = np.arange(0, 0.006, 1 / fs)
        # 이상성 파형 흉내: 가우시안의 1차 미분
        def spike(t0, w=1.5e-4):
            u = (t - t0) / w
            return -u * np.exp(-0.5 * u * u)
        rng = np.random.default_rng(0)
        a = spike(0.002) + 0.30 * rng.standard_normal(t.size)
        b = spike(0.002 + dt_true) + 0.30 * rng.standard_normal(t.size)
        est = estimate_dt(bandpass(a, fs), bandpass(b, fs), fs)
        v = velocity(d_mm, est.dt_s)
        print(f"참값 {v_true:6.3f} m/s (Δt {dt_true*1e6:7.2f} µs)  ->  "
              f"추정 {v:6.3f} m/s (Δt {est.dt_us:7.2f} µs)  {classify(v)}")
