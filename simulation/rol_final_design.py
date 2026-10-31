"""CL420 final design: four-state simulation, oxygen screen and batch budget.

Run from any directory with: python simulation/rol_final_design.py
Requires the already installed numpy and matplotlib packages. The midterm
module supplies its published kinetic functions; its main routine is not run.
Literature inputs and design assumptions are distinguished in the report.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from rol_fed_batch_simulation import (
    Parameters,
    q_oxygen,
    q_substrate,
    rk4_step,
    specific_rates,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "output" / "data" / "final"
FIGURES = ROOT / "report" / "final" / "figures"
TEAL, ORANGE, INK = "#087F8C", "#D65B29", "#263640"


@dataclass(frozen=True)
class Design:
    # Source: thesis pp. 94-95, 103. Other values below are design assumptions.
    nitrogen_per_methanol: float = 0.12  # g NH4Cl / g methanol
    nitrogen_stock: float = 200.0  # g NH4Cl / L stock
    initial_s: float = 2.0  # common initial condition chosen for model comparisons
    maximum_volume: float = 3.5  # L; 30% freeboard in a nominal 5 L vessel
    dt: float = 0.01  # h
    horizon: float = 120.0  # h
    ramp_duration: float = 60.0  # h; study definition, not a published ramp duration
    cs_target: float = 2.0  # g methanol / L
    air_solubility: float = 2.3e-4  # mol O2/L at source temperature, air saturation
    do_fraction_air: float = 0.25
    kla: float = 1000.0  # h^-1; qualification target, NOT a measurement
    oxygen_fraction: float = 0.75  # inlet fraction for the proposed enriched case
    vvm: float = 2.0  # actual L gas / L broth / min at stated vessel conditions
    gas_temperature: float = 303.15  # K
    gas_pressure: float = 1.0  # bar absolute, screening assumption
    capacity_allowance: float = 1.20  # OTR must exceed OUR by 20%
    tank_diameter: float = 0.13  # m, assumed geometry allowing initial impeller immersion
    impeller_diameter: float = 0.065  # m
    impeller_count: int = 2
    lower_impeller_center: float = 0.040  # m above the floor
    upper_impeller_center: float = 0.105  # m above the floor
    impeller_blade_height: float = 0.013  # m
    rpm: float = 1000.0
    power_number: float = 5.0
    gassed_power_fraction: float = 0.70
    broth_density: float = 1000.0  # kg/m^3
    recovery: float = 0.70  # assumed combined activity recovery
    pre_induction_hours: float = 23.0  # budget: 18 h batch allowance + source 5 h transition
    turnaround_hours: float = 6.0  # assumed equipment occupancy


def volume_per_feed(p: Parameters, d: Design) -> float:
    """L total liquid added per g methanol; minor feeds/evaporation omitted."""
    return 1.0 / p.rho_methanol + d.nitrogen_per_methanol / d.nitrogen_stock


def prescribed_growth(t: float, strategy: str, d: Design) -> tuple[float, float]:
    """Target mu and integral(mu dt), defining a feed without biomass feedback."""
    if strategy == "CM":
        return 0.03, 0.03 * t
    slope = 0.03 / d.ramp_duration
    ramp_t = min(t, d.ramp_duration)
    integral = 0.01 * ramp_t + 0.5 * slope * ramp_t**2
    integral += 0.04 * max(t - d.ramp_duration, 0.0)
    return 0.01 + slope * ramp_t, integral


def feed(t: float, y: np.ndarray, model: str, strategy: str, p: Parameters, d: Design) -> float:
    if strategy == "CF":
        return 14.0
    if strategy in ("CM", "LM"):
        mu_target, integral = prescribed_growth(t, strategy, d)
        return q_substrate(mu_target, p) * p.biomass_0 * p.volume_0 * math.exp(integral)
    if strategy == "CS":
        s = y[2] / y[0]
        mu, _ = specific_rates(model, s, p)
        return q_substrate(mu, p) * y[1] / (1.0 - volume_per_feed(p, d) * s)
    raise ValueError(strategy)


def rhs(t: float, y: np.ndarray, model: str, strategy: str, p: Parameters, d: Design) -> np.ndarray:
    s = y[2] / y[0]
    mu, qp = specific_rates(model, s, p)
    f = feed(t, y, model, strategy, p, d)
    return np.array([volume_per_feed(p, d) * f, mu * y[1], f - q_substrate(mu, p) * y[1], qp * y[1]])


def gas_capacity(volume: np.ndarray | float, d: Design, oxygen: float | None = None) -> np.ndarray:
    """Self-consistent maximum OTR per litre, at the specified liquid DO.

    Integrate the plug-flow gas balance against a well-mixed liquid. RQ=1
    keeps dry gas molar flow constant. Inlet vvm, kLa and gas composition
    are fixed, so volumetric capacity is constant, not a function of OUR.
    Volume supplies the output broadcast shape; total capacity equals OTRV*V.
    """
    y_in = d.oxygen_fraction if oxygen is None else oxygen
    g = d.vvm * 60.0 * d.gas_pressure / (0.083144626 * d.gas_temperature)
    c = d.air_solubility / 0.21
    c_l = d.do_fraction_air * d.air_solubility
    gas_limit = (g / c) * max(c * y_in - c_l, 0.0)
    capacity = gas_limit * (-math.expm1(-d.kla * c / g))
    return np.full_like(np.asarray(volume), capacity, dtype=float)


def required_kla(our_vol: float, d: Design, oxygen: float | None = None) -> float:
    """Invert the capacity balance after including the demand allowance."""
    y_in = d.oxygen_fraction if oxygen is None else oxygen
    g = d.vvm * 60.0 * d.gas_pressure / (0.083144626 * d.gas_temperature)
    c = d.air_solubility / 0.21
    gas_limit = (g / c) * max(c * y_in - d.do_fraction_air * d.air_solubility, 0.0)
    target = d.capacity_allowance * our_vol
    if target >= gas_limit:
        return math.inf
    return -(g / c) * math.log1p(-target / gas_limit)


def properties(t: float, y: np.ndarray, model: str, strategy: str, p: Parameters, d: Design) -> dict[str, float]:
    v, b, substrate, activity = y
    mu, qp = specific_rates(model, substrate / v, p)
    our = q_oxygen(mu, p) * b
    return {"time_h": t, "V_L": v, "X_g_L": b / v, "S_g_L": substrate / v,
            "P_U_mL": activity / v / 1000.0, "biomass_g": b, "substrate_g": substrate,
            "activity_U": activity, "mu_h_inv": mu, "qP_U_g_h": qp,
            "qS_g_g_h": q_substrate(mu, p), "methanol_feed_g_h": feed(t, y, model, strategy, p, d),
            "OUR_mol_h": our, "OUR_mol_L_h": our / v,
            "OTR_air_mol_L_h": float(gas_capacity(v, d, 0.21)),
            "OTR_enriched_mol_L_h": float(gas_capacity(v, d))}


def simulate(model: str, strategy: str, p: Parameters, d: Design) -> tuple[dict[str, np.ndarray], str]:
    initial_s = d.cs_target if strategy == "CS" else d.initial_s
    y = np.array([p.volume_0, p.biomass_0 * p.volume_0, initial_s * p.volume_0, p.product_0 * 1000 * p.volume_0])
    t, rows, stop = 0.0, [], "time limit"
    fn = lambda local_t, local_y: rhs(local_t, local_y, model, strategy, p, d)
    while True:
        rows.append(properties(t, y, model, strategy, p, d))
        if t >= d.horizon - 1e-10:
            break
        h = min(d.dt, d.horizon - t)
        next_y = rk4_step(fn, t, y, h)
        if np.any(next_y < -1e-8):
            raise ArithmeticError("Negative state: reduce time step rather than clip the trajectory")
        crossings = []
        for label, index, limit, concentration in [("biomass", 1, p.x_max, True), ("volume", 0, d.maximum_volume, False), ("methanol", 2, p.methanol_max, True)]:
            value = next_y[index] / next_y[0] if concentration else next_y[index]
            if value >= limit:
                low, high = 0.0, h
                for _ in range(35):
                    mid = (low + high) / 2
                    trial = rk4_step(fn, t, y, mid)
                    value = trial[index] / trial[0] if concentration else trial[index]
                    if value >= limit:
                        high = mid
                    else:
                        low = mid
                crossings.append((high, label))
        if crossings:
            step, stop = min(crossings)
            y = rk4_step(fn, t, y, step)
            t += step
            rows.append(properties(t, y, model, strategy, p, d))
            break
        y, t = next_y, t + h
    return {key: np.array([r[key] for r in rows]) for key in rows[0]}, stop


def exact_cs(model: str, p: Parameters, d: Design) -> tuple[dict[str, np.ndarray], str]:
    """Closed-form CS solution, independent verification of the RK4 result."""
    s, v0, b0 = d.cs_target, p.volume_0, p.biomass_0 * p.volume_0
    mu, qp = specific_rates(model, s, p)
    a = volume_per_feed(p, d)
    k = a * q_substrate(mu, p) * b0 / (mu * (1 - a * s))
    events = [(d.horizon, "time limit")]
    if b0 > p.x_max * k:
        z_x = p.x_max * (v0 - k) / (b0 - p.x_max * k)
        if z_x > 1:
            events.append((math.log(z_x) / mu, "biomass"))
    z_v = 1 + (d.maximum_volume - v0) / k
    events.append((math.log(z_v) / mu, "volume"))
    final_t, stop = min(events)
    times = np.linspace(0, final_t, 301)
    rows = []
    for t in times:
        z = math.exp(mu * t)
        v, b = v0 + k * (z - 1), b0 * z
        activity = p.product_0 * 1000 * v0 + qp / mu * (b - b0)
        rows.append(properties(t, np.array([v, b, s * v, activity]), model, "CS", p, d))
    return {key: np.array([r[key] for r in rows]) for key in rows[0]}, stop


def metrics(model: str, strategy: str, a: dict[str, np.ndarray], stop: str, p: Parameters, d: Design) -> dict:
    v, t = a["V_L"][-1], a["time_h"][-1]
    methanol_feed = (v - p.volume_0) / volume_per_feed(p, d)
    consumed = a["substrate_g"][0] + methanol_feed - a["substrate_g"][-1]
    net_activity = a["activity_U"][-1] - a["activity_U"][0]
    net_biomass = a["biomass_g"][-1] - a["biomass_g"][0]
    feasibility = a["OTR_enriched_mol_L_h"] / (d.capacity_allowance * a["OUR_mol_L_h"])
    return {"model": model, "strategy": strategy, "time_h": float(t), "V_L": float(v),
            "X_g_L": float(a["X_g_L"][-1]), "S_g_L": float(a["S_g_L"][-1]),
            "P_U_mL": float(a["P_U_mL"][-1]), "QP_U_L_h": float(net_activity / v / t),
            "activity_U": float(a["activity_U"][-1]), "net_activity_U": float(net_activity),
            "methanol_feed_g": float(methanol_feed), "methanol_consumed_g": float(consumed),
            "NH4Cl_g": float(d.nitrogen_per_methanol * methanol_feed),
            "nitrogen_feed_L": float(d.nitrogen_per_methanol * methanol_feed / d.nitrogen_stock),
            "YX_S_g_g": float(net_biomass / consumed), "YP_S_U_g": float(net_activity / consumed),
            "max_feed_g_h": float(np.max(a["methanol_feed_g_h"])),
            "max_OUR_mol_h": float(np.max(a["OUR_mol_h"])),
            "max_OUR_mol_L_h": float(np.max(a["OUR_mol_L_h"])),
            "min_oxygen_capacity_ratio": float(np.min(feasibility)),
            "oxygen_feasible_with_allowance": bool(np.min(feasibility) >= 1.0), "stop": stop}


def hardware(volume: float, d: Design) -> dict:
    n = d.rpm / 60.0
    ungassed = d.impeller_count * d.power_number * d.broth_density * n**3 * d.impeller_diameter**5
    gassed = d.gassed_power_fraction * ungassed
    power_volume = gassed / (volume / 1000.0)
    gas_m3_s = d.vvm * volume / 1000.0 / 60.0
    superficial = gas_m3_s / (math.pi * d.tank_diameter**2 / 4)
    liquid_depth = volume / 1000.0 / (math.pi * d.tank_diameter**2 / 4)
    return {"ungassed_power_W": ungassed, "gassed_power_W": gassed,
            "gassed_power_W_m3": power_volume, "gas_L_min": d.vvm * volume,
            "superficial_velocity_m_s": superficial,
            "tip_speed_m_s": math.pi * d.impeller_diameter * n,
            "liquid_depth_m": liquid_depth,
            "upper_blade_immersion_m": liquid_depth - d.upper_impeller_center - d.impeller_blade_height / 2,
            "kla_water_h_inv": 3600 * 0.026 * power_volume**0.4 * superficial**0.5,
            "kla_electrolyte_h_inv": 3600 * 0.002 * power_volume**0.7 * superficial**0.2}


def budget(a: dict[str, np.ndarray], m: dict, d: Design, recovery: float | None = None) -> dict:
    """Illustrative INR batch budget, unit rates are assumptions, not quotations."""
    recovery = d.recovery if recovery is None else recovery
    t, v = a["time_h"], a["V_L"]
    total_gas_L = float(np.trapezoid(d.vvm * v * 60, t))
    # Mixing pure O2 with air: pure-O2 fraction = (yin - 0.21)/(1 - 0.21).
    pure_fraction = (d.oxygen_fraction - 0.21) / 0.79
    oxygen_L = pure_fraction * total_gas_L
    air_L = total_gas_L - oxygen_L
    occupied = d.pre_induction_hours + m["time_h"] + d.turnaround_hours
    hw = hardware(m["V_L"], d)
    mixing_kWh = hw["ungassed_power_W"] / 1000 * (d.pre_induction_hours + m["time_h"])
    rows = [
        {"item": "Seed medium and basal salts", "quantity": 1.0, "unit": "batch", "INR_per_unit": 450.0},
        {"item": "Initial glycerol", "quantity": 0.080, "unit": "kg", "INR_per_unit": 200.0},
        {"item": "Transition feeds, pH stocks and antifoam", "quantity": 1.0, "unit": "batch allowance", "INR_per_unit": 250.0},
        {"item": "Induction methanol", "quantity": (m["methanol_feed_g"] + 2 * d.cs_target) / 1000, "unit": "kg", "INR_per_unit": 80.0},
        {"item": "Induction NH4Cl", "quantity": m["NH4Cl_g"] / 1000, "unit": "kg", "INR_per_unit": 200.0},
        {"item": "Supplemental oxygen, induction", "quantity": oxygen_L / 1000, "unit": "m3 at 30 C, 1 bar", "INR_per_unit": 100.0},
        {"item": "Compressed air, all phases", "quantity": air_L / 1000 + d.pre_induction_hours * 2 * 60 / 1000, "unit": "m3 at 30 C, 1 bar", "INR_per_unit": 10.0},
        {"item": "Mixing electricity", "quantity": mixing_kWh, "unit": "kWh", "INR_per_unit": 10.0},
        {"item": "Sterilization and cooling", "quantity": 1.0, "unit": "batch allowance", "INR_per_unit": 300.0},
        {"item": "Reactor occupancy", "quantity": occupied, "unit": "h", "INR_per_unit": 100.0},
        {"item": "Clarification, membrane use and buffers", "quantity": 1.0, "unit": "batch allowance", "INR_per_unit": 1500.0},
        {"item": "Hands-on labor", "quantity": 6.0, "unit": "h", "INR_per_unit": 150.0},
        {"item": "Waste treatment", "quantity": 1.0, "unit": "batch allowance", "INR_per_unit": 150.0},
    ]
    for row in rows:
        row["cost_INR"] = row["quantity"] * row["INR_per_unit"]
    total = sum(r["cost_INR"] for r in rows)
    recovered = recovery * m["activity_U"]
    return {"rows": rows, "total_INR": total, "recovery": recovery,
            "recovered_activity_U": recovered, "INR_per_million_recovered_U": total / recovered * 1e6,
            "occupancy_h": occupied, "total_induction_gas_L": total_gas_L,
            "supplemental_oxygen_L": oxygen_L, "induction_air_L": air_L, "mixing_kWh": mixing_kWh,
            "pre_induction_gas_limitation": "air allowance only; transition enrichment included in stock allowance, not metered"}


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save_figure(fig: plt.Figure, name: str) -> None:
    for extension in ("png", "pdf"):
        fig.savefig(FIGURES / f"{name}.{extension}", dpi=260, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_report_numbers(summary: dict) -> None:
    """Keep report numbers linked to the executed calculations."""
    selected, baseline, cost = summary["selected_CS"], summary["baseline_CS"], summary["budget"]
    h, d = summary["hardware_harvest"], summary["design_assumptions"]
    values = {
        "Setpoint": (summary["best_feasible_constant_setpoint"]["setpoint_g_L"], ".1f"),
        "FinalTime": (selected["time_h"], ".2f"), "FinalVolume": (selected["V_L"], ".3f"),
        "FinalBiomass": (selected["X_g_L"] * selected["V_L"], ".2f"),
        "FinalActivity": (selected["P_U_mL"], ".2f"), "FinalProductivity": (selected["QP_U_L_h"], ",.0f"),
        "FinalTotalActivity": (selected["activity_U"] / 1e6, ".3f"), "FinalNetActivity": (selected["net_activity_U"] / 1e6, ".3f"),
        "MethanolFed": (selected["methanol_feed_g"], ".2f"), "MethanolConsumed": (selected["methanol_consumed_g"], ".2f"),
        "NitrogenMass": (selected["NH4Cl_g"], ".2f"), "NitrogenVolume": (selected["nitrogen_feed_L"], ".3f"),
        "MethanolVolume": (selected["methanol_feed_g"] / summary["kinetic_parameters"]["rho_methanol"], ".3f"),
        "BiomassYield": (selected["YX_S_g_g"], ".4f"), "ActivityYield": (selected["YP_S_U_g"], ",.0f"),
        "MaxFeed": (selected["max_feed_g_h"], ".2f"), "PeakOUR": (selected["max_OUR_mol_h"], ".3f"),
        "PeakVolOUR": (selected["max_OUR_mol_L_h"] * 1000, ".1f"),
        "KlaRequired": (required_kla(selected["max_OUR_mol_L_h"], Design(**d)), ".0f"),
        "TransferCapacity": (float(gas_capacity(selected["V_L"], Design(**d))) * 1000, ".1f"),
        "WaterKla": (h["kla_water_h_inv"], ".0f"), "ElectrolyteKla": (h["kla_electrolyte_h_inv"], ".0f"),
        "GassedPower": (h["gassed_power_W"], ".1f"), "PowerDensity": (h["gassed_power_W_m3"] / 1000, ".2f"),
        "GasFlow": (h["gas_L_min"], ".2f"), "Superficial": (h["superficial_velocity_m_s"], ".5f"),
        "BatchCost": (cost["total_INR"], ",.0f"), "UnitCost": (cost["INR_per_million_recovered_U"], ",.0f"),
        "RecoveredActivity": (cost["recovered_activity_U"] / 1e6, ".3f"), "Occupancy": (cost["occupancy_h"], ".2f"),
        "OxygenVolume": (cost["supplemental_oxygen_L"] / 1000, ".2f"),
        "MixingEnergy": (cost["mixing_kWh"], ".2f"),
        "CycleProductivity": (selected["net_activity_U"] / selected["V_L"] / cost["occupancy_h"], ",.0f"),
        "MonodFeasibleSetpoint": (summary["best_feasible_monod_setpoint"]["setpoint_g_L"], ".1f"),
        "MonodFeasibleProductivity": (summary["best_feasible_monod_setpoint"]["QP_U_L_h"], ",.0f"),
        "ProductivityGain": (100 * (selected["QP_U_L_h"] / baseline["QP_U_L_h"] - 1), ".1f"),
    }
    lines = ["% Generated by simulation/rol_final_design.py. Do not edit numerical values here."]
    for name, (value, fmt) in values.items():
        lines.append("\\newcommand{\\" + name + "}{" + format(value, fmt) + "}")
    for recovery, name in [(0.5, "LowRecoveryCost"), (0.9, "HighRecoveryCost")]:
        value = cost["total_INR"] / (selected["activity_U"] * recovery) * 1e6
        lines.append("\\newcommand{\\" + name + "}{" + format(value, ",.0f") + "}")
    result_rows = []
    for r in summary["results"]:
        result_rows.append(f"{r['model'].split()[0]} & {r['strategy']} & {r['time_h']:.2f} & {r['V_L']:.3f} & {r['P_U_mL']:.2f} & {r['QP_U_L_h']:,.0f} & {r['max_OUR_mol_h']:.3f} " + r"\\")
    (FIGURES.parent / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    table_start = r"\begin{tabular}{@{}llrrrrr@{}}\toprule" + "\n" + r"Model & Feed & \shortstack{$t_f$\\h} & \shortstack{$V_f$\\L} & \shortstack{$P_f$\\U mL$^{-1}$} & \shortstack{$Q_P$\\U L$^{-1}$ h$^{-1}$} & \shortstack{Peak OUR\\mol h$^{-1}$}\\\midrule" + "\n"
    (FIGURES.parent / "result_rows.tex").write_text(table_start + "\n".join(result_rows) + "\n" + r"\bottomrule\end{tabular}" + "\n", encoding="utf-8")


def figures(cases: dict, results: list[dict], scan: list[dict], sensitivities: list[dict], p: Parameters, d: Design) -> None:
    plt.rcParams.update({"font.family": "Times New Roman", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.labelcolor": INK, "text.color": INK, "axes.edgecolor": "#8C979D",
                         "axes.grid": True, "grid.alpha": 0.16, "legend.frameon": False})
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.25), constrained_layout=True)
    s = np.linspace(0, 10, 400)
    for model, color, style in [("Haldane inhibition", TEAL, "-"), ("Monod comparator", ORANGE, "--")]:
        rates = np.array([specific_rates(model, float(v), p) for v in s])
        for index, ax in enumerate(axes):
            ax.plot(s, rates[:, index], color=color, ls=style, lw=2, label=model.replace(" comparator", ""))
    axes[0].set_ylabel("Specific growth rate [h$^{-1}$]")
    axes[1].set_ylabel("Product rate [U g$^{-1}$ h$^{-1}$]")
    for ax in axes:
        ax.set_xlabel("Methanol [g L$^{-1}$]")
    axes[0].legend(fontsize=9)
    save_figure(fig, "kinetic_models")

    fig, axes = plt.subplots(2, 3, figsize=(7.2, 3.65), constrained_layout=True)
    for row, strategy in enumerate(("CF", "CS")):
        for model, color, ls in [("Haldane inhibition", TEAL, "-"), ("Monod comparator", ORANGE, "--")]:
            a = cases[(model, strategy)][0]
            for ax, key in zip(axes[row], ("X_g_L", "S_g_L", "P_U_mL")):
                ax.plot(a["time_h"], a[key], color=color, ls=ls, lw=1.8, label=model.split()[0])
                ax.set_xlabel("Induction time [h]")
        for ax, ylabel in zip(axes[row], ("Biomass [g L$^{-1}$]", "Methanol [g L$^{-1}$]", "Activity [U mL$^{-1}$]")):
            ax.set_ylabel(ylabel)
        if strategy == "CS":
            axes[row, 1].set_ylim(d.cs_target - 0.1, d.cs_target + 0.1)
            axes[row, 1].ticklabel_format(axis="y", style="plain", useOffset=False)
        axes[row, 0].set_title(strategy, loc="left", weight="bold")
    axes[0, 0].legend(fontsize=9)
    save_figure(fig, "dynamic_comparison")

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.25), constrained_layout=True)
    x = np.arange(4)
    for offset, model, color in [(-0.18, "Haldane inhibition", TEAL), (0.18, "Monod comparator", ORANGE)]:
        selected = [r for r in results if r["model"] == model]
        for ax, key in zip(axes, ("P_U_mL", "QP_U_L_h")):
            ax.bar(x + offset, [r[key] for r in selected], 0.34, color=color, label=model.split()[0], zorder=3)
    axes[0].set_ylabel("Harvest activity [U mL$^{-1}$]")
    axes[1].set_ylabel("Net productivity [U L$^{-1}$ h$^{-1}$]")
    for ax in axes:
        ax.set_xticks(x, ["CF", "CM", "LM", "CS"])
        ax.grid(axis="x", visible=False)
    axes[0].legend(fontsize=9)
    save_figure(fig, "feeding_comparison")

    a = cases[("Haldane inhibition", "CS-selected")][0]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.5), constrained_layout=True)
    axes[0].plot(a["time_h"], a["OUR_mol_L_h"] * 1000, color=TEAL, lw=2, label="Predicted OUR")
    axes[0].plot(a["time_h"], d.capacity_allowance * a["OUR_mol_L_h"] * 1000, color=TEAL, ls=":", label="OUR + 20% allowance")
    axes[0].plot(a["time_h"], a["OTR_air_mol_L_h"] * 1000, color="#8C979D", label="Air capacity")
    axes[0].plot(a["time_h"], a["OTR_enriched_mol_L_h"] * 1000, color=ORANGE, lw=2, label="75% O2 capacity")
    axes[0].set(xlabel="Induction time [h]", ylabel="Oxygen rate [mmol L$^{-1}$ h$^{-1}$]")
    axes[0].set_ylim(0, float(np.max(a["OTR_enriched_mol_L_h"])) * 1330)
    axes[0].legend(fontsize=8, ncol=2, columnspacing=0.8, handlelength=1.6)
    fractions = np.linspace(0.21, 1.0, 120)
    required = [required_kla(float(a["OUR_mol_L_h"][-1]), d, float(frac)) for frac in fractions]
    axes[1].plot(fractions * 100, required, color=TEAL, lw=2)
    axes[1].axhline(d.kla, color=ORANGE, ls="--", label="Qualification target")
    axes[1].set(xlabel="Inlet oxygen [mol %]", ylabel="Required kLa incl. allowance [h$^{-1}$]")
    axes[1].legend(fontsize=9)
    save_figure(fig, "oxygen_design")

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.4), constrained_layout=True)
    for model, color, ls in [("Haldane inhibition", TEAL, "-"), ("Monod comparator", ORANGE, "--")]:
        selected = [r for r in scan if r["model"] == model]
        for ax, key in zip(axes, ("P_U_mL", "QP_U_L_h")):
            ax.plot([r["setpoint_g_L"] for r in selected], [r[key] for r in selected], color=color, ls=ls, lw=2, alpha=0.38 if model == "Monod comparator" else 1, label="Monod unfiltered" if model == "Monod comparator" else "Haldane")
            if model == "Monod comparator":
                feasible = [r for r in selected if r["oxygen_feasible_with_allowance"]]
                ax.plot([r["setpoint_g_L"] for r in feasible], [r[key] for r in feasible], color=color, lw=2)
                best_monod = max(feasible, key=lambda r: r["QP_U_L_h"])
                ax.plot(best_monod["setpoint_g_L"], best_monod[key], marker="o", ms=5, color=color, label="Monod feasible limit")
    for ax in axes:
        ax.set_xlabel("Constant methanol setpoint [g L$^{-1}$]")
    axes[0].set_ylabel("Harvest activity [U mL$^{-1}$]")
    axes[1].set_ylabel("Net productivity [U L$^{-1}$ h$^{-1}$]")
    axes[0].legend(fontsize=9)
    selected = max((r for r in scan if r["model"] == "Haldane inhibition" and r["oxygen_feasible_with_allowance"]), key=lambda r: r["QP_U_L_h"])
    for ax in axes:
        ax.axvline(selected["setpoint_g_L"], color="#73838B", lw=1, ls=":")
    save_figure(fig, "setpoint_scan")

    fig, ax = plt.subplots(figsize=(7.1, 2.25), constrained_layout=True)
    labels = list(dict.fromkeys(r["parameter"] for r in sensitivities))
    positions = np.arange(len(labels))
    for factor, color in [(0.8, TEAL), (1.2, ORANGE)]:
        values = [next(r["QP_change_percent"] for r in sensitivities if r["parameter"] == label and r["factor"] == factor) for label in labels]
        ax.barh(positions + (-0.16 if factor == 0.8 else 0.16), values, height=0.3, color=color, label=f"{(factor-1)*100:+.0f}% input")
    ax.set_yticks(positions, labels)
    ax.axvline(0, color=INK, lw=0.7)
    ax.set_xlabel("Change in net CS productivity [%]")
    ax.legend(loc="lower right", fontsize=9)
    save_figure(fig, "sensitivity")


def main() -> None:
    for path in (DATA, FIGURES):
        path.mkdir(parents=True, exist_ok=True)
    p, d = Parameters(), Design()
    cases, results, checks, time_rows = {}, [], [], []
    for model in ("Haldane inhibition", "Monod comparator"):
        for strategy in ("CF", "CM", "LM", "CS"):
            a, stop = simulate(model, strategy, p, d)
            cases[(model, strategy)] = a, stop
            m = metrics(model, strategy, a, stop, p, d)
            results.append(m)
            finer, _ = simulate(model, strategy, p, replace(d, dt=d.dt / 2))
            error = abs(finer["P_U_mL"][-1] - a["P_U_mL"][-1]) / finer["P_U_mL"][-1]
            f_integral = float(np.trapezoid(a["methanol_feed_g_h"], a["time_h"]))
            qs_integral = float(np.trapezoid(a["qS_g_g_h"] * a["biomass_g"], a["time_h"]))
            substrate_error = a["substrate_g"][-1] - a["substrate_g"][0] - f_integral + qs_integral
            qp_integral = float(np.trapezoid(a["qP_U_g_h"] * a["biomass_g"], a["time_h"]))
            product_error = abs(qp_integral - m["net_activity_U"]) / m["net_activity_U"]
            checks.append({"model": model, "strategy": strategy, "step_halving_relative_P_error": float(error),
                           "substrate_integral_residual_g": float(substrate_error),
                           "product_integral_relative_error": float(product_error)})
            if error > 1e-5 or abs(substrate_error) > 0.01 or product_error > 1e-4:
                raise AssertionError(checks[-1])
            for i in range(len(a["time_h"])):
                time_rows.append({"model": model, "strategy": strategy, **{key: float(value[i]) for key, value in a.items()}})
    scan = []
    for model in ("Haldane inhibition", "Monod comparator"):
        for setpoint in np.round(np.arange(0.5, 5.001, 0.1), 2):
            modified = replace(d, cs_target=float(setpoint))
            a, stop = exact_cs(model, p, modified)
            scan.append({"setpoint_g_L": float(setpoint), **metrics(model, "CS", a, stop, p, modified)})
    base = next(r for r in results if r["model"] == "Haldane inhibition" and r["strategy"] == "CS")
    a_cs, _ = cases[("Haldane inhibition", "CS")]
    exact, _ = exact_cs("Haldane inhibition", p, d)
    exact_error = abs(exact["P_U_mL"][-1] - base["P_U_mL"]) / base["P_U_mL"]
    if exact_error > 1e-7 or np.max(np.abs(a_cs["S_g_L"] - d.cs_target)) > 1e-8:
        raise AssertionError("Exact CS solution or setpoint invariant failed")
    feasible_scan = [r for r in scan if r["model"] == "Haldane inhibition" and r["oxygen_feasible_with_allowance"]]
    best = max(feasible_scan, key=lambda r: r["QP_U_L_h"])
    best_monod = max((r for r in scan if r["model"] == "Monod comparator" and r["oxygen_feasible_with_allowance"]), key=lambda r: r["QP_U_L_h"])
    selected_d = replace(d, cs_target=best["setpoint_g_L"])
    selected_a, selected_stop = simulate("Haldane inhibition", "CS", p, selected_d)
    selected_m = metrics("Haldane inhibition", "CS-selected", selected_a, selected_stop, p, selected_d)
    cases[("Haldane inhibition", "CS-selected")] = selected_a, selected_stop
    selected_fine, _ = simulate("Haldane inhibition", "CS", p, replace(selected_d, dt=d.dt / 2))
    selected_exact, _ = exact_cs("Haldane inhibition", p, selected_d)
    selected_step_error = abs(selected_fine["P_U_mL"][-1] - selected_a["P_U_mL"][-1]) / selected_fine["P_U_mL"][-1]
    selected_exact_error = abs(selected_exact["P_U_mL"][-1] - selected_a["P_U_mL"][-1]) / selected_a["P_U_mL"][-1]
    if max(selected_step_error, selected_exact_error) > 1e-7:
        raise AssertionError("Selected CS verification failed")
    for i in range(len(selected_a["time_h"])):
        time_rows.append({"model": "Haldane inhibition", "strategy": "CS-selected", **{key: float(value[i]) for key, value in selected_a.items()}})
    sensitivities = []
    for label, field in [("Growth rate coefficient", "mu_max"), ("Growth inhibition constant", "ki_mu"),
                         ("Product rate coefficient", "qp_max"), ("Product inhibition constant", "ki_qp"),
                         ("Methanol maintenance", "ms_x")]:
        for factor in (0.8, 1.2):
            modified = replace(p, **{field: getattr(p, field) * factor})
            a, stop = exact_cs("Haldane inhibition", modified, selected_d)
            m = metrics("Haldane inhibition", "CS", a, stop, modified, selected_d)
            sensitivities.append({"parameter": label, "field": field, "factor": factor,
                                  "QP_change_percent": 100 * (m["QP_U_L_h"] / selected_m["QP_U_L_h"] - 1),
                                  "P_change_percent": 100 * (m["P_U_mL"] / selected_m["P_U_mL"] - 1),
                                  "oxygen_feasible": m["oxygen_feasible_with_allowance"]})
    feasibility = []
    for kla in (500, 750, 1000, 1250, 1500):
        for oxygen in (0.21, 0.4, 0.6, 0.75, 0.9, 1.0):
            candidate = replace(d, kla=kla, oxygen_fraction=oxygen)
            ratio = gas_capacity(selected_a["V_L"], candidate) / (d.capacity_allowance * selected_a["OUR_mol_L_h"])
            feasibility.append({"kla_h_inv": kla, "inlet_O2_fraction": oxygen,
                                "min_capacity_to_required_ratio": float(np.min(ratio)), "feasible": bool(np.min(ratio) >= 1)})
    costs = budget(selected_a, selected_m, selected_d)
    cost_sensitivity = []
    for recovery in (0.5, 0.7, 0.9):
        for rate_factor in (0.75, 1.0, 1.25):
            cost_sensitivity.append({"activity_recovery": recovery, "all_budget_rate_factor": rate_factor,
                                     "batch_cost_INR": costs["total_INR"] * rate_factor,
                                     "INR_per_million_recovered_U": costs["total_INR"] * rate_factor / (selected_m["activity_U"] * recovery) * 1e6})
    summary = {"software": {"python": sys.version.split()[0], "numpy": np.__version__, "matplotlib": matplotlib.__version__},
               "kinetic_parameter_source": "Ponte Font 2017 thesis, Table 5.1, printed page 103",
               "kinetic_parameters": asdict(p), "design_assumptions": asdict(d), "results": results,
               "verification": checks, "exact_CS_relative_error": exact_error,
               "best_feasible_constant_setpoint": best, "best_feasible_monod_setpoint": best_monod,
               "baseline_CS": base, "selected_CS": selected_m,
               "selected_CS_verification": {"step_halving_relative_error": selected_step_error, "exact_solution_relative_error": selected_exact_error},
               "hardware_initial": hardware(p.volume_0, d), "hardware_harvest": hardware(selected_m["V_L"], d),
               "budget": costs, "capacity_scenarios": feasibility, "cost_sensitivity": cost_sensitivity}
    if summary["hardware_initial"]["upper_blade_immersion_m"] <= 0:
        raise AssertionError("Upper impeller is not submerged at the initial volume")
    for gas in (0.21, 0.75, 1.0):
        candidate = replace(d, oxygen_fraction=gas)
        capacity = float(gas_capacity(2.0, candidate))
        g = candidate.vvm * 60.0 / (0.083144626 * candidate.gas_temperature)
        c = candidate.air_solubility / 0.21
        delta_in = c * gas - candidate.do_fraction_air * candidate.air_solubility
        delta_out = delta_in - c * capacity / g
        log_mean = (delta_in - delta_out) / math.log(delta_in / delta_out)
        if not math.isclose(capacity, candidate.kla * log_mean, rel_tol=1e-10):
            raise AssertionError("Integrated gas balance failed its independent log-mean check")
        needed = required_kla(selected_m["max_OUR_mol_L_h"], candidate)
        restored = float(gas_capacity(2.0, replace(candidate, kla=needed)))
        if not math.isclose(restored, d.capacity_allowance * selected_m["max_OUR_mol_L_h"], rel_tol=1e-10):
            raise AssertionError("Required kLa does not supply the specified allowance")
    for name, rows in [("summary_metrics", results), ("simulation_timeseries", time_rows),
                       ("numerical_checks", checks), ("setpoint_scan", scan), ("parameter_sensitivity", sensitivities),
                       ("oxygen_feasibility", feasibility), ("batch_budget", costs["rows"]), ("cost_sensitivity", cost_sensitivity)]:
        write_csv(DATA / f"{name}.csv", rows)
    (DATA / "design_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report_numbers(summary)
    figures(cases, results, scan, sensitivities, p, d)
    for row in results:
        print(f"{row['model']:20} {row['strategy']} t={row['time_h']:.3f} h V={row['V_L']:.4f} L P={row['P_U_mL']:.3f} U/mL QP={row['QP_U_L_h']:.1f} OUR={row['max_OUR_mol_h']:.4f} mol/h")
    print("Best feasible CS setpoint:", best["setpoint_g_L"], "g/L; productivity", round(best["QP_U_L_h"], 2))
    print("Batch budget INR:", round(costs["total_INR"], 2))
    print("Maximum step-halving relative error:", max(c["step_halving_relative_P_error"] for c in checks))


if __name__ == "__main__":
    main()
