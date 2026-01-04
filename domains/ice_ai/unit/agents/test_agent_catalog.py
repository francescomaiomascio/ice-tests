import pytest

from ice_ai.agents.catalog import AgentCatalog
from ice_ai.agents.spec import AgentSpec


@pytest.mark.unit
@pytest.mark.domain
def test_agent_catalog_rejects_duplicate_names():
    """
    Invariant:
    AgentCatalog must reject duplicate AgentSpec names.
    """
    spec_a = AgentSpec(
        name="agent-a",
        description="First agent",
        domains={"code"},
    )

    spec_b = AgentSpec(
        name="agent-a",  # duplicate
        description="Second agent",
        domains={"code"},
    )

    with pytest.raises(ValueError):
        AgentCatalog([spec_a, spec_b])


@pytest.mark.unit
@pytest.mark.domain
def test_agent_catalog_lookup_by_name():
    """
    Invariant:
    AgentCatalog.get() returns the correct AgentSpec.
    """
    spec = AgentSpec(
        name="planner",
        description="Planner agent",
        domains={"workflow"},
        is_planner=True,
    )

    catalog = AgentCatalog([spec])

    result = catalog.get("planner")
    assert result is spec


@pytest.mark.unit
@pytest.mark.domain
def test_agent_catalog_exists():
    """
    Invariant:
    exists() correctly reports presence or absence of agents.
    """
    spec = AgentSpec(
        name="analyzer",
        description="Analyzer agent",
        domains={"code"},
        is_observer=True,
    )

    catalog = AgentCatalog([spec])

    assert catalog.exists("analyzer") is True
    assert catalog.exists("missing-agent") is False


@pytest.mark.unit
@pytest.mark.domain
def test_agent_catalog_all_is_sorted_and_stable():
    """
    Invariant:
    all() returns all AgentSpec sorted by name.
    """
    specs = [
        AgentSpec(name="zeta", description="Z", domains={"x"}),
        AgentSpec(name="alpha", description="A", domains={"x"}),
        AgentSpec(name="beta", description="B", domains={"x"}),
    ]

    catalog = AgentCatalog(specs)

    names = [a.name for a in catalog.all()]
    assert names == ["alpha", "beta", "zeta"]


@pytest.mark.unit
@pytest.mark.domain
def test_agent_catalog_filter_by_domain():
    """
    Invariant:
    by_domain() returns only agents declaring that domain.
    """
    code_agent = AgentSpec(
        name="code",
        description="Code agent",
        domains={"code"},
    )

    log_agent = AgentSpec(
        name="log",
        description="Log agent",
        domains={"logs"},
    )

    catalog = AgentCatalog([code_agent, log_agent])

    code_agents = catalog.by_domain("code")
    assert code_agents == [code_agent]

    logs_agents = catalog.by_domain("logs")
    assert logs_agents == [log_agent]


@pytest.mark.unit
@pytest.mark.domain
def test_agent_catalog_role_filters():
    """
    Invariant:
    planners(), executors(), observers(), system_agents()
    correctly filter by declared roles.
    """
    planner = AgentSpec(
        name="planner",
        description="Planner",
        domains={"workflow"},
        is_planner=True,
    )

    executor = AgentSpec(
        name="executor",
        description="Executor",
        domains={"code"},
        is_executor=True,
    )

    observer = AgentSpec(
        name="observer",
        description="Observer",
        domains={"logs"},
        is_observer=True,
    )

    system = AgentSpec(
        name="system",
        description="System",
        domains={"system"},
        is_system=True,
    )

    catalog = AgentCatalog([planner, executor, observer, system])

    assert catalog.planners() == [planner]
    assert catalog.executors() == [executor]
    assert catalog.observers() == [observer]
    assert catalog.system_agents() == [system]


@pytest.mark.unit
@pytest.mark.domain
def test_agent_catalog_to_dict_is_complete_and_stable():
    """
    Invariant:
    to_dict() returns a complete serializable snapshot.
    """
    spec = AgentSpec(
        name="validator",
        description="Validator",
        domains={"code"},
        is_observer=True,
    )

    catalog = AgentCatalog([spec])
    data = catalog.to_dict()

    assert data["total_agents"] == 1
    assert "validator" in data["agents"]
    assert data["agents"]["validator"]["name"] == "validator"
