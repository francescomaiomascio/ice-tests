"""
Contract tests for MemoryContract shape.

These tests guarantee that the memory contract
remains stable, serializable and explicit.

Any change here is a breaking cognitive contract.
"""

from __future__ import annotations

import pytest

from ice_ai.memory.contracts import (
    MemoryContract,
    MemoryKind,
    MemoryScope,
)


pytestmark = [
    pytest.mark.contract,
    pytest.mark.domain,
]


def test_memory_contract_has_required_fields():
    """
    Invariant:
    MemoryContract exposes a fixed set of public fields.
    """
    contract = MemoryContract(
        name="test",
        description="desc",
        kind=MemoryKind.FACT,
        scope=MemoryScope.GLOBAL,
    )

    data = contract.__dict__

    assert set(data.keys()) == {
        "name",
        "description",
        "kind",
        "scope",
        "mutable",
        "expires",
        "user_visible",
        "system_critical",
        "tags",
    }


def test_memory_contract_kind_and_scope_are_enums():
    """
    Invariant:
    kind and scope must be enum instances.
    """
    contract = MemoryContract(
        name="test",
        description="desc",
        kind=MemoryKind.DECISION,
        scope=MemoryScope.SESSION,
    )

    assert isinstance(contract.kind, MemoryKind)
    assert isinstance(contract.scope, MemoryScope)


def test_memory_contract_tags_is_set():
    """
    Invariant:
    tags must always be a set of strings.
    """
    contract = MemoryContract(
        name="test",
        description="desc",
        kind=MemoryKind.NOTE,
        scope=MemoryScope.TASK,
        tags={"a", "b"},
    )

    assert isinstance(contract.tags, set)
    assert all(isinstance(t, str) for t in contract.tags)


def test_memory_contract_to_dict_is_serializable():
    """
    Invariant:
    to_dict() returns only JSON-serializable primitives.
    """
    contract = MemoryContract(
        name="test",
        description="desc",
        kind=MemoryKind.PLAN,
        scope=MemoryScope.WORKSPACE,
        user_visible=True,
    )

    data = contract.to_dict()

    assert isinstance(data, dict)
    assert data["kind"] == "plan"
    assert data["scope"] == "workspace"
