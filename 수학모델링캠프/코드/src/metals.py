"""중금속 세 종을 막 파라미터의 변화로 옮긴다.

★ 이 파일이 이 프로젝트에서 가장 조심해야 할 곳이다.
   여기 있는 숫자 중 문헌에서 온 것은 하나도 없다. 전부 우리가 세운 구조이고,
   상수는 훑어야 하는 미지수다. 근거의 층위는 정리/금속별_기전.md 에 정리했다.
   요약하면:

   확립된 것   2가 양이온이 막 표면 음전하를 가리면 게이팅 곡선이 탈분극
              쪽으로 밀린다 (표면전하 효과 · Frankenhaeuser & Hodgkin 1957
              · 원문 미확보). Cd2+ 는 표준적인 Ca2+ 통로 차단제다.
              Fe2+ 는 펜톤 반응으로 하이드록실 라디칼을 만든다.
   우리 가설   그 이동폭이 지렁이 MGF 에서 얼마인가. 철의 산화 손상이
              축삭 누설 전도도로 이어지는가. 결합 상수가 얼마인가.

세 금속을 굳이 다른 구조로 놓는 이유가 이 프로젝트의 핵심 주장이다.
같은 식에 계수만 바꿔 넣으면 "세 금속이 다르다"는 결과가 나와도 그것은
우리가 계수를 다르게 넣었기 때문이지 발견이 아니다.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

import hh


def occupancy(conc, k_half: float, hill: float = 1.0):
    """결합 점유율 (Langmuir / Hill). 0에서 1 사이.

        theta = C^h / (C^h + K^h)

    conc 와 k_half 는 같은 단위이기만 하면 된다. 절대 농도를 모르므로
    이 모델은 '반효과농도의 몇 배인가'로만 말한다.
    """
    c = np.asarray(conc, dtype=float)
    if k_half <= 0:
        raise ValueError("k_half 는 양수여야 한다")
    return c ** hill / (c ** hill + k_half ** hill)


def cumulative_damage(conc, days, k_rate: float, d_max: float = 1.0):
    """누적 손상. 농도x시간에 의존한다.

        D = d_max * (1 - exp(-k_rate * C * t))

    차단과 결정적으로 다른 점: 시간이 들어간다. 그리고 노출을 끊어도
    되돌아가지 않는다 (이 함수에는 회복항이 없다).
    이 차이가 실험에서 기전을 가르는 관측량이 된다.
    """
    c = np.asarray(conc, dtype=float)
    t = np.asarray(days, dtype=float)
    return d_max * (1.0 - np.exp(-k_rate * c * t))


@dataclass(frozen=True)
class Metal:
    """금속 하나의 작용 방식.

    shift_max_mv : 포화 시 게이팅 전압 이동 [mV]  (차단형 경로)
    na_block_max : 포화 시 Na 전도도가 남는 비율  (1.0 이면 구멍 차단 없음)
    k_half       : 반효과농도 (conc 와 같은 단위)
    leak_max     : 손상 포화 시 누설 전도도 배수  (손상형 경로)
    k_damage     : 손상 축적 속도 [1/(농도*일)]
    time_dependent : True 면 손상형 — 효과가 농도x시간으로 자란다
    essential    : True 면 필수 원소 — 용량반응이 U자가 될 수 있다
    """

    name: str
    shift_max_mv: float = 0.0
    na_block_max: float = 1.0
    k_half: float = 1.0
    leak_max: float = 1.0
    k_damage: float = 0.0
    time_dependent: bool = False
    essential: bool = False

    def membrane(self, base: hh.Membrane, conc: float, days: float = 7.0) -> hh.Membrane:
        """이 금속에 conc 농도로 days 일 노출된 막."""
        theta = float(occupancy(conc, self.k_half))
        shift = self.shift_max_mv * theta
        na = 1.0 - (1.0 - self.na_block_max) * theta

        leak = 1.0
        if self.time_dependent and self.k_damage > 0:
            dmg = float(cumulative_damage(conc, days, self.k_damage))
            leak = 1.0 + (self.leak_max - 1.0) * dmg
        return base.with_metal(shift_mv=shift, na_scale=na, leak_scale=leak)


# ---------------------------------------------------------------------------
# 세 금속. 상수는 전부 잠정값이다 — 훑을 대상이지 인용할 값이 아니다.
# ---------------------------------------------------------------------------

# 납. 사람 직업노출에서 전도속도 저하가 보고돼 있고 (약 3 % ·
# 문헌/납신경독성_문헌군.md · 논문 특정 안 됨), Ca2+ 를 흉내내는 것이
# 알려져 있다. 차단형으로 놓는다 — 농도에 평형, 시간에 거의 무관.
LEAD = Metal(name="납", shift_max_mv=15.0, na_block_max=0.85, k_half=1.0)

# 카드뮴. 전기생리에서 표준 Ca2+ 통로 차단제로 쓰인다. 구멍 차단이 납보다
# 강하고 표면전하 이동은 약하다고 놓았다 — 이 대비 자체가 가설이다.
CADMIUM = Metal(name="카드뮴", shift_max_mv=8.0, na_block_max=0.70, k_half=1.5)

# 철. 필수 원소이고 주 기전이 펜톤 반응 -> 지질 과산화다.
# 통로 차단이 아니라 막 손상으로 놓는다. 시간 의존이고 되돌아가지 않는다.
IRON = Metal(name="철", shift_max_mv=2.0, na_block_max=0.97, k_half=4.0,
             leak_max=6.0, k_damage=0.25, time_dependent=True, essential=True)

ALL = (LEAD, CADMIUM, IRON)


def iron_u_curve(conc, k_deficiency: float = 0.3, k_toxicity: float = 4.0,
                 include_deficiency: bool = True):
    """철의 U자 용량반응 — 상대 손상도 (0이 최적).

    철은 필수 원소라 부족해도 나쁘고 과해도 나쁘다. 납·카드뮴에는 없는 성질이다.

    ★ 왼쪽 가지(결핍)는 우리 실험에서 만들어지지 않을 가능성이 높다.
      노출 실험은 흙에 이미 있는 철에 더 얹는 것이고, 7일은 저장 철을
      고갈시키기에 짧다. 그래서 이 함수는 '모델이 U자를 안다'는 것을
      보이는 용도이고, 실제 예측에 쓰는 것은 오른쪽 가지뿐이다.
      include_deficiency=False 로 두면 오른쪽 가지만 쓴다.

    결핍 가지의 형태와 상수는 전부 우리 가정이다. 문헌 근거가 없다.
    """
    c = np.asarray(conc, dtype=float)
    tox = occupancy(c, k_toxicity)
    if not include_deficiency:
        return tox
    defi = 1.0 - occupancy(c, k_deficiency)
    return defi + tox
