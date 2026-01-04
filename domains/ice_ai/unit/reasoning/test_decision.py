import pytest

from ice_ai.reasoning.decision import (
    Decision,
    DecisionContext,
    DecisionPolicy,
    DefaultDecisionPolicy,
)
from ice_ai.reasoning.routing import RoutingDecision, Intent


# ---------------------------------------------------------------------
# INVARIANTS — DATA MODEL
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_decision_is_immutable():
    """
    Invariant:
    Decision must be immutable (frozen dataclass).
    """

    decision = Decision(
        intent=Intent.RESPOND,
        proceed=True,
        reason="ok",
    )

    with pytest.raises(Exception):
        decision.proceed = False


@pytest.mark.unit
@pytest.mark.domain
def test_decision_context_is_immutable():
    """
    Invariant:
    DecisionContext must be immutable and side-effect free.
    """

    ctx = DecisionContext(
        user_intent="do something",
        lifecycle_state="idle",
    )

    with pytest.raises(Exception):
        ctx.lifecycle_state = "executing"


# ---------------------------------------------------------------------
# INVARIANTS — POLICY INTERFACE
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_decision_policy_is_abstract():
    """
    Invariant:
    DecisionPolicy must not be directly usable.
    """

    policy = DecisionPolicy()

    routing = RoutingDecision(
        intent=Intent.RESPOND,
        reason="test",
    )

    context = DecisionContext()

    with pytest.raises(NotImplementedError):
        policy.decide(routing=routing, context=context)


# ---------------------------------------------------------------------
# DEFAULT POLICY — GUARDRAILS
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_default_policy_blocks_low_confidence_routing():
    """
    Invariant:
    Routing with too low confidence must be blocked.
    """

    policy = DefaultDecisionPolicy()

    routing = RoutingDecision(
        intent=Intent.RESPOND,
        reason="uncertain",
        confidence=0.1,
    )

    context = DecisionContext()

    decision = policy.decide(
        routing=routing,
        context=context,
    )

    assert decision.proceed is False
    assert decision.intent is Intent.RESPOND
    assert "confidence" in decision.reason.lower()
    assert decision.meta["action"] == "ask_clarification"


@pytest.mark.unit
@pytest.mark.domain
def test_default_policy_blocks_plan_during_execution():
    """
    Invariant:
    Planning must not be allowed while execution is in progress.
    """

    policy = DefaultDecisionPolicy()

    routing = RoutingDecision(
        intent=Intent.PLAN,
        reason="need a plan",
        confidence=0.9,
    )

    context = DecisionContext(
        lifecycle_state="executing"
    )

    decision = policy.decide(
        routing=routing,
        context=context,
    )

    assert decision.proceed is False
    assert decision.intent is Intent.PLAN
    assert "execution" in decision.reason.lower()
    assert decision.meta["action"] == "wait"


# ---------------------------------------------------------------------
# DEFAULT POLICY — ACCEPT PATH
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_default_policy_accepts_valid_routing():
    """
    Invariant:
    Valid routing decisions must be accepted by default policy.
    """

    policy = DefaultDecisionPolicy()

    routing = RoutingDecision(
        intent=Intent.ANALYZE,
        reason="analysis requested",
        confidence=0.8,
        payload={"data": "x"},
        suggested_roles=["analyzer"],
    )

    context = DecisionContext(
        lifecycle_state="idle"
    )

    decision = policy.decide(
        routing=routing,
        context=context,
    )

    assert decision.proceed is True
    assert decision.intent is Intent.ANALYZE
    assert decision.confidence == routing.confidence
    assert decision.meta["suggested_roles"] == ["analyzer"]
    assert decision.meta["payload"] == {"data": "x"}
