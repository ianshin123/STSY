"""대응표본 t-검정의 검출력 계산.

전도속도의 노출 전후 비교에서, 반복 측정 변동(SD_rep)이 주어졌을 때
n마리로 검출 가능한 최소 변화율(MDE)을 구한다.

단위 약속: SD와 MDE 모두 '변화율 %'. 절대 속도(m/s)가 아니다.
개체마다 기저 속도가 다르므로 % 단위로만 비교가 의미를 갖는다.

정규(z) 근사를 쓰지 않는 이유는 정리/통계_검출력.md 참조.
n이 작을 때 검출 한계를 낙관적으로 내놓는다 (n=5에서 25 % 과소평가).
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats

ALPHA = 0.05
POWER = 0.80


def power_paired(n: int, effect_over_sd: float, alpha: float = ALPHA) -> float:
    """대응표본 t-검정(양측)의 검정력.

    effect_over_sd 는 Cohen's d — 차이의 평균 ÷ 차이의 표준편차.
    검정통계량이 비중심모수 d·sqrt(n) 인 비중심 t를 따른다는 사실을 쓴다.
    """
    if n < 2:
        raise ValueError("n은 2 이상이어야 한다")
    df = n - 1
    ncp = effect_over_sd * np.sqrt(n)
    t_crit = stats.t.ppf(1 - alpha / 2, df)

    upper = stats.nct.sf(t_crit, df, ncp)
    lower = stats.nct.cdf(-t_crit, df, ncp)
    # 반대쪽 꼬리는 ncp가 클 때 수치적으로 0에 눌려 nan이 되기도 한다.
    # 그 영역에서 실제 기여는 1e-10 미만이라 0으로 둔다.
    if not np.isfinite(lower):
        lower = 0.0
    return float(upper + lower)


def mde(n: int, sd_pct: float = 1.0, alpha: float = ALPHA,
        power: float = POWER) -> float:
    """검출 가능 최소 변화율(%). sd_pct=1.0 이면 SD 배수로 나온다."""
    def gap(x: float) -> float:
        return power_paired(n, x, alpha) - power

    # n이 작으면 필요한 d가 커진다(n=2에서 d>10). 위쪽 괄호를 넓혀가며 잡는다.
    hi = 2.0
    while gap(hi) < 0.0:
        hi *= 2.0
        if hi > 1e3:
            raise ValueError(f"n={n} 에서는 어떤 효과 크기로도 검정력 {power}에 못 미친다")
    d = optimize.brentq(gap, 1e-6, hi, xtol=1e-12)
    return d * sd_pct


def mde_normal_approx(n: int, sd_pct: float = 1.0, alpha: float = ALPHA,
                      power: float = POWER) -> float:
    """정규근사 버전. 비교용으로만 둔다 — 설계에 쓰지 마라."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return z / np.sqrt(n) * sd_pct


def required_n(sd_pct: float, target_pct: float, alpha: float = ALPHA,
               power: float = POWER, n_max: int = 500) -> int:
    """target_pct 변화를 검출하는 데 필요한 최소 개체 수."""
    for n in range(2, n_max + 1):
        if mde(n, sd_pct, alpha, power) <= target_pct:
            return n
    raise ValueError(f"n={n_max} 까지도 {target_pct}% 검출 불가 (SD={sd_pct}%)")


def table(ns=(5, 10, 15, 20, 30), sds=(1, 2, 3, 5)) -> str:
    """정리/통계_검출력.md 의 표를 그대로 재생성한다."""
    head = "| n | " + " | ".join(f"SD {s} %" for s in sds) + " |"
    rule = "|---|" + "---|" * len(sds)
    rows = [
        "| {} | {} |".format(n, " | ".join(f"{mde(n, s):.2f} %" for s in sds))
        for n in ns
    ]
    return "\n".join([head, rule, *rows])


if __name__ == "__main__":
    print("검출 가능 최소 변화율 (α=0.05 양측 · 검정력 0.80)\n")
    print(table())
    print("\n3 % 검출에 필요한 개체 수")
    for sd in (1, 2, 3, 5):
        n = required_n(sd, 3.0)
        print(f"  SD_rep {sd} %  ->  n = {n:2d}  (MDE {mde(n, sd):.2f} %)")
    print("\n정규근사와의 차이 (SD 배수)")
    for n in (5, 10, 15, 20, 30):
        exact, approx = mde(n), mde_normal_approx(n)
        print(f"  n={n:2d}  정확 {exact:.4f}  근사 {approx:.4f}"
              f"  과소평가 {100 * (1 - approx / exact):5.1f} %")
