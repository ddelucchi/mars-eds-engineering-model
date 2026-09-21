# EDS / HDMS Simulation

Python research archive for electrodynamic dust shields (EDS) and a hybrid dust mitigation system (HDMS), focused on Martian dust, particle adhesion, and solar array protection.

## Project layout

- [`simulation/`](simulation/README.md) contains the three standalone Python research programs.
- [`renders/`](renders/README.md) contains visual outputs and supporting project figures.

## Run the physics analysis

From the repository root, run the physics analysis:

```powershell
python simulation/eds_physics_analysis.py
```

To save the analysis plots under `renders/physics-analysis/`, run this in PowerShell from the repository root:

```powershell
Push-Location renders/physics-analysis
python ../../simulation/eds_physics_analysis.py
Pop-Location
```

The plot script writes PNG and PDF exports locally; this repository keeps the PNG renders. The scripts are archival research prototypes. Their numerical assumptions and outputs have not been independently validated as flight-ready engineering results. Dependencies vary by script and are not pinned. The repository has no open-source license.
