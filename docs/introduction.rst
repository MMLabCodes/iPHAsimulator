Introduction
============

Welcome to the **iPHAsimulator** documentation!

iPHAsimulator (Satisfactory PHA - Polyhydroxyalkanoate - Action Simulator) is a professional, open-source Python package that provides a comprehensive framework for building, parameterizing, and simulating polyhydroxyalkanoate (PHA) systems and polymers using molecular dynamics (MD).

Key Features
------------

- **Molecular Structure Building** – Create polymer chains, arrays, and complex molecular systems with support for SMILES and PDB formats.
- **Force Field Parameterization** – Integrate with AMBER force fields (GAFF, GAFF2) for accurate molecular representations.
- **Simulation Engine** – Run production-grade MD simulations using OpenMM with customizable equilibration and production workflows.
- **Analysis Tools** – Comprehensive post-processing and trajectory analysis capabilities for extracting meaningful results from simulations.
- **Open Source** – Built by researchers, for researchers, with a welcoming community ready to support your work.

Project Refactoring
-------------------

This project has undergone significant refactoring to improve code clarity, maintainability, and accessibility. Recent improvements include:

- Refactored 6 core modules with type hints and comprehensive documentation
- PEP 8 compliant code organization
- Updated module names for clarity (e.g., ``sw_directories.py`` → ``filepath_manager.py``)
- Full backward compatibility maintained for existing code
- Enhanced error handling and validation

For details, see :doc:`REFACTORING_SUMMARY.md <../REFACTORING_SUMMARY>`.

Quick Start
-----------

To get started quickly:

1. Clone the repository: ``git clone https://github.com/MMLabCodes/iPHAsimulator.git``
2. Create a conda environment: ``conda create --name iphAsimulator python=3.11``
3. Activate and install: ``conda env update --file docs/environment.yml``
4. Begin using iPHAsimulator!

If you are new to iPHAsimulator, start with the :doc:`installation` guide.

About Polyhydroxyalkanoates (PHAs)
----------------------------------

PHAs are sustainable, biodegradable thermoplastic biopolymers produced by various microorganisms. They have applications in:

- **Packaging materials** – Environmentally friendly alternatives to conventional plastics
- **Biomedical devices** – Drug delivery systems, scaffolds for tissue engineering
- **Industrial applications** – Coatings, adhesives, fibers, and composites

iPHAsimulator enables researchers to explore PHA properties at the molecular level through computational simulations, supporting the development of next-generation sustainable materials.

Authors
-------

The iPHAsimulator was developed and maintained by:

- **Daniel J. York**
- **Dr. Isaac Vidal-Daza**
- **Dr. Francisco Martin-Martinez**

Testing and feedback by:

- **Sinem Bektas**
- **Daniel Clarke**

All contributors are current or past members of the `Martin-Martinez Lab <https://www.martinmartinezlab.com/>`_.
