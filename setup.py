"""
Setup configuration for iPHAsimulator package installation.

This file enables installation via pip and makes the package properly discoverable.

Installation:
    pip install -e .  # Install in development mode
    pip install .     # Install normally

Usage:
    After installation, import modules normally:
    >>> from modules.molecule_builder import smiles_to_pdb
    >>> from modules.system_builder import BuildAmberSystems
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iPHAsimulator',
    version='1.1.0',
    description='iPHAsimulator: Build PHA polymer structures and run DFT calculations or MD simulations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel J. York, Isaac Vidal-Daza, Francisco Martin-Martinez',
    author_email='support@martinmartinezlab.com',
    url='https://github.com/MMLabCodes/iPHAsimulator',
    project_urls={
        'Documentation': 'https://github.com/MMLabCodes/iPHAsimulator#readme',
        'Source Code': 'https://github.com/MMLabCodes/iPHAsimulator',
        'Issues': 'https://github.com/MMLabCodes/iPHAsimulator/issues',
    },
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.19.0',
        'pandas>=2.0.0',
        'scipy>=1.7.0',
        'matplotlib>=3.3.0',
        'seaborn>=0.11.0',
        'scikit-learn>=0.24.0',
    ],
    extras_require={
        'simulation': [
            'openmm>=7.7',
            'parmed>=3.3',
            'rdkit>=2021.03',
            'openbabel-wheel>=3.1.1',
            'MDAnalysis>=2.0',
        ],
        'quantum': [
            'nglview>=3.0',
        ],
        'docs': [
            'sphinx>=4.0',
            'sphinx-rtd-theme>=1.0',
        ],
        'dev': [
            'pytest>=6.0',
            'black>=21.0',
            'flake8>=3.9',
            'mypy>=0.900',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Multimedia :: Graphics :: 3D Visualization',
    ],
    keywords=[
        'molecular-dynamics',
        'polymer simulations',
        'biopolymers',
        'pha',
        'polyhydroxyalkanoates',
        'computational-chemistry',
        'openmm',
        'amber',
        'chemistry',
        'biology',
        'molecular-simulation',
    ],
    include_package_data=True,
    zip_safe=False,
)
