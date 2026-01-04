import pytest

from ice_ai.llm.scoring import (
    CognitiveScore,
    ScoringProfile,
    DEFAULT_PROFILE,
    PLANNING_PROFILE,
    DIAGNOSTIC_PROFILE,
    GENERATION_PROFILE,
    SCORING_PROFILES,
)


# ---------------------------------------------------------------------
# INVARIANTS — COGNITIVE SCORE
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_cognitive_score_is_immutable():
    """
    Invariant:
    CognitiveScore must be immutable.
    """

    score = CognitiveScore(
        clarity=1.0,
        coherence=1.0,
        usefulness=1.0,
        confidence=1.0,
        correctness=1.0,
    )

    with pytest.raises(Exception):
        score.clarity = 0.0


@pytest.mark.unit
@pytest.mark.domain
def test_cognitive_score_overall_is_arithmetic_mean():
    """
    Invariant:
    overall() must be the arithmetic mean of all components.
    """

    score = CognitiveScore(
        clarity=1.0,
        coherence=0.0,
        usefulness=0.0,
        confidence=0.0,
        correctness=0.0,
    )

    assert score.overall() == pytest.approx(0.2)


@pytest.mark.unit
@pytest.mark.domain
def test_cognitive_score_to_dict_is_complete():
    """
    Invariant:
    to_dict() must expose all components plus overall().
    """

    score = CognitiveScore(
        clarity=0.5,
        coherence=0.6,
        usefulness=0.7,
        confidence=0.8,
        correctness=0.9,
        notes="test",
    )

    data = score.to_dict()

    for key in (
        "clarity",
        "coherence",
        "usefulness",
        "confidence",
        "correctness",
        "overall",
        "notes",
    ):
        assert key in data


# ---------------------------------------------------------------------
# INVARIANTS — SCORING PROFILE
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_scoring_profile_ignores_unknown_weights():
    """
    Invariant:
    ScoringProfile must ignore weights for unknown score attributes.
    """

    score = CognitiveScore(
        clarity=1.0,
        coherence=1.0,
        usefulness=1.0,
        confidence=1.0,
        correctness=1.0,
    )

    profile = ScoringProfile(
        name="test",
        weights={
            "clarity": 1.0,
            "nonexistent": 100.0,
        },
    )

    assert profile.score(score) == pytest.approx(1.0)


@pytest.mark.unit
@pytest.mark.domain
def test_scoring_profile_zero_weights_is_safe():
    """
    Invariant:
    A profile with no valid weights must return 0.0, not crash.
    """

    score = CognitiveScore(
        clarity=1.0,
        coherence=1.0,
        usefulness=1.0,
        confidence=1.0,
        correctness=1.0,
    )

    profile = ScoringProfile(
        name="empty",
        weights={},
    )

    assert profile.score(score) == 0.0


@pytest.mark.unit
@pytest.mark.domain
def test_scoring_profiles_produce_distinct_scores():
    """
    Invariant:
    Different profiles must weight dimensions differently.
    """

    score = CognitiveScore(
        clarity=1.0,
        coherence=1.0,
        usefulness=1.0,
        confidence=0.0,
        correctness=0.0,
    )

    default_score = DEFAULT_PROFILE.score(score)
    planning_score = PLANNING_PROFILE.score(score)

    assert default_score != planning_score


# ---------------------------------------------------------------------
# INVARIANTS — REGISTRY
# ---------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.domain
def test_scoring_registry_is_complete():
    """
    Invariant:
    SCORING_PROFILES must expose all canonical profiles.
    """

    expected = {
        "default",
        "planning",
        "diagnostic",
        "generation",
    }

    assert set(SCORING_PROFILES.keys()) == expected


@pytest.mark.unit
@pytest.mark.domain
def test_scoring_registry_values_are_profiles():
    """
    Invariant:
    All registry values must be ScoringProfile instances.
    """

    for profile in SCORING_PROFILES.values():
        assert isinstance(profile, ScoringProfile)
