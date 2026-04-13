"""
DFT input file generation for quantum chemistry calculations.

This module provides utilities for generating ORCA DFT input files
with configurable computational parameters. It handles the generation
of input files from XYZ coordinate files with customizable basis sets,
functionals, and computational options.

Example:
    Generate a DFT input file::

        from modules.input_generator import DFTInputGenerator

        # Configure parameters
        DFTInputGenerator.set_functional("B3LYP")
        DFTInputGenerator.set_basis_set("def2-TZVP")
        DFTInputGenerator.set_nprocs(10)

        # Generate input file
        input_text = DFTInputGenerator.generate_input(
            xyz_filepath='/path/to/molecule.xyz',
            input_filepath='/path/to/molecule.inp',
            filename='molecule'
        )

Note:
    This module requires that XYZ coordinate files include HOMO/LUMO
    information which is extracted using get_homo_lumo_from_xyz().
"""

from typing import Tuple, Optional
import os

try:
    from modules.sw_basic_functions import get_homo_lumo_from_xyz
except ImportError:
    get_homo_lumo_from_xyz = None

__all__ = [
    'DFTInputGenerator',
    'DFT_input_generator',  # Legacy alias
]


# ============================================================================
# DFTInputGenerator Class
# ============================================================================

class DFTInputGenerator:
    """
    Generator for ORCA DFT quantum chemistry input files.

    This class provides configuration and generation of ORCA input files
    for DFT calculations. It uses a template-based approach with support
    for various basis sets, functionals, and computational options.

    Class Attributes:
        dft_template (str): Template string for ORCA input files.
        functional (str): Functional for DFT calculation (default: B3LYP).
        basis_set (str): Basis set for calculation (default: def2-tzvp).
        dispersion_correction (bool): Apply D3BJ dispersion correction.
        keepdens (bool): Keep density files after calculation.
        opt (bool): Perform geometry optimization.
        resp (bool): Generate RESP charges.
        nprocs (int): Number of processors to use (default: 10).
    """

    # ORCA input file template with placeholders
    dft_template: str = """
    {keywords}
    %scf
        MaxIter 1000
    end
    %output
        Print[ P_Hirshfeld] 1
    end
    %elprop
        Polar 1
    end
    %plots
        dim1 100
        dim2 100
        dim3 100
        Format Gaussian_Cube
        ElDens("{dens_file}");
        MO("{homo_file}", {homo_index}, 0);
        MO("{lumo_file}", {lumo_index}, 0);
    end
    %pal
        nprocs {nprocs}
    end
    *xyzfile 0 1 {xyz_filename}
    """

    # Class configuration parameters
    functional: str = "B3LYP"
    dispersion_correction: bool = True
    basis_set: str = "def2-tzvp"
    keepdens: bool = True
    opt: bool = True
    resp: bool = False
    nprocs: int = 10

    def __init__(self) -> None:
        """
        Initialize DFTInputGenerator.

        Note:
            This class uses only class methods and should not be instantiated.
            Use class methods directly: DFTInputGenerator.generate_input()
        """
        pass

    @classmethod
    def generate_input(
        cls,
        xyz_filepath: str,
        input_filepath: str,
        filename: str
    ) -> str:
        """
        Generate ORCA DFT input file from XYZ coordinates.

        Creates an ORCA input file based on the current class configuration,
        extracting HOMO/LUMO indices from the XYZ file and filling in the
        template with appropriate keywords and file references.

        Args:
            xyz_filepath: Path to the XYZ coordinate file.
                         Must contain HOMO/LUMO information.
            input_filepath: Path where the input file will be written.
            filename: Base filename (without extension) for cube files.

        Returns:
            Generated input file content as string.

        Raises:
            FileNotFoundError: If xyz_filepath does not exist.
            RuntimeError: If HOMO/LUMO extraction fails.

        Example:
            >>> content = DFTInputGenerator.generate_input(
            ...     '/path/to/mol.xyz',
            ...     '/path/to/mol.inp',
            ...     'mol'
            ... )
            >>> print(f"Generated {len(content)} characters of input")
        """
        if get_homo_lumo_from_xyz is None:
            raise RuntimeError("get_homo_lumo_from_xyz function not available")

        # Extract HOMO/LUMO indices from XYZ file
        homo_index, lumo_index = get_homo_lumo_from_xyz(xyz_filepath)

        # Build keyword string based on configuration
        keywords: str = f"!{cls.functional}"

        if cls.dispersion_correction:
            keywords += " D3BJ"

        keywords += (" " + cls.basis_set)

        if cls.opt:
            keywords += " Opt"

        if cls.resp:
            keywords += " chelpg"

        # Fill template with parameters
        template_filled: str = cls.dft_template.format(
            keywords=keywords,
            dens_file=filename + ".dens.cube",
            homo_file=filename + ".homo.cube",
            lumo_file=filename + ".lumo.cube",
            homo_index=homo_index,
            lumo_index=lumo_index,
            nprocs=cls.nprocs,
            xyz_filename=filename + ".xyz"
        )

        # Write to file
        with open(input_filepath, 'w') as file:
            file.writelines(template_filled)

        return template_filled

    @classmethod
    def set_opt(cls, opt: bool) -> None:
        """
        Enable or disable geometry optimization.

        Args:
            opt: True to enable optimization, False to disable.

        Raises:
            TypeError: If opt is not a boolean.

        Example:
            >>> DFTInputGenerator.set_opt(True)
            Geometry optimization will be executed.
        """
        if not isinstance(opt, bool):
            print("Please provide True or False.")
            return

        cls.opt = opt

        if opt:
            print("Geometry optimization will be executed.")
        else:
            print("No geometry optimization will be executed.")

    @classmethod
    def set_resp(cls, resp: bool) -> None:
        """
        Enable or disable RESP charge generation.

        Args:
            resp: True to enable RESP, False to disable.

        Raises:
            TypeError: If resp is not a boolean.

        Example:
            >>> DFTInputGenerator.set_resp(True)
            Resp file will be generated.
        """
        if not isinstance(resp, bool):
            print("Please provide True or False.")
            return

        cls.resp = resp

        if resp:
            print("Resp file will be generated.")
        else:
            print("No resp file will be generated.")

    @classmethod
    def set_functional(cls, functional: str) -> None:
        """
        Set the DFT functional for calculations.

        Currently only HF is in the whitelist beyond default B3LYP.
        Invalid functionals fall back to B3LYP.

        Args:
            functional: Name of the functional (e.g., 'B3LYP', 'HF').

        Example:
            >>> DFTInputGenerator.set_functional("B3LYP")
            >>> # Or attempt custom functional
            >>> DFTInputGenerator.set_functional("PBE")
            Functional not accepted. Using B3LYP as default.
        """
        list_of_accepted_functionals: list = ["HF"]

        if functional in list_of_accepted_functionals:
            print(f"Functional set to {functional}")
            cls.functional = functional
        else:
            print("Functional not accepted. Using B3LYP as default.")

    @classmethod
    def set_dispersion_correction(cls, dispersion_correction: bool) -> None:
        """
        Enable or disable D3BJ dispersion correction.

        Args:
            dispersion_correction: True to enable D3BJ, False to disable.

        Raises:
            TypeError: If dispersion_correction is not a boolean.

        Example:
            >>> DFTInputGenerator.set_dispersion_correction(True)
            Disperion correction will be applied.
        """
        if not isinstance(dispersion_correction, bool):
            print("Please provide True or False")
            return

        cls.dispersion_correction = dispersion_correction

        if dispersion_correction:
            print("Dispersion correction will be applied.")
        else:
            print("Dispersion correction will not be applied.")

    @classmethod
    def set_basis_set(cls, basis_set: str) -> None:
        """
        Set the basis set for calculations.

        Currently only 6-31G* is in the whitelist beyond default def2-tzvp.
        Invalid basis sets fall back to def2-tzvp.

        Args:
            basis_set: Name of the basis set (e.g., 'def2-tzvp', '6-31G*').

        Example:
            >>> DFTInputGenerator.set_basis_set("def2-TZVP")
        """
        list_of_accepted_basis_sets: list = ["6-31G*"]

        if basis_set in list_of_accepted_basis_sets:
            print(f"Basis set set to {basis_set}")
            cls.basis_set = basis_set
        else:
            print("Basis set not accepted. Using def2-tzvp as default.")

    @classmethod
    def set_nprocs(cls, nprocs: int) -> None:
        """
        Set the number of processors for parallel calculations.

        Args:
            nprocs: Number of processors to use.

        Example:
            >>> DFTInputGenerator.set_nprocs(16)
        """
        cls.nprocs = nprocs

    @classmethod
    def print_parameters(cls) -> None:
        """
        Print current DFT calculation parameters.

        Displays all configuration options currently set for the generator.

        Example:
            >>> DFTInputGenerator.print_parameters()
            Current parameters of DFT_input_generator:
            Functional: B3LYP
            Basis set: def2-tzvp
            Geometry optimization: True
            Dispersion correction: True
        """
        print("Current parameters of DFT_input_generator:")
        print(f"Functional: {cls.functional}")
        print(f"Basis set: {cls.basis_set}")
        print(f"Geometry optimization: {cls.opt}")
        print(f"Dispersion correction: {cls.dispersion_correction}")


# Legacy alias for backward compatibility
DFT_input_generator = DFTInputGenerator
