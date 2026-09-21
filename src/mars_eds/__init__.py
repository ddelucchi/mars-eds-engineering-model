"""Mars EDS engineering analysis package."""

from .model import (
    Drive,
    ElectrodeGeometry,
    MarsEnvironment,
    Particle,
    ejection_margin,
    force_budget,
    required_peak_voltage,
)

__all__ = [
    "Drive",
    "ElectrodeGeometry",
    "MarsEnvironment",
    "Particle",
    "ejection_margin",
    "force_budget",
    "required_peak_voltage",
]

__version__ = "0.1.0"
