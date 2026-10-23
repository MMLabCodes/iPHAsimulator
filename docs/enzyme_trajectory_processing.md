# Enzyme–PHA trajectory preparation

The Bash/GROMACS templates used to prepare the project's own enzyme–PHA
trajectories (`process_trajectory.sh` and its instruction file) are not included
in the public release. The packaged equivalent is the configuration-driven
`iphasimulator.trajectory_processing` module, installed as the
`ipha-process-trajectory` command. It streams one GROMACS XTC through
`gmx trjconv`, keeps every processed frame for analysis and writes a separate
first-frame structure and VMD script for inspection. It needs GROMACS and the
`analysis` extra (MDAnalysis verifies the written frames); no simulation or
viewer is launched.

## 1. Write the instruction file

Create a YAML instruction file inside the simulation's `analysis/` folder.
Relative paths resolve against that file's directory. Unknown or duplicate keys,
quoted booleans and unsupported `pbc`/`fit` values are rejected.

```yaml
schema_version: 1
input_trajectory: ../production_combined_1us.xtc
structure: ../step7_production.tpr
index: ../index.ndx
output_dir: processed
stride: 100          # keep every 100th stored frame
pbc: mol             # none, mol, whole, res or atom
center: true
center_group: SOLU   # exact group name from the index file
fit: none            # none, rot+trans or translation (then set fit_group)
output_group: SYSTEM
prepare_vmd: true
overwrite: false
gmx: gmx
```

`custom_groups` maps additional group names to MDAnalysis selection strings when
the index file lacks a suitable group. Enabled centring and fitting require an
explicit group; `output_group` is always required.

## 2. Check the plan

```bash
ipha-process-trajectory analysis/instructions.yaml --dry-run
```

`python -m iphasimulator.trajectory_processing` is equivalent. The dry run
validates the inputs, resolves the groups and prints the planned `trjconv`
operations as JSON without writing a trajectory.

## 3. Run and inspect

```bash
ipha-process-trajectory analysis/instructions.yaml
```

Results are assembled in a staging directory and installed into `output_dir`
only after every written frame has been verified against the input (stride,
times and, when nothing is transformed, coordinates and box). An existing
`output_dir` is refused unless `overwrite: true`, and even then only a directory
created by this workflow is replaced; the previous result is archived.

| File | Contents |
| --- | --- |
| `processed.xtc` | All processed frames, for analysis |
| `viewing.gro` | The first processed frame, as topology for viewers |
| `view.vmd` | VMD script loading the GRO and XTC (`prepare_vmd: true`) |
| `selections.ndx` | Index groups passed to `trjconv` |
| `summary.json` | Resolved settings, input fingerprints, plan, frame counts and status |

The `trjconv` logs and a per-frame time/step table are kept alongside them.
Inspect the result in VMD (`vmd -e /absolute/path/to/view.vmd`) before analysis.

For Python analysis, continue with the [enzyme-contact guide](enzyme_contacts.md),
supplying the full `processed.xtc` and the matching production TPR. Do not use
rotationally fitted coordinates with an untransformed box for periodic contacts.
Notebook 08 covers the shared polymer preprocessing helpers instead; see
[trajectory preprocessing](workflows/trajectory.md).

API: {py:func}`iphasimulator.trajectory_processing.process_trajectory`,
{py:func}`iphasimulator.trajectory_processing.load_config`.
