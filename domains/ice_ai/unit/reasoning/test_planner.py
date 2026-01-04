import pytest

from ice_ai.reasoning.planner import Planner, PlanStep


@pytest.mark.unit
@pytest.mark.domain
def test_planner_fallback_when_no_actions_provided():
    """
    Invariant:
    If no raw actions are provided, the Planner MUST return
    a deterministic fallback plan containing at least one step.
    """

    goal = "Analyze the project structure"

    plan = Planner.build_plan(goal=goal, raw_actions=None)

    assert isinstance(plan, list)
    assert len(plan) >= 1

    step = plan[0]
    assert isinstance(step, PlanStep)
    assert goal in step.payload.get("goal", "")


@pytest.mark.unit
@pytest.mark.domain
def test_planner_normalizes_dict_actions():
    """
    Invariant:
    Planner must normalize dict-based actions into PlanStep objects
    without mutating input data.
    """

    raw_actions = [
        {
            "title": "Scan files",
            "description": "Scan all source files",
            "type": "analyze",
            "agent_hint": "scanner",
            "payload": {"path": "src/"},
        }
    ]

    plan = Planner.build_plan(
        goal="Scan project",
        raw_actions=raw_actions,
    )

    assert len(plan) == 1
    step = plan[0]

    assert isinstance(step, PlanStep)
    assert step.title == "Scan files"
    assert step.description == "Scan all source files"
    assert step.type == "analyze"
    assert step.agent_hint == "scanner"
    assert step.payload == {"path": "src/"}

    # Input must not be mutated
    assert "agent" not in raw_actions[0]


@pytest.mark.unit
@pytest.mark.domain
def test_planner_normalizes_string_actions():
    """
    Invariant:
    Planner must accept string actions and convert them
    into valid PlanStep objects.
    """

    raw_actions = [
        "Analyze codebase",
        "Generate report",
    ]

    plan = Planner.build_plan(
        goal="Analyze project",
        raw_actions=raw_actions,
    )

    assert len(plan) == 2

    for idx, step in enumerate(plan, start=1):
        assert isinstance(step, PlanStep)
        assert step.id == f"step-{idx}"
        assert isinstance(step.description, str)
        assert step.description


@pytest.mark.unit
@pytest.mark.domain
def test_planner_produces_deterministic_ids():
    """
    Invariant:
    Given the same input, Planner must always produce
    the same step IDs in the same order.
    """

    raw_actions = [
        {"description": "Step A"},
        {"description": "Step B"},
    ]

    plan1 = Planner.build_plan(goal="Test", raw_actions=raw_actions)
    plan2 = Planner.build_plan(goal="Test", raw_actions=raw_actions)

    ids1 = [step.id for step in plan1]
    ids2 = [step.id for step in plan2]

    assert ids1 == ids2


@pytest.mark.unit
@pytest.mark.domain
def test_planner_plan_steps_are_immutable():
    """
    Invariant:
    PlanStep objects must be immutable (frozen dataclass).
    """

    plan = Planner.build_plan(goal="Immutability test", raw_actions=None)
    step = plan[0]

    with pytest.raises(Exception):
        step.title = "Mutated title"
