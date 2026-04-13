"""
Backward compatibility module for sw_complex_fluid_models.

This module maintains backward compatibility with code that imports from
the old sw_complex_fluid_models module. All functionality has been refactored
into the complex_fluid_models_refactored module with improved organization
and type hints.

For new code, import directly from complex_fluid_models_refactored:
    from modules.complex_fluid_models_refactored import ComplexFluidModels

For legacy code, this module provides the same exports:
    from modules.sw_complex_fluid_models import complex_fluid_models

Deprecated:
    This module is maintained for backward compatibility only.
    New code should import from modules.complex_fluid_models_refactored instead.
"""

from modules.complex_fluid_models_refactored import (
    ComplexFluidModel,
    ComplexFluidModels,
    ComplexFluidModelBuilder,
    complex_fluid_model,
    complex_fluid_models,
    complex_fluid_model_builder,
)

__all__ = [
    'complex_fluid_model',
    'complex_fluid_models',
    'complex_fluid_model_builder',
    'ComplexFluidModel',
    'ComplexFluidModels',
    'ComplexFluidModelBuilder',
]
