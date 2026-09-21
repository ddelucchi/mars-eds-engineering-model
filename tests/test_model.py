import math

import pytest

from mars_eds.model import (
    Drive,
    Particle,
    dep_force,
    ejection_margin,
    maximum_vdw_scale_for_ejection,
    particle_mass,
    required_peak_voltage,
    van_der_waals_force,
)


def test_mass_scales_with_radius_cubed() -> None:
    m1 = particle_mass(Particle(radius_m=1e-6))
    m2 = particle_mass(Particle(radius_m=2e-6))
    assert m2 / m1 == pytest.approx(8.0)


def test_vdw_scales_linearly_with_radius() -> None:
    f1 = van_der_waals_force(Particle(radius_m=1e-6))
    f2 = van_der_waals_force(Particle(radius_m=2e-6))
    assert f2 / f1 == pytest.approx(2.0)


def test_dep_force_is_positive_for_basaltic_particle() -> None:
    assert dep_force(Particle(radius_m=1e-6), Drive(peak_voltage_v=1000.0)) > 0


def test_margin_increases_with_voltage() -> None:
    p = Particle(radius_m=1e-6)
    low = ejection_margin(p, Drive(peak_voltage_v=500.0))
    high = ejection_margin(p, Drive(peak_voltage_v=1500.0))
    assert high > low


def test_required_voltage_is_finite_and_positive() -> None:
    v = required_peak_voltage(Particle(radius_m=1e-6))
    assert math.isfinite(v)
    assert v > 0


def test_invalid_radius_rejected() -> None:
    with pytest.raises(ValueError):
        particle_mass(Particle(radius_m=0.0))


def test_effective_vdw_scale_reduces_adhesion_explicitly() -> None:
    full = van_der_waals_force(
        Particle(radius_m=1e-6, effective_vdw_scale=1.0)
    )
    tenth = van_der_waals_force(
        Particle(radius_m=1e-6, effective_vdw_scale=0.1)
    )
    assert tenth / full == pytest.approx(0.1)


def test_baseline_reports_contact_reduction_requirement() -> None:
    particle = Particle(radius_m=0.75e-6)
    scale = maximum_vdw_scale_for_ejection(
        particle, Drive(peak_voltage_v=1500.0)
    )
    assert 0.0 < scale < 1.0


def test_invalid_vdw_scale_rejected() -> None:
    with pytest.raises(ValueError):
        van_der_waals_force(
            Particle(radius_m=1e-6, effective_vdw_scale=1.1)
        )
