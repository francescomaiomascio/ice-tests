# CI Strategy (Conceptual)

CI exists to enforce invariants, not speed.

---

## CI tiers

### Tier 1 — Domain CI
- Unit
- Integration
- Contract

Runs on every commit.

---

### Tier 2 — Aggregate CI
- Integration
- Selected e2e

Runs on merge or nightly.

---

### Tier 3 — Core CI
- Full boot
- Critical flows

Runs on release candidates only.

---

### Tier 4 — Product CI
- UX flows
- Upgrade paths

Runs per product lifecycle.

---

## Principle

> CI must fail loudly and meaningfully.

Flaky tests are removed.
Silent failures are unacceptable.

CI is a guardian, not a checkbox.