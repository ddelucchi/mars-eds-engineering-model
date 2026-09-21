# Physics model

This repository is a **screening model**, not a field solver or a flight
qualification model. Its purpose is to make the dominant assumptions and force
terms explicit enough to support trade studies and sensitivity analysis.

## 1. Particle approximation

Dust is represented as a spherical particle of radius `R`, density `rho_p`,
and relative permittivity `eps_r,p`.

`m_p = (4/3) pi R^3 rho_p` and `F_g = m_p g_Mars`.

The spherical approximation is a simplification; irregular Martian dust shape,
roughness, contact geometry, and agglomeration are not resolved.

## 2. Adhesion

The baseline van der Waals term uses a sphere-plane Hamaker approximation,

`F_vdW,ideal = A_H R / (6 z_0^2)`.\n\nThe supported model then exposes an effective-contact factor `s_vdW`,\n\n`F_vdW = s_vdW F_vdW,ideal`, with `0 <= s_vdW <= 1`.

`A_H` is a Hamaker constant and `z_0` is an effective separation. These are
uncertain inputs and should be swept rather than treated as exact material
constants. `s_vdW=1` deliberately preserves the ideal smooth-contact estimate;\nvalues below one represent unresolved reductions in real contact from roughness,\nsurface topology, coatings, or contamination. It is not assigned a favorable\ndefault.

Electrostatic adhesion, surface-roughness distributions, and JKR/DMT-style\ncontact mechanics are not resolved explicitly. Instead, the model can invert\nthe force balance and report the **maximum `s_vdW` compatible with lift** at a\ngiven drive. That output is a design/validation requirement, not a measured\nmaterial property.

## 3. Charge proxy and Coulomb force

A bounded surface-charge-density proxy is used only for sensitivity analysis,

`sigma_ref = eps_0 eps_r,m E_ref`,

`q = 4 pi R^2 sigma_ref f_q`,

with `0 <= f_q <= 1`. The Coulomb contribution is then `F_C ~ qE`.

This is **not** a triboelectric charging, plasma, or charge-relaxation model.

## 4. Dielectrophoretic force

For a spherical dielectric particle, the low-order dipole expression is

`F_DEP ~ 2 pi eps_m R^3 K grad(E^2)`,

with Clausius-Mossotti factor

`K = (eps_r,p - eps_r,m) / (eps_r,p + 2 eps_r,m)`.

The current implementation approximates `E ~ V/L` and
`grad(E^2) ~ E^2/L`, where `L` is a configurable field length scale. A 2-D/3-D
electrostatic field solution or measured field map should replace this closure
for design-grade work.

## 5. Ejection criterion

The current screening criterion is

`F_C + F_DEP > F_vdW + F_g`.

This is a static lift criterion. It does not by itself demonstrate sustained
traveling-wave transport, clearing efficiency, or long-duration operation.

## 6. Voltage solution

Because the low-order lift model has the form `F_lift = aV + bV^2`, the code
solves the positive quadratic root for the peak voltage required to match
modeled retention. The result is a **trend metric**, not a hardware voltage
requirement, because detailed electrode fields, discharge limits, material
interfaces, and dust charging remain outside the model.

## 7. Mars electrical-breakdown boundary

NASA EDS literature identifies low-pressure electrical breakdown as a central
Mars design constraint. This repository therefore does **not** claim that a
voltage is safe simply because the force model predicts ejection. A defensible
breakdown model requires electrode geometry, gas composition, pressure,
temperature, surface condition, dielectric stack, and discharge-test data.

That separation is intentional: the force-balance model asks what would produce
lift under the stated assumptions, while discharge analysis asks whether the
hardware can apply the drive safely.
