"""
Contract tests for MemoryScope rules.

These tests define cognitive expectations
about memory visibility and lifecycle.

They do NOT enforce runtime behavior.
"""

from __future__ import annotations

import pytest

from ice_ai.memory.contracts import MemoryScope


pytestmark = [
    pytest.mark.contract,
    pytest.mark.domain,
]


def test_memory_scope_values_are_stable():
    """
    Invariant:
    MemoryScope values must remain stable strings.
    """
    assert MemoryScope.GLOBAL.value == "global"
    assert MemoryScope.WORKSPACE.value == "workspace"
    assert MemoryScope.SESSION.value == "session"
    assert MemoryScope.TASK.value == "task"


def test_memory_scope_is_ordered_by_generality():
    """
    Invariant (documented):
    GLOBAL > WORKSPACE > SESSION > TASK

    This ordering is semantic, not enforced in code,
    but must remain documented and stable.
    """
    scopes = [
        MemoryScope.GLOBAL,
        MemoryScope.WORKSPACE,
        MemoryScope.SESSION,
        MemoryScope.TASK,
    ]

    assert scopes[0] is MemoryScope.GLOBAL
    assert scopes[-1] is MemoryScope.TASK


def test_memory_scope_enum_is_closed():
    """
    Invariant:
    No dynamic or unknown scopes are allowed.
    """
    allowed = {
        MemoryScope.GLOBAL,
        MemoryScope.WORKSPACE,
        MemoryScope.SESSION,
        MemoryScope.TASK,
    }

    assert set(MemoryScope) == allowed
