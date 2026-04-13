"""
Backward compatibility module for sw_charge_benchmarking.

This module maintains backward compatibility with code that imports from
the old sw_charge_benchmarking module. All functionality has been refactored
into the charge_calculator module with improved organization and type hints.

For new code, import directly from charge_calculator:
    from modules.charge_calculator import ChargeCalculator

For legacy code, this module provides the same exports:
    from modules.sw_charge_benchmarking import benchmark_charges

Deprecated:
    This module is maintained for backward compatibility only.
    New code should import from modules.charge_calculator instead.
"""

from modules.charge_calculator import (
    ChargeCalculator,
    benchmark_charges,
    extract_mol2_charges,
    extract_nagl_charges,
    extract_naglmbis_charges,
)

__all__ = [
    'benchmark_charges',
    'ChargeCalculator',
    'extract_mol2_charges',
    'extract_nagl_charges',
    'extract_naglmbis_charges',
]
