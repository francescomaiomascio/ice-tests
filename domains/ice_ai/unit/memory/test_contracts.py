import pytest

from ice_ai.memory.contracts import (
    MemoryContract,
    MemoryScope,
    MemoryKind,
)


# ---------------------------------------------------------------------
# ENUMS
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_memory_scope_enum_is_closed():
    """
    Invariant:
    MemoryScope defines a closed set of semantic scopes.
    """

    values = {scope.value for scope in MemoryScope}

    assert values == {
        "global",
        "workspace",
        "session",
        "task",
    }


@pytest.mark.unit
@pytest.mark.domain
def test_memory_kind_enum_is_closed():
    """
    Invariant:
    MemoryKind defines a closed set of semantic kinds.
    """

    values = {kind.value for kind in MemoryKind}

    assert values == {
        "fact",
        "decision",
        "plan",
        "summary",
        "code_change",
        "event",
        "note",
    }


# ---------------------------------------------------------------------
# MEMORY CONTRACT
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_memory_contract_is_immutable():
    """
    Invariant:
    MemoryContract must be immutable once defined.
    """

    contract = MemoryContract(
        name="test",
        description="test memory",
        kind=MemoryKind.FACT,
        scope=MemoryScope.GLOBAL,
    )

    with pytest.raises(Exception):
        contract.name = "changed"


@pytest.mark.unit
@pytest.mark.domain
def test_memory_contract_required_fields():
    """
    Invariant:
    MemoryContract requires name, description, kind and scope.
    """

    contract = MemoryContract(
        name="decision",
        description="system decision",
        kind=MemoryKind.DECISION,
        scope=MemoryScope.SESSION,
    )

    assert contract.name == "decision"
    assert contract.kind is MemoryKind.DECISION
    assert contract.scope is MemoryScope.SESSION


@pytest.mark.unit
@pytest.mark.domain
def test_memory_contract_governance_flags_default_to_false():
    """
    Invariant:
    Governance flags default to False.
    """

    contract = MemoryContract(
        name="note",
        description="note",
        kind=MemoryKind.NOTE,
        scope=MemoryScope.TASK,
    )

    assert contract.mutable is False
    assert contract.expires is False
    assert contract.user_visible is False
    assert contract.system_critical is False


@pytest.mark.unit
@pytest.mark.domain
def test_memory_contract_to_dict_is_serializable():
    """
    Invariant:
    to_dict() must return only JSON-serializable primitives.
    """

    contract = MemoryContract(
        name="fact",
        description="verified fact",
        kind=MemoryKind.FACT,
        scope=MemoryScope.GLOBAL,
        user_visible=True,
        tags={"verified", "core"},
    )

    data = contract.to_dict()

    assert data["kind"] == "fact"
    assert data["scope"] == "global"
    assert data["user_visible"] is True
    assert sorted(data["tags"]) == ["core", "verified"]
