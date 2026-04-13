"""
iPHAsimulator - Molecular Structure Utilities.

This module provides functions for working with molecular structures,
including volume calculations, SMILES-to-PDB conversions, and molecular
property analysis. It uses RDKit for chemistry operations.

A SMILES string is a compact text representation of a molecule.
For example, '3HB' (3-hydroxybutyrate) is 'CC(O)CC(=O)O'.

Key Functions:
    vol_from_smiles(smiles)     - Estimate molecular volume from a SMILES string
    vol_from_pdb(pdb_path)      - Estimate molecular volume from a PDB file
    smiles_to_pdb(smiles, out)  - Convert SMILES string to a 3D PDB file
    has_heteroatoms(mol)        - Check if a molecule contains N, O, or S atoms
    has_rings(mol)              - Check if a molecule contains ring structures
    count_elements_in_pdb(path) - Count atoms by element in a PDB file
    calculate_molecular_weight(pdb) - Calculate molecular weight from a PDB

Example::

    from modules.molecule_builder import vol_from_smiles, has_heteroatoms
    from rdkit import Chem

    # 3-Hydroxybutyrate (3HB) - the most common PHA monomer
    smiles = 'CC(O)CC(=O)O'
    volume = vol_from_smiles(smiles)
    print(f'Volume: {volume:.1f} Angstrom^3')

    mol = Chem.MolFromSmiles(smiles)
    print(f'Has heteroatoms: {has_heteroatoms(mol)}')
"""

from rdkit import Chem
from rdkit.Chem import AllChem
from typing import List, Tuple, Dict, Optional
import math
import os

# Optional: safely ignore Draw import if system libraries are missing
try:
    from rdkit.Chem import Draw
except ImportError:
    Draw = None

# ============================================================================
# Constants
# ============================================================================

# Van der Waals radii for common elements (in Angstroms)
VDW_RADII: Dict[str, float] = {
    'H': 1.20,  'C': 1.70,  'N': 1.55,  'O': 1.52,
    'P': 1.80,  'S': 1.80,  'F': 1.47,  'Cl': 1.75,
    'Br': 1.85, 'I': 1.98
}

# Atomic weights for common elements in PDB files (in g/mol)
ATOMIC_WEIGHTS: Dict[str, float] = {
    "H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999, "P": 30.974, "S": 32.06,
    "Cl": 35.45, "Na": 22.99, "K": 39.10, "Ca": 40.08, "Mg": 24.305, "Fe": 55.845, "F": 19
}

# SMARTS patterns and names for heteroatom detection
HETEROATOM_PATTERNS: Dict[str, str] = {
    "[#7]": "nitrogen",
    "[#8]": "oxygen",
    "[#16]": "sulfur"
}

# SMARTS patterns and names for ring detection
RING_PATTERNS: Dict[str, str] = {
    "[r5]": "5-membered ring",
    "[r6]": "6-membered ring",
    "[r7]": "7-membered ring",
    "[r8]": "8-membered ring"
}

# ============================================================================
# Volume Calculation Functions
# ============================================================================

def vol_from_smiles(smiles: str) -> float:
    """
    Calculate molecular volume from a SMILES string.

    Args:
        smiles: SMILES representation of the molecule.

    Returns:
        Molecular volume in cubic Angstroms.

    Example:
        >>> volume = vol_from_smiles("CC(C)C")
        >>> print(f"Volume: {volume:.2f} cubic Angstroms")
    """
    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(mol)
    volume = AllChem.ComputeMolVolume(mol)
    return volume


def vol_from_mol(mol: Chem.Mol) -> float:
    """
    Calculate molecular volume from an RDKit molecule object.

    Args:
        mol: RDKit Mol object.

    Returns:
        Molecular volume in cubic Angstroms.

    Example:
        >>> mol = Chem.MolFromSmiles("CCO")
        >>> volume = vol_from_mol(mol)
    """
    AllChem.EmbedMolecule(mol)
    volume = AllChem.ComputeMolVolume(mol)
    return volume


