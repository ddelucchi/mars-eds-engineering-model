"""Transparent, low-order engineering model for a Mars electrodynamic dust shield.

The model is intentionally compact and auditable. It combines gravity, van der
Waals adhesion, an estimated Coulomb term, and a dipole/DEP term. It is useful
for screening trends and sensitivity studies, not for certifying hardware.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt

EPSILON_0 = 8.854_187_8128e-12


@dataclass(frozen=True)
class MarsEnvironment:
    """Environmental assumptions used by the screening model."""

    gravity_m_s2: float = 3.71
    pressure_pa: float = 600.0
    temperature_k: float = 210.0
    relative_permittivity: float = 1.0009


@dataclass(frozen=True)
class Particle:
    """Spherical dust-particle approximation."""

    radius_m: float
    density_kg_m3: float = 2900.0
    relative_permittivity: float = 4.5
    hamaker_constant_j: float = 6.5e-20
    separation_m: float = 0.4e-9
    surface_charge_fraction: float = 0.25
    charge_reference_field_v_m: float = 25_000.0


@dataclass(frozen=True)
class ElectrodeGeometry:
    """Concept-level three-phase EDS geometry.

    Width, spacing, and period are independent design parameters here; this
    model does not solve the detailed electrode boundary-value problem.
    """

    electrode_width_m: float = 100e-6
    electrode_spacing_m: float = 400e-6
    spatial_period_m: float = 1.0e-3
    field_length_scale_m: float = 400e-6
    phases: int = 3


@dataclass(frozen=True)
class Drive:
    """Concept-level electrical drive assumptions."""

    peak_voltage_v: float = 1500.0
    frequency_hz: float = 25.0


def _require_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive; got {value!r}")


def particle_mass(particle: Particle) -> float:
    _require_positive("particle.radius_m", particle.radius_m)
    _require_positive("particle.density_kg_m3", particle.density_kg_m3)
    return (4.0 / 3.0) * pi * particle.radius_m**3 * particle.density_kg_m3


def gravity_force(particle: Particle, env: MarsEnvironment = MarsEnvironment()) -> float:
    _require_positive("env.gravity_m_s2", env.gravity_m_s2)
    return particle_mass(particle) * env.gravity_m_s2


def van_der_waals_force(particle: Particle) -> float:
    """Sphere-plane Hamaker approximation: F = A R / (6 z^2)."""

    _require_positive("particle.hamaker_constant_j", particle.hamaker_constant_j)
    _require_positive("particle.separation_m", particle.separation_m)
    return (
        particle.hamaker_constant_j
        * particle.radius_m
        / (6.0 * particle.separation_m**2)
    )


def estimated_particle_charge(
    particle: Particle, env: MarsEnvironment = MarsEnvironment()
) -> float:
    """Estimate charge from a bounded surface-charge-density proxy.

    sigma_ref = eps_0 * eps_r * E_ref and q = 4*pi*R^2*sigma_ref*f_charge.

    This is a sensitivity parameterization, not a charge-transport model.
    """

    if not 0.0 <= particle.surface_charge_fraction <= 1.0:
        raise ValueError("surface_charge_fraction must be between 0 and 1")
    _require_positive(
        "particle.charge_reference_field_v_m", particle.charge_reference_field_v_m
    )
    sigma_ref = (
        EPSILON_0
        * env.relative_permittivity
        * particle.charge_reference_field_v_m
    )
    return (
        4.0
        * pi
        * particle.radius_m**2
        * sigma_ref
        * particle.surface_charge_fraction
    )


def field_scale(
    drive: Drive, geometry: ElectrodeGeometry = ElectrodeGeometry()
) -> float:
    """Voltage-to-field scale E ~ V/L for first-order trade studies."""

    _require_positive("drive.peak_voltage_v", drive.peak_voltage_v)
    _require_positive("geometry.field_length_scale_m", geometry.field_length_scale_m)
    return drive.peak_voltage_v / geometry.field_length_scale_m


def coulomb_force(
    particle: Particle,
    drive: Drive,
    geometry: ElectrodeGeometry = ElectrodeGeometry(),
    env: MarsEnvironment = MarsEnvironment(),
) -> float:
    return estimated_particle_charge(particle, env) * field_scale(drive, geometry)


def clausius_mossotti_factor(
    particle: Particle, env: MarsEnvironment = MarsEnvironment()
) -> float:
    ep = particle.relative_permittivity
    em = env.relative_permittivity
    denominator = ep + 2.0 * em
    if denominator == 0:
        raise ValueError("invalid permittivity combination")
    return (ep - em) / denominator


def dep_force(
    particle: Particle,
    drive: Drive,
    geometry: ElectrodeGeometry = ElectrodeGeometry(),
    env: MarsEnvironment = MarsEnvironment(),
) -> float:
    """Lumped dielectrophoretic force.

    Uses F_DEP ~= 2*pi*eps_m*R^3*K*grad(E^2), with grad(E^2) approximated as
    E^2/L. The detailed field map should replace this approximation when FEM or
    measured electrode-field data are available.
    """

    e_field = field_scale(drive, geometry)
    grad_e2 = e_field**2 / geometry.field_length_scale_m
    eps_m = EPSILON_0 * env.relative_permittivity
    return (
        2.0
        * pi
        * eps_m
        * particle.radius_m**3
        * clausius_mossotti_factor(particle, env)
        * grad_e2
    )


def force_budget(
    particle: Particle,
    drive: Drive = Drive(),
    geometry: ElectrodeGeometry = ElectrodeGeometry(),
    env: MarsEnvironment = MarsEnvironment(),
) -> dict[str, float]:
    """Return an auditable lift/retention force budget in newtons."""

    f_c = coulomb_force(particle, drive, geometry, env)
    f_dep = dep_force(particle, drive, geometry, env)
    f_vdw = van_der_waals_force(particle)
    f_g = gravity_force(particle, env)
    lift = f_c + f_dep
    retention = f_vdw + f_g
    return {
        "coulomb_n": f_c,
        "dep_n": f_dep,
        "vdw_n": f_vdw,
        "gravity_n": f_g,
        "lift_n": lift,
        "retention_n": retention,
        "margin_n": lift - retention,
        "lift_to_retention": lift / retention,
    }


def ejection_margin(
    particle: Particle,
    drive: Drive = Drive(),
    geometry: ElectrodeGeometry = ElectrodeGeometry(),
    env: MarsEnvironment = MarsEnvironment(),
) -> float:
    """Positive means modeled lift exceeds modeled retention."""

    return force_budget(particle, drive, geometry, env)["margin_n"]


def required_peak_voltage(
    particle: Particle,
    geometry: ElectrodeGeometry = ElectrodeGeometry(),
    env: MarsEnvironment = MarsEnvironment(),
) -> float:
    """Solve the low-order force balance for the positive voltage root.

    With E=V/L, the modeled lift has the form a*V + b*V^2.
    """

    _require_positive("geometry.field_length_scale_m", geometry.field_length_scale_m)
    retention = van_der_waals_force(particle) + gravity_force(particle, env)

    q = estimated_particle_charge(particle, env)
    length = geometry.field_length_scale_m
    a = q / length

    eps_m = EPSILON_0 * env.relative_permittivity
    k_cm = clausius_mossotti_factor(particle, env)
    b = 2.0 * pi * eps_m * particle.radius_m**3 * k_cm / length**3

    if b > 0:
        discriminant = a * a + 4.0 * b * retention
        return (-a + sqrt(discriminant)) / (2.0 * b)
    if a > 0:
        return retention / a
    return float("inf")
