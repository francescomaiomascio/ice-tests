# Naming Conventions

Naming in ICE Tests is not cosmetic.
It encodes intent, scope, and responsibility.

If a name is ambiguous, the test is wrong.

---

## 1. General Rules

### 1.1 English only
All test files, folders, functions, markers, and scripts use **English only**.

No mixed language.
No localized abbreviations.

---

### 1.2 Explicit over concise
Clarity always wins over brevity.

Good:
- test_agent_memory_contract_violation
- test_runtime_boot_without_config_fails

Bad:
- test_mem_fail
- test_boot_err

---

### 1.3 One concept per name
A name must describe **one and only one concept**.

If a name requires "and", it is invalid.

---

## 2. Directory Naming

### 2.1 Semantic, not technical
Directory names describe **intent**, not implementation details.

Correct:
```
integration/memory_rag_pipeline/
```

Incorrect:
```
integration/pipeline_v2/
integration/new_flow/
```

---

### 2.2 Plural vs singular
- Categories → plural
- Concrete concepts → singular

Examples:
- scenarios/
- failure_modes/
- agent_execution/

---

## 3. Test File Naming (pytest)

### 3.1 Base pattern
```
test_<subject>_<behavior>.py
```

Examples:
- test_agent_decision_routing.py
- test_rag_context_construction.py
- test_runtime_boot_sequence.py

---

### 3.2 Failure cases are explicit
Failure tests must say **why** they fail.
```
test_<subject>_<failure_condition>.py
```

Examples:
- test_storage_backend_unavailable.py
- test_invalid_agent_spec_rejected.py

Never mix success and failure in the same file.

---

## 4. Test Function Naming

### 4.1 Mandatory structure
```
def test_<subject>_<action>_<expected_outcome>():
```

Examples:
- test_agent_planner_builds_task_graph()
- test_runtime_boot_fails_without_config()
- test_rag_pipeline_includes_relevant_context()

---

### 4.2 Forbidden words
Do NOT use:
- works
- runs
- handles
- correctly
- properly
- as_expected

If the outcome cannot be named precisely, the test is invalid.

---

## 5. Scenario Naming

Scenarios describe **human-meaningful stories**, not mechanics.

### 5.1 Scenario directory naming
```
<verb>_<domain_object>_<context>/
```

Examples:
- refactor_project_with_agent/
- restore_workspace_after_crash/
- upgrade_studio_without_data_loss/

---

### 5.2 Scenario test files
```
test_scenario_<short_description>.py
```

Example:
- test_scenario_multi_agent_code_refactor.py

Scenario tests may group assertions, but intent must remain clear.

---

## 6. Contract Test Naming

Contracts encode **guarantees**, not behavior.

### 6.1 Contract file naming
```
test_contract_<entity>_<guarantee>.py
```

Examples:
- test_contract_agent_spec_backward_compatible.py
- test_contract_ipc_message_schema_stable.py

Contracts must never test business logic.

---

## 7. Aggregate Test Naming

Aggregate tests must clearly imply **all involved domains**.

Good:
- test_agent_storage_memory_interaction.py

Bad:
- test_integration_flow.py
- test_full_pipeline.py

If domain interaction is unclear, the test is invalid.

---

## 8. Product Test Naming

Product tests describe **user intent**, never internal mechanics.

### 8.1 Product test naming
```
test_<user_intent>_<expected_result>.py
```

Examples:
- test_create_project_and_generate_code.py
- test_open_existing_workspace_without_reindex.py

Forbidden:
- referencing internal services
- referencing domain names (ice_ai, ice_engine, etc.)

---

## 9. Pytest Marker Naming

Markers are lowercase, underscore-separated.

Core markers:
- unit
- integration
- contract
- e2e
- scenario
- core
- product

Custom markers must:
- encode scope
- be documented
- never encode implementation details

---

## 10. Final Rule

Naming is the first assertion.

If a test name does not teach you something about ICE,
the test should not exist.