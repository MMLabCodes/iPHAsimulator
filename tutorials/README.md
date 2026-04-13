# SatisPHAction Simulator Tutorials

Welcome to the tutorial collection! This folder contains comprehensive Jupyter notebook tutorials organized by topic and complexity level.

## Quick Navigation

### 🟢 **Beginner Level** (Start here!)

1. **Tutorial_1_filepath_manager.ipynb**
   - Learn: File and directory management
   - Duration: ~1-2 hours
   - Prerequisites: None
   - Key concepts: Project structure, directory organization

2. **Tutorial_2_Parameterizing_Small_Molecules_and Polymers.ipynb**
   - Learn: Molecule parameterization with AMBER
   - Duration: ~2-3 hours
   - Prerequisites: Tutorial 1
   - Key concepts: Force fields, charge calculations, atom types

### 🟡 **Intermediate Level**

3. **Tutorial_3_Solvating_Small_Molecules_and_Polymers.ipynb**
   - Learn: Add solvent molecules to systems
   - Duration: ~1-2 hours
   - Prerequisites: Tutorials 1-2
   - Key concepts: Solvation boxes, water models, periodic boundaries

4. **Tutorial_4_Building_Systems_with_Polymers.ipynb**
   - Learn: Construct complete polymer systems
   - Duration: ~3-4 hours
   - Prerequisites: Tutorials 1-3
   - Key concepts: Polymer chains, molecular arrays, system building

4b. **Tutorial_4b_Building_AMBER_Systems_Advanced.ipynb** (Optional advanced variant)
   - Learn: Deep dive into AMBER system building with BuildAmberSystems class
   - Duration: ~2-3 hours
   - Prerequisites: Tutorial_4
   - Key concepts: Advanced AMBER parameterization, system configuration

5. **Tutorial_5_Running_Openmm_Simulations.ipynb**
   - Learn: Execute MD simulations
   - Duration: ~2-3 hours
   - Prerequisites: Tutorials 1-4
   - Key concepts: Ensembles, minimization, production runs

### 🔴 **Advanced Level**

6. **Tutorial_6_Building_Chitin_Polymers_and_Systems.ipynb**
   - Learn: Specialized polymer handling (Chitin)
   - Duration: ~2-3 hours
   - Prerequisites: Tutorials 1-5
   - Key concepts: Complex polymers, specialized workflows

7. **Tutorial_7_Building_PET_Polymers_and_Systems.ipynb**
   - Learn: Build PET (polyethylene terephthalate) systems
   - Duration: ~1-2 hours
   - Prerequisites: Tutorials 1-5
   - Key concepts: Aromatic polymers, synthesis

8. **Tutorial_9_Stress_strain_simulations.ipynb**
   - Learn: Run mechanical deformation simulations
   - Duration: ~2-3 hours
   - Prerequisites: Tutorials 1-5
   - Key concepts: Mechanical properties, stress-strain curves

9. **Tutorial_10_Analysis_module.ipynb** and **Tutorial_11_Analysis_module_2.ipynb**
   - Learn: Analyze simulation results
   - Duration: ~2-3 hours each
   - Prerequisites: At least one completed simulation (Tutorial 5)
   - Key concepts: Trajectory analysis, property calculations, visualization

**Note**: Tutorial numbering follows the main learning path. Tutorial_4b is an optional advanced variant of Tutorial_4 for users wanting deeper AMBER system building knowledge.

## 🔧 **Guides & Reference Materials**

### Complementary Guides (Advanced Reference)
- **openmm_simulation_guide.ipynb** - Comprehensive OpenMM simulation guide with examples
- **parametrization_guide.ipynb** - Detailed parameterization workflow reference

### Examples & Walkthroughs
- **Simulating_Monodisperse_PHAs_Example_Scripts.ipynb** - Complete PHA simulation workflow
- **Simulating_Monodisperse_PHAs_Walkthrough.ipynb** - Step-by-step PHA examples
- **SMILES_to_orca_input.ipynb** - Quantum chemistry workflows

## 📺 Learning Path Recommendation

### Path 1: Getting Started (6-8 hours)
1. Tutorial_1 → Understand directory structure
2. Tutorial_2 → Learn parameterization
3. Tutorial_3 → Add solvation
4. Tutorial_5 → Run a simulation

### Path 2: Polymer Simulations (12-15 hours)
1. Tutorials 1-3 (Setup fundamentals)
2. Tutorial_4 (Build polymer systems)
3. Tutorial_5 (Run simulations)
4. Tutorials 10-11 (Analyze results)

### Path 3: Specialized Systems (15-20 hours)
1. Tutorials 1-5 (Foundation)
2. Tutorial_6 (Chitin systems) OR Tutorial_7 (PET systems)
3. Tutorial_9 (Mechanical properties)
4. Tutorials 10-11 (Analysis)

## Running Tutorials

### In Jupyter:
```bash
jupyter notebook
# Navigate to tutorials folder and open desired notebook
```

### Command line:
```bash
cd tutorials
jupyter notebook Tutorial_1_filepath_manager.ipynb
```

## Requirements

All tutorials require the SatisPHAction Simulator environment:

```bash
conda create -n satisfaction -c conda-forge python=3.9
conda activate satisfaction
conda install -c conda-forge ambertools openmm rdkit openbabel mdanalysis
git clone <repo-url>
cd satisfaction-simulator
pip install -e .
```

See main `README.md` for detailed setup instructions.

## Tutorial Features

✅ Comprehensive explanations
✅ Runnable code cells
✅ Output examples
✅ Visualizations
✅ Practice exercises
✅ Links to documentation

## Tips for Learning

1. **Read before running**: Understand what each cell does
2. **Modify code**: Try changing parameters to see effects
3. **Save results**: Keep successful runs for reference
4. **Take notes**: Record what works for your system
5. **Refer to docs**: Use module docstrings (help(function_name))
6. **Check examples**: See `/examples/` folder for quick scripts

## Common Issues & Solutions

**Issue**: Import errors
- **Solution**: Ensure all packages installed from main README

**Issue**: Output files not created
- **Solution**: Check file paths and write permissions

**Issue**: Simulation won't converge
- **Solution**: Try longer equilibration, different parameters

**Issue**: Running out of memory
- **Solution**: Reduce system size, use GPU acceleration

## Next Steps After Tutorials

1. **Apply to your system**: Use tutorials as templates
2. **Modify parameters**: Adjust for your research
3. **Run production**: Scale to larger systems
4. **Analyze results**: Use Tutorial 10-11 methods
5. **Publish**: Document your workflow

## Contributing

Have improvements to tutorials?
1. Make changes in a notebook
2. Test thoroughly
3. Submit pull request with explanation

## Contact & Support

- See main project README for support options
- Check ARCHITECTURE.md for system overview
- Review /examples/ folder for quick examples

---

**Happy learning!** 🧬

Start with Tutorial_1 if you're new to the project.
