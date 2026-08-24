"""막전류에서 전극이 실제로 보는 파형을 만든다.

이 파일이 모델과 실험을 잇는 다리다. 시뮬레이션이 내놓는 것은 막전위 V(x,t)
지만, 우리 장치가 보는 것은 몸 표면 두 접점 사이의 전위차다. 둘은 다르다.

선전류원 근사(line source approximation):

    phi_e(x_e, r) = 1/(4 pi sigma) * sum_j  i_m,j * A_j / sqrt((x_j-x_e)^2 + r^2)

단위가 저절로 맞는다 — i_m*A [µA] / (sigma [S/cm] * r [cm]) = µV.
문헌의 표면 신호가 20-100 µV 급이므로 (Yoshida 2009: MGF 29.4 µV) 자릿수를
바로 대조할 수 있다.

전제 (전부 근사다):
- 세포외 매질이 무한하고 균질하며 등방적이다. 실제 지렁이는 체벽·체강액·
  각피가 층을 이룬다. 절대 진폭은 이 근사에서 믿을 수 없고, 파형의 모양과
  채널 간 시간차는 비교적 잘 살아남는다 (우리 판단).
- 축삭이 직선이다.
"""

from __future__ import annotations

import numpy as np

# 세포외 매질 전도도 [S/cm]. 생리식염수가 약 0.0125, 조직이 0.002-0.006 급.
# 지렁이 체벽의 실측값은 확보하지 못했다 — 훑어야 하는 파라미터다.
SIGMA_DEFAULT = 0.01


def monopolar(run, x_e_cm, depth_cm: float = 0.05,
              sigma: float = SIGMA_DEFAULT) -> np.ndarray:
    """전극 한 점이 보는 전위 [µV]. (n_t,) 또는 (n_t, n_e).

    depth_cm 은 축삭에서 전극까지의 수직 거리다. 지렁이 배쪽 표면 기록이면
    체벽 두께에 해당한다. 이 값이 진폭을 크게 좌우한다.
    """
    x_e = np.atleast_1d(np.asarray(x_e_cm, dtype=float))
    # r[j, e] = 구획 j 에서 전극 e 까지의 거리
    r = np.hypot(run.x_cm[:, None] - x_e[None, :], depth_cm)
    w = run.area_cm2 / (4.0 * np.pi * sigma * r)     # (n_x, n_e)
    out = run.i_m @ w                                 # (n_t, n_e)
    return out[:, 0] if np.ndim(x_e_cm) == 0 else out


def bipolar(run, x1_cm: float, x2_cm: float, depth_cm: float = 0.05,
            sigma: float = SIGMA_DEFAULT) -> np.ndarray:
    """접점 두 개의 차동 기록 [µV]. 우리 장치가 실제로 잡는 신호다.

    차동을 쓰는 이유는 멀리서 오는 성분이 두 접점에 비슷하게 들어와
    상쇄되기 때문이다 (연구설계.md 「근육 전위를 분리하는 5중 방어」 5번).
    """
    p = monopolar(run, [x1_cm, x2_cm], depth_cm, sigma)
    return p[:, 0] - p[:, 1]


def channel_pair(run, span_mm: float = 25.0, contact_gap_mm: float = 12.5,
                 x_start_cm: float = 1.0, depth_cm: float = 0.05,
                 sigma: float = SIGMA_DEFAULT):
    """STSY 전극 배치를 그대로 흉내낸 두 채널.

    접점 5개 · 12.5 mm 간격 · 인접 이극 채널을 합성해 25 mm 간격을 만드는
    구성이다 (결정기록.md 「전극 구성」). 여기서는 그 합성 결과에 해당하는
    두 이극 채널만 만든다 — 중심 간 거리가 span_mm 이 된다.

    돌려주는 것: (t_ms, ch_a, ch_b, 실제_중심간_거리_mm)
    실제 거리를 같이 돌려주는 이유는, 전도속도를 되계산할 때 쓰는 d 가
    이 값이어야 하기 때문이다. 실험에서 d 를 1 mm 잘못 재면 4 % 오차다.
    """
    gap = contact_gap_mm * 0.1          # mm -> cm
    a1 = x_start_cm
    a2 = a1 + gap
    b1 = a1 + span_mm * 0.1
    b2 = b1 + gap
    ch_a = bipolar(run, a1, a2, depth_cm, sigma)
    ch_b = bipolar(run, b1, b2, depth_cm, sigma)
    d_mm = (b1 + b2) / 2.0 * 10.0 - (a1 + a2) / 2.0 * 10.0
    return run.t_ms, ch_a, ch_b, d_mm


def resample(t_ms: np.ndarray, y: np.ndarray, fs_hz: float):
    """시뮬레이션 시간격자를 실제 샘플레이트로 다시 찍는다.

    시뮬레이션 dt 는 안정성 때문에 1 µs 급인데, 우리 장치는 192 kHz(5.2 µs)다.
    분석 코드에 넣기 전에 실제 샘플레이트로 내려야 조건이 같아진다.
    """
    t_new = np.arange(t_ms[0], t_ms[-1], 1000.0 / fs_hz)
    return t_new, np.interp(t_new, t_ms, y)


def add_noise(y: np.ndarray, rms_uv: float, seed: int | None = None):
    """전극에서 더해지는 잡음. 축삭 안이 아니라 기록 단에서 섞인다.

    Yoshida 2009 Fig. 8 실측 잡음이 19.3 µV 다 (원문 확인).
    잡음을 여기서 더하는 것이 물리적으로도 맞고 계산도 싸다 —
    시행마다 축삭을 다시 풀 필요가 없다.
    """
    rng = np.random.default_rng(seed)
    return y + rms_uv * rng.standard_normal(y.shape)
