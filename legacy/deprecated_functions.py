"""
Legacy and deprecated functions from SatisPHAction Simulator.

This module contains functions that are no longer actively maintained and support
is not continued for these functions. They are preserved for backward compatibility
with older code but should not be used in new projects.

DEPRECATION TIMELINE:
- v1.1: Functions moved here with deprecation warnings
- v2.0: Functions available but with explicit warnings
- v3.0: Functions will be removed

MIGRATION INSTRUCTIONS:

For old array generation functions, use the new system_builder module:
    OLD: use gen_3_3_array() or build_3_3_polymer_array_old()
    NEW: from modules.system_builder import BuildAmberSystems
         builder = BuildAmberSystems(directories)
         builder.gen_3_3_array(molecule_name)

For old analysis functions, use the new trajectory_analyzer module:
    OLD: use Analysis() class directly
    NEW: from modules.trajectory_analyzer import Analysis
         (The new Analysis class is fully refactored with better documentation)

For max_pairwise_distance, use new calculation methods:
    OLD: max_dist = obj.max_pairwise_distance(mol)
    NEW: from modules.system_builder import BuildAmberSystems
         builder = BuildAmberSystems(directories)
         max_dist = builder.max_pairwise_distance(mol)

See MIGRATION_GUIDE.md in the legacy/ folder for detailed migration instructions.
"""

import warnings
import numpy as np
import os
import subprocess
from rdkit.Chem import MolFromPDBFile

# ============================================================================
# DEPRECATED: Old Array Generation Functions
# ============================================================================

