# Product Testing

ICE is a platform.
Products are consumers of the platform.

This distinction is absolute.

---

## ICE Core
- Must function headless
- Must survive without products
- Must preserve invariants

Tested in:
- core/
- domains/
- aggregates/

---

## Products (e.g. ICE Studio)
- Define UX
- Define workflows
- Define upgrade paths

Tested in:
- products/<product_name>/

---

## Product tests focus on:
- User intent
- UX correctness
- Backward compatibility
- Data migration

---

## Forbidden

Products must NOT:
- Test core invariants
- Redefine platform behavior
- Patch around core failures

If a product test reveals a core bug,
the fix belongs in Core — not in the product.
