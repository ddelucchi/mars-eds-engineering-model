"""Load a documented JSON configuration into model dataclasses."""

from __future__ import annotations

import json
from pathlib import Path

from .model import Drive, ElectrodeGeometry, MarsEnvironment, Particle


def load_config(
    path: str | Path,
) -> tuple[MarsEnvironment, Particle, ElectrodeGeometry, Drive]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    env_data = data["environment"]
    p_data = data["particle"]
    g_data = data["geometry"]
    d_data = data["drive"]

    env = MarsEnvironment(**env_data)
    particle = Particle(
        radius_m=float(p_data["diameter_um"]) * 1e-6 / 2.0,
        density_kg_m3=float(p_data["density_kg_m3"]),
        relative_permittivity=float(p_data["relative_permittivity"]),
        hamaker_constant_j=float(p_data["hamaker_constant_j"]),
        separation_m=float(p_data["separation_m"]),
        surface_charge_fraction=float(p_data["surface_charge_fraction"]),
        charge_reference_field_v_m=float(p_data["charge_reference_field_v_m"]),
    )
    geometry = ElectrodeGeometry(
        electrode_width_m=float(g_data["electrode_width_um"]) * 1e-6,
        electrode_spacing_m=float(g_data["electrode_spacing_um"]) * 1e-6,
        spatial_period_m=float(g_data["spatial_period_mm"]) * 1e-3,
        field_length_scale_m=float(g_data["field_length_scale_um"]) * 1e-6,
        phases=int(g_data["phases"]),
    )
    drive = Drive(**d_data)
    return env, particle, geometry, drive
