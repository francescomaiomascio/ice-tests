import pytest

from ice_ai.llm.modes import (
    CognitiveMode,
    EXPLAIN_MODE,
    DIAGNOSE_MODE,
    PLAN_MODE,
    DECIDE_MODE,
    EXPLORE_MODE,
    SUMMARIZE_MODE,
    GENERATE_MODE,
    MODE_REGISTRY,
)


# ---------------------------------------------------------------------
# INVARIANTS — COGNITIVE MODE
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_cognitive_mode_is_immutable():
    """
    Invariant:
    CognitiveMode must be immutable once defined.
    """

    mode = CognitiveMode(
        name="test",
        description="test mode",
        structured=True,
    )

    with pytest.raises(Exception):
        mode.name = "changed"


@pytest.mark.unit
@pytest.mark.domain
def test_cognitive_mode_to_dict_is_complete():
    """
    Invariant:
    to_dict() must expose name, description, traits and notes.
    """

    mode = CognitiveMode(
        name="test",
        description="test mode",
        structured=True,
        exploratory=False,
        deterministic=True,
        critical=False,
        generative=False,
        summarizing=False,
        notes="note",
    )

    data = mode.to_dict()

    assert data["name"] == "test"
    assert data["description"] == "test mode"

    traits = data["traits"]
    for key in (
        "structured",
        "exploratory",
        "deterministic",
        "critical",
        "generative",
        "summarizing",
    ):
        assert key in traits

    assert data["notes"] == "note"


# ---------------------------------------------------------------------
# INVARIANTS — CANONICAL MODES
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_canonical_modes_have_unique_names():
    """
    Invariant:
    All canonical modes must have unique names.
    """

    names = {
        EXPLAIN_MODE.name,
        DIAGNOSE_MODE.name,
        PLAN_MODE.name,
        DECIDE_MODE.name,
        EXPLORE_MODE.name,
        SUMMARIZE_MODE.name,
        GENERATE_MODE.name,
    }

    assert len(names) == 7


@pytest.mark.unit
@pytest.mark.domain
def test_explain_mode_is_deterministic_and_not_exploratory():
    """
    Invariant:
    Explain mode must be deterministic and non-exploratory.
    """

    assert EXPLAIN_MODE.deterministic is True
    assert EXPLAIN_MODE.exploratory is False


@pytest.mark.unit
@pytest.mark.domain
def test_explore_mode_is_exploratory_and_non_deterministic():
    """
    Invariant:
    Explore mode favors exploration over determinism.
    """

    assert EXPLORE_MODE.exploratory is True
    assert EXPLORE_MODE.deterministic is False


@pytest.mark.unit
@pytest.mark.domain
def test_plan_mode_is_structured_and_deterministic():
    """
    Invariant:
    Plan mode must produce structured and deterministic output.
    """

    assert PLAN_MODE.structured is True
    assert PLAN_MODE.deterministic is True


@pytest.mark.unit
@pytest.mark.domain
def test_summarize_mode_is_not_generative():
    """
    Invariant:
    Summarization must not generate new content.
    """

    assert SUMMARIZE_MODE.generative is False
    assert SUMMARIZE_MODE.summarizing is True


# ---------------------------------------------------------------------
# INVARIANTS — REGISTRY
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_mode_registry_is_complete():
    """
    Invariant:
    MODE_REGISTRY must expose all canonical modes.
    """

    expected = {
        "explain",
        "diagnose",
        "plan",
        "decide",
        "explore",
        "summarize",
        "generate",
    }

    assert set(MODE_REGISTRY.keys()) == expected


@pytest.mark.unit
@pytest.mark.domain
def test_mode_registry_values_are_modes():
    """
    Invariant:
    MODE_REGISTRY values must all be CognitiveMode instances.
    """

    for mode in MODE_REGISTRY.values():
        assert isinstance(mode, CognitiveMode)
