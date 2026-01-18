# ICE Tests
## Canonical Validation Authority of the ICE Ecosystem

ICE Tests is the **validation authority** of the ICE ecosystem.

This repository does not merely test implementations.
It defines and enforces the **structural, semantic, and cognitive constraints**
that ICE must obey over time.

ICE Tests is where ICE is **proven**,
not just exercised.

---

## Important Notice

ICE Tests is **not** a distributable package.

Do **not** run:

```bash
pip install -e .
```

ICE Tests is a validation harness.

It is executed exclusively via pytest
and consumes the real ICE packages installed
in the active environment.

Attempting to install this repository
is considered a configuration error by design.

Purpose

ICE is a modular system composed of:

independent domains

cooperative subsystems

user-facing products

long-running executions

ICE Tests exists to preserve:

architectural intent

semantic invariants

cross-domain correctness

long-term system identity

As ICE evolves,
this repository ensures it does not drift.

Scope of Authority

ICE Tests is authoritative over:

domain-level correctness

cross-domain interaction rules

platform-level invariants

product-level guarantees

If a behavior is not validated here, it is not guaranteed by ICE.

Documentation may explain.
Code may execute.

Tests decide what is acceptable.

What This Repository Is

ICE Tests is:

a semantic contract for ICE behavior

a governance mechanism over system evolution

a guardrail against architectural erosion

a validation framework for large-scale refactoring

ICE Tests allows ICE to change
without losing its identity.

What This Repository Is Not

ICE Tests is not:

a mirror of production repositories

a collection of ad-hoc tests

a playground for experiments

a substitute for observability or monitoring

Tests here are:

intentional

declarative

durable

Convenience is not a goal.

Test Topology

ICE Tests is organized into four strictly separated layers:

domains/
Local responsibility and isolated invariants

aggregates/
Cooperative subsystems spanning multiple domains

core/
ICE as a platform-level cognitive system

products/
User-facing applications built on top of ICE

Crossing layers within a single test
is explicitly forbidden.

Each layer answers a different class of questions.

Design Principles

Structure precedes implementation

Semantics precede behavior

Invariants precede features

Tests define truth, not convenience

If a test fails, the code is wrong — not the test.

Current Status

This repository is intentionally initialized
with minimal executable tests.

At this stage:

structure is finalized

semantics are defined

invariants are formalized

Test implementations are introduced incrementally,
starting from domain contracts
and expanding outward.

Entry Points
Documentation

docs/philosophy.md — testing philosophy

docs/test-levels.md — validation layers

docs/domain-boundaries.md — what is tested where (and why)

Execution

scripts/run_domain.sh

scripts/run_aggregate.sh

scripts/run_core.sh

scripts/run_product.sh

These scripts define the supported execution paths.

Direct invocation outside these paths
is discouraged.

Canonical Status

ICE Tests is normative.

If ICE Tests becomes unclear,
ICE itself has lost definition.

This repository exists
to ensure that never happens.