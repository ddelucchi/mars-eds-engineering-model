# Literature benchmark and design guardrails

This page separates **published EDS observations** from the project's concept
baseline. The distinction matters because a force model can predict lift at a
voltage that a real low-pressure CO2 system cannot safely sustain.

## NASA Mars EDS reference observations

NASA KSC EDS literature reports that:

- EDS uses non-uniform electric fields to act on charged particles through
  electrostatic force and on neutral/polarizable particles through
  dielectrophoresis.
- Three-phase and other multiphase electrode configurations have been studied
  to generate traveling fields.
- Numerical work has used finite-element electric-field solutions as a check on
  analytical field models for parallel electrodes.
- Low-pressure electrical breakdown is a first-order Mars design constraint.
- In one published prototype study at simulated Martian pressure (7 torr CO2),
  breakdown did not occur until the applied-potential amplitude exceeded about
  800 V (about 1.6 kV peak-to-peak for that setup). The same report shows strong
  dependence of transport/removal behavior on electrode width, spacing, and
  drive frequency.

These observations are **not universal limits**. Breakdown voltage depends on
gas pressure/composition, electrode geometry, dielectric stack, surface
condition, waveform, and test configuration.

## Implication for this repository's concept baseline

The project concept baseline of 1.5 kV peak (3 kVpp) at ~25 Hz must therefore
be treated as a **design variable requiring discharge validation**, not a safe
Mars operating point. It should never be presented as validated solely because
it appears in a force-balance calculation.

That is why the supported package keeps breakdown outside the current force
model and explicitly lists a CO2 discharge model and Mars-chamber correlation
as future validation work.

## What would count as a real benchmark

A stronger future model should reproduce published trends for a specific EDS
screen geometry, then compare predicted and measured transport thresholds at
matched:

- CO2 pressure and temperature;
- electrode width and gap;
- dielectric/substrate construction;
- waveform phase and frequency;
- particle material and size distribution.

Only after that matched-configuration comparison should the model be used to
predict a new geometry with quantified uncertainty.
