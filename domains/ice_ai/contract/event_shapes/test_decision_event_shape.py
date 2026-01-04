"""
Contract tests for Decision event shape.

These tests protect the public cognitive decision contract.
"""

from __future__ import annotations

import pytest

from ice_ai.reasoning.decision import Decision
from ice_ai.reasoning.routing import Intent


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

def test_decision_has_required_fields():
    """
    Invariant:
    Decision exposes a stable set of fields.
    """
    decision = Decision(
        intent=Intent.PLAN,
        proceed=True,
        reason="ok",
    )

    data = decision.__dict__

    assert set(data.keys()) == {
        "intent",
        "proceed",
        "reason",
        "confidence",
        "meta",
    }


def test_decision_meta_is_dict():
    """
    Invariant:
    meta must always be a dictionary.
    """
    decision = Decision(
        intent=Intent.ANALYZE,
        proceed=True,
        reason="ok",
        meta={"note": "x"},
    )

    assert isinstance(decision.meta, dict)


def test_decision_confidence_is_float():
    """
    Invariant:
    confidence is always a float between 0.0 and 1.0.
    """
    decision = Decision(
        intent=Intent.RESPOND,
        proceed=False,
        reason="low confidence",
        confidence=0.3,
    )

    assert isinstance(decision.confidence, float)
    assert 0.0 <= decision.confidence <= 1.0
