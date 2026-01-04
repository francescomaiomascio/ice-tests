import pytest

from ice_ai.memory.usage import (
    MemoryUsageMode,
    MemoryUsagePolicy,
)
from ice_ai.memory.contracts import (
    MemoryContract,
    MemoryScope,
    MemoryKind,
)


# ---------------------------------------------------------------------
# ENUM
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_memory_usage_mode_enum_is_closed():
    """
    Invariant:
    MemoryUsageMode defines a closed cognitive set.
    """

    values = {mode.value for mode in MemoryUsageMode}

    assert values == {
        "read",
        "reference",
        "reasoning",
        "context",
        "audit",
    }


# ---------------------------------------------------------------------
# BASIC POLICY
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_policy_denies_unlisted_mode():
    """
    Invariant:
    A policy must deny modes not explicitly allowed.
    """

    policy = MemoryUsagePolicy(
        allowed_modes={MemoryUsageMode.READ}
    )

    contract = MemoryContract(
        name="fact",
        description="fact",
        kind=MemoryKind.FACT,
        scope=MemoryScope.GLOBAL,
    )

    assert policy.allows(
        contract=contract,
        mode=MemoryUsageMode.READ,
    ) is True

    assert policy.allows(
        contract=contract,
        mode=MemoryUsageMode.REASONING,
    ) is False


# ---------------------------------------------------------------------
# USER VISIBILITY
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_policy_requires_user_visible_memory():
    """
    Invariant:
    require_user_visibility forbids hidden memories.
    """

    policy = MemoryUsagePolicy(
        allowed_modes={MemoryUsageMode.REFERENCE},
        require_user_visibility=True,
    )

    hidden = MemoryContract(
        name="hidden",
        description="hidden memory",
        kind=MemoryKind.NOTE,
        scope=MemoryScope.SESSION,
        user_visible=False,
    )

    visible = MemoryContract(
        name="visible",
        description="visible memory",
        kind=MemoryKind.NOTE,
        scope=MemoryScope.SESSION,
        user_visible=True,
    )

    assert policy.allows(
        contract=hidden,
        mode=MemoryUsageMode.REFERENCE,
    ) is False

    assert policy.allows(
        contract=visible,
        mode=MemoryUsageMode.REFERENCE,
    ) is True


# ---------------------------------------------------------------------
# SCOPE GOVERNANCE
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_policy_forbids_cross_scope_when_enabled():
    """
    Invariant:
    forbid_cross_scope prevents memory use outside its scope.
    """

    policy = MemoryUsagePolicy(
        allowed_modes={MemoryUsageMode.CONTEXT},
        forbid_cross_scope=True,
    )

    contract = MemoryContract(
        name="workspace_fact",
        description="workspace fact",
        kind=MemoryKind.FACT,
        scope=MemoryScope.WORKSPACE,
    )

    assert policy.allows(
        contract=contract,
        mode=MemoryUsageMode.CONTEXT,
        target_scope=MemoryScope.WORKSPACE,
    ) is True

    assert policy.allows(
        contract=contract,
        mode=MemoryUsageMode.CONTEXT,
        target_scope=MemoryScope.GLOBAL,
    ) is False


# ---------------------------------------------------------------------
# REASONING MODE — DOCUMENTED RISK
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_reasoning_mode_is_not_blocked_by_policy():
    """
    Invariant:
    MemoryUsagePolicy does NOT enforce system_critical checks
    for REASONING mode.

    This is a documented cognitive constraint, enforced at
    higher-level policy (router / decision layer).
    """

    policy = MemoryUsagePolicy(
        allowed_modes={MemoryUsageMode.REASONING}
    )

    non_critical = MemoryContract(
        name="note",
        description="non critical note",
        kind=MemoryKind.NOTE,
        scope=MemoryScope.SESSION,
        system_critical=False,
    )

    assert policy.allows(
        contract=non_critical,
        mode=MemoryUsageMode.REASONING,
    ) is True
