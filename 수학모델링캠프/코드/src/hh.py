"""호지킨–헉슬리 막 모델 — 게이팅 변수와 이온 전류.

단위 약속 (표준 HH 단위계. 섞으면 조용히 틀린 답이 나온다):

    전압 V      mV
    시간 t      ms
    막용량 C    µF/cm^2
    전도도 g    mS/cm^2
    전류밀도 I  µA/cm^2

이 파일은 '한 조각의 막'만 다룬다. 조각을 이어 붙여 축삭을 만드는 것은
axon.py, 그것이 만드는 세포외 파형은 recording.py.

원 상수는 오징어 거대축삭 6.3 도 값이다 (Hodgkin & Huxley 1952 · 원문 미확보).
지렁이 MGF 값이 아니다 — 왜 그래도 쓰는지는
정리/축삭모델_선택.md 「파라미터가 없다는 문제」 참조.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

# 오징어 거대축삭 표준값 (Hodgkin & Huxley 1952 · 원문 미확보).
# 정지전위 -65 mV 를 기준으로 쓰는 현대 표기다.
V_REST = -65.0
T_REF_C = 6.3          # 원 상수가 측정된 온도
Q10_GATE = 3.0         # 게이팅 속도상수의 Q10. HH 원논문 값 · 원문 미확보


@dataclass(frozen=True)
class Membrane:
    """막 파라미터 한 벌.

    shift_mv 가 중금속이 들어오는 자리다.
    2가 양이온이 막 표면 음전하를 가리면 통로가 느끼는 전압이 실제보다
    과분극된 것처럼 되어, 활성화 곡선 전체가 탈분극 쪽으로 밀린다.
    (표면전하 효과 · Frankenhaeuser & Hodgkin 1957 · 원문 미확보)

    leak_scale 은 산화 손상이 들어오는 자리다 — 지질 과산화로 막이 새면
    누설 전도도가 올라간다. 이 연결은 문헌이 아니라 우리 가설이다
    (정리/금속별_기전.md).
    """

    c_m: float = 1.0            # µF/cm^2
    g_na: float = 120.0         # mS/cm^2
    g_k: float = 36.0
    g_l: float = 0.3
    e_na: float = 50.0          # mV
    e_k: float = -77.0
    e_l: float = -54.387
    shift_mv: float = 0.0       # 게이팅 전압 이동 (+면 흥분하기 어려워진다)
    na_scale: float = 1.0       # 통로 구멍 자체가 막히는 경우
    leak_scale: float = 1.0     # 막이 새는 경우

    def with_metal(self, shift_mv=0.0, na_scale=1.0, leak_scale=1.0) -> "Membrane":
        """중금속 효과를 얹은 새 파라미터. 원본은 건드리지 않는다."""
        return replace(
            self,
            shift_mv=self.shift_mv + shift_mv,
            na_scale=self.na_scale * na_scale,
            leak_scale=self.leak_scale * leak_scale,
        )


def phi(temp_c: float, q10: float = Q10_GATE) -> float:
    """온도 계수. 모든 속도상수 alpha, beta 에 곱한다.

    이것이 이 모델에서 온도가 들어오는 유일한 통로다.
    STSY 저장소가 들고 있는 '약 7 %/도'는 van't Hoff 어림값일 뿐
    전도속도의 실측 Q10 이 아니다 (정리/전도속도_결정요인.md).
    이 모델은 게이팅 Q10 에서 출발해 전도속도 Q10 을 계산해 낸다 —
    그 둘은 같지 않다.
    """
    return float(q10 ** ((temp_c - T_REF_C) / 10.0))


def _lin_exp(x):
    """x / (1 - exp(-x)) 를 x=0 에서도 안전하게.

    alpha_m, alpha_n 의 분모가 특정 전압에서 정확히 0이 된다.
    수학적 극한은 1 이므로 그 근처만 갈아끼운다. 이걸 빼먹으면
    막이 그 전압을 지날 때 nan 이 뜨고, 원인 찾기가 매우 어렵다.
    """
    x = np.asarray(x, dtype=float)
    small = np.abs(x) < 1e-6
    # safe 는 0으로 나누는 것을 막으려는 임시값이다. 극한 분기의 테일러 전개에는
    # 반드시 원래 x 를 써야 한다 — 여기에 safe 를 쓰면 특이점에서만 값이 1.5 로
    # 튀는데, 스파이크는 그대로 나기 때문에 눈으로는 알아챌 수 없다.
    safe = np.where(small, 1.0, x)
    return np.where(small, 1.0 + x / 2.0, safe / (1.0 - np.exp(-safe)))


def rates(v, shift_mv: float = 0.0):
    """게이팅 속도상수 6개. 단위 1/ms.

    v 에서 shift_mv 를 빼는 것이 표면전하 효과의 구현 전부다.
    shift_mv 가 양수면 막은 더 과분극된 것처럼 행동한다 = 흥분하기 어려워진다.
    """
    u = np.asarray(v, dtype=float) - shift_mv
    # 주의: 원식은 0.1*(V+40)/(1-exp(-(V+40)/10)) 이다.
    # _lin_exp 에 (V+40)/10 을 넣으면 분자가 이미 10으로 나뉘어 있으므로
    # 앞 계수도 10배 해줘야 한다 (0.1 -> 1.0, 0.01 -> 0.1).
    # 여기서 10배를 놓치면 정지전위가 -65 가 아니라 -54 mV 로 나온다.
    a_m = 1.0 * _lin_exp((u + 40.0) / 10.0)
    b_m = 4.0 * np.exp(-(u + 65.0) / 18.0)
    a_h = 0.07 * np.exp(-(u + 65.0) / 20.0)
    b_h = 1.0 / (1.0 + np.exp(-(u + 35.0) / 10.0))
    a_n = 0.1 * _lin_exp((u + 55.0) / 10.0)
    b_n = 0.125 * np.exp(-(u + 65.0) / 80.0)
    return a_m, b_m, a_h, b_h, a_n, b_n


def steady_state(v, shift_mv: float = 0.0):
    """주어진 전압에서의 m, h, n 정상상태. 시뮬레이션 초기값으로 쓴다."""
    a_m, b_m, a_h, b_h, a_n, b_n = rates(v, shift_mv)
    return a_m / (a_m + b_m), a_h / (a_h + b_h), a_n / (a_n + b_n)


def resting_potential(mem: Membrane, lo: float = -90.0, hi: float = -40.0) -> float:
    """이온 전류의 합이 0이 되는 전압을 이분법으로 찾는다.

    shift_mv 나 leak_scale 을 건드리면 정지전위 자체가 움직인다.
    그걸 무시하고 -65 mV 에서 출발시키면 자극 없이도 막이 표류해,
    중금속 효과인지 초기값 오류인지 구별할 수 없게 된다.
    """
    def net(v: float) -> float:
        m, h, n = steady_state(v, mem.shift_mv)
        return float(
            mem.na_scale * mem.g_na * m ** 3 * h * (v - mem.e_na)
            + mem.g_k * n ** 4 * (v - mem.e_k)
            + mem.leak_scale * mem.g_l * (v - mem.e_l)
        )

    if net(lo) * net(hi) > 0:
        raise ValueError(f"[{lo}, {hi}] mV 안에 정지전위가 없다")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if net(lo) * net(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)
