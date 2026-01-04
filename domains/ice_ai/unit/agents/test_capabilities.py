import pytest
from dataclasses import FrozenInstanceError

from ice_ai.agents.capabilities import AgentCapabilities


@pytest.mark.unit
@pytest.mark.domain
def test_agent_capabilities_is_immutable():
    """
    Invariant:
    AgentCapabilities must be immutable.
    """
    caps = AgentCapabilities(is_executor=True)

    with pytest.raises(FrozenInstanceError):
        caps.is_executor = False


@pytest.mark.unit
@pytest.mark.domain
def test_agent_capabilities_supports_declared_capability():
    """
    Invariant:
    supports() returns True only for declared capabilities.
    """
    caps = AgentCapabilities(capabilities={"code.read", "code.write"})

    assert caps.supports("code.read") is True
    assert caps.supports("code.write") is True
    assert caps.supports("code.delete") is False


@pytest.mark.unit
@pytest.mark.domain
def test_with_capability_returns_new_instance():
    """
    Invariant:
    with_capability() must not mutate the original instance.
    """
    caps = AgentCapabilities(capabilities={"analyze"})
    new_caps = caps.with_capability("validate")

    assert caps is not new_caps
    assert caps.capabilities == {"analyze"}
    assert new_caps.capabilities == {"analyze", "validate"}


@pytest.mark.unit
@pytest.mark.domain
def test_with_capability_preserves_all_flags():
    """
    Invariant:
    with_capability() must preserve all non-capability flags.
    """
    caps = AgentCapabilities(
        is_planner=True,
        uses_llm=True,
        experimental=True,
        capabilities={"plan"},
    )

    new_caps = caps.with_capability("route")

    assert new_caps.is_planner is True
    assert new_caps.uses_llm is True
    assert new_caps.experimental is True
    assert new_caps.capabilities == {"plan", "route"}


@pytest.mark.unit
@pytest.mark.domain
def test_to_dict_is_stable_and_serializable():
    """
    Invariant:
    to_dict() must return a fully serializable, stable structure.
    """
    caps = AgentCapabilities(
        is_executor=True,
        uses_knowledge=True,
        capabilities={"knowledge.read"},
    )

    data = caps.to_dict()

    assert isinstance(data, dict)
    assert data["roles"]["executor"] is True
    assert data["dependencies"]["knowledge"] is True
    assert data["capabilities"] == ["knowledge.read"]
