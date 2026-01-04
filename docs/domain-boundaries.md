# Domain Boundaries

Each domain in ICE owns a semantic responsibility.
Tests must never leak responsibility across domains.

---

## Domain owns:
- Its internal logic
- Its invariants
- Its internal errors

## Domain does NOT own:
- Behavior of other domains
- System lifecycle
- User-facing guarantees

---

## Examples

### ice_ai
Owns:
- Agent reasoning
- Decision logic
- Memory interaction semantics

Does NOT own:
- Storage reliability
- Runtime lifecycle
- UI synchronization

---

### ice_engine
Owns:
- Orchestration
- Persistence
- Ingest pipelines

Does NOT own:
- Agent cognition
- User flows

---

### ice_runtime
Owns:
- Boot
- Session lifecycle
- Transport layers

Does NOT own:
- Business meaning
- Agent intelligence

---

## Rule of thumb

> If a test requires knowledge of another domain’s internals,
> it does not belong in a domain test.
