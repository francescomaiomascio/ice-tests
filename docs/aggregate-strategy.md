# Aggregate Strategy

Aggregates exist to test cooperation, not ownership.

An aggregate represents a **coherent subsystem** of ICE
that only makes sense when multiple domains interact.

---

## When to create an aggregate

Create an aggregate if:
- More than one domain is required
- The interaction has emergent behavior
- Failure modes cross domain boundaries

---

## Examples

### ai_stack
- ice_ai
- ice_engine
- ice_conscious
- ice_providers

Tests:
- RAG pipelines
- Agent + memory + storage interaction

---

### runtime_stack
- ice_runtime
- ice_protocols
- ice_api

Tests:
- Boot to ready
- Transport negotiation
- Session lifecycle

---

## What aggregates must NOT do

- Test UI
- Test product workflows
- Replace domain tests

Aggregates validate *composition*, not *ownership*.

---

## Anti-pattern

If an aggregate grows too large:
- Split it
- Or promote it to Core tests
