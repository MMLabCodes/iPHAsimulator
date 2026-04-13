# SatisPHAction Simulator

A professional, open-source Python package for simulating **polyhydroxyalkanoate (PHA)** systems and polymers using molecular dynamics.

SatisPHAction stands for **Satisfactory PHA (Polyhydroxyalkanoate) Action Simulator** - a comprehensive toolkit that enables researchers to build molecular structures, parameterize them with the **Amber** force field, and run production-grade simulations using **OpenMM**.

## What is SatisPHAction?

PHAs are sustainable, biodegradable biopolymers with applications in packaging, biomedics, and industrial materials. SatisPHAction provides researchers with:

- **Structure Building**: Generate polymer arrays and complex molecular systems
- **Force Field Parameterization**: AMBER force field integration for accurate simulations
- **Simulation Engine**: OpenMM-based molecular dynamics with equilibration and production workflows
- **Analysis Tools**: Post-processing and trajectory analysis capabilities
- **Community-Driven**: Fully open-source and welcoming to contributions

The project has undergone significant refactoring to improve code clarity, maintainability, and accessibility. See [REFACTORING.md](REFACTORING.md) for details.

For detailed documentation, visit: https://polymersimulator.readthedocs.io/en/latest/index.html

---

## Quick Start

Get up and running with SatisPHAction in 5 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/MMLabCodes/polymersimulator.git
cd polymersimulator

# 2. Create and activate environment
conda create --name satisfaction python=3.11
conda activate satisfaction

# 3. Install dependencies
conda env update --file docs/environment.yml

