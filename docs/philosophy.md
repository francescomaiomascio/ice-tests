# ICE Tests — Philosophy

ICE Tests is not a test suite.
It is the epistemic backbone of the ICE ecosystem.

This repository exists to answer one question only:

> **What is ICE allowed to be?**

Tests are not written to increase coverage.
They are written to **preserve meaning** while the system evolves.

## Core principles

### 1. Tests define truth, not implementation
Implementation is temporary.
Tests encode invariants.

If an implementation changes but tests remain valid, the system is still ICE.
If tests fail, ICE has changed — intentionally or not.

### 2. Structure precedes execution
A system without clear test topology degenerates.
ICE Tests defines structure *before* behavior.

### 3. Separation of concerns is non-negotiable
- Domains test themselves
- Aggregates test cooperation
- Core tests system existence
- Products test user-facing behavior

Mixing these levels destroys signal.

### 4. No test is neutral
Every test encodes a belief about ICE.
Beliefs must be explicit, reviewable, and intentional.

### 5. ICE is a platform, not an app
ICE Core must survive without any product.
Products may evolve or die.
Core invariants must not.

## Final rule

> **If ICE Tests is unclear, ICE itself is unclear.**

This repository is the canonical source of clarity.