def vol_from_pdb(pdb_file: str) -> float:
    """
    Calculate molecular volume from a PDB file.

    Args:
        pdb_file: Path to PDB file.

    Returns:
        Molecular volume in cubic Angstroms.

    Raises:
        ValueError: If molecule cannot be loaded from PDB file.

    Example:
        >>> volume = vol_from_pdb("molecule.pdb")
    """
    mol = Chem.MolFromPDBFile(pdb_file, removeHs=False)
    if mol is None:
        raise ValueError(f"Could not load molecule from PDB file: {pdb_file}")

    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    volume = AllChem.ComputeMolVolume(mol)
    return volume


def estimated_volume(pdb_file_path: str) -> Optional[float]:
    """
    Estimate molecular volume from a PDB file using van der Waals radii.

    Uses the van der Waals radii of atoms to estimate molecular volume
    without relying on RDKit's embedding. Useful for molecules with
    unusual geometries or valence issues.

    Args:
        pdb_file_path: Path to PDB file.

    Returns:
        Estimated volume in cubic Angstroms, or None if loading fails.

    Example:
        >>> volume = estimated_volume("complex_molecule.pdb")
    """
    # Load the PDB file without sanitizing
    mol = Chem.MolFromPDBFile(pdb_file_path, removeHs=False, sanitize=False)

    if not mol:
        return None

    # Try sanitizing, but continue if it fails
    try:
        Chem.SanitizeMol(mol)
    except Exception:
        pass  # Continue with unsanitized molecule

    # Calculate total volume
    total_volume = 0.0

    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        if symbol in VDW_RADII:
            radius = VDW_RADII[symbol]
            atom_volume = (4/3) * math.pi * (radius ** 3)
            total_volume += atom_volume

    return total_volume / 2


def volume_model(temperature: float, a: float, b: float, c: float) -> float:
    """
    Calculate volume from thermal expansion model.

    Uses a polynomial model for predicting material expansion with temperature:
    V(T) = a + b*T + c*T²

    Args:
        temperature: Temperature in appropriate units.
        a: Constant coefficient.
        b: Linear coefficient.
        c: Quadratic coefficient.

    Returns:
        Predicted volume.

    Example:
        >>> volume = volume_model(300, 100, 0.1, 0.001)
    """
    return a + b * temperature + c * temperature ** 2


# ============================================================================
# Molecular Property Detection Functions
# ============================================================================

def has_heteroatoms(mol: Chem.Mol) -> List[str]:
    """
    Identify heteroatoms (N, O, S) present in a molecule.

    Args:
        mol: RDKit Mol object.

    Returns:
        List of heteroatom names found. Returns ["No heteroatoms"] if none found.

    Example:
        >>> mol = Chem.MolFromSmiles("CC(=O)N")
        >>> heteroatoms = has_heteroatoms(mol)
        >>> print(heteroatoms)  # ['oxygen', 'nitrogen']
    """
    heteroatoms_in_mol = []

    for smarts_pattern, heteroatom_name in HETEROATOM_PATTERNS.items():
        pattern_smarts = Chem.MolFromSmarts(smarts_pattern)
        if mol.HasSubstructMatch(pattern_smarts):
            heteroatoms_in_mol.append(heteroatom_name)

    if not heteroatoms_in_mol:
        heteroatoms_in_mol.append("No heteroatoms")

    return heteroatoms_in_mol


def has_rings(mol: Chem.Mol) -> List[str]:
    """
    Identify ring systems in a molecule.

    Detects aromatic and alicyclic rings of sizes 5-8 atoms.

    Args:
        mol: RDKit Mol object.

    Returns:
        List of ring types found. Returns ["N"] if no rings detected.

    Example:
        >>> mol = Chem.MolFromSmiles("c1ccccc1")  # benzene
        >>> rings = has_rings(mol)
        >>> print(rings)  # ['6-membered ring']
    """
    ring_groups_in_mol = []

    for smarts_pattern, ring_name in RING_PATTERNS.items():
        pattern_smarts = Chem.MolFromSmarts(smarts_pattern)
        if mol.HasSubstructMatch(pattern_smarts):
            ring_groups_in_mol.append(ring_name)

    if not ring_groups_in_mol:
        ring_groups_in_mol.append("N")

    return ring_groups_in_mol


# ============================================================================
# File I/O and Format Conversion Functions
# ============================================================================

