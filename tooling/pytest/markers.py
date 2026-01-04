"""
Canonical pytest markers for the ICE test ecosystem.

This file defines the only allowed semantic markers.
Any test using undeclared or ambiguous markers is invalid.

Markers encode TEST INTENT, not implementation detail.
"""

# =========================
# LEVEL MARKERS
# =========================

LEVEL_MARKERS = {
    "unit": "Unit-level tests (pure logic, no IO, no environment)",
    "integration": "Integration tests within a domain or aggregate",
    "contract": "Contract and compatibility tests (schemas, protocols)",
    "e2e": "End-to-end tests with real processes and state",
    "scenario": "Scenario-based tests describing meaningful workflows",
}

# =========================
# SCOPE MARKERS
# =========================

SCOPE_MARKERS = {
    "domain": "Domain-scoped tests (single ICE domain)",
    "aggregate": "Aggregate-scoped tests (multiple cooperating domains)",
    "core": "ICE core platform tests",
    "product": "Product-level tests (user-facing applications)",
}

# =========================
# EXECUTION MARKERS
# =========================

EXECUTION_MARKERS = {
    "slow": "Slow tests (explicitly opt-in)",
    "destructive": "Tests that modify or destroy state",
    "requires_network": "Tests requiring network access",
    "requires_gpu": "Tests requiring GPU availability",
}

# =========================
# ALL MARKERS (FLATTENED)
# =========================

ALL_MARKERS = {
    **LEVEL_MARKERS,
    **SCOPE_MARKERS,
    **EXECUTION_MARKERS,
}


def get_all_markers():
    """
    Returns all canonical ICE pytest markers.

    Used by conftest.py to register markers and enforce strictness.
    """
    return ALL_MARKERS
