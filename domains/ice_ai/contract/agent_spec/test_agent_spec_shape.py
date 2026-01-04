"""
Contract tests for AgentSpec shape.

This module defines the PUBLIC, STABLE contract of ice_ai.agents.spec.AgentSpec.

These tests MUST NOT change unless a deliberate breaking change
is introduced and versioned.

No runtime logic.
No agent execution.
Pure structural contract.
"""

from __future__ import annotations

import pytest
from dataclasses import is_dataclass, FrozenInstanceError

from ice_ai.agents.spec import AgentSpec


# ============================================================
# MARKERS
# ============================================================

pytestmark = [
    pytest.mark.contract,
    pytest.mark.domain,
]


# ============================================================
# SHAPE & IDENTITY
# ============================================================

def test_agent_spec_is_frozen_dataclass():
    """
    Invariant:
    AgentSpec must be an immutable (frozen) dataclass.
    """
    assert is_dataclass(AgentSpec)
    assert AgentSpec.__dataclass_params__.frozen is True


def test_agent_spec_required_fields_exist():
    """
    Invariant:
    AgentSpec exposes a stable set of required fields.
    """
    field_names = {f.name for f in AgentSpec.__dataclass_fields__.values()}

    expected = {
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

    assert expected.issubset(field_names)


# ============================================================
# DOMAIN CONTRACT
# ============================================================

def test_agent_spec_domains_is_non_empty_set():
    """
    Invariant:
    domains must be a non-empty set of strings.
    """
    spec = AgentSpec(
        name="test",
        description="test agent",
        domains={"test"},
    )

    assert isinstance(spec.domains, set)
    assert len(spec.domains) > 0
    assert all(isinstance(d, str) for d in spec.domains)


# ============================================================
# ROLE FLAGS COHERENCE
# ============================================================

def test_agent_spec_role_flags_are_boolean():
    """
    Invariant:
    Role flags are explicit booleans.
    """
    spec = AgentSpec(
        name="test",
        description="test agent",
        domains={"test"},
        is_planner=True,
        is_executor=False,
        is_observer=False,
        is_system=False,
    )

    assert isinstance(spec.is_planner, bool)
    assert isinstance(spec.is_executor, bool)
    assert isinstance(spec.is_observer, bool)
    assert isinstance(spec.is_system, bool)


# ============================================================
# IMMUTABILITY
# ============================================================

def test_agent_spec_is_immutable():
    """
    Invariant:
    Any attempt to mutate an AgentSpec must fail.
    """
    spec = AgentSpec(
        name="immutable",
        description="immutable agent",
        domains={"test"},
    )

    with pytest.raises(FrozenInstanceError):
        spec.name = "mutated"


# ============================================================
# SERIALIZATION CONTRACT
# ============================================================

def test_agent_spec_to_dict_shape_is_stable():
    """
    Invariant:
    to_dict() returns a stable, JSON-serializable structure.
    """
    spec = AgentSpec(
        name="serialize",
        description="serialization agent",
        domains={"a", "b"},
        is_planner=True,
        capabilities={"cap1", "cap2"},
        version="1.0",
        ui_label="SerializeAgent",
        ui_group="core",
    )

    data = spec.to_dict()

    assert isinstance(data, dict)

    expected_keys = {
        "name",
        "description",
        "domains",
        "roles",
        "capabilities",
        "version",
        "experimental",
        "deprecated",
        "ui",
    }

    assert expected_keys == set(data.keys())

    assert isinstance(data["domains"], list)
    assert isinstance(data["capabilities"], list)
    assert isinstance(data["roles"], dict)
    assert isinstance(data["ui"], dict)


# ============================================================
# BACKWARD COMPATIBILITY GUARD
# ============================================================

def test_agent_spec_to_dict_contains_no_runtime_fields():
    """
    Invariant:
    to_dict() MUST NOT expose runtime or execution details.
    """
    spec = AgentSpec(
        name="guard",
        description="guard agent",
        domains={"test"},
    )

    forbidden = {
        "runner",
        "session",
        "context",
        "state",
        "execute",
        "run",
    }

    data = spec.to_dict()
    assert forbidden.isdisjoint(data.keys())
