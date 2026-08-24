"""축삭 케이블 — 막 조각을 이어 붙여 활동전위를 달리게 한다.

    c_m dV_i/dt = -I_ion(V_i) + g_ax (V_{i-1} - 2V_i + V_{i+1}) + I_stim

    g_ax = 1000 * d / (4 * R_a * dx^2)      [mS/cm^2]

d [cm] · R_a [ohm*cm] · dx [cm]. 1000 은 S/cm^2 -> mS/cm^2 환산이다.
단위 약속은 hh.py 머리말과 같다.

양 끝은 밀봉단(sealed end) — 축삭 밖으로 전류가 새지 않는다고 본다.

풀이는 명시적 오일러다. 이유는 두 가지다.
- 한 줄이라 무슨 일이 일어나는지 눈으로 보인다
- 안정 조건이 명시적이라, 왜 dt 를 줄여야 하는지가 수식으로 드러난다
대가는 dt 가 작아야 한다는 것이고, 그 한계는 max_stable_dt() 가 계산해 준다.
왜 음해법(implicit)을 쓰지 않았는지는 결정기록.md 참조.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

import hh

# 축삭 세로저항. 오징어 거대축삭 35.4, 일반 무척추동물 100 ohm*cm 급이 쓰인다.
# 지렁이 MGF 실측값은 확보하지 못했다 — 훑어야 하는 파라미터다.
R_A_DEFAULT = 100.0


@dataclass(frozen=True)
class Axon:
    """균일한 원통 축삭 하나."""

    diameter_um: float = 70.0       # MGF 약 0.07 mm (정리/지렁이_해부와생리.md)
    length_mm: float = 60.0
    dx_um: float = 100.0            # 구획 길이
    r_a: float = R_A_DEFAULT        # ohm*cm
    membrane: hh.Membrane = hh.Membrane()

    @property
    def n_comp(self) -> int:
        return int(round(self.length_mm * 1000.0 / self.dx_um))

    @property
    def x_cm(self) -> np.ndarray:
        """각 구획 중심의 위치 [cm]."""
        return (np.arange(self.n_comp) + 0.5) * self.dx_um * 1e-4

    @property
    def g_ax(self) -> float:
        """이웃 구획과의 결합 전도도 [mS/cm^2]."""
        d_cm = self.diameter_um * 1e-4
        dx_cm = self.dx_um * 1e-4
        return 1000.0 * d_cm / (4.0 * self.r_a * dx_cm ** 2)

    @property
    def area_cm2(self) -> float:
        """구획 하나의 막 면적 [cm^2]. 세포외 전위 계산에 쓴다."""
        return np.pi * (self.diameter_um * 1e-4) * (self.dx_um * 1e-4)

    def max_stable_dt(self, safety: float = 0.4) -> float:
        """명시적 오일러가 발산하지 않는 dt 상한 [ms].

        가장 빠른 시간상수는 축방향 결합에서 온다. 이산 라플라시안의
        고유값이 [-4, 0] 이므로 결합항의 감쇠율이 최대 4*g_ax/c_m 이고,
        여기에 이온 전도도 최대치가 더해진다.

            dt < 2 / (4*g_ax/c_m + g_ion_max/c_m)

        safety 는 그 상한에 곱하는 여유다. 이 함수가 주는 값보다 큰 dt 를
        쓰면 화면 가득 nan 이 뜨는데, 처음 보면 원인을 찾기 어렵다.

        g_ax 가 1/dx^2 이므로 dx 를 키우면 한계가 크게 완화된다. 다만 이온
        전도도 항은 dx 에 무관해서, dx 를 2배 해도 한계는 4배가 아니라
        2.5배쯤 늘어난다.
        """
        m = self.membrane
        g_ion = m.na_scale * m.g_na + m.g_k + m.leak_scale * m.g_l
        return safety * 2.0 / ((4.0 * self.g_ax + g_ion) / m.c_m)


@dataclass(frozen=True)
class Run:
    """시뮬레이션 한 번의 결과."""

    t_ms: np.ndarray        # (n_t,)
    x_cm: np.ndarray        # (n_x,)
    v: np.ndarray           # (n_t, n_x) 막전위 [mV]
    i_m: np.ndarray         # (n_t, n_x) 막전류 밀도 [µA/cm^2], 바깥쪽이 양수
    area_cm2: float

    def peak_times_ms(self, threshold_mv: float = -20.0) -> np.ndarray:
        """구획마다 활동전위 정점 시각. 역치를 못 넘으면 nan.

        전도가 도중에 실패하면 그 지점부터 nan 이 되므로,
        nan 이 나타나는 위치가 곧 전도 차단 지점이다.
        """
        out = np.full(self.v.shape[1], np.nan)
        fired = self.v.max(axis=0) > threshold_mv
        idx = self.v[:, fired].argmax(axis=0)
        out[fired] = self.t_ms[idx]
        return out

    def conduction_velocity(self, x0_cm: float, x1_cm: float) -> float:
        """두 지점의 정점 시각차로 구한 참값 전도속도 [m/s].

        이것이 '정답'이다. 세포외 파형에서 추정한 값과 대조하는 대상이다.
        """
        pk = self.peak_times_ms()
        i0 = int(np.argmin(np.abs(self.x_cm - x0_cm)))
        i1 = int(np.argmin(np.abs(self.x_cm - x1_cm)))
        if not np.isfinite(pk[i0]) or not np.isfinite(pk[i1]):
            return float("nan")          # 스파이크가 거기까지 못 갔다
        dt_ms = pk[i1] - pk[i0]
        if dt_ms == 0.0:
            return float("nan")
        dist_cm = self.x_cm[i1] - self.x_cm[i0]
        return float(dist_cm * 1e-2 / (dt_ms * 1e-3))

    def propagated(self, threshold_mv: float = -20.0) -> bool:
        """끝까지 갔는가. 발화 확률 계산의 판정 기준이다."""
        return bool(self.v[:, -1].max() > threshold_mv)


def simulate(axon: Axon, temp_c: float = 20.0, dt_ms: float | None = None,
             t_end_ms: float = 6.0, stim_ua_cm2: float = 60.0,
             stim_start_ms: float = 0.2, stim_dur_ms: float = 0.2,
             stim_comps: int = 5, record_every: int = 1,
             noise_ua_cm2: float = 0.0, seed: int | None = None) -> Run:
    """축삭 하나를 풀고 (t, x) 격자의 V 와 막전류를 돌려준다.

    stim_* : 왼쪽 끝 stim_comps 개 구획에 주입하는 전류 펄스.
             실험의 '머리를 톡 건드리기'에 해당한다.
    noise_ua_cm2 : 막 전류에 섞는 백색잡음. 발화 확률 계산에 쓴다.
                   0 이면 완전히 결정론적이다.
    """
    m = axon.membrane
    n = axon.n_comp
    dt_max = axon.max_stable_dt()
    if dt_ms is None:
        dt_ms = dt_max
    if dt_ms > dt_max:
        raise ValueError(
            f"dt={dt_ms:.5f} ms 는 안정 한계 {dt_max:.5f} ms 를 넘는다. "
            f"dt 를 줄이거나 dx 를 키워라 (g_ax 가 1/dx^2 이라 dx 를 키우면 완화된다. "
            f"단 이온 전도도 항은 dx 에 무관하므로 정확히 dx^2 배가 되지는 않는다)"
        )

    n_steps = int(round(t_end_ms / dt_ms))
    v_rest = hh.resting_potential(m)
    v = np.full(n, v_rest)
    gm, gh, gn = (np.full(n, float(s)) for s in hh.steady_state(v_rest, m.shift_mv))

    ph = hh.phi(temp_c)
    g_ax = axon.g_ax
    rng = np.random.default_rng(seed)

    stim = np.zeros(n)
    stim[:stim_comps] = stim_ua_cm2
    lap = np.empty(n)

    n_rec = n_steps // record_every + 1
    v_out = np.empty((n_rec, n))
    im_out = np.empty((n_rec, n))
    t_out = np.empty(n_rec)
    k = 0

    for step in range(n_steps + 1):
        a_m, b_m, a_h, b_h, a_n, b_n = hh.rates(v, m.shift_mv)
        i_na = m.na_scale * m.g_na * gm ** 3 * gh * (v - m.e_na)
        i_k = m.g_k * gn ** 4 * (v - m.e_k)
        i_l = m.leak_scale * m.g_l * (v - m.e_l)
        i_ion = i_na + i_k + i_l

        # 이산 라플라시안. 양 끝은 밀봉단이라 이웃이 하나뿐이다.
        lap[1:-1] = v[:-2] - 2.0 * v[1:-1] + v[2:]
        lap[0] = v[1] - v[0]
        lap[-1] = v[-2] - v[-1]
        i_ax = g_ax * lap

        t = step * dt_ms
        on = stim_start_ms <= t < stim_start_ms + stim_dur_ms
        i_stim = stim if on else 0.0
        if noise_ua_cm2:
            # 잡음은 dt 에 무관한 세기를 갖도록 sqrt(dt) 로 규격화한다.
            i_stim = i_stim + noise_ua_cm2 * rng.standard_normal(n) / np.sqrt(dt_ms)

        if step % record_every == 0:
            t_out[k] = t
            v_out[k] = v
            # KCL: 막 바깥으로 나가는 전류 = 축방향으로 들어온 전류 + 주입 전류
            im_out[k] = i_ax + i_stim
            k += 1

        dv = (-i_ion + i_ax + i_stim) / m.c_m
        v = v + dt_ms * dv
        gm = gm + dt_ms * ph * (a_m * (1.0 - gm) - b_m * gm)
        gh = gh + dt_ms * ph * (a_h * (1.0 - gh) - b_h * gh)
        gn = gn + dt_ms * ph * (a_n * (1.0 - gn) - b_n * gn)

        if not np.isfinite(v).all():
            raise FloatingPointError(
                f"{t:.3f} ms 에서 발산했다. dt={dt_ms:.5f} ms, 한계 {dt_max:.5f} ms. "
                f"dt 를 절반으로 줄여 보라"
            )

    return Run(t_out[:k], axon.x_cm, v_out[:k], im_out[:k], axon.area_cm2)
