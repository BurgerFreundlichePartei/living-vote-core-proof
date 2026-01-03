# Living Vote Protocol — Invariants

These invariants are **non-negotiable**.  
If any invariant is violated, the system is **not** a Living Vote implementation.

This repository is a **Phase A core proof**. Some invariants are validated by tests,
others require identity binding and are introduced in the next step.

---

## I-1: One Profile per Citizen

A citizen MUST have exactly one political profile.

- No duplicate profiles for one citizen.
- No shared profile between citizens.
- A profile MUST be bound to exactly one citizen.

---

## I-2: Persistence

A political profile MUST NOT expire or disappear due to inactivity.

- NEUTRAL and DORMANT profiles remain valid and persistent.
- Inactivity MUST NOT reduce ownership or existence.

---

## I-3: Ownership / Authorization

Only the profile owner (citizen) MAY modify the profile state.

- No administrative override.
- No third-party modification.
- Ownership MUST be enforceable at the domain level (before auth/crypto).

---

## I-4: Reversibility

Any delegation MUST be revocable at any time.

- No lock-in.
- No minimum duration.
- Withdrawal MUST affect aggregation immediately.

---

## I-5: Deterministic Aggregation

Given the same profile states, aggregation MUST always produce the same result.

- No randomness.
- No hidden weighting.
- Tie-break rules MUST be explicit.

---

## I-6: No Implicit Transitions

Profile states MUST NOT change without explicit user action.

- No decay.
- No timeout effects.
- Aggregation MUST NOT mutate profile state.

---

## I-7: Cycle Safety

Delegation cycles MUST NOT produce voting power.

- Cycles invalidate affected delegated weight.
- The system MUST fail safe (exclude invalid weight).

---

## I-8: No Decision Authority

The system MUST NOT make or enforce political decisions.

- It MAY derive a Decision Context (signals).
- It MUST NOT execute outcomes.

---

## I-9: Identity Separation

Individual identities MUST NOT be inferable from aggregated results.

- Aggregation outputs MUST not reveal personal identity.
- Any public representation MUST be anonymized/aggregated.

---

## I-10: Protocol Supremacy

No implementation detail may override protocol rules.

- Code adapts to the protocol.
- Implementations MUST remain compatible with the invariants.

---

## Status Notes (Phase A)

Currently validated by tests:

- I-4, I-5, I-6, I-7, I-8 (behavioral core)

Introduced next (requires identity binding):

- I-1, I-3 (domain-level identity/ownership)
