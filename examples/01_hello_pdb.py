#!/usr/bin/env python
"""
Example 1: Hello PDB - Load and inspect a PDB file

This is the simplest example - it shows how to load a molecular structure
from a PDB file and extract basic information.

Topics covered:
- Loading PDB files
- Extracting molecular information
- Calculating molecular weight
- Counting atoms and residues

Output: Basic information about the loaded molecule
Time needed: ~2 minutes
Difficulty: Beginner
"""

from modules.molecule_builder import calculate_molecular_weight, count_elements_in_pdb
import os

def main():
    """Main example function."""

    print("=" * 60)
    print("Example 1: Hello PDB - Load and Inspect Structures")
    print("=" * 60)
    print()

    # Look for existing PDB files in the repo
    pdb_dir = "pdb_files/molecules"

    if not os.path.exists(pdb_dir):
        print(f"Note: PDB directory '{pdb_dir}' not found in repository.")
        print("This example demonstrates how to work with PDB files.")
        print()
        print("To use this example, ensure you have:")
        print("1. A PDB file from the repository, or")
        print("2. Run 02_smiles_to_structure.py first to create a PDB file")
        print()
        print("Example PDB path: pdb_files/molecules/3HB_monomer/3HB_monomer.pdb")
        print()

        # Create a demo that shows what the code would do
        print("Demo (without actual PDB file):")
        print("-" * 60)
        print("If we had a PDB file at 'demo.pdb', we would:")
        print()
        print("  # Count elements in the molecule")
        print("  element_counts = count_elements_in_pdb('demo.pdb')")
        print("  print(f'Atoms: {element_counts}')")
        print()
        print("  # Calculate molecular weight")
        print("  weight, elements = calculate_molecular_weight('demo.pdb')")
        print("  print(f'Molecular weight: {weight:.2f} g/mol')")
        print()
        return

    # Find the first PDB file in the directory
    print(f"Searching for PDB files in {pdb_dir}...")
    print()

    pdb_files = []
    for root, dirs, files in os.walk(pdb_dir):
        for file in files:
            if file.endswith(".pdb"):
                pdb_files.append(os.path.join(root, file))

    if not pdb_files:
        print("No PDB files found. Please create one with Example 2.")
        return

    # Analyze the first PDB file
    pdb_file = pdb_files[0]
    print(f"Found PDB file: {pdb_file}")
    print()
    print("Analyzing structure...")
    print("-" * 60)

    try:
        # Count elements
        element_counts = count_elements_in_pdb(pdb_file)
        print(f"\nAtomic Composition:")
        for element, count in sorted(element_counts.items()):
            print(f"  {element}: {count} atoms")

        # Calculate molecular weight
        weight, elements = calculate_molecular_weight(pdb_file)
        print(f"\nMolecular Weight: {weight:.2f} g/mol")

        total_atoms = sum(element_counts.values())
        print(f"Total Atoms: {total_atoms}")

    except Exception as e:
        print(f"Error analyzing PDB file: {e}")
        print("Make sure the PDB file is correctly formatted.")
        return

    print()
    print("=" * 60)
    print("Example completed successfully!")
    print()
    print("Next steps:")
    print("1. Modify pdb_file variable to analyze different structures")
    print("2. Try Example 2 to create structures from SMILES strings")
    print("3. See other examples for polymer building and simulations")
    print()


if __name__ == "__main__":
    main()