def pdb_to_mol(pdb_filename: str) -> Optional[Chem.Mol]:
    """
    Convert a PDB file to an RDKit molecule object.

    Reads PDB structure and assigns chiral tags based on 3D geometry.

    Args:
        pdb_filename: Path to PDB file.

    Returns:
        RDKit Mol object, or None if conversion fails.

    Example:
        >>> mol = pdb_to_mol("protein.pdb")
        >>> if mol:
        ...     print(f"Molecule has {mol.GetNumAtoms()} atoms")
    """
    with open(pdb_filename, 'r') as pdb_file:
        pdb_content = pdb_file.read()

    mol = Chem.MolFromPDBBlock(pdb_content)
    if mol is not None:
        AllChem.AssignAtomChiralTagsFromStructure(mol)

    return mol


def smiles_to_pdb(smiles_string: str, output_file: str) -> None:
    """
    Convert a SMILES string to a PDB file with 3D structure.

    Generates 3D coordinates for the molecule and saves as PDB format.
    Requires Open Babel (pybel) to be installed.

    Args:
        smiles_string: SMILES representation of the molecule.
        output_file: Path where PDB file will be written.

    Raises:
        ImportError: If pybel (Open Babel) is not available.

    Example:
        >>> smiles_to_pdb("CC(C)C", "isobutane.pdb")

    Note:
        This function requires Open Babel. Install with:
        conda install -c conda-forge openbabel
    """
    try:
        from openbabel import openbabel as ob
        from openbabel import pybel
    except ImportError:
        raise ImportError(
            "pybel (Open Babel) is required for SMILES to PDB conversion. "
            "Install with: conda install -c conda-forge openbabel"
        )

    # Create a molecule from the SMILES string
    molecule = pybel.readstring("smi", smiles_string)

    # Generate the 3D structure
    molecule.make3D()

    # Convert the molecule to PDB format
    pdb_string = molecule.write("pdb")

    # Write the PDB string to a file
    with open(output_file, "w") as f:
        f.write(pdb_string)


def clean_mol_name(molecule_name: str) -> str:
    """
    Clean molecule name by removing special characters.

    Removes parentheses, spaces, and commas that may be incompatible
    with file systems or simulation software.

    Args:
        molecule_name: Original molecule name.

    Returns:
        Cleaned molecule name.

    Example:
        >>> clean_mol_name("Poly(lactic acid)")
        'PolylacticI'
    """
    chars_to_replace = ["(", ")", " ", ","]
    for char in chars_to_replace:
        molecule_name = molecule_name.replace(char, '')
    return molecule_name


def remove_conect_master_lines(file_path: str) -> None:
    """
    Remove CONECT and MASTER lines from a PDB file.

    These lines are often auto-generated by structure viewers and can
    cause issues with simulation software. Modifies the file in-place.

    Args:
        file_path: Path to PDB file to modify.

    Example:
        >>> remove_conect_master_lines("structure.pdb")
    """
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Filter out lines containing 'CONECT' or 'MASTER'
        filtered_lines = [line for line in lines if not ('CONECT' in line or 'MASTER' in line)]

        # Overwrite the file with the filtered content
        with open(file_path, 'w') as file:
            file.writelines(filtered_lines)
    except Exception as e:
        raise IOError(f"Error processing PDB file {file_path}: {e}")


def write_output(filepath: str, lines: List[str]) -> None:
    """
    Write a list of strings to a file, one per line.

    Args:
        filepath: Path to output file.
        lines: List of strings to write.

    Example:
        >>> write_output("output.txt", ["line 1", "line 2"])
    """
    with open(filepath, "w") as f:
        for line in lines:
            f.write(line)
            f.write('\n')


# ============================================================================
# Quantum Chemistry Analysis Functions
# ============================================================================

