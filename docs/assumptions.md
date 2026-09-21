# Baseline assumptions and provenance

The default values are a reproducible **concept baseline**, not a claim that
they are optimal or flight-qualified.

| Parameter | Default | Role |
|---|---:|---|
| Mars gravity | 3.71 m/s^2 | particle weight |
| Mars pressure | 600 Pa | environment context |
| Mars temperature | 210 K | environment context |
| dust density | 2900 kg/m^3 | basaltic-silicate screening assumption |
| particle relative permittivity | 4.5 | screening assumption |
| Hamaker constant | 6.5e-20 J | adhesion sensitivity input |
| effective contact separation | 0.4 nm | adhesion sensitivity input |
| electrode width | 100 um | project concept baseline |
| electrode spacing | 400 um | project concept baseline |
| spatial period | 1 mm | project concept baseline |
| phases | 3 | project concept baseline |
| peak drive voltage | 1.5 kV | project concept baseline |
| drive frequency | 25 Hz | project concept baseline |

The code deliberately keeps uncertain quantities as parameters. Values that
came from the original project concept are labeled as such instead of being
presented as NASA design recommendations.

## Interpretation rules

1. A positive force margin means only that the modeled lift terms exceed the
   modeled retention terms.
2. The model does not establish electrical-breakdown safety.
3. The model does not establish a technology readiness level.
4. The model does not imply NASA endorsement or NASA software provenance.
5. Sensitivity to adhesion, charge, and field-gradient assumptions should be
   reported whenever quantitative results are used.
