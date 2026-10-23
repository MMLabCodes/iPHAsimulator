# Analysis

Choose the analysis that matches your research question. Structure fluctuations
and minimum-image contacts have different coordinate-preparation requirements.

## Enzyme–PHA distances and contacts

This reusable workflow measures each enzyme residue's minimum distance to all
selected PHA heavy atoms. It supports all-heavy and side-chain-heavy modes,
preserves residue identities and unavailable glycine side chains, and reports
the percentage of sampled frames below each contact cutoff.

1. Write a YAML configuration with `topology`, `trajectory`, `output_root` and
   `pha_selection` (all keys are listed under
   [configuration and sampling](../enzyme_contacts.md#configuration-and-sampling)).
   Use a matching TPR and one original production XTC, or the full processed
   trajectory from the [preparation workflow](../enzyme_trajectory_processing.md).
   Relative paths resolve against the YAML file's directory.
2. Review the protein/PHA selections, time window, sampling and cutoffs. The
   default `preview_frames: 31` gives a preview; `preview_frames: null` or the
   `--full` flag requests the full selected analysis.
3. Run the input checks and analysis from the repository root:

   ```bash
   python -m iphasimulator.analysis_contacts <path-to-your-data>/contacts.yaml
   ```

   Four PNG plots are saved.
4. Inspect `residue_summary.csv`, `distances.npz` and the saved provenance.

Add `--full` for all configured sampled frames. The research notebook and the
configuration used for the project's own simulations are not included in the
public release; configure your own paths explicitly.

Distances use Å, time uses ns, occupancy uses 0–100%. A residue contributes once
per sampled frame when `distance < cutoff`; default comparisons are 4.0, 4.5 and
5.0 Å. These are correlated sampled-frame proportions, not affinity, catalytic
activity or independent observations. No equilibration period is discarded
automatically. See the [full contact method and validation record](../enzyme_contacts.md).

## Basic polymer structure

Notebook **09** uses MDTraj and the centered trajectory from notebook 08 to
calculate radius of gyration, an example end-to-end distance, and SASA. Review
the atom selection and units in that notebook: its MDTraj calculations are not
the contact module's Å/ns interface. Its end-to-end example uses the first and
last selected atoms, which need not be the most meaningful chemical endpoints.
Its SASA is computed on the polymer-only trajectory.

## Enzyme/polymer stability diagnostics

Notebook **12** examines total energy, protein-backbone RMSD and polymer RMSD
after protein alignment. Its inputs and selections are system-specific. These
diagnostics support manual review; the notebook does not establish convergence.
Do not reuse fitted coordinates with an untransformed periodic box for contacts.

APO RMSF comparisons, catalytic geometry, PHA repeat-unit mapping and batch
contact comparisons are **future extensions**. Existing empty APO notebook
placeholders do not implement them.

API: {py:func}`iphasimulator.analysis_contacts.run_contacts`,
{py:func}`iphasimulator.analysis_contacts.load_distances`,
{py:func}`iphasimulator.analysis_contacts.plot_contacts`.
