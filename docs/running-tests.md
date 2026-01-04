# Running ICE Tests

ICE Tests is intentionally explicit.
There is no “run everything blindly”.

---

## Run by scope

### Domain tests
```bash
./scripts/run_domain.sh ice_ai
```

### Aggregate tests
./scripts/run_aggregate.sh ai_stack

### Core tests
./scripts/run_core.sh

### Product tests
./scripts/run_product.sh ice_studio

## Philosophy

Small scope first

Escalate only when needed

Never run system tests casually

Environment

The repository expects:

Local ICE repos available

Explicit environment configuration

No hidden magic

If a test requires assumptions,
those assumptions must be written.


Environment

The repository expects:

Local ICE repos available

Explicit environment configuration

No hidden magic

If a test requires assumptions,
those assumptions must be written.