import pytest

from ice_ai.agents.prompts import (
    CANONICAL_PROMPT,
    SYSTEM_ROLE_PROMPT,
    SYSTEM_HARD_RULES,
    ROLE_PROMPTS,
    MODE_PROMPTS,
    LIFECYCLE_PROMPTS,
    PROMPT_COMPONENTS,
)


@pytest.mark.unit
@pytest.mark.domain
def test_canonical_prompts_exist_and_are_strings():
    """
    Invariant:
    Core canonical prompts must exist and be non-empty strings.
    """
    assert isinstance(CANONICAL_PROMPT, str)
    assert CANONICAL_PROMPT.strip() != ""

    assert isinstance(SYSTEM_ROLE_PROMPT, str)
    assert SYSTEM_ROLE_PROMPT.strip() != ""

    assert isinstance(SYSTEM_HARD_RULES, str)
    assert SYSTEM_HARD_RULES.strip() != ""


@pytest.mark.unit
@pytest.mark.domain
def test_role_prompts_are_static_strings():
    """
    Invariant:
    ROLE_PROMPTS must be a dict[str, str] with non-empty values.
    """
    assert isinstance(ROLE_PROMPTS, dict)
    assert ROLE_PROMPTS, "ROLE_PROMPTS must not be empty"

    for role, prompt in ROLE_PROMPTS.items():
        assert isinstance(role, str)
        assert isinstance(prompt, str)
        assert prompt.strip() != ""


@pytest.mark.unit
@pytest.mark.domain
def test_mode_prompts_are_static_strings():
    """
    Invariant:
    MODE_PROMPTS must be a dict[str, str] with non-empty values.
    """
    assert isinstance(MODE_PROMPTS, dict)
    assert MODE_PROMPTS, "MODE_PROMPTS must not be empty"

    for mode, prompt in MODE_PROMPTS.items():
        assert isinstance(mode, str)
        assert isinstance(prompt, str)
        assert prompt.strip() != ""


@pytest.mark.unit
@pytest.mark.domain
def test_lifecycle_prompts_are_static_strings():
    """
    Invariant:
    LIFECYCLE_PROMPTS must be a dict[str, str] with non-empty values.
    """
    assert isinstance(LIFECYCLE_PROMPTS, dict)
    assert LIFECYCLE_PROMPTS, "LIFECYCLE_PROMPTS must not be empty"

    for state, prompt in LIFECYCLE_PROMPTS.items():
        assert isinstance(state, str)
        assert isinstance(prompt, str)
        assert prompt.strip() != ""


@pytest.mark.unit
@pytest.mark.domain
def test_prompt_components_registry_is_complete():
    """
    Invariant:
    PROMPT_COMPONENTS must expose all canonical prompt sections.
    """
    assert isinstance(PROMPT_COMPONENTS, dict)

    expected_keys = {
        "canonical",
        "system_role",
        "system_rules",
        "roles",
        "modes",
        "lifecycle",
    }

    assert expected_keys.issubset(PROMPT_COMPONENTS.keys())


@pytest.mark.unit
@pytest.mark.domain
def test_prompt_components_values_are_well_formed():
    """
    Invariant:
    Each entry in PROMPT_COMPONENTS must be well-typed.
    """
    for key, value in PROMPT_COMPONENTS.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                assert isinstance(sub_key, str)
                assert isinstance(sub_value, str)
                assert sub_value.strip() != ""
        else:
            assert isinstance(value, str)
            assert value.strip() != ""
