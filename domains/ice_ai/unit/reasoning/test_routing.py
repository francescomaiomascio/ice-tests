import pytest

from ice_ai.reasoning.routing import (
    Router,
    RoutingDecision,
    Intent,
)


@pytest.mark.unit
@pytest.mark.domain
def test_routing_decision_is_immutable():
    """
    Invariant:
    RoutingDecision must be immutable (frozen dataclass).
    """

    decision = RoutingDecision(
        intent=Intent.RESPOND,
        reason="test",
    )

    with pytest.raises(Exception):
        decision.intent = Intent.PLAN


@pytest.mark.unit
@pytest.mark.domain
def test_explicit_mode_plan_overrides_everything():
    """
    Invariant:
    Explicit mode must override all heuristics.
    """

    decision = Router.route(
        user_query="Do something complex",
        llm_output={"actions": ["fake"]},
        mode="plan",
    )

    assert decision.intent is Intent.PLAN
    assert decision.suggested_roles == ["planner"]
    assert decision.confidence == 1.0
    assert decision.payload["goal"] == "Do something complex"


@pytest.mark.unit
@pytest.mark.domain
def test_routing_to_plan_when_actions_detected():
    """
    Invariant:
    If structured actions are present, routing must produce PLAN intent.
    """

    decision = Router.route(
        user_query="Refactor project",
        llm_output={
            "actions": [
                {"title": "Step 1", "description": "Analyze"},
                {"title": "Step 2", "description": "Refactor"},
            ]
        },
    )

    assert decision.intent is Intent.PLAN
    assert "planner" in decision.suggested_roles
    assert decision.payload["goal"] == "Refactor project"
    assert decision.confidence > 0.5


@pytest.mark.unit
@pytest.mark.domain
def test_routing_to_validate_when_issues_detected():
    """
    Invariant:
    If issues are present, routing must produce VALIDATE intent.
    """

    decision = Router.route(
        user_query="Check correctness",
        llm_output={
            "issues": [
                {"type": "error", "message": "Something is wrong"}
            ]
        },
    )

    assert decision.intent is Intent.VALIDATE
    assert "validator" in decision.suggested_roles
    assert "issues" in decision.payload
    assert decision.confidence >= 0.8


@pytest.mark.unit
@pytest.mark.domain
def test_routing_to_analyze_when_analysis_like_output_detected():
    """
    Invariant:
    Analytical-looking output should route to ANALYZE intent.
    """

    decision = Router.route(
        user_query="Explain this code",
        llm_output={
            "analysis": "This function does X because Y"
        },
    )

    assert decision.intent is Intent.ANALYZE
    assert "analyzer" in decision.suggested_roles
    assert decision.payload["content"]["analysis"].startswith("This function")


@pytest.mark.unit
@pytest.mark.domain
def test_routing_defaults_to_respond():
    """
    Invariant:
    If no heuristics or modes apply, routing must default to RESPOND.
    """

    decision = Router.route(
        user_query="Hello",
        llm_output={"answer": "Hi"},
    )

    assert decision.intent is Intent.RESPOND
    assert decision.payload["answer"] == "Hi"
    assert decision.confidence <= 0.5


@pytest.mark.unit
@pytest.mark.domain
def test_unknown_mode_falls_back_to_respond():
    """
    Invariant:
    Unknown modes must not crash routing and must fall back to RESPOND.
    """

    decision = Router.route(
        user_query="Test",
        llm_output={"answer": "fallback"},
        mode="unknown_mode",
    )

    assert decision.intent is Intent.RESPOND
    assert decision.confidence < 0.5
