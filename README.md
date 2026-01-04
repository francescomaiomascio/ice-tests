# ICE Tests

ICE Tests is the **canonical validation authority** for the ICE ecosystem.

This repository does not simply test code.  
It defines the **structural, semantic, and cognitive constraints** that ICE must obey over time.

ICE Tests is where ICE is *proven*, not just exercised.

---

## ⚠️ Important Notice

This repository is **not** a Python package.

Do **not** run:

```bash
pip install -e .
```

ICE Tests is a test harness, not a distributable library.

It is executed exclusively via `pytest` and consumes the real ICE packages installed in the active environment.

Attempting to install this repository is considered a configuration error by design.

---

## Purpose

ICE is a modular cognitive platform composed of multiple independent domains, cooperative subsystems, and user-facing products.

ICE Tests exists to preserve:

- **architectural intent**
- **semantic invariants**
- **cross-domain correctness**
- **long-term system identity**

as the ICE ecosystem evolves.

This repository acts as the **single source of truth** for validating whether ICE still *is* ICE.

---

## Scope of Authority

ICE Tests is authoritative over:

- domain-level correctness
- cross-domain interaction rules
- platform-level invariants
- product-level guarantees

**If a behavior is not validated here, it is not guaranteed by ICE.**

---

## What This Repository Is

- A semantic contract for ICE behavior
- A governance layer over system evolution
- A guardrail against architectural drift
- A validation framework for refactoring at scale

ICE Tests allows ICE to **change without losing coherence**.

---

## What This Repository Is Not

- Not a mirror of production repositories
- Not a collection of ad-hoc tests
- Not a playground for experiments
- Not a substitute for runtime monitoring

Tests here are **intentional, declarative, and durable**.

---

## Test Topology

ICE Tests is organized into four strictly separated validation layers:

1. **`domains/`**  
   Isolated responsibility and local invariants

2. **`aggregates/`**  
   Cooperative subsystems spanning multiple domains

3. **`core/`**  
   ICE as a platform-level cognitive system

4. **`products/`**  
   User-facing applications built on top of ICE

Each layer answers a different class of questions.

**Crossing layers inside a single test is explicitly forbidden.**

---

## Design Principles

- **Structure precedes implementation**
- **Semantics precede behavior**
- **Invariants precede features**
- **Tests define truth, not convenience**

**If a test fails, the code is wrong — not the test.**

---

## Current Status

This repository is intentionally initialized with minimal executable tests.

At this stage:

- structure is finalized
- semantics are defined
- invariants are being formalized

Test implementations are introduced **incrementally**, starting from domain-level contracts, then expanding outward.

---

## Entry Points

### Documentation

- `docs/philosophy.md` — testing philosophy and intent
- `docs/test-levels.md` — definition of validation layers
- `docs/domain-boundaries.md` — what is tested where (and why)

### Execution

- `scripts/run_domain.sh`
- `scripts/run_aggregate.sh`
- `scripts/run_core.sh`
- `scripts/run_product.sh`

These scripts define the supported execution paths.

Direct invocation outside these paths is discouraged.

---

## Final Note

**If ICE Tests becomes unclear, ICE itself has lost definition.**

This repository exists to ensure that never happens.