def get_homo_lumo_from_xyz(xyz_filepath: str) -> Tuple[int, int]:
    """
    Calculate HOMO and LUMO orbital indices from an XYZ geometry file.

    For a closed-shell molecule, uses the total electron count to determine
    the highest occupied and lowest unoccupied orbital indices.

    Args:
        xyz_filepath: Path to XYZ coordinate file.

    Returns:
        Tuple of (HOMO index, LUMO index).

    Raises:
        KeyError: If unknown atomic symbol is encountered.
        FileNotFoundError: If XYZ file not found.

    Example:
        >>> homo, lumo = get_homo_lumo_from_xyz("geometry.xyz")
        >>> print(f"HOMO={homo}, LUMO={lumo}")
    """
    atomic_numbers = {
        'C': 6, 'H': 1, 'O': 8, 'S': 16, 'F': 9, 'N': 7, 'Cl': 17
    }
    atoms = []

    with open(xyz_filepath, 'r') as xyz_file:
        for i, line in enumerate(xyz_file):
            # Skip the first two lines (header lines)
            if i < 2:
                continue

            # Split the line and extract the atomic symbol
            parts = line.split()
            if parts:  # Ensure the line isn't empty
                atom = parts[0].strip()
                # Verify that the atom is in the atomic_numbers dictionary
                if atom in atomic_numbers:
                    atoms.append(atom)
                else:
                    raise KeyError(f"Unknown atomic symbol '{atom}' in line: {line.strip()}")

    # Calculate the total atomic number and derive HOMO and LUMO indices
    atomic_num = sum(atomic_numbers[atom] for atom in atoms)
    homo_num = int(atomic_num / 2 - 1)
    lumo_num = homo_num + 1
    return homo_num, lumo_num


# ============================================================================
# PDB Parsing and Molecular Weight Functions
# ============================================================================

def get_element_from_pdb_line(line: str) -> Optional[str]:
    """
    Extract atomic element from a PDB file line.

    Uses multiple strategies to robustly identify the element:
    1. Check the standard element column (76-78)
    2. Infer from atomic name if not found

    Args:
        line: Single line from a PDB file.

    Returns:
        Element symbol if found, None otherwise.

    Example:
        >>> line = "ATOM      1  C   ALA A   1      20.154  29.699   5.276  1.00 20.00           C"
        >>> element = get_element_from_pdb_line(line)
    """
    # Try the standard element column first
    element = line[76:78].strip() if len(line) > 77 else ""

    if not element or element not in ATOMIC_WEIGHTS:
        # Extract atomic name (cols 13-16)
        atom_name = line[12:16].strip() if len(line) > 15 else ""

        # Infer element from atomic name (handling multi-character elements like 'CL', 'CA')
        if len(atom_name) >= 1:
            possible_element = (
                atom_name[:2].capitalize()
                if len(atom_name) >= 2 and atom_name[:2].capitalize() in ATOMIC_WEIGHTS
                else atom_name[0].capitalize()
            )

            if possible_element in ATOMIC_WEIGHTS:
                element = possible_element

    return element if element in ATOMIC_WEIGHTS else None


def count_elements_in_pdb(pdb_filepath: str) -> Dict[str, int]:
    """
    Count element occurrences in a PDB file.

    Analyzes ATOM and HETATM records to determine elemental composition.

    Args:
        pdb_filepath: Path to PDB file.

    Returns:
        Dictionary mapping element symbols to counts.

    Example:
        >>> counts = count_elements_in_pdb("protein.pdb")
        >>> print(counts)  # {'C': 1250, 'O': 450, 'N': 200, ...}
    """
    element_counts: Dict[str, int] = {}

    with open(pdb_filepath, "r") as pdb_file:
        for line in pdb_file:
            if line.startswith(("ATOM", "HETATM")):
                element = get_element_from_pdb_line(line)
                if element:
                    element_counts[element] = element_counts.get(element, 0) + 1

    return element_counts


def calculate_molecular_weight(pdb_filepath: str) -> Tuple[float, Dict[str, int]]:
    """
    Calculate molecular weight from a PDB file.

    Sums atomic weights based on elemental composition analysis.

    Args:
        pdb_filepath: Path to PDB file.

    Returns:
        Tuple of (molecular weight in g/mol, element count dictionary).

    Raises:
        FileNotFoundError: If PDB file not found.
        ValueError: If no valid elements found in PDB.

    Example:
        >>> weight, elements = calculate_molecular_weight("molecule.pdb")
        >>> print(f"Molecular weight: {weight:.2f} g/mol")
    """
    if not os.path.exists(pdb_filepath):
        raise FileNotFoundError(f"File '{pdb_filepath}' not found!")

    element_counts = count_elements_in_pdb(pdb_filepath)

    if not element_counts:
        raise ValueError(f"No valid elements found in PDB file: {pdb_filepath}")

    molecular_weight = sum(ATOMIC_WEIGHTS[el] * count for el, count in element_counts.items())

    return molecular_weight, element_counts
