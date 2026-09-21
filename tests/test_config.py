import json

from mars_eds.config import load_config


def test_load_config(tmp_path) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(
            {
                "environment": {
                    "gravity_m_s2": 3.71,
                    "pressure_pa": 600.0,
                    "temperature_k": 210.0,
                    "relative_permittivity": 1.0009,
                },
                "particle": {
                    "diameter_um": 2.0,
                    "density_kg_m3": 2900.0,
                    "relative_permittivity": 4.5,
                    "hamaker_constant_j": 6.5e-20,
                    "separation_m": 4e-10,
                    "surface_charge_fraction": 0.25,
                    "charge_reference_field_v_m": 25000.0,
                },
                "geometry": {
                    "electrode_width_um": 100.0,
                    "electrode_spacing_um": 400.0,
                    "spatial_period_mm": 1.0,
                    "field_length_scale_um": 400.0,
                    "phases": 3,
                },
                "drive": {"peak_voltage_v": 1500.0, "frequency_hz": 25.0},
            }
        ),
        encoding="utf-8",
    )
    env, particle, geometry, drive = load_config(path)
    assert env.gravity_m_s2 == 3.71
    assert particle.radius_m == 1e-6
    assert geometry.phases == 3
    assert drive.frequency_hz == 25.0
