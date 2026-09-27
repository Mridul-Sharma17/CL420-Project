"""Four-state fed-batch simulation for the CL 420 mid-term project.

The inhibition branch reproduces the model structure and parameter set reported
by Ponte et al. for recombinant Rhizopus oryzae lipase production by Pichia
pastoris under methanol induction. The Monod branch is a controlled comparator
that keeps qmax and KS unchanged and removes the inhibition term.

States are culture volume V, biomass amount XV, methanol amount SV, and total
ROL activity PV. Oxygen demand is calculated from the published oxygen uptake
relationship and is not included as a fifth dynamic state.

Units
-----
V       L
XV      g
SV      g methanol
PV      U ROL
mu      h^-1
qP      U g^-1 h^-1
qS      g g^-1 h^-1
qO2     mol O2 g^-1 h^-1
feed    g methanol h^-1
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "report" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class Parameters:
    """Published parameters and process limits from Ponte et al."""

    mu_max: float = 0.069
    ks_mu: float = 0.50
    ki_mu: float = 7.5
    qp_max: float = 2200.0
    ks_qp: float = 10.0
    ki_qp: float = 1.2
    ys_x: float = 5.14
    ms_x: float = 0.013
    yo2_x: float = 0.206
    mo2_x: float = 6.1e-4
    rho_methanol: float = 792.0
    volume_0: float = 2.0
    biomass_0: float = 27.0
    methanol_0: float = 1.0
    product_0: float = 50.0
    x_max: float = 55.0
    volume_max: float = 5.0
    methanol_max: float = 10.0


@dataclass(frozen=True)
class SimulationConfig:
    dt: float = 0.01
    t_end: float = 120.0
    constant_substrate_gain: float = 4.0


@dataclass
class Trajectory:
    model: str
    strategy: str
    data: dict[str, np.ndarray]
    stop_reason: str


def h_function(substrate: float, ks: float, ki: float) -> float:
    """Haldane substrate function used in the reference model."""

    s = max(0.0, substrate)
    return s / (ks + s + s * s / ki)


def monod_function(substrate: float, ks: float) -> float:
    """Monod substrate function used for the controlled comparator."""

    s = max(0.0, substrate)
    return s / (ks + s)


def specific_rates(model: str, substrate: float, p: Parameters) -> tuple[float, float]:
    """Return specific growth and product rates for one model branch."""

    if model == "Haldane inhibition":
        mu = p.mu_max * h_function(substrate, p.ks_mu, p.ki_mu)
        qp = p.qp_max * h_function(substrate, p.ks_qp, p.ki_qp)
    elif model == "Monod comparator":
        mu = p.mu_max * monod_function(substrate, p.ks_mu)
        qp = p.qp_max * monod_function(substrate, p.ks_qp)
    else:
        raise ValueError(f"Unknown model: {model}")
    return mu, qp


def q_substrate(mu: float, p: Parameters) -> float:
    """Specific methanol uptake from the published yield and maintenance law."""

    return p.ys_x * mu + p.ms_x


def q_oxygen(mu: float, p: Parameters) -> float:
    """Specific oxygen uptake from the published yield and maintenance law."""

    return p.yo2_x * mu + p.mo2_x


def feed_mass_rate(
    t: float,
    state: np.ndarray,
    model: str,
    strategy: str,
    p: Parameters,
    config: SimulationConfig,
) -> float:
    """Return methanol feed in g h^-1 for a reported standard strategy.

    CM and LM use the paper's open-loop biomass-based feed relation. CS uses
    the exact algebraic feed needed to hold S at the paper's 2 g L^-1 target,
    with a proportional correction only if numerical drift occurs. The paper
    reports the controller form but not its tuned gains, so this transparent
    setpoint implementation avoids inventing them.
    """

    volume, biomass_amount, substrate_amount, _ = state
    volume = max(volume, 1.0e-12)
    biomass_amount = max(biomass_amount, 0.0)
    substrate = max(substrate_amount / volume, 0.0)

    if strategy == "CF":
        return 14.0

    if strategy == "CM":
        target_mu = 0.03
        return max(0.0, q_substrate(target_mu, p) * biomass_amount)

    if strategy == "LM":
        target_mu = 0.01 + (0.04 - 0.01) * min(max(t / config.t_end, 0.0), 1.0)
        return max(0.0, q_substrate(target_mu, p) * biomass_amount)

    if strategy == "CS":
        target_s = 2.0
        mu, _ = specific_rates(model, target_s, p)
        uptake = q_substrate(mu, p) * biomass_amount
        correction = config.constant_substrate_gain * volume * (target_s - substrate)
        dilution_denominator = 1.0 - substrate / p.rho_methanol
        return max(0.0, (uptake + correction) / dilution_denominator)

    raise ValueError(f"Unknown strategy: {strategy}")


def state_properties(
    t: float,
    state: np.ndarray,
    model: str,
    strategy: str,
    p: Parameters,
    config: SimulationConfig,
) -> dict[str, float]:
    """Calculate concentrations, rates, feed, and oxygen demand."""

    volume, biomass_amount, substrate_amount, product_amount = state
    volume = max(volume, 1.0e-12)
    biomass_amount = max(biomass_amount, 0.0)
    substrate_amount = max(substrate_amount, 0.0)
    product_amount = max(product_amount, 0.0)
    biomass = biomass_amount / volume
    substrate = substrate_amount / volume
    product = product_amount / volume / 1000.0
    mu, qp = specific_rates(model, substrate, p)
    qs = q_substrate(mu, p)
    qo2 = q_oxygen(mu, p)
    feed = feed_mass_rate(t, state, model, strategy, p, config)
    oxygen_rate = qo2 * biomass_amount
    oxygen_rate_concentration = qo2 * biomass
    return {
        "t": t,
        "V": volume,
        "X": biomass,
        "S": substrate,
        "P": product,
        "mu": mu,
        "qP": qp,
        "qS": qs,
        "qO2": qo2,
        "feed": feed,
        "OUR_total": oxygen_rate,
        "OUR_vol": oxygen_rate_concentration,
    }


def rhs(
    t: float,
    state: np.ndarray,
    model: str,
    strategy: str,
    p: Parameters,
    config: SimulationConfig,
) -> np.ndarray:
    """Four-state fed-batch balances in amount form."""

    props = state_properties(t, state, model, strategy, p, config)
    biomass_amount = max(state[1], 0.0)
    feed = props["feed"]
    d_volume = feed / p.rho_methanol
    d_biomass_amount = props["mu"] * biomass_amount
    d_substrate_amount = feed - props["qS"] * biomass_amount
    d_product_amount = props["qP"] * biomass_amount
    return np.array(
        [d_volume, d_biomass_amount, d_substrate_amount, d_product_amount],
        dtype=float,
    )


def rk4_step(
    rhs_function: Callable[[float, np.ndarray], np.ndarray],
    t: float,
    state: np.ndarray,
    dt: float,
) -> np.ndarray:
    """One classical fourth-order Runge Kutta step."""

    k1 = rhs_function(t, state)
    k2 = rhs_function(t + dt / 2.0, state + dt * k1 / 2.0)
    k3 = rhs_function(t + dt / 2.0, state + dt * k2 / 2.0)
    k4 = rhs_function(t + dt, state + dt * k3)
    return state + dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0


def simulate(
    model: str,
    strategy: str,
    p: Parameters | None = None,
    config: SimulationConfig | None = None,
) -> Trajectory:
    """Simulate one model and one feed strategy until a process limit is met."""

    p = p or Parameters()
    config = config or SimulationConfig()
    initial_substrate = 2.0 if strategy == "CS" else p.methanol_0
    initial_state = np.array(
        [
            p.volume_0,
            p.biomass_0 * p.volume_0,
            initial_substrate * p.volume_0,
            p.product_0 * 1000.0 * p.volume_0,
        ],
        dtype=float,
    )

    rows: list[dict[str, float]] = []
    state = initial_state
    t = 0.0
    stop_reason = "time limit"
    max_steps = int(np.ceil(config.t_end / config.dt))
    for _ in range(max_steps + 1):
        props = state_properties(t, state, model, strategy, p, config)
        rows.append(props)

        if props["X"] >= p.x_max:
            stop_reason = "biomass limit X = 55 g/L"
            break
        if props["V"] >= p.volume_max:
            stop_reason = "working volume limit V = 5 L"
            break
        if props["S"] >= p.methanol_max:
            stop_reason = "methanol limit S = 10 g/L"
            break
        if t >= config.t_end:
            break

        step = min(config.dt, config.t_end - t)
        rhs_function = lambda local_t, local_state: rhs(
            local_t, local_state, model, strategy, p, config
        )
        next_state = np.maximum(rk4_step(rhs_function, t, state, step), 0.0)
        next_time = t + step
        next_props = state_properties(next_time, next_state, model, strategy, p, config)
        crossing_fractions: list[float] = []
        for key, limit in (("X", p.x_max), ("V", p.volume_max), ("S", p.methanol_max)):
            current_value = props[key]
            next_value = next_props[key]
            if current_value < limit <= next_value and next_value > current_value:
                crossing_fractions.append((limit - current_value) / (next_value - current_value))
        if crossing_fractions:
            fraction = min(crossing_fractions)
            state = state + fraction * (next_state - state)
            t += fraction * step
        else:
            state = next_state
            t = next_time

    keys = list(rows[0].keys())
    data = {key: np.array([row[key] for row in rows]) for key in keys}
    return Trajectory(model=model, strategy=strategy, data=data, stop_reason=stop_reason)


def trajectory_metrics(trajectory: Trajectory, p: Parameters) -> dict[str, float | str]:
    """Return final performance metrics and the derived oxygen demand."""

    data = trajectory.data
    final_volume = data["V"][-1]
    final_time = data["t"][-1]
    initial_product_amount = p.product_0 * 1000.0 * p.volume_0
    final_product_amount = data["P"][-1] * 1000.0 * final_volume
    delta_product_amount = final_product_amount - initial_product_amount
    volumetric_productivity = delta_product_amount / final_volume / max(final_time, 1.0e-12)
    return {
        "model": trajectory.model,
        "strategy": trajectory.strategy,
        "final_time_h": final_time,
        "final_volume_L": final_volume,
        "final_biomass_g_L": data["X"][-1],
        "final_methanol_g_L": data["S"][-1],
        "final_product_U_mL": data["P"][-1],
        "volumetric_productivity_U_L_h": volumetric_productivity,
        "max_OUR_mol_h": float(np.max(data["OUR_total"])),
        "max_OUR_mol_L_h": float(np.max(data["OUR_vol"])),
        "stop_reason": trajectory.stop_reason,
    }


def save_csv(trajectories: list[Trajectory], p: Parameters) -> None:
    """Write combined time profiles and final metrics for reproducibility."""

    profile_path = FIGURE_DIR / "simulation_timeseries.csv"
    metric_path = FIGURE_DIR / "summary_metrics.csv"
    profile_rows: list[str] = []
    profile_header = [
        "model",
        "strategy",
        "t_h",
        "V_L",
        "X_g_L",
        "S_g_L",
        "P_U_mL",
        "mu_h_inv",
        "qP_U_g_h",
        "qS_g_g_h",
        "qO2_mol_g_h",
        "feed_g_h",
        "OUR_total_mol_h",
        "OUR_vol_mol_L_h",
    ]
    for trajectory in trajectories:
        d = trajectory.data
        for index in range(len(d["t"])):
            values = [
                trajectory.model,
                trajectory.strategy,
                d["t"][index],
                d["V"][index],
                d["X"][index],
                d["S"][index],
                d["P"][index],
                d["mu"][index],
                d["qP"][index],
                d["qS"][index],
                d["qO2"][index],
                d["feed"][index],
                d["OUR_total"][index],
                d["OUR_vol"][index],
            ]
            profile_rows.append(",".join(str(value) for value in values))
    profile_path.write_text(",".join(profile_header) + "\n" + "\n".join(profile_rows) + "\n")

    metric_rows = [trajectory_metrics(trajectory, p) for trajectory in trajectories]
    metric_header = list(metric_rows[0].keys())
    metric_lines = [
        ",".join(metric_header),
        *[
            ",".join(str(row[key]) for key in metric_header)
            for row in metric_rows
        ],
    ]
    metric_path.write_text("\n".join(metric_lines) + "\n")


def plot_kinetic_laws(p: Parameters) -> None:
    """Plot the exact inhibition laws and the Monod comparator."""

    substrate = np.linspace(0.0, 12.0, 600)
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.2), constrained_layout=True)
    for model, color, linestyle in [
        ("Haldane inhibition", "#0b7285", "-"),
        ("Monod comparator", "#d9480f", "--"),
    ]:
        mu = np.array([specific_rates(model, s, p)[0] for s in substrate])
        qp = np.array([specific_rates(model, s, p)[1] for s in substrate])
        axes[0].plot(substrate, mu, color=color, linestyle=linestyle, linewidth=2.2, label=model)
        axes[1].plot(substrate, qp, color=color, linestyle=linestyle, linewidth=2.2, label=model)
    axes[0].axvline(np.sqrt(p.ks_mu * p.ki_mu), color="#868e96", linewidth=1.0, alpha=0.8)
    axes[1].axvline(np.sqrt(p.ks_qp * p.ki_qp), color="#868e96", linewidth=1.0, alpha=0.8)
    axes[0].set(xlabel="Methanol, S [g L$^{-1}$]", ylabel="Specific growth, mu [h$^{-1}$]")
    axes[1].set(xlabel="Methanol, S [g L$^{-1}$]", ylabel="Specific productivity, qP [U g$^{-1}$ h$^{-1}$]")
    for axis in axes:
        axis.grid(alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.savefig(FIGURE_DIR / "kinetic_laws.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def plot_model_comparison(trajectories: list[Trajectory]) -> None:
    """Compare Monod and inhibition branches for CF and CS."""

    chosen = [("CF", 0), ("CS", 1)]
    colors = {"Haldane inhibition": "#0b7285", "Monod comparator": "#d9480f"}
    labels = {"Haldane inhibition": "Haldane inhibition", "Monod comparator": "Monod"}
    fig, axes = plt.subplots(2, 3, figsize=(10.0, 5.8), constrained_layout=True)
    for strategy, row in chosen:
        for trajectory in trajectories:
            if trajectory.strategy != strategy:
                continue
            d = trajectory.data
            style = {"color": colors[trajectory.model], "label": labels[trajectory.model]}
            axes[row, 0].plot(d["t"], d["X"], linewidth=2.0, **style)
            axes[row, 1].plot(d["t"], d["S"], linewidth=2.0, **style)
            axes[row, 2].plot(d["t"], d["P"], linewidth=2.0, **style)
        axes[row, 0].set_ylabel(f"{strategy}\nX [g L$^{{-1}}$]")
        axes[row, 1].set_ylabel("S [g L$^{-1}$]")
        axes[row, 2].set_ylabel("P [U mL$^{-1}$]")
        for col in range(3):
            axes[row, col].grid(alpha=0.22)
            axes[row, col].set_xlabel("Time [h]")
            axes[row, col].legend(frameon=False, fontsize=7)
    axes[0, 0].set_title("Biomass")
    axes[0, 1].set_title("Methanol")
    axes[0, 2].set_title("ROL activity")
    fig.savefig(FIGURE_DIR / "model_comparison.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def plot_strategy_summary(trajectories: list[Trajectory], p: Parameters) -> None:
    """Plot final activity and productivity for all standard strategies."""

    strategies = ["CF", "CM", "LM", "CS"]
    models = ["Haldane inhibition", "Monod comparator"]
    colors = {"Haldane inhibition": "#0b7285", "Monod comparator": "#d9480f"}
    metrics = {
        (trajectory.model, trajectory.strategy): trajectory_metrics(trajectory, p)
        for trajectory in trajectories
    }
    x = np.arange(len(strategies))
    width = 0.36
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.6), constrained_layout=True)
    for offset, model in zip((-width / 2.0, width / 2.0), models):
        product = [metrics[(model, strategy)]["final_product_U_mL"] for strategy in strategies]
        productivity = [
            metrics[(model, strategy)]["volumetric_productivity_U_L_h"]
            for strategy in strategies
        ]
        label = "Haldane inhibition" if model == models[0] else "Monod"
        axes[0].bar(x + offset, product, width, label=label, color=colors[model])
        axes[1].bar(x + offset, productivity, width, label=label, color=colors[model])
    axes[0].set_ylabel("Final P [U mL$^{-1}$]")
    axes[1].set_ylabel("Volumetric productivity [U L$^{-1}$ h$^{-1}$]")
    for axis in axes:
        axis.set_xticks(x, strategies)
        axis.grid(axis="y", alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.savefig(FIGURE_DIR / "strategy_summary.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def plot_oxygen_demand(trajectories: list[Trajectory]) -> None:
    """Plot derived oxygen demand for CF and CS under inhibition kinetics."""

    colors = {"CF": "#5f3dc4", "CS": "#2b8a3e"}
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.4), constrained_layout=True)
    for strategy in ("CF", "CS"):
        trajectory = next(
            item
            for item in trajectories
            if item.model == "Haldane inhibition" and item.strategy == strategy
        )
        d = trajectory.data
        axes[0].plot(d["t"], d["OUR_total"], linewidth=2.1, color=colors[strategy], label=strategy)
        axes[1].plot(d["t"], d["OUR_vol"], linewidth=2.1, color=colors[strategy], label=strategy)
    axes[0].set_ylabel("OUR [mol O$_2$ h$^{-1}$]")
    axes[1].set_ylabel("OUR [mol O$_2$ L$^{-1}$ h$^{-1}$]")
    for axis in axes:
        axis.set_xlabel("Time [h]")
        axis.grid(alpha=0.22)
        axis.legend(frameon=False)
    fig.savefig(FIGURE_DIR / "oxygen_demand.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def convergence_check(p: Parameters) -> float:
    """Compare dt = 0.01 h with dt = 0.005 h for the reference case."""

    coarse = simulate("Haldane inhibition", "CS", p, SimulationConfig(dt=0.01))
    fine = simulate("Haldane inhibition", "CS", p, SimulationConfig(dt=0.005))
    coarse_final = coarse.data["P"][-1]
    fine_final = fine.data["P"][-1]
    return abs(fine_final - coarse_final) / max(abs(fine_final), 1.0)


def main() -> None:
    p = Parameters()
    config = SimulationConfig()
    models = ["Haldane inhibition", "Monod comparator"]
    strategies = ["CF", "CM", "LM", "CS"]
    trajectories = [
        simulate(model, strategy, p, config)
        for model in models
        for strategy in strategies
    ]
    save_csv(trajectories, p)
    plot_kinetic_laws(p)
    plot_model_comparison(trajectories)
    plot_strategy_summary(trajectories, p)
    plot_oxygen_demand(trajectories)

    print("Parameters")
    for key, value in asdict(p).items():
        print(f"  {key}: {value}")
    print("\nResults")
    for trajectory in trajectories:
        metrics = trajectory_metrics(trajectory, p)
        print(
            f"  {trajectory.model:22s} {trajectory.strategy}: "
            f"t={metrics['final_time_h']:.2f} h, "
            f"X={metrics['final_biomass_g_L']:.2f} g/L, "
            f"S={metrics['final_methanol_g_L']:.2f} g/L, "
            f"P={metrics['final_product_U_mL']:.2f} U/mL, "
            f"QP={metrics['volumetric_productivity_U_L_h']:.2f} U/L/h, "
            f"OURmax={metrics['max_OUR_mol_h']:.3f} mol/h, "
            f"stop={metrics['stop_reason']}"
        )
    print(f"\nCS convergence relative difference: {convergence_check(p):.3e}")


if __name__ == "__main__":
    main()
