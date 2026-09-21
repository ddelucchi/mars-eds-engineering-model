# Mars EDS Engineering Model

[![CI](https://github.com/ddelucchi/mars-eds-engineering-model/actions/workflows/ci.yml/badge.svg)](https://github.com/ddelucchi/mars-eds-engineering-model/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-concept--level%20engineering%20model-orange)

An auditable, low-order engineering model of a **Mars-adapted electrodynamic
dust shield (EDS)**. The repository couples dust adhesion, gravity, an
electrostatic charge proxy, dielectrophoretic forcing, electrode/drive design
parameters, and particle-size sweeps to examine when modeled electric lift can
exceed modeled retention.

The emphasis is **engineering traceability**: assumptions are explicit,
equations are documented, uncertain inputs are configurable, and the limits of
the model are stated alongside the outputs.

> **Scope:** concept-level analysis and trade-study support. This is not NASA
> software, is not flight-qualified, does not establish a technology readiness
> level, and has not been validated as a predictor of absolute dust-clearing
> efficiency or low-pressure electrical-breakdown margin.

## What this model answers

- How do gravity and van der Waals adhesion scale with particle size?
- How do the Coulomb and dielectrophoretic terms scale with voltage and a
  characteristic electrode-field length?
- For a stated set of assumptions, what peak-voltage scale balances the modeled
  retention forces?
- Which parameters dominate the ejection margin and therefore deserve better
  measurement or higher-fidelity modeling?
- Where does the current low-order model stop being adequate?

It does **not** answer whether a particular high-voltage design is discharge
safe in low-pressure CO2, what clearing efficiency a fabricated shield will
achieve, or whether a specific dielectric/electrode stack is flight ready.

## Concept baseline

The project baseline is a three-phase traveling-wave EDS with project-level
design inputs of **100 um electrode width, 400 um spacing, 1 mm spatial
periodicity, 1.5 kV peak (3 kVpp), and ~25 Hz**. These are configurable inputs,
not claims of optimality.

NASA EDS research has demonstrated the technology heritage relevant to this
model: patterned electrodes create non-uniform electric fields that can lift
and transport dust through electrostatic and dielectrophoretic forces, while
Mars applications must explicitly contend with low-pressure electrical
breakdown.

## Model architecture

| Layer | Current treatment | Engineering boundary |
|---|---|---|
| Mars environment | gravity + documented pressure/temperature context | no atmospheric/plasma solver |
| particle | spherical radius, density, permittivity | no irregular-shape/contact distribution |
| adhesion | Hamaker sphere-plane vdW term | no full JKR/DMT/roughness model |
| charge | bounded surface-charge proxy | no triboelectric/plasma charging dynamics |
| electric field | `E ~ V/L` scale | no FEM electrode field map yet |
| DEP | dipole expression with `grad(E^2) ~ E^2/L` | screening approximation |
| ejection | lift > retention | static threshold, not clearing efficiency |
| breakdown | documented as a constraint | not solved or certified here |

The governing equations and their limitations are in
[`docs/physics-model.md`](docs/physics-model.md).

## Quick start

```bash
git clone https://github.com/ddelucchi/mars-eds-engineering-model.git
cd mars-eds-engineering-model
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
mars-eds-baseline
```

The default run reads `configs/baseline.json`, so every headline parameter is
visible in one reviewable file instead of being buried in source code.

The baseline command prints a force budget for a 1.5 um particle and writes a
particle-size voltage sweep to `results/baseline_voltage_sweep.png`.

## Programmatic use

```python
from mars_eds import Drive, Particle, force_budget, required_peak_voltage

particle = Particle(radius_m=0.75e-6)
budget = force_budget(particle, Drive(peak_voltage_v=1500.0))
required_v = required_peak_voltage(particle)

print(budget["lift_to_retention"])
print(required_v)
```

Every returned force is in SI units.

## Verification status

Automated tests verify analytical scaling and software behavior on Python
3.10-3.12. They do **not** constitute physical validation.

See [`docs/verification-and-validation.md`](docs/verification-and-validation.md)
for the explicit verification boundary and a proposed validation ladder from
screening model to chamber-correlated engineering model.

## Repository map

```text
.
├── src/mars_eds/                  supported model
│   ├── model.py                   force budget + voltage solution
│   ├── config.py                  typed baseline loader
│   └── baseline.py                reproducible baseline sweep
├── configs/baseline.json          reviewable concept baseline
├── tests/                         analytical/software checks
├── docs/
│   ├── physics-model.md           equations and approximations
│   ├── assumptions.md             parameter provenance
│   ├── literature-benchmark.md    published guardrails vs concept baseline
│   ├── verification-and-validation.md
│   └── references.md
├── assets/legacy-renders/         preserved figures from the original workspace
└── archive/original-simulations/  preserved exploratory source programs
```

## Legacy material

The original project workspace contained broader exploratory scripts, including
a generic hybrid dust-mitigation model and a large multipurpose particle
dynamics program. Those files are preserved under `archive/` for provenance but
are intentionally excluded from the supported package and CI.

This separation prevents historical experiments from being mistaken for the
current Mars EDS engineering model.

## Technical heritage

The repository is informed by NASA Kennedy Space Center EDS literature,
including numerical/analytical Mars EDS work, active dust-control research,
and current NASA descriptions of EDS as a patterned-electrode technology for
dust removal on planetary surfaces.

See [`docs/literature-benchmark.md`](docs/literature-benchmark.md) for the
published Mars guardrails and [`docs/references.md`](docs/references.md) for
the primary NASA sources.

## Project context

The model grew from electrodynamic-dust-mitigation work performed in the
NASA-funded L'SPACE Proposal Writing & Evaluation Experience (NPWEE)
environment. This repository is an independent engineering reconstruction and
software artifact. It should not be interpreted as NASA-authored software or
as evidence of NASA certification, endorsement, or employment.

## Next fidelity upgrades

The highest-value technical upgrades are:

1. replace the lumped `E ~ V/L` field closure with a 2-D electrostatic field
   solution for the electrode/dielectric geometry;
2. add parameter uncertainty propagation for adhesion and particle charge;
3. implement a CO2 discharge/breakdown model with clearly sourced coefficients;
4. correlate lift thresholds with Mars-pressure chamber data;
5. add time-domain traveling-wave particle transport after the static threshold
   is validated.

Those upgrades are deliberately listed as future work rather than implied as
features already present.
