"""
Backward compatibility tests for AgentSpec.

These tests ensure that the public AgentSpec contract
cannot be changed accidentally.

Any failure here requires:
- explicit version bump
- documented migration
"""

from __future__ import annotations

import pytest

from ice_ai.agents.spec import AgentSpec


# ============================================================
# MARKERS
# ============================================================

pytestmark = [
    pytest.mark.contract,
    pytest.mark.domain,
]


# ============================================================
# FIELD STABILITY
# ============================================================

def test_agent_spec_field_names_are_backward_compatible():
    """
    Invariant:
    Existing AgentSpec field names MUST NOT be removed or renamed.
    New fields may be added, but removals are breaking changes.
    """
    current_fields = {
        f.name for f in AgentSpec.__dataclass_fields__.values()
    }

    # 🔒 CANONICAL FIELD SET (DO NOT EDIT LIGHTLY)
    canonical_fields = {
        "name",
        "description",
        "domains",
        "is_planner",
        "is_executor",
        "is_observer",
        "is_system",
        "capabilities",
        "version",
        "experimental",
        "deprecated",
        "ui_label",
        "ui_group",
    }

    assert canonical_fields.issubset(current_fields)


# ============================================================
# ROLE DICT STABILITY
# ============================================================

def test_agent_spec_roles_dict_keys_are_stable():
    """
    Invariant:
    The roles dictionary returned by to_dict()
    exposes a stable set of keys.
    """
    spec = AgentSpec(
        name="roles",
        description="roles agent",
        domains={"test"},
        is_planner=True,
        is_executor=True,
        is_observer=False,
        is_system=False,
    )

    roles = spec.to_dict()["roles"]

    assert set(roles.keys()) == {
        "planner",
        "executor",
        "observer",
        "system",
    }


# ============================================================
# UI BLOCK STABILITY
# ============================================================

def test_agent_spec_ui_block_is_always_present():
    """
    Invariant:
    The 'ui' block must always exist, even if empty.
    """
    spec = AgentSpec(
        name="ui",
        description="ui agent",
        domains={"test"},
    )

    data = spec.to_dict()

    assert "ui" in data
    assert isinstance(data["ui"], dict)
    assert set(data["ui"].keys()) == {"label", "group"}


# ============================================================
# CAPABILITIES TYPE GUARANTEE
# ============================================================

def test_agent_spec_capabilities_serialized_as_list():
    """
    Invariant:
    Capabilities are always serialized as a list of strings.
    """
    spec = AgentSpec(
        name="caps",
        description="caps agent",
        domains={"test"},
        capabilities={"a", "b", "c"},
    )

    data = spec.to_dict()

    assert isinstance(data["capabilities"], list)
    assert all(isinstance(c, str) for c in data["capabilities"])


# ============================================================
# VERSION FIELD GUARANTEE
# ============================================================

def test_agent_spec_version_field_is_optional_but_present():
    """
    Invariant:
    The version field must always be present in serialization,
    even if its value is None.
    """
    spec = AgentSpec(
        name="versioned",
        description="version agent",
        domains={"test"},
    )

    data = spec.to_dict()

    assert "version" in data
