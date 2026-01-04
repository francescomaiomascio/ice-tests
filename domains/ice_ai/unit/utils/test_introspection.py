from __future__ import annotations

import pytest

from ice_ai.utils.introspection import introspect
from ice_ai.version import ICE_AI_VERSION


@pytest.mark.unit
@pytest.mark.domain
def test_introspection_returns_static_snapshot():
    """
    Invariant:
    Introspection must return a static, deterministic snapshot.
    """
    snapshot = introspect()

    assert isinstance(snapshot, dict)
    assert "ice_ai" in snapshot
    assert "agents" in snapshot
    assert "indexes" in snapshot


@pytest.mark.unit
@pytest.mark.domain
def test_introspection_exposes_version_and_agent_count():
    """
    Invariant:
    ICE-AI introspection must expose version and agent_count.
    """
    snapshot = introspect()

    ice_ai = snapshot["ice_ai"]

    assert ice_ai["version"] == ICE_AI_VERSION
    assert isinstance(ice_ai["agent_count"], int)
    assert ice_ai["agent_count"] > 0


@pytest.mark.unit
@pytest.mark.domain
def test_introspection_agents_are_serialized_specs():
    """
    Invariant:
    Agents exposed via introspection are serialized AgentSpec only.
    """
    snapshot = introspect()
    agents = snapshot["agents"]

    assert isinstance(agents, dict)
    assert agents, "Agents registry must not be empty"

    for name, spec in agents.items():
        assert isinstance(name, str)
        assert isinstance(spec, dict)

        # Required spec fields
        assert "name" in spec
        assert "description" in spec
        assert "domains" in spec
        assert "roles" in spec
        assert "capabilities" in spec

        # No runtime leakage
        forbidden_keys = {
            "runner",
            "execute",
            "session",
            "runtime",
            "state",
        }
        assert forbidden_keys.isdisjoint(spec.keys())


@pytest.mark.unit
@pytest.mark.domain
def test_introspection_domain_index_is_consistent():
    """
    Invariant:
    Domain index must list agents by declared domain.
    """
    snapshot = introspect()

    domains = snapshot["indexes"]["domains"]
    agents = snapshot["agents"]

    for domain, names in domains.items():
        assert isinstance(domain, str)
        assert isinstance(names, list)

        for agent_name in names:
            assert agent_name in agents
            assert domain in agents[agent_name]["domains"]


@pytest.mark.unit
@pytest.mark.domain
def test_introspection_role_index_is_consistent():
    """
    Invariant:
    Role index must reflect AgentSpec role flags.
    """
    snapshot = introspect()

    roles = snapshot["indexes"]["roles"]
    agents = snapshot["agents"]

    for role, names in roles.items():
        assert isinstance(role, str)
        assert isinstance(names, list)

        for agent_name in names:
            assert agent_name in agents
            assert agents[agent_name]["roles"].get(role) is True


@pytest.mark.unit
@pytest.mark.domain
def test_introspection_capability_index_is_consistent():
    """
    Invariant:
    Capability index must reflect AgentSpec capabilities.
    """
    snapshot = introspect()

    capabilities = snapshot["indexes"]["capabilities"]
    agents = snapshot["agents"]

    for cap, names in capabilities.items():
        assert isinstance(cap, str)
        assert isinstance(names, list)

        for agent_name in names:
            assert agent_name in agents
            assert cap in agents[agent_name]["capabilities"]


@pytest.mark.unit
@pytest.mark.domain
def test_introspection_is_deterministic():
    """
    Invariant:
    Multiple calls to introspection must return identical data.
    """
    snap_a = introspect()
    snap_b = introspect()

    assert snap_a == snap_b
