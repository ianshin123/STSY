"""문서에 들어가는 표를 만드는 곳.

    python3 수학모델링캠프/코드/src/sweep.py

정리/ 아래 노트의 숫자 표는 전부 이 파일이 뽑은 것이다.
표를 고칠 일이 생기면 문서를 손으로 고치지 말고 여기를 고쳐 다시 뽑는다
(CLAUDE.md 「복사하지 말고 링크해라」 · 분석/README.md 의 power.py 와 같은 방식).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "분석" / "src"))

import axon as A
import hh
import metals as M
import recording as R

FS = 192_000.0
STIM = dict(stim_ua_cm2=300.0, stim_dur_ms=0.5, stim_comps=20)
SPAN_MM = 25.0
X0_CM = 1.5
# 채널 중심 위치 — channel_pair 의 기본 배치와 맞춰 둔다.
PROBE = (X0_CM + 0.625, X0_CM + SPAN_MM * 0.1 + 0.625)


def one(membrane=None, temp_c=20.0, diameter_um=70.0, r_a=A.R_A_DEFAULT,
        t_end_ms=22.0, noise_uv=0.0, seed=0):
    """한 조건을 돌리고 관측량을 전부 돌려준다.

    돌려주는 것 (전부 실험에서 실제로 잴 수 있는 양이다):
        v_true  케이블에서 직접 잰 전도속도 [m/s]
        v_est   세포외 파형을 분석 코드에 넣어 추정한 속도 [m/s]
        amp     이극 채널의 peak-to-peak [µV]
        ok      끝까지 전파했는가
    """
    import velocity as V

    ax = A.Axon(diameter_um=diameter_um, r_a=r_a, dx_um=100.0,
                length_mm=60.0, membrane=membrane or hh.Membrane())
    r = A.simulate(ax, temp_c, t_end_ms=t_end_ms, record_every=2, **STIM)

    v_true = r.conduction_velocity(*PROBE)
    t, a, b, d = R.channel_pair(r, span_mm=SPAN_MM, x_start_cm=X0_CM)
    amp = float(np.ptp(a))

    v_est = float("nan")
    if r.propagated():
        _, aa = R.resample(t, a, FS)
        _, bb = R.resample(t, b, FS)
        if noise_uv:
            aa = R.add_noise(aa, noise_uv, seed)
            bb = R.add_noise(bb, noise_uv, seed + 5000)
        est = V.estimate_dt(V.bandpass(aa, FS), V.bandpass(bb, FS), FS)
        if est.dt_s > 0:
            v_est = V.velocity(d, est.dt_s)
    return dict(v_true=v_true, v_est=v_est, amp=amp, ok=r.propagated())


def table_myelin_gap() -> str:
    """무수 모델이 MGF 속도에 얼마나 못 미치는가."""
    rows = ["| 세로저항 R_a | 지름 70 µm | 140 µm | 280 µm |", "|---|---|---|---|"]
    for ra in (35.4, 100.0):
        vals = [one(r_a=ra, diameter_um=d)["v_true"] for d in (70.0, 140.0, 280.0)]
        rows.append(f"| {ra} Ω·cm | " + " | ".join(f"{v:.2f} m/s" for v in vals) + " |")
    return "\n".join(rows)


def table_temperature() -> tuple[str, float]:
    """게이팅 Q10 = 3 이 전도속도 Q10 으로는 얼마가 되는가."""
    temps = np.array([10.0, 15.0, 20.0, 25.0])
    vs = np.array([one(temp_c=T, t_end_ms=30.0)["v_true"] for T in temps])
    slope = float(np.polyfit(temps, np.log(vs), 1)[0])
    q10 = float(np.exp(10.0 * slope))
    rows = ["| 온도 | 전도속도 | 기준(20 °C) 대비 |", "|---|---|---|"]
    base = vs[temps == 20.0][0]
    for T, v in zip(temps, vs):
        rows.append(f"| {T:.0f} °C | {v:.3f} m/s | {100 * (v / base - 1):+.1f} % |")
    return "\n".join(rows), q10


def table_signature(days: float = 7.0) -> str:
    """세 금속의 지문 — 속도와 진폭이 어떻게 같이 움직이는가."""
    base = hh.Membrane()
    ref = one(base)
    rows = ["| 금속 | 농도 | 속도 변화 | 진폭 변화 | 전파 |", "|---|---|---|---|---|"]
    for m in M.ALL:
        for c in (0.5, 1.0, 2.0, 4.0):
            g = one(m.membrane(base, c, days=days))
            dv = 100.0 * (g["v_true"] - ref["v_true"]) / ref["v_true"]
            da = 100.0 * (g["amp"] - ref["amp"]) / ref["amp"]
            rows.append(f"| {m.name} | {c:.1f} | {dv:+.2f} % | {da:+.2f} % | "
                        f"{'○' if g['ok'] else '**차단**'} |")
    return "\n".join(rows)


def table_timecourse(conc: float = 2.0) -> str:
    """시간 경과 — 차단형은 평평하고 손상형은 자란다."""
    base = hh.Membrane()
    ref = one(base)["v_true"]
    rows = ["| 일차 | 납 | 카드뮴 | 철 |", "|---|---|---|---|"]
    for d in (0, 1, 2, 4, 7):
        vals = [one(m.membrane(base, conc, days=float(d)))["v_true"] for m in M.ALL]
        rows.append(f"| {d}일 | " + " | ".join(f"{100 * (v - ref) / ref:+.2f} %" for v in vals) + " |")
    return "\n".join(rows)


def table_chain(noise_uv: float = 19.3, n_seeds: int = 5) -> str:
    """참값과 추정값의 차이 — 분석 파이프라인이 얼마나 정확한가."""
    rows = ["| 잡음 | 참값 | 추정값 | 오차 |", "|---|---|---|---|"]
    clean = one()
    rows.append(f"| 없음 | {clean['v_true']:.3f} m/s | {clean['v_est']:.3f} m/s | "
                f"{100 * (clean['v_est'] - clean['v_true']) / clean['v_true']:+.3f} % |")
    errs = []
    for s in range(n_seeds):
        g = one(noise_uv=noise_uv, seed=s)
        errs.append(100.0 * (g["v_est"] - g["v_true"]) / g["v_true"])
    rows.append(f"| {noise_uv} µV RMS · 단발 {n_seeds}회 | {clean['v_true']:.3f} m/s | — | "
                f"최대 {max(abs(e) for e in errs):.3f} % |")
    return "\n".join(rows)


def table_slope(temp_steps=(-3.0, -2.0, -1.0, 1.0, 2.0, 3.0),
                concs=(1.0, 2.0)) -> str:
    """★ 판별 지표 — 진폭 변화를 속도 변화로 나눈 기울기.

        S = (진폭 변화 %) / (속도 변화 %)

    네 요인(납·카드뮴·온도·철)이 이 한 숫자로 갈리는가를 본다.
    이것이 이 프로젝트가 STSY 에 내놓는 산출물이다
    (정리/파형에서_지표까지.md).
    """
    base = hh.Membrane()
    ref = one(base, t_end_ms=30.0)
    v0, a0 = ref["v_true"], ref["amp"]

    def row(label, g):
        dv = 100.0 * (g["v_true"] - v0) / v0
        da = 100.0 * (g["amp"] - a0) / a0
        return f"| {label} | {dv:+.2f} % | {da:+.2f} % | **{da / dv:+.3f}** |"

    rows = ["| 요인 | 속도 변화 | 진폭 변화 | 기울기 S |", "|---|---|---|---|"]
    for m in M.ALL:
        for c in concs:
            rows.append(row(f"{m.name} · 농도 {c:.1f}",
                            one(m.membrane(base, c, days=7.0), t_end_ms=30.0)))
    for d in temp_steps:
        rows.append(row(f"온도 {20 + d:.0f} °C ({d:+.0f})",
                        one(base, temp_c=20.0 + d, t_end_ms=30.0)))
    return "\n".join(rows)


def table_block() -> str:
    """전도 차단이 시작되는 지점 — 발화 확률 계산이 성립하는 구간."""
    base = hh.Membrane()
    rows = ["| 손상 방식 | 세기 | 전파 | 속도 |", "|---|---|---|---|"]
    for na in (0.7, 0.5, 0.4, 0.3):
        g = one(base.with_metal(na_scale=na), t_end_ms=40.0)
        rows.append(f"| Na 전도도 | ×{na:.2f} | {'○' if g['ok'] else '**차단**'} | "
                    f"{g['v_true']:.3f} m/s |" if g["ok"] else
                    f"| Na 전도도 | ×{na:.2f} | **차단** | — |")
    for lk in (5, 10, 20, 40):
        g = one(base.with_metal(leak_scale=float(lk)), t_end_ms=40.0)
        rows.append(f"| 누설 전도도 | ×{lk} | {'○' if g['ok'] else '**차단**'} | "
                    f"{g['v_true']:.3f} m/s |" if g["ok"] else
                    f"| 누설 전도도 | ×{lk} | **차단** | — |")
    return "\n".join(rows)


if __name__ == "__main__":
    print("## 무수 모델과 MGF 속도의 간격\n")
    print(table_myelin_gap())
    temp, q10 = table_temperature()
    print(f"\n\n## 온도 (속도 Q10 = {q10:.3f} · 도당 {100 * (q10 ** 0.1 - 1):.2f} %)\n")
    print(temp)
    print("\n\n## 금속별 지문 (7일)\n")
    print(table_signature())
    print("\n\n## 시간 경과 (농도 2.0)\n")
    print(table_timecourse())
    print("\n\n## 전 구간 정확도\n")
    print(table_chain())
    print("\n\n## 전도 차단 지점\n")
    print(table_block())
    print("\n\n## 판별 지표 S = 진폭변화 / 속도변화\n")
    print(table_slope())
