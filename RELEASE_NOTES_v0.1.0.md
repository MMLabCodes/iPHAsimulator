# iPHAsimulator 0.1.0

First public release.

iPHAsimulator is a Python toolkit for building polyhydroxyalkanoate (PHA)
oligomers and polymers and preparing them for molecular simulation. It builds
chains from the common PHA monomers (3HB, 3HO, 3HDD) or from custom 3-hydroxy
acids, checks that every stereocentre has the natural R configuration, exports
the structures as PDB and SDF files, and prepares force-field parameters and
simulation inputs for Amber/GAFF2, GROMACS and OpenMM. The workflow is taught
through numbered Jupyter notebooks; reusable code lives in the `iphasimulator`
package. Documentation: https://mmlabcodes.github.io/iPHAsimulator/

## Included

- Tutorial notebooks in `notebooks/`:
  - 01–04: build, design, validate and export PHA oligomers (RDKit only)
  - 05A/05B: GAFF2 (AmberTools) and CGenFF (CHARMM-GUI) parameterisation
  - 06A/06B/06C: GROMACS and OpenMM simulation preparation, plus an optional
    OpenMM quick check of the 05A parameters
  - 07: HPC/SLURM execution
  - 08–10: trajectory preprocessing, polymer analysis and a benchmark batch
  - 11–12: docking input preparation and stability diagnostics
- `ipha-process-trajectory`, a command-line tool for configuration-driven
  GROMACS trajectory processing
- A Streamlit graphical interface (`python -m streamlit run pha_gui.py`)
- The `iphasimulator` package (`pip install -e .`) with `md`, `analysis` and
  `gui` optional extras

## Requirements

- Python 3.10 or newer and RDKit. Notebooks 01–04 and the quick-start need
  nothing else.
- Only for the notebooks that use them: AmberTools (05A, 06C); GROMACS (06A,
  08, 10, 12; optional in 06B); OpenMM with ParmEd and MDTraj (`.[md]`) for the
  quick check, 06A, 06C and 09. 05B/06B use the CHARMM-GUI website; 07 and 10
  expect a cluster or locally installed engines.
- MDAnalysis and matplotlib (`.[analysis]`) for the trajectory and contact
  tools; Streamlit (`.[gui]`) for the interface.

## Known limitations

- For custom monomers the R check uses the CIP label of the stereocentre. When
  the side chain outranks the backbone in CIP priority (for example vinyl,
  isopropyl or CH2OMe side chains), "R" corresponds to the mirror image of the
  natural PHA geometry. Inspect such structures visually.
- Notebook 06A combines a GAFF2 solute with CHARMM-style TIP3P water and ions.
  Treat it as a preparation example, not a validated force-field combination.
- The optional OpenMM route in notebook 06C is a template: it does not run
  end-to-end as written and needs local adjustment.
- The polymer-only benchmark systems were parameterised with GAFF2 and AM1-BCC
  charges, while the package default is ABCG2, so parameters generated with
  the default are not identical to the benchmark ones.

## Citation

Use the "Cite this repository" button on the GitHub page (from `CITATION.cff`).

Authors: Zhiwen Zhong, Daniel York, Francisco J. Martin-Martinez
