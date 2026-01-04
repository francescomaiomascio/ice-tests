"""
Contract tests for RoutingDecision event shape.

These tests guarantee that routing decisions
expose a stable, serializable structure.

Any change here is a breaking contract change.
"""

from __future__ import annotations

import pytest

from ice_ai.reasoning.routing import RoutingDecision, Intent


# ============================================================
# MARKERS
# ============================================================

pytestmark = [
    pytest.mark.contract,
    pytest.mark.domain,
]


# ============================================================
# SHAPE TESTS
# ============================================================

def test_routing_decision_has_required_fields():
    """
    Invariant:
    RoutingDecision exposes a fixed set of public fields.
    """
    decision = RoutingDecision(
        intent=Intent.PLAN,
        reason="test",
    )

    data = decision.__dict__

    assert set(data.keys()) == {
        "intent",
        "reason",
        "payload",
        "suggested_roles",
        "confidence",
    }


def test_routing_decision_payload_is_dict():
    """
    Invariant:
    payload must always be a dictionary.
    """
    decision = RoutingDecision(
        intent=Intent.ANALYZE,
        reason="test",
        payload={"a": 1},
    )

    assert isinstance(decision.payload, dict)


def test_routing_decision_suggested_roles_is_list():
    """
    Invariant:
    suggested_roles must always be a list of strings.
    """
    decision = RoutingDecision(
        intent=Intent.VALIDATE,
        reason="test",
        suggested_roles=["validator", "system"],
    )

    assert isinstance(decision.suggested_roles, list)
    assert all(isinstance(r, str) for r in decision.suggested_roles)


def test_routing_decision_confidence_is_float():
    """
    Invariant:
    confidence is always a float between 0.0 and 1.0.
    """
    decision = RoutingDecision(
        intent=Intent.RESPOND,
        reason="test",
        confidence=0.5,
    )

    assert isinstance(decision.confidence, float)
    assert 0.0 <= decision.confidence <= 1.0
