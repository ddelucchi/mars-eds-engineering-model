# Simulation programs

These standalone scripts preserve the three Python programs from the original HDMS SIM workspace. Their filenames now describe their main subject; the code itself has not been refactored.

| Program | Main contents |
| --- | --- |
| [`mars_particle_dynamics.py`](mars_particle_dynamics.py) | Martian environment, dust-particle force and thermal models, surface interactions, and particle simulation. |
| [`hdms_system_model.py`](hdms_system_model.py) | Hybrid dust mitigation system model and system-level visualizations. |
| [`eds_physics_analysis.py`](eds_physics_analysis.py) | Analytical EDS potential and field, adhesion and deposition forces, charge dissipation, voltage and power estimates, and comparison plots. |

Run a script from the repository root, for example:

```powershell
python simulation/eds_physics_analysis.py
```

Dependencies vary by script and are imported in the source files. Some optional scientific packages have fallbacks; there is no pinned environment file. Plotting scripts write generated files to the current working directory. The programs are exploratory research prototypes, and syntax checking does not establish numerical validity or suitability for engineering decisions.