# 4. Verify installation
python -c "import openmm; from rdkit import Chem; print('Success!')"
```

---

## Installation Instructions

### 1. Setting up the environment and cloning repository

(Important: If you are working in windows, please follow the steps in section section 3 <a name="section-3"></a> (Working with windows) to first set up a linux system in your computer before following the steps to set up the environment. If you are working in Unix (linux or macOS), you will not require any prerequisite steps before setting up the environment given below)

To run this code, a Python environment containing **RDkit**, **AmberTools** and **openmm** is required. This environment is set up by running the lines described in the following steps 1-4 in your terminal (command line). (In windows, open ubuntu and enter these lines into the terminal)

1. Install miniconda

   Miniconda is a package and environment manager for Python. The following commands install miniconda in your home directory and intialise it for setting up environments.
   
```
cd 
mkdir -p ~/miniconda3 
cd miniconda3/ 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh 
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
~/miniconda3/bin/conda init bash 
~/miniconda3/bin/conda init zsh
```
2. Create environment

Creating an environment is useful as it creates a separate container for all packages required in the project. 
The following commands create an environment called "AmberTools23" and activate it.
   ```
   conda create --name AmberTools23 
   conda activate AmberTools23 
   ```
3. Install **openmm**, **RDkit** and **AmberTools**

   Now the environment has been activated the following commands install the 3 packages required.
   
   ```
   conda install -c conda-forge ambertools=23
   conda install -c conda-forge openmm
   conda install -c conda-forge rdkit
   conda install -c conda-forge openbabel
   ```
   
3.1 Install **Jupyter notebooks**

   We need to install Jupyter notebooks in this environment to run AmberTools from a Python notebook (in addition to running it from the terminal)
    
   ```
   sudo apt install python3-pip python3-dev
   pip install jupyter
   ```
    
3.2 Test the Jupyter notebook

   In the terminal (or Ubuntu terminal if using a Windows machine), we need to enter the following:
    
   ```
   jupyter notebook
   ```
   This will start a remote Jupyter notebook server within the environment we have just set up.
    
   You will see the following prompt after entering 'Jupyter notebook':

<img width="510" alt="jupyter_tut" src="https://github.com/DanielYyork/polymer_simulator/assets/93723782/9718b875-aeb0-421b-a134-87e945d9b585">

   Now, you can select the first URL (the one containing 'localhost:8888') and copy and paste it into a browser, this will launch Jupyter notebook (fingers crossed!)
    
   From there you can navigate to the Jupyter notebook folder and launch any additional notebooks from there.
    
   For now, we will close the notebook and ensure our other packages are working properly.
    
   To close the notebook, return to Ubuntu: hold "ctr" + "c" at the same time, you will be asked if you want to close Jupyter notebook - yes!
    
4. Ensure the required packages are available

   Before running any code, it is recommended to check the availability of different packages.

   **AmberTools** is a collection of different tools. Among them, **antechamber** and **tleap** are used extensively. To check these tools are available, enter the commands below into your terminal.
   ```
   antechamber
   ```
   If antechamber is available, you will see this in your terminal:
   ```
   Welcome to antechamber 22.0: molecular input file processor.
   Usage: antechamber -i     input file name
                   -fi    input file format
                   -o     output file name
                   -fo    output file format
                   -c     charge method
                   -cf    charge file name
                   -nc    net molecular charge (int)
                   -a     additional file name
                   -fa    additional file format
                   -ao    additional file operation
                   ... more operations ..
   ```

   ```
   tleap
   ```
   If tleap is available, you will see this in your terminal:
   ```
   Welcome to LEaP!
   (no leaprc in search path)
   >
   ```
   Note: The 'tleap' command opens an interactive version of the tool where you can enter tleap commands. To exit this press ctr+c.

   Checking the availability of **openmm** is slightly different as it is a Python package - not a standalone program. Open the Python interpreter as follows:
   ```
   python3
   ```
   If python3 is available, you will see this in your terminal:
   ```
   Python 3.12.1 | packaged by conda-forge | (main, Dec 23 2023, 08:03:24) [GCC 12.3.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>>
   ```
   Like 'tleap' the 'python3' command opens an interactive version of Python and Python code can be entered after '>>>'. To check openmm is imported enter the following into the Python interpreter:
   ```
   >>> from simtk.openmm import app
   ```
   You may see the following warning:
   ```
   Warning: importing 'simtk.openmm' is deprecated.  Import 'openmm' instead.
   ```
   This warning can be ignored, "import openmm" is better but importing from simtk will still load the openmm package.
   Note: This is an interactive Python interpreter and pressing ctr+d will exit this - ctr+c acts as a keyboard interrupt in the python interpreter and will interrupt any running code but will not exit.

   If openmm is not installed properly you will see this:
   ```
   >>> from simtk.openmm import app
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ModuleNotFoundError: No module named 'simtk'
   >>>
   ```
   In this case return to step 3 and try to install openmm again. An update to the openmm package may also be the issue; it can be updated with the following line:
   ```
   conda update -c conda-forge openmm
   ```
   Now, try an import openmm to the python interpreter again - it should work!

5. Cloning the repository

5.1 Normal git clone method
    
   At the top of the GitHub page there will a blue button labelled '<> code'. Click here and select 'HTTPS' and copy the link. No return to Ubuntu and enter:
    
   ```
   git clone copied_link
   ``` 
   This will clone the repository into Ubuntu and you will be able to access all the required files.
   Don't forget you can navigate through the file explorer to view these files (see section 4 for where linux files are located).
    
   If this method does not work, see the alternative method below.

5.2 Alternative git clone method

   To download these Python scripts and Jupyter notebooks it is necessary to clone the BCSW repository. **You will need a GitHub account**.
   This will give you access to all the files in your own computer. The commands below should be executed in a terminal,
   this will create a new directory in you home directory.
    
   First you will need to obtain a personal access token from GitHub, once you have logged into GitHub, 
   click on your profile in the top right and navigate to (settings --> developer settings --> personal access tokens --> Tokens (classic)). 
   Here, click on "generate new token --> generate new token (classic)" and enter a note "clone repo" and in the tick boxes, select "repo". 
   Now scroll to the bottom and "generate token".
   This will give you a token you will need for the next step.
   ```
   cd 
   git clone https://USERNAME:YOUR_TOKEN@github.com/MMLabCodes/BCSW.git
   cd polymer_simulator
   ```
   The final command navigates to the directory containing the notebooks and scripts required for the tutorial.

## Tutorials & Documentation

### Jupyter Notebooks

A series of Jupyter notebooks provide step-by-step guides and examples for common tasks:

- **Building molecular structures** - Learn to construct polymer chains and arrays
- **Parameterization workflows** - Apply AMBER force fields to your systems
- **Running simulations** - Set up and execute production MD simulations
- **Analysis workflows** - Process and analyze simulation trajectories

Launch Jupyter notebooks from your terminal:

```bash
jupyter notebook
```

Then open the first localhost URL in your browser and navigate to the tutorials folder.

### Examples Directory

Pre-built examples for quick reference: `/examples/`

### Documentation

Complete documentation with API reference: [Documentation Site](https://polymersimulator.readthedocs.io/)

---

## Windows Compatibility

### Setting up Windows Subsystem for Linux (WSL) <a name="section-3"></a>

The Amber package requires a Linux environment. On Windows, WSL (Windows Subsystem for Linux) provides the best solution:

1. **Enable Windows Subsystem for Linux**

   Open Windows PowerShell (as Administrator) and run:
   ```
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   ```

2. **Install Ubuntu from Microsoft Store**

   Visit: https://apps.microsoft.com/search?query=ubuntu

3. **Launch Ubuntu and set up**

   ```
   sudo apt update
   sudo apt upgrade
   ```

4. **Follow the Linux Installation Steps**

   Once Ubuntu is running, follow the standard installation instructions above.

---

## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help makes SatisPHAction better for everyone.

**Get started:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For detailed contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Citation

If you use SatisPHAction in your research, please cite:

```bibtex
@software{York2024SatisPHAction,
  author = {York, Daniel J. and Vidal-Daza, Isaac and Martin-Martinez, Francisco},
  title = {SatisPHAction Simulator: A Python Package for PHA Molecular Dynamics Simulations},
  year = {2024},
  url = {https://github.com/MMLabCodes/polymersimulator}
}
```

---

## Authors

SatisPHAction Simulator is developed and maintained by:

- **Daniel J. York** (Lead Developer)
- **Dr. Isaac Vidal-Daza** (Core Architecture)
- **Dr. Francisco Martin-Martinez** (Principal Investigator)

With testing and feedback from:
- Sinem Bektas
- Daniel Clarke

All contributors are members of the [Martin-Martinez Lab](https://www.martinmartinezlab.com/).

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Acknowledgments

- AmberTools and OpenMM teams for excellent MD simulation tools
- RDKit team for molecular informatics capabilities
- The open-source scientific computing community

---

## Support

For questions, issues, or suggestions:
- Open an [Issue](https://github.com/MMLabCodes/polymersimulator/issues)
- Check the [Documentation](https://polymersimulator.readthedocs.io/)
- Review [REFACTORING.md](REFACTORING.md) for recent improvements

---

**Project**: SatisPHAction Simulator
**Repository**: https://github.com/MMLabCodes/polymersimulator
**Status**: Active Development