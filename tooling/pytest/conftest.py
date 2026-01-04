"""
Global pytest configuration for ICE Tests.

This conftest is intentionally minimal.
It provides:
- canonical marker registration
- strict marker enforcement
- explicit environment loading

No heavy fixtures live here.
"""

import os
import pytest
from pathlib import Path

from tooling.pytest.markers import get_all_markers


# =========================
# MARKER REGISTRATION
# =========================

def pytest_configure(config):
    """
    Register all canonical ICE markers.
    Unknown markers are treated as errors.
    """
    for name, description in get_all_markers().items():
        config.addinivalue_line("markers", f"{name}: {description}")


# =========================
# STRICT MODE
# =========================

def pytest_collection_modifyitems(config, items):
    """
    Enforce that every test has at least:
    - one LEVEL marker
    - one SCOPE marker
    """
    level_markers = {"unit", "integration", "contract", "e2e", "scenario"}
    scope_markers = {"domain", "aggregate", "core", "product"}

    for item in items:
        item_markers = {m.name for m in item.iter_markers()}

        if not (item_markers & level_markers):
            pytest.fail(
                f"Test '{item.nodeid}' has no LEVEL marker "
                f"(one of {sorted(level_markers)})",
                pytrace=False,
            )

        if not (item_markers & scope_markers):
            pytest.fail(
                f"Test '{item.nodeid}' has no SCOPE marker "
                f"(one of {sorted(scope_markers)})",
                pytrace=False,
            )


# =========================
# ENVIRONMENT LOADING
# =========================

def pytest_sessionstart(session):
    """
    Load environment configuration explicitly.

    ICE Tests never rely on implicit environment state.
    """
    env_example = Path(".env.example")
    if env_example.exists():
        # Only informational: real env must be explicit
        session.config._ice_env_example_present = True
