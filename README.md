# ICE Tests

ICE Tests is the canonical test authority for the ICE ecosystem.

This repository does not merely test code.
It defines **what ICE is allowed to be**.

---

## Purpose

ICE is a modular cognitive platform composed of multiple domains, aggregates, and products.
ICE Tests exists to preserve meaning, invariants, and system identity as ICE evolves.

This repository is the **single source of truth** for:
- domain correctness
- cross-domain cooperation
- core system validity
- product-level guarantees

---

## What this repository is

- A semantic contract for ICE behavior
- A guardrail against architectural drift
- A platform-level validation system

---

## What this repository is NOT

- A dump of unit tests
- A mirror of production repositories
- A place for ad-hoc experiments

---

## Test topology

ICE Tests is structured across four levels:

- **domains/** — isolated responsibility
- **aggregates/** — cooperative subsystems
- **core/** — ICE as a platform
- **products/** — user-facing applications

Each level answers a different question.
Mixing levels is forbidden.

---

## Status

This repository is intentionally initialized without test implementations.
Structure and semantics come first.

Tests will be introduced incrementally, starting from integration-level guarantees.

---

## Entry points

Documentation:
- `docs/philosophy.md`
- `docs/test-levels.md`
- `docs/domain-boundaries.md`

Execution:
- `scripts/run_domain.sh`
- `scripts/run_aggregate.sh`
- `scripts/run_core.sh`
- `scripts/run_product.sh`

---

## Final note

If ICE Tests is unclear, ICE itself is unclear.

This repository exists to prevent that.
