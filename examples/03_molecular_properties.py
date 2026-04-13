#!/usr/bin/env python
"""
Example 3: Molecular Properties - Analyze molecular features

This example demonstrates analysis of molecular properties including
heteroatoms, ring systems, and structural features that are important
for understanding polymer behavior.

Topics covered:
- Detecting heteroatoms (N, O, S)
- Detecting ring systems (5,6,7,8-membered rings)
- Understanding molecular structure
- Comparing different molecules

Output: Detailed analysis of molecular features
Time needed: ~5 minutes
Difficulty: Beginner
"""

from rdkit import Chem
from modules.molecule_builder import has_heteroatoms, has_rings


def analyze_features(smiles_dict: dict) -> None:
    """
    Analyze molecular features for a set of SMILES strings.

    Args:
        smiles_dict: Dictionary of {name: smiles} pairs
    """

    print("Molecular Feature Analysis")
    print("=" * 70)
    print()
    print(f"{'Molecule':<25} {'Formula':<12} {'Heteroatoms':<20} {'Rings':<20}")
    print("-" * 70)

    for name, smiles in smiles_dict.items():
        try:
            mol = Chem.MolFromSmiles(smiles)

            if mol is None:
                print(f"{name:<25} ERROR parsing SMILES")
                continue

            # Get formula
            formula = Chem.rdMolDescriptors.CalcMolFormula(mol)

            # Analyze features
            heteroatoms = has_heteroatoms(mol)
            rings = has_rings(mol)

            # Format heteroatoms
            heteroatom_str = ", ".join(heteroatoms)
            if heteroatom_str == "No heteroatoms":
                heteroatom_str = "None"

            # Format rings
            ring_str = ", ".join(rings)
            if ring_str == "N":
                ring_str = "None"

            print(
                f"{name:<25} {formula:<12} {heteroatom_str:<20} {ring_str:<20}"
            )

        except Exception as e:
            print(f"{name:<25} Error: {str(e)[:40]}")

    print()


def main():
    """Main example function."""

    print("=" * 70)
    print("Example 3: Molecular Properties")
    print("=" * 70)
    print()

    print("This example analyzes molecular features that are important for")
    print("understanding how molecules interact and behave in simulations.")
    print()

    # Organic compounds (no heteroatoms)
    organic_compounds = {
        "Methane": "C",
        "Octane": "CCCCCCCC",
        "Benzene": "c1ccccc1",
        "Naphthalene": "c1ccc2ccccc2c1",
    }

    print("\n1. Organic compounds (hydrocarbons)")
    print("-" * 70)
    analyze_features(organic_compounds)

    # Compounds with heteroatoms
    heteroatom_compounds = {
        "Methanol": "CO",
        "Aniline": "Nc1ccccc1",
        "Pyridine": "c1ccncc1",
        "Thiophene": "c1ccsc1",
        "Furfural": "O=Cc1cccoc1",
    }

    print("\n2. Compounds with heteroatoms")
    print("-" * 70)
    analyze_features(heteroatom_compounds)

    # PHA-related compounds
    pha_compounds = {
        "3-Hydroxybutyrate (PHA)": "CC(O)CC(=O)O",
        "3-Hydroxyvalerate (PHA)": "CCC(O)CC(=O)O",
        "3-Hydroxyhexanoate (PHA)": "CCCC(O)CC(=O)O",
        "Lactic acid": "CC(O)C(=O)O",
    }

    print("\n3. PHA (Polyhydroxyalkanoate) building blocks")
    print("-" * 70)
    analyze_features(pha_compounds)

    print("=" * 70)
    print("Analysis Complete!")
    print()
    print("Key observations:")
    print("- Hydrocarbons contain only C and H atoms (no heteroatoms)")
    print("- Aromatic rings enable π-electron conjugation")
    print("- Heteroatoms (N, O, S) create polar sites for interactions")
    print("- PHA building blocks contain oxygen (C=O and OH groups)")
    print()
    print("These features affect:")
    print("- How molecules pack and organize in solution")
    print("- Interactions with solvents and other molecules")
    print("- Polymer chain flexibility and mechanical properties")
    print("- Degradation mechanisms and environmental behavior")
    print()
    print("=" * 70)
    print("Example completed!")
    print()
    print("Next steps:")
    print("1. Try Examples 1 and 2 to load and create molecules")
    print("2. See Tutorial_2 for parameterization workflows")
    print("3. See Tutorial_4 for building complete polymer systems")
    print()


if __name__ == "__main__":
    main()
