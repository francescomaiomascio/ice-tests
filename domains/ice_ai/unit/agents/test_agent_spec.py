import pytest
from dataclasses import FrozenInstanceError

from ice_ai.agents.spec import AgentSpec


# ============================================================================
# INVARIANTI FONDAMENTALI — AgentSpec
#
# Questo file definisce i vincoli NON NEGOZIABILI dell'entità AgentSpec.
# Se uno di questi test fallisce, il codice è sbagliato, non il test.
# ============================================================================


@pytest.mark.unit
@pytest.mark.domain
def test_agent_spec_is_immutable():
    """
    Invariant:
    An AgentSpec must be immutable once defined.

    Rationale:
    AgentSpec rappresenta un contratto cognitivo statico.
    Se mutabile, il routing, la validazione e l'introspezione
    diventano non deterministici.
    """
    spec = AgentSpec(
        name="test-agent",
        description="Test agent",
        domains={"test"},
    )

    with pytest.raises(FrozenInstanceError):
        spec.name = "other-name"


@pytest.mark.unit
@pytest.mark.domain
def test_agent_spec_requires_name_description_and_domains():
    """
    Invariant:
    An AgentSpec must declare:
    - a name
    - a description
    - at least one domain
    """
    spec = AgentSpec(
        name="minimal-agent",
        description="Minimal valid agent",
        domains={"core"},
    )

    assert spec.name
    assert spec.description
    assert isinstance(spec.domains, set)
    assert len(spec.domains) >= 1


@pytest.mark.unit
@pytest.mark.domain
def test_agent_spec_domains_are_a_set_of_strings():
    """
    Invariant:
    domains must be a set[str].

    Rationale:
    Domains are used for routing and filtering.
    Order must not matter and duplicates must be impossible.
    """
    spec = AgentSpec(
        name="domain-agent",
        description="Agent with domains",
        domains={"code", "analysis"},
    )

    assert isinstance(spec.domains, set)
    for domain in spec.domains:
        assert isinstance(domain, str)


@pytest.mark.unit
@pytest.mark.domain
def test_agent_spec_roles_are_boolean_flags():
    """
    Invariant:
    Role fields are explicit boolean flags.
    No implicit role inference is allowed.
    """
    spec = AgentSpec(
        name="role-agent",
        description="Agent with roles",
        domains={"system"},
        is_planner=True,
        is_executor=False,
        is_observer=True,
        is_system=False,
    )

    assert isinstance(spec.is_planner, bool)
    assert isinstance(spec.is_executor, bool)
    assert isinstance(spec.is_observer, bool)
    assert isinstance(spec.is_system, bool)


@pytest.mark.unit
@pytest.mark.domain
def test_agent_spec_capabilities_is_a_set():
    """
    Invariant:
    capabilities must be a set[str].

    Rationale:
    Capabilities are matched declaratively during planning
    and must support set operations.
    """
    spec = AgentSpec(
        name="cap-agent",
        description="Agent with capabilities",
        domains={"code"},
        capabilities={"read", "write"},
    )

    assert isinstance(spec.capabilities, set)
    assert "read" in spec.capabilities
    assert "write" in spec.capabilities


@pytest.mark.unit
@pytest.mark.domain
def test_agent_spec_to_dict_is_stable_and_serializable():
    """
    Invariant:
    to_dict() must:
    - return only JSON-serializable primitives
    - include all declared semantic fields
    - not leak implementation details
    """
    spec = AgentSpec(
        name="dict-agent",
        description="Agent for dict conversion",
        domains={"test"},
        is_planner=True,
        capabilities={"plan"},
        version="1.0",
        experimental=True,
        ui_label="Dict Agent",
        ui_group="Testing",
    )

    data = spec.to_dict()

    assert isinstance(data, dict)

    # Identity
    assert data["name"] == "dict-agent"
    assert data["description"]

    # Domains
    assert isinstance(data["domains"], list)
    assert "test" in data["domains"]

    # Roles
    roles = data["roles"]
    assert roles["planner"] is True
    assert roles["executor"] is False

    # Capabilities
    assert "plan" in data["capabilities"]

    # Governance
    gov = data["governance"]
    assert gov["version"] == "1.0"
    assert gov["experimental"] is True
    assert gov["deprecated"] is False


    # UI
    assert data["ui"]["label"] == "Dict Agent"
    assert data["ui"]["group"] == "Testing"


@pytest.mark.unit
@pytest.mark.domain
def test_agent_spec_does_not_depend_on_runtime_or_engine():
    """
    Invariant:
    AgentSpec must be completely decoupled from:
    - runtime execution
    - orchestrator
    - engine internals
    """
    spec = AgentSpec(
        name="pure-agent",
        description="Pure declarative agent",
        domains={"core"},
    )

    forbidden_attrs = {
        "run",
        "execute",
        "handle",
        "dispatch",
        "context",
        "session",
    }

    for attr in forbidden_attrs:
        assert not hasattr(spec, attr)
