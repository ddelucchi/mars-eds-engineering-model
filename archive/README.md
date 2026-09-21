# Legacy project archive

This directory preserves the original exploratory scripts from the project
workspace for provenance.

They are **not** the supported engineering interface of the repository and are
not run by CI. Some contain broad experimental dependencies, historical
assumptions, and analyses that predate the current Mars EDS package.

Use `src/mars_eds/` for the auditable model described in the root README.

Preserving the originals rather than silently rewriting them makes the
development history inspectable while keeping the current engineering model
clean.
