"""Project 4: startup behavior of a first-order continuous stirred-tank reactor."""

from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cheme-matplotlib-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parent / "results" / "project_4_cstr"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    k, residence_s, inlet, initial = 0.1, 10.0, 1.0, 0.0
    time_s = np.linspace(0, 100, 1001)

    def balance(_time: float, concentration: np.ndarray) -> np.ndarray:
        return (inlet - concentration) / residence_s - k * concentration

    solution = solve_ivp(balance, (0, 100), [initial], t_eval=time_s, rtol=1e-9, atol=1e-11)
    if not solution.success:
        raise RuntimeError(solution.message)
    concentration = solution.y[0]
    steady_state = inlet / (1 + k * residence_s)

    with (ROOT / "project_4_cstr_data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["time_s", "outlet_concentration_mol_L"])
        writer.writerows(zip(time_s, concentration))

    fig, ax = plt.subplots(figsize=(8.4, 5))
    ax.plot(time_s, concentration, color="#2A9D8F", linewidth=2.8, label="Numerical solution")
    ax.axhline(steady_state, color="#E76F51", linestyle="--", linewidth=2,
               label=f"Steady state = {steady_state:.3f} mol/L")
    ax.set(title="CSTR Startup Behavior", xlabel="Time (s)", ylabel="Outlet concentration (mol/L)")
    ax.grid(True, alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(ROOT / "project_4_cstr_plot.png", dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Steady-state concentration: {steady_state:.3f} mol/L")
    print(f"Saved results to {ROOT}")


if __name__ == "__main__":
    main()


