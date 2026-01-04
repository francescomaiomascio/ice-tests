import pytest

from ice_ai.llm.roles import (
    CognitiveRole,
    ROLE_REGISTRY,
    SYSTEM_ROLE,
    PLANNER_ROLE,
    ANALYZER_ROLE,
    VALIDATOR_ROLE,
    EXECUTOR_ROLE,
    OBSERVER_ROLE,
)


# ---------------------------------------------------------------------
# INVARIANTS — DATA MODEL
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_cognitive_role_is_immutable():
    """
    Invariant:
    CognitiveRole must be immutable once defined.
    """

    role = CognitiveRole(
        name="test",
        description="test role",
        can_plan=True,
    )

    with pytest.raises(Exception):
        role.can_plan = False


@pytest.mark.unit
@pytest.mark.domain
def test_cognitive_role_to_dict_is_stable():
    """
    Invariant:
    CognitiveRole.to_dict() must be deterministic and complete.
    """

    role = CognitiveRole(
        name="planner",
        description="planning role",
        can_plan=True,
        can_execute=False,
        can_observe=True,
        can_decide=False,
    )

    data = role.to_dict()

    assert data["name"] == "planner"
    assert data["description"] == "planning role"
    assert data["capabilities"]["plan"] is True
    assert data["capabilities"]["execute"] is False
    assert data["capabilities"]["observe"] is True
    assert data["capabilities"]["decide"] is False
    assert "notes" in data


# ---------------------------------------------------------------------
# INVARIANTS — ROLE SEPARATION
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_system_role_is_not_executable():
    """
    Invariant:
    System role must never be executable.
    """

    assert SYSTEM_ROLE.is_system is True
    assert SYSTEM_ROLE.can_execute is False
    assert SYSTEM_ROLE.can_plan is False


@pytest.mark.unit
@pytest.mark.domain
def test_executor_role_cannot_plan_or_decide():
    """
    Invariant:
    Executor role must not plan or decide.
    """

    assert EXECUTOR_ROLE.can_execute is True
    assert EXECUTOR_ROLE.can_plan is False
    assert EXECUTOR_ROLE.can_decide is False


@pytest.mark.unit
@pytest.mark.domain
def test_planner_role_cannot_execute():
    """
    Invariant:
    Planner role must not execute actions.
    """

    assert PLANNER_ROLE.can_plan is True
    assert PLANNER_ROLE.can_execute is False


@pytest.mark.unit
@pytest.mark.domain
def test_validator_can_decide_but_not_execute():
    """
    Invariant:
    Validator may decide but never execute.
    """

    assert VALIDATOR_ROLE.can_decide is True
    assert VALIDATOR_ROLE.can_execute is False


# ---------------------------------------------------------------------
# INVARIANTS — REGISTRY
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_role_registry_is_complete_and_consistent():
    """
    Invariant:
    ROLE_REGISTRY must contain all canonical roles and nothing invalid.
    """

    expected = {
        "system",
        "planner",
        "analyzer",
        "validator",
        "executor",
        "observer",
    }

    assert set(ROLE_REGISTRY.keys()) == expected


@pytest.mark.unit
@pytest.mark.domain
def test_registry_roles_are_instances_of_cognitive_role():
    """
    Invariant:
    All registered roles must be CognitiveRole instances.
    """

    for role in ROLE_REGISTRY.values():
        assert isinstance(role, CognitiveRole)