def build_3_3_polymer_array_old(self, directories=None, molecule_name=None, number_of_units=None):
    """
    DEPRECATED: Old function that builds 3x3 arrays of polymers using tleap.

    This function is deprecated due to issues with:
    - Final box is too large
    - Some polymers not in correct conformation
    - Large forces cause simulation failures

    Use BuildAmberSystems.gen_3_3_array() instead.
    """
    warnings.warn(
        "build_3_3_polymer_array_old() is deprecated. "
        "Use BuildAmberSystems.gen_3_3_array() instead.",
        DeprecationWarning,
        stacklevel=2
    )

    if directories == None or molecule_name == None or number_of_units == None:
        print("Please provide 3 arguments as follows: build_3_3_polymer_array(directories, molecule_name, number_of_units)")
        print("Directories: A python object generated with the PolymerSimulatorDirs(filepath) method imported from sw_directories")
        print("Molecule name: A string of the molecule name, i.e. 'Ethane'")
        print("Number of units: An integer denoting polymer length, i.e. 10. NOTE: number_of_units >= 3")
        return(None)

    if self.is_poly_prepped(directories, molecule_name) == True:
        pass
    if self.is_poly_prepped(directories, molecule_name) == False:
        print("Please prepare prepin files for so polymers can be generated.")
        return(None)

    if number_of_units < 3:
        print("A minimum number of 3 units is required to construct the polymer.")
        return(None)

    molecule_dir = os.path.join(directories.molecules_dir, molecule_name)
    cd_command = "cd " + molecule_dir
    print(cd_command)

    molecule_dir = os.path.join(directories.molecules_dir, molecule_name)

    try:
        os.chdir(molecule_dir)
        print("Current directory:", os.getcwd())
    except Exception as e:
        print("Exception:", e)

    file_subtype = "_3_3_array_" + str(number_of_units) + "_polymer"

    head_prepi_filepath = "head_" + molecule_name + ".prepi"
    mainchain_prepi_filepath = "mainchain_" + molecule_name + ".prepi"
    tail_prepi_filepath = "tail_" + molecule_name + ".prepi"

    output_dir = os.path.join(directories.systems_dir, (molecule_name.split("_")[0] + file_subtype))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdb_filepath = molecule_name + ".pdb"

    monomer_name = molecule_name.split("_")[0] + "_monomer"
    monomer_pdb_filepath = os.path.join(directories.molecules_dir, monomer_name, (monomer_name + ".pdb"))
    current_directory = os.getcwd()
    print("Current working directory:", current_directory)
    Mol = MolFromPDBFile(pdb_filepath)
    monomer = MolFromPDBFile(monomer_pdb_filepath)
    max_dist = self.max_pairwise_distance(monomer)
    print("monomer max dist is: ", max_dist)
    translate_distance = float((int(max_dist)*2))
    polymer_length = max_dist * number_of_units

    box_dist = int(float(polymer_length*3))

    polymer_name = molecule_name.split("_")[0] + "_" + str(number_of_units) + "_polymer"
    molecule_name_1 = polymer_name + "_1"
    molecule_name_2 = polymer_name + "_2"
    molecule_name_3 = polymer_name + "_3"
    molecule_name_4 = polymer_name + "_4"
    molecule_name_5 = polymer_name + "_5"
    molecule_name_6 = polymer_name + "_6"
    molecule_name_7 = polymer_name + "_7"
    molecule_name_8 = polymer_name + "_8"
    molecule_name_9 = polymer_name + "_9"

    translate_line_1 = "{0.0 0.0 0.0}"
    translate_line_2 = "{" + str(translate_distance) + " 0.0 0.0}"
    translate_line_3 = "{" + str(-translate_distance) + " 0.0 0.0}"


    translate_line_4 = "{" + str(translate_distance) + " " + str(translate_distance) + " 0.0}"
    translate_line_5 = "{" + str(-translate_distance) + " " + str(translate_distance) + " 0.0}"
    translate_line_6 = "{0.0 " + str(translate_distance) + " 0.0}"

    translate_line_7 = "{" + str(translate_distance) + " " + str(-translate_distance) + " 0.0}"
    translate_line_8 = "{" + str(-translate_distance) + " " + str(-translate_distance) + " 0.0}"
    translate_line_9 = "{0.0 " + str(-translate_distance) + " 0.0}"

    combine_line = "{" + molecule_name_1 + " " + molecule_name_2 + " " + molecule_name_3 + " " + molecule_name_4 + " " + molecule_name_5 + " " + molecule_name_6 + " " + molecule_name_7 + " " + molecule_name_8 + " " + molecule_name_9 + "}"

    base_mol_name = molecule_name.split("_")[0]
    intleap_path = base_mol_name + file_subtype + ".intleap"

    prmtop_filepath =  os.path.join(output_dir, base_mol_name + file_subtype + "_" + str(box_dist) + ".prmtop")
    rst_filepath = os.path.join(output_dir, base_mol_name + file_subtype + "_" + str(box_dist) + ".rst7")

    unsolved_prmtop_filepath =  os.path.join(output_dir, "unsolved_" + base_mol_name + file_subtype + ".prmtop")
    unsolved_rst_filepath = os.path.join(output_dir, "unsolved_" + base_mol_name + file_subtype + ".rst7")

    three_three_array_pdb_filepath = os.path.join(output_dir, base_mol_name + file_subtype + "_" + str(box_dist) + ".pdb")
    unsolved_three_three_array_pdb_filepath = os.path.join(output_dir, "unsolved_" + base_mol_name + file_subtype + ".pdb")

    head_rescode, mainchain_rescode, tail_rescode = directories.retrieve_polymeric_rescodes("3HB_trimer")

    polymer_code = " ".join([head_rescode] + [mainchain_rescode] * (number_of_units - 2) + [tail_rescode])
    polymer_command = "{" + polymer_code + "}"

    file_content = f"""source leaprc.gaff
    source leaprc.water.fb3
    source leaprc.protein.ff14SB

    loadamberprep {head_prepi_filepath}
    loadamberprep {mainchain_prepi_filepath}
    loadamberprep {tail_prepi_filepath}

    list

    {molecule_name_1} = sequence {polymer_command}
    {molecule_name_2} = sequence {polymer_command}
    {molecule_name_3} = sequence {polymer_command}
    {molecule_name_4} = sequence {polymer_command}
    {molecule_name_5} = sequence {polymer_command}
    {molecule_name_6} = sequence {polymer_command}
    {molecule_name_7} = sequence {polymer_command}
    {molecule_name_8} = sequence {polymer_command}
    {molecule_name_9} = sequence {polymer_command}

    check {molecule_name_1}

    translate {molecule_name_1} {translate_line_1}
    translate {molecule_name_2} {translate_line_2}
    translate {molecule_name_3} {translate_line_3}
    translate {molecule_name_4} {translate_line_4}
    translate {molecule_name_5} {translate_line_5}
    translate {molecule_name_6} {translate_line_6}
    translate {molecule_name_7} {translate_line_7}
    translate {molecule_name_8} {translate_line_8}
    translate {molecule_name_9} {translate_line_9}

    system = combine {combine_line}
    saveamberparm system {unsolved_prmtop_filepath} {unsolved_rst_filepath}
    savepdb system {unsolved_three_three_array_pdb_filepath}

    solvatebox system TIP3PBOX {box_dist}

    saveamberparm system {prmtop_filepath} {rst_filepath}
    savepdb system {three_three_array_pdb_filepath}
    quit
    """

    with open(intleap_path, 'w') as file:
        file.write(file_content)

    leap_command = "tleap -f " + intleap_path
    print(intleap_path)
    try:
        result = subprocess.run(leap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("Output:", result.stdout)
        else:
            print("Error:", result.stderr)
    except Exception as e:
        print("Exception:", e)

    cd_command = "cd " + str(directories.main_dir)
    result = subprocess.run(cd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return()


def gen_3_3_array(self, directories, molecule_name):
    """
    DEPRECATED: Generate a 3x3 array of molecules and solvate in water.

    Use BuildAmberSystems.gen_3_3_array() instead.
    """
    warnings.warn(
        "gen_3_3_array() is deprecated. Use BuildAmberSystems.gen_3_3_array() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    if self.is_mol_parametrized(directories, molecule_name) == True:
        pass
    if self.is_mol_parametrized(directories, molecule_name) == False:
        print(self.error_param)
        return()

    file_subtype = "_3_3_array"

    pdb_filepath = os.path.join(directories.molecules_dir, molecule_name, (molecule_name + ".pdb"))
    mol2_filepath = os.path.join(directories.molecules_dir, molecule_name, (molecule_name + ".mol2"))
    output_dir = os.path.join(directories.systems_dir, (molecule_name + file_subtype))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mol = MolFromPDBFile(pdb_filepath)
    max_dist = self.max_pairwise_distance(mol)
    translate_distance = float((int(max_dist)+1))
    box_dist = float((int(max_dist)+1)*3)

    molecule_name_1 = molecule_name + "_1"
    molecule_name_2 = molecule_name + "_2"
    molecule_name_3 = molecule_name + "_3"
    molecule_name_4 = molecule_name + "_4"
    molecule_name_5 = molecule_name + "_5"
    molecule_name_6 = molecule_name + "_6"
    molecule_name_7 = molecule_name + "_7"
    molecule_name_8 = molecule_name + "_8"
    molecule_name_9 = molecule_name + "_9"

    translate_line_1 = "{0.0 0.0 0.0}"
    translate_line_2 = "{0.0 0.0 " + str(translate_distance) + "}"
    translate_line_3 = "{0.0 0.0 " + str(-translate_distance) + "}"

    translate_line_4 = "{0.0 " + str(translate_distance) + " " + str(translate_distance) + "}"
    translate_line_5 = "{0.0 " + str(translate_distance) + " " + str(-translate_distance) + "}"
    translate_line_6 = "{0.0 " + str(translate_distance) + " 0.0}"

    translate_line_7 = "{0.0 " + str(-translate_distance) + " " + str(translate_distance) + "}"
    translate_line_8 = "{0.0 " + str(-translate_distance) + " " + str(-translate_distance) + "}"
    translate_line_9 = "{0.0 " + str(-translate_distance) + " 0.0}"

    combine_line = "{" + molecule_name_1 + " " + molecule_name_2 + " " + molecule_name_3 + " " + molecule_name_4 + " " + molecule_name_5 + " " + molecule_name_6 + " " + molecule_name_7 + " " + molecule_name_8 + " " + molecule_name_9 + "}"

    intleap_path = os.path.join(output_dir, (molecule_name + file_subtype + ".intleap"))
    prmtop_filepath =  os.path.join(output_dir, molecule_name + file_subtype + ".prmtop")
    rst_filepath = os.path.join(output_dir, molecule_name + file_subtype + ".rst7")
    three_three_array_pdb_filepath = os.path.join(output_dir, molecule_name + file_subtype + ".pdb")
    unsolved_three_three_array_pdb_filepath = os.path.join(output_dir, "unsovled_" + molecule_name + file_subtype + ".pdb")

    file_content = f"""source leaprc.protein.ff14SB
    source leaprc.gaff
    source leaprc.water.fb3
    {molecule_name_1} = loadMol2 {mol2_filepath}
    {molecule_name_2} = loadMol2 {mol2_filepath}
    {molecule_name_3} = loadMol2 {mol2_filepath}
    {molecule_name_4} = loadMol2 {mol2_filepath}
    {molecule_name_5} = loadMol2 {mol2_filepath}
    {molecule_name_6} = loadMol2 {mol2_filepath}
    {molecule_name_7} = loadMol2 {mol2_filepath}
    {molecule_name_8} = loadMol2 {mol2_filepath}
    {molecule_name_9} = loadMol2 {mol2_filepath}

    translate {molecule_name_1} {translate_line_1}
    translate {molecule_name_2} {translate_line_2}
    translate {molecule_name_3} {translate_line_3}
    translate {molecule_name_4} {translate_line_4}
    translate {molecule_name_5} {translate_line_5}
    translate {molecule_name_6} {translate_line_6}
    translate {molecule_name_7} {translate_line_7}
    translate {molecule_name_8} {translate_line_8}
    translate {molecule_name_9} {translate_line_9}

    system = combine {combine_line}

    savePDB system {unsolved_three_three_array_pdb_filepath}

    solvateBox system TIP3PBOX {box_dist}

    saveamberparm system {prmtop_filepath} {rst_filepath}
    savepdb system {three_three_array_pdb_filepath}
    quit
    """
    with open(intleap_path, 'w') as file:
        file.write(file_content)

    leap_command = "tleap -f " + intleap_path
    subprocess.run(leap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def gen_2_2_array(self, directories, molecule_name):
    """
    DEPRECATED: Generate a 2x2 array of molecules and solvate in water.

    Use BuildAmberSystems.gen_2_2_array() instead.
    """
    warnings.warn(
        "gen_2_2_array() is deprecated. Use BuildAmberSystems.gen_2_2_array() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    if self.is_mol_parametrized(directories, molecule_name) == True:
        pass
    if self.is_mol_parametrized(directories, molecule_name) == False:
        print(self.error_param)
        return()

    file_subtype = "_2_2_array"

    pdb_filepath = os.path.join(directories.molecules_dir, molecule_name, (molecule_name + ".pdb"))
    mol2_filepath = os.path.join(directories.molecules_dir, molecule_name, (molecule_name + ".mol2"))
    output_dir = os.path.join(directories.systems_dir, (molecule_name + file_subtype))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mol = MolFromPDBFile(pdb_filepath)
    max_dist = self.max_pairwise_distance(mol)

    translate_dist = float((int(max_dist)+1))
    box_dist = float((int(max_dist)+1)*4)

    molecule_name_1 = molecule_name + "_1"
    molecule_name_2 = molecule_name + "_2"
    molecule_name_3 = molecule_name + "_3"
    molecule_name_4 = molecule_name + "_4"

    translate_line_1 = "{0.0 " + str(translate_dist) + " " + str(translate_dist) + "}"
    translate_line_2 = "{0.0 " + str(-translate_dist) + " " + str(translate_dist) + "}"
    translate_line_3 = "{0.0 " + str(translate_dist) + " " + str(-translate_dist) + "}"
    translate_line_4 = "{0.0 " + str(-translate_dist) + " " + str(-translate_dist) + "}"

    combine_line = "{" + molecule_name_1 + " " + molecule_name_2 + " " + molecule_name_3 + " " + molecule_name_4 + "}"

    intleap_path = os.path.join(output_dir, (molecule_name + file_subtype + ".intleap"))
    prmtop_filepath =  os.path.join(output_dir, molecule_name + file_subtype + ".prmtop")
    rst_filepath = os.path.join(output_dir, molecule_name + file_subtype + ".rst7")
    two_two_array_pdb_filepath = os.path.join(output_dir, molecule_name + file_subtype + ".pdb")

    file_content = f"""source leaprc.protein.ff14SB
    source leaprc.gaff
    source leaprc.water.fb3
    {molecule_name_1} = loadMol2 {mol2_filepath}
    {molecule_name_2} = loadMol2 {mol2_filepath}
    {molecule_name_3} = loadMol2 {mol2_filepath}
    {molecule_name_4} = loadMol2 {mol2_filepath}

    translate {molecule_name_1} {translate_line_1}
    translate {molecule_name_2} {translate_line_2}
    translate {molecule_name_3} {translate_line_3}
    translate {molecule_name_4} {translate_line_4}

    system = combine {combine_line}

    saveamberparm system {prmtop_filepath} {rst_filepath}
    savepdb system {two_two_array_pdb_filepath}
    quit
    """
    with open(intleap_path, 'w') as file:
        file.write(file_content)

    leap_command = "tleap -f " + intleap_path
    subprocess.run(leap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


# ============================================================================
# DEPRECATED: Utility Functions
# ============================================================================

def parametrized_mols_avail(self):
    """
    DEPRECATED: Retrieve molecules with mol2 files.

    Use BuildSystems.mol2_avail() instead.
    """
    warnings.warn(
        "parametrized_mols_avail() is deprecated. Use BuildSystems.mol2_avail() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    a = False
    for root, dirs, files in os.walk(self.molecules_dir):
        dirs[:] = [d for d in dirs if d != 'depreceated']
        for file in files:
            if file.endswith(".mol2"):
                a = True
                pdb_file_path = os.path.join(root, file)
                pdb_file = pdb_file_path.split("/")[-1]
                print(pdb_file)
    if a == False:
        print("No parametrized molecules.")


def max_pairwise_distance(self, mol):
    """
    DEPRECATED:  Calculate maximum pairwise distance between atoms in a molecule.

    Use BuildSystems.max_pairwise_distance() instead.
    """
    warnings.warn(
        "max_pairwise_distance() is deprecated. Use BuildSystems.max_pairwise_distance() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    conformer = mol.GetConformer()
    num_atoms = mol.GetNumAtoms()
    atom_positions = np.zeros((num_atoms, 3))
    for i in range(num_atoms):
        pos = conformer.GetAtomPosition(i)
        atom_positions[i] = (pos.x, pos.y, pos.z)
    distances = np.linalg.norm(atom_positions[:, np.newaxis, :] - atom_positions, axis=2)
    np.fill_diagonal(distances, 0)
    max_distance = np.max(distances)
    return max_distance


# ============================================================================
# DEPRECATED: Analysis Classes and Functions
# ============================================================================

class DeprecatedAnalysis:
    """
    DEPRECATED: Legacy Analysis class.

    Use the new trajectory_analyzer module with the Analysis class instead.
    """
    cached_ROG_data = None
    cached_ROG_average = None
    cached_COG_data = None
    cached_COG_average = None

    def __init__(self):
        warnings.warn(
            "DeprecatedAnalysis is deprecated. Use the new Analysis class from trajectory_analyzer instead.",
            DeprecationWarning,
            stacklevel=2
        )
        pass


__all__ = [
    'build_3_3_polymer_array_old',
    'gen_3_3_array',
    'gen_2_2_array',
    'parametrized_mols_avail',
    'max_pairwise_distance',
    'DeprecatedAnalysis',
]
