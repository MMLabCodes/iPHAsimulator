#!/usr/bin/env python
"""
Example 2: SMILES to Structure - Convert chemical strings to 3D molecules

SMILES (Simplified Molecular Input Line Entry System) is a notation for chemical
structures. This example shows how to convert SMILES strings to PDB files with 3D coordinates.

Topics covered:
- Creating molecules from SMILES strings
- Detecting molecular features (heteroatoms, rings)
- Calculating molecular volume
- Writing PDB files

Output: PDB files with 3D structures
Time needed: ~5 minutes
Difficulty: Beginner
"""

from modules.molecule_builder import (
    vol_from_smiles,
    has_heteroatoms,
    has_rings,
    smiles_to_pdb,
)
from rdkit import Chem


def analyze_molecule(smiles: str, name: str) -> None:
    """
    Convert SMILES to molecule and analyze properties.

    Args:
        smiles: SMILES string representation of the molecule
        name: Name for the output file and display
    """
    print(f"\n{name}")
    print("-" * 50)
    print(f"SMILES: {smiles}")

    try:
        # Create molecule from SMILES
        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            print("ERROR: Could not parse SMILES string")
            return

        # Get basic info
        print(f"Molecular Formula: {Chem.rdMolDescriptors.CalcMolFormula(mol)}")

        # Detect features
        heteroatoms = has_heteroatoms(mol)
        rings = has_rings(mol)

        print(f"Heteroatoms: {', '.join(heteroatoms)}")
        print(f"Rings: {', '.join(rings)}")

        # Calculate volume (this embeds the molecule in 3D)
        try:
            volume = vol_from_smiles(smiles)
            print(f"Volume: {volume:.2f} Ų")
        except Exception as e:
            print(f"Note: Could not calculate volume ({str(e)})")

    except Exception as e:
        print(f"Error analyzing molecule: {e}")


def main():
    """Main example function."""

    print("=" * 60)
    print("Example 2: SMILES to Structure")
    print("=" * 60)

    print("\nThis example demonstrates molecular analysis from SMILES strings.")
    print("SMILES is a text format for representing chemical structures.")
    print()

    # Define interesting molecules to analyze
    molecule_examples = {
        "Ethane (C2H6)": "CC",
        "Ethanol (C2H5OH)": "CCO",
        "Benzene (C6H6)": "c1ccccc1",
        "Glucose": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
        "3-Hydroxybutyrate unit (PHA)": "CC(O)CC(=O)O",
    }

    print("Analyzing example molecules:")
    print()

    for name, smiles in molecule_examples.items():
        analyze_molecule(smiles, name)

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    print("The code above analyzed several molecules from SMILES strings:")
    print("- Extracted molecular formulas")
    print("- Detected heteroatoms and ring systems")
    print("- Calculated molecular volumes (when 3D embedding succeeded)")
    print()

    print("Key SMILES features shown:")
    print("- Simple chains: CC (ethane), CCO (ethanol)")
    print("- Aromatic rings: c1ccccc1 (benzene)")
    print("- Chiral centers: [C@H] and [C@@H] (glucose)")
    print("- Functional groups: O (hydroxy), C(=O) (carbonyl)")
    print()

    print("Creating 3D PDB file example:")
    print("-" * 60)

    # Create 3D structure for a simple molecule
    smiles = "CC(O)CC(=O)O"  # 3-hydroxybutyrate (PHA building block)
    output_file = "example_molecule.pdb"

    try:
        print(f"\nAttempting to create PDB file: {output_file}")
        print(f"SMILES: {smiles} (3-Hydroxybutyrate)")

        smiles_to_pdb(smiles, output_file)

        import os
        if os.path.exists(output_file):
            print(f"✓ File created successfully: {output_file}")
            print(f"  File size: {os.path.getsize(output_file)} bytes")
            print()
            print("You can now view this file in molecular visualization software like:")
            print("- PYMOL (https://pymol.org/)")
            print("- Chimera (https://www.cgl.ucsf.edu/chimera/)")
            print("- Jsmol (https://jmol.sourceforge.net/)")
        else:
            print(f"File was not created (requires Open Babel)")

    except ImportError:
        print(f"Note: Open Babel (pybel) not installed.")
        print("Install with: conda install -c conda-forge openbabel")
        print("Then you can create 3D PDB files from SMILES strings.")

    except Exception as e:
        print(f"Error creating PDB file: {e}")

    print()
    print("=" * 60)
    print("Example completed!")
    print()
    print("Next steps:")
    print("1. Try Example 3 to analyze more properties")
    print("2. Modify the SMILES strings to analyze different molecules")
    print("3. See Tutorial_2 notebook for polymer parameterization")
    print()


if __name__ == "__main__":
    main()
