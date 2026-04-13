"""
Configuration Module - Paths and External Tool Configuration.

This module manages configuration for external tools and file paths used by
iPHAsimulator. Tool paths can be set via environment variables, a JSON config
file, or by calling create_config_file() once.

Environment Variables (checked in priority order):
    IPHSIMULATOR_CONFIG   : Path to a JSON config file (overrides all other vars)
    PACKMOL_PATH          : Path to the packmol executable
    AMBER_HOME            : Path to your AmberTools installation directory
    ORCA_PATH             : Path to the ORCA quantum chemistry executable
    NAGLMBIS_DIR          : Directory containing NAGL MBIS scripts
    IPHSIMULATOR_MBIS     : Path to the MBIS calculation script

One-time setup (run once, saves to a JSON file):
    >>> from modules.config import create_config_file
    >>> create_config_file(packmol_path='/usr/local/bin/packmol')

Runtime usage:
    >>> from modules.config import get_packmol_path, get_amber_home
    >>> packmol = get_packmol_path()   # returns path string or None
    >>> amber   = get_amber_home()     # returns AMBER_HOME path or None
"""

import os
import json
from typing import Dict, Optional, Any
from pathlib import Path

# Default configuration - user should override via environment variables
_DEFAULT_CONFIG = {
    "packmol_path": None,  # Must be set by user
    "amber_home": os.environ.get("AMBER_HOME", None),
    "orca_path": os.environ.get("ORCA_PATH", None),
    "naglmbis_dir": os.environ.get("NAGLMBIS_DIR", None),
    "mbis_script_path": os.environ.get("IPHSIMULATOR_MBIS", None),
}

_config: Optional[Dict[str, Any]] = None


def _load_config() -> Dict[str, Any]:
    """Load configuration from environment and config file if available."""
    config = _DEFAULT_CONFIG.copy()

    # Check for explicit PACKMOL_PATH environment variable
    if "PACKMOL_PATH" in os.environ:
        config["packmol_path"] = os.environ["PACKMOL_PATH"]

    # Check for config file
    config_file = os.environ.get("IPHSIMULATOR_CONFIG")
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")

    return config


def get_config() -> Dict[str, Any]:
    """Get the current configuration dictionary."""
    global _config
    if _config is None:
        _config = _load_config()
    return _config


def reset_config() -> None:
    """Reset configuration (useful for testing)."""
    global _config
    _config = None


def set_config_value(key: str, value: Optional[str]) -> None:
    """Set a specific configuration value at runtime.

    Args:
        key: Configuration key (e.g., 'packmol_path')
        value: Path or value to set
    """
    global _config
    if _config is None:
        _config = _load_config()
    _config[key] = value


def get_packmol_path() -> str:
    """Get path to packmol executable.

    Raises:
        ValueError: If packmol path is not configured or file not found
    """
    config = get_config()
    path = config.get("packmol_path")

    if not path:
        raise ValueError(
            "Packmol path not configured. Set PACKMOL_PATH environment variable or "
            "use set_config_value('packmol_path', '/path/to/packmol')"
        )

    if not os.path.exists(path):
        raise ValueError(f"Packmol path does not exist: {path}")

    return path


def get_amber_home() -> str:
    """Get path to AmberTools installation.

    Raises:
        ValueError: If AMBER_HOME is not set
    """
    config = get_config()
    path = config.get("amber_home")

    if not path:
        raise ValueError(
            "AmberTools path not configured. Set AMBER_HOME environment variable"
        )

    return path


def get_mbis_script_path() -> str:
    """Get path to MBIS calculation script.

    Raises:
        ValueError: If MBIS script path is not configured
    """
    config = get_config()
    path = config.get("mbis_script_path")

    if not path:
        raise ValueError(
            "MBIS script path not configured. Set IPHSIMULATOR_MBIS "
            "environment variable"
        )

    if not os.path.exists(path):
        raise ValueError(f"MBIS script not found: {path}")

    return path


def get_naglmbis_dir() -> str:
    """Get path to NAGL MBIS directory.

    Raises:
        ValueError: If NAGL MBIS directory is not configured
    """
    config = get_config()
    path = config.get("naglmbis_dir")

    if not path:
        raise ValueError(
            "NAGL MBIS directory not configured. Set NAGLMBIS_DIR environment variable"
        )

    if not os.path.exists(path):
        raise ValueError(f"NAGL MBIS directory not found: {path}")

    return path


def create_config_file(path: str, overwrite: bool = False) -> None:
    """Create a configuration template file.

    Args:
        path: Path where to save the config file
        overwrite: If True, overwrite existing file
    """
    if os.path.exists(path) and not overwrite:
        raise FileExistsError(f"Config file already exists: {path}")

    template = {
        "packmol_path": "/path/to/packmol/executable",
        "amber_home": "/path/to/ambertools",
        "orca_path": "/path/to/orca",
        "naglmbis_dir": "/path/to/naglmbis",
        "mbis_script_path": "/path/to/calculate_mbis.sh"
    }

    with open(path, 'w') as f:
        json.dump(template, f, indent=2)

    print(f"Config template created at: {path}")
    print("Please edit the file with your actual paths")


if __name__ == "__main__":
    # Print current configuration for debugging
    config = get_config()
    print("Current Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
