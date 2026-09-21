"""Run the documented baseline sweep and optionally save a plot."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .config import load_config
from .model import (
    Particle,
    force_budget,
    maximum_vdw_scale_for_ejection,
    required_peak_voltage,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/baseline.json"),
        help="JSON baseline configuration",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/baseline_voltage_sweep.png"),
        help="output figure path",
    )
    args = parser.parse_args()

    env, baseline_particle, geometry, drive = load_config(args.config)
    radii = np.logspace(-7, -5, 120)
    diam_um = 2.0 * radii * 1e6
    v_req = np.array(
        [
            required_peak_voltage(
                Particle(
                    radius_m=r,
                    density_kg_m3=baseline_particle.density_kg_m3,
                    relative_permittivity=baseline_particle.relative_permittivity,
                    hamaker_constant_j=baseline_particle.hamaker_constant_j,
                    separation_m=baseline_particle.separation_m,
                    surface_charge_fraction=baseline_particle.surface_charge_fraction,
                    charge_reference_field_v_m=(
                        baseline_particle.charge_reference_field_v_m
                    ),
                    effective_vdw_scale=baseline_particle.effective_vdw_scale,
                ),
                geometry,
                env,
            )
            for r in radii
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.loglog(diam_um, v_req, label="screening balance voltage")
    ax.axhline(
        drive.peak_voltage_v,
        linestyle="--",
        label=f"concept baseline ({drive.peak_voltage_v / 1000:.1f} kV peak)",
    )
    ax.set_xlabel("Particle diameter [um]")
    ax.set_ylabel("Peak voltage [V]")
    ax.set_title("Mars EDS low-order force-balance screening")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(args.output, dpi=180)
    plt.close(fig)

    budget = force_budget(baseline_particle, drive, geometry, env)
    print("Configured baseline particle force budget")
    for name, value in budget.items():
        print(f"{name:>20}: {value:.6e}")
    max_scale = maximum_vdw_scale_for_ejection(
        baseline_particle, drive, geometry, env
    )
    print(f"{'max_vdw_scale':>20}: {max_scale:.6e}")
    print(
        "\nNOTE: max_vdw_scale is the largest fraction of the ideal "
        "smooth-contact Hamaker adhesion compatible with static lift at the "
        "configured drive. It is a design/sensitivity requirement, not a "
        "fitted material value."
    )
    print(
        "Balance voltage is an unvalidated screening result, not a safe "
        "hardware voltage. See docs/verification-and-validation.md."
    )


if __name__ == "__main__":
    main()
