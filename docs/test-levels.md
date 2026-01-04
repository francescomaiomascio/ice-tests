# Test Levels

ICE Tests defines five test levels.
Each level answers a different question.
Crossing levels is forbidden.

---

## unit/

**Question:**  
Does this logic behave correctly in isolation?

**Properties:**
- Pure logic
- No filesystem
- No network
- No processes
- Deterministic

**Allowed:**
- Functions
- Classes
- Local invariants

**Forbidden:**
- IO
- Environment dependence
- External state

---

## integration/

**Question:**  
Do components within the same domain cooperate correctly?

**Properties:**
- Multiple modules
- Controlled IO
- Local databases (sqlite, memory)
- Real code paths

**Allowed:**
- Adapters
- Pipelines
- Internal protocols

**Forbidden:**
- Cross-domain assumptions
- User flows

---

## contract/

**Question:**  
Are external expectations preserved?

**Properties:**
- Schemas
- Message shapes
- Protocol versions
- Backward compatibility

**Allowed:**
- Validation
- Schema evolution tests

**Forbidden:**
- Business logic
- Behavior testing

---

## e2e/

**Question:**  
Does this domain or system function when executed for real?

**Properties:**
- Real processes
- Real runtime
- Real state transitions

**Allowed:**
- Boot
- Shutdown
- Recovery

**Forbidden:**
- Mocking the system itself

---

## scenarios/

**Question:**  
Does ICE behave meaningfully in real situations?

**Properties:**
- Narrative-driven
- Cross-cutting
- Human-readable intent

**Allowed:**
- High-level workflows

**Forbidden:**
- Fine-grained assertions
