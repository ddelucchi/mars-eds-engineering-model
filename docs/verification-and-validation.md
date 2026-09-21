# Verification and validation status

## What is verified in this repository

The automated test suite checks software-level invariants and basic analytical
behavior:

- particle mass scales as radius cubed;
- the baseline Hamaker sphere-plane term scales linearly with radius;
- the baseline DEP term has the expected sign for a particle more polarizable
  than the surrounding medium;
- modeled lift margin increases with drive voltage;
- the analytical required-voltage solution is finite for the baseline case;
- invalid physical inputs are rejected.

CI runs the tests and static lint checks on Python 3.10, 3.11, and 3.12.

## What is not yet validated

The model has **not** been validated against a dedicated Mars-chamber EDS test
article. In particular, this repository does not currently establish:

- absolute dust-clearing efficiency;
- electrical-breakdown margin in low-pressure CO2;
- field enhancement at electrode edges;
- dielectric lifetime or flashover resistance;
- actual particle charge distributions;
- dynamic traveling-wave transport velocity;
- long-duration dust loading, abrasion, or contamination behavior;
- flight-qualified high-voltage electronics performance.

## Validation ladder

A defensible path from screening model to engineering model is:

1. Reproduce published reference trends for electrode geometry and drive.
2. Replace the lumped field closure with a 2-D electrostatic field solution.
3. Perform uncertainty/sensitivity sweeps over adhesion and charge parameters.
4. Compare predicted lift threshold with Mars-pressure chamber measurements.
5. Add measured high-voltage waveforms and dielectric-loss parameters.
6. Validate particle transport and clearing efficiency across dust size bins.
7. Freeze a model version only after configuration-controlled test correlation.

Until those steps exist, outputs should be described as **concept-level
engineering estimates** or **screening calculations**, not validated hardware
performance.
