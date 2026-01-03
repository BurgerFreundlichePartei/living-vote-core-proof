# Protocol Compliance — living-vote-core-proof

This document maps the **Living Vote Protocol (LVP)** specification and invariants
to the reference implementation contained in this repository.

This repository represents **Phase A: Core Proof**.
It proves the logical correctness of the protocol at minimal scale.

---

## Scope

Implemented and verified in this repository:

- Political Profiles (PP)
- Profile State Machine
- Delegation and Delegation Resolution
- Cycle Safety
- Deterministic Aggregation
- Decision Context derivation (non-decision)
- Identity Binding (domain-level)
- Ownership Enforcement (domain-level)

Explicitly out of scope:

- Authentication systems
- Cryptography
- Persistence layers (DB)
- User interfaces
- Networking / APIs
- AI-based decision making

---

## Protocol Sections → Implementation Mapping

### LVP §2 — Core Definition

**Spec:** Legitimacy is derived from current profile configuration  
**Implementation:**

- `PoliticalProfile` holds current state and preferences
- `aggregate_issue()` derives legitimacy deterministically

Files:

- `living_vote/model.py`
- `living_vote/engine.py`

---

### LVP §3 — Fundamental Principles

| Principle               | Status | Evidence                                                    |
|-------------------------|--------|-------------------------------------------------------------|
| Persistence             | ✔      | NEUTRAL/DORMANT profiles persist and contribute zero weight |
| Configurability         | ✔      | Profile state & preferences mutable via registry            |
| Reversibility           | ✔      | Delegation withdrawal immediately affects aggregation       |
| Direct Effect           | ✔      | DIRECT profiles add weight directly                         |
| Transparent Aggregation | ✔      | Deterministic totals and tie-break rules                    |

---

## Political Profile (PP)

### LVP §4.3 — Minimal Data Model

| Field         | Implemented | Notes                                       |
|---------------|-------------|---------------------------------------------|
| profile_id    | ✔           | Unique identifier                           |
| state         | ✔           | Enum-based state machine                    |
| delegation    | ✔           | Explicit delegated target                   |
| configuration | ◐           | Implemented minimally via issue preferences |
| history       | ✖           | Deferred (not required for Phase A proof)   |

---

## Identity & Ownership (Phase A+)

### Invariant I-1 — One Profile per Citizen

**Status:** ✔ Enforced

**Implementation:**

- `CitizenRegistry` ensures a strict 1:1 mapping:

```

citizen_id → PoliticalProfile

```

- Duplicate profile creation is rejected.

Files:

- `living_vote/registry.py`

Tests:

- `tests/test_identity_binding.py::test_invariant_one_profile_per_citizen`

---

### Invariant I-3 — Ownership / Authorization

**Status:** ✔ Enforced

**Implementation:**

- All profile mutations go through `CitizenRegistry`
- Only the owning `citizen_id` may:
- change profile state
- set preferences
- create delegation

Unauthorized access raises `AuthorizationError`.

Files:

- `living_vote/registry.py`

Tests:

- `tests/test_identity_binding.py::test_invariant_owner_only_can_update_state`
- `tests/test_identity_binding.py::test_owner_only_can_set_preference`

---

## Delegation

### LVP §6 — Delegation Rules

**Status:** ✔ Fully implemented

- Explicit delegation only
- Chains supported
- Cycles invalidate weight
- Delegation is revocable at any time

Files:

- `living_vote/engine.py::_resolve_delegation_chain`

Tests:

- `test_cycle_delegation_is_invalid`
- `test_reversibility_with_withdraw_delegation`

---

## Aggregation

### LVP §7 — Deterministic Aggregation

**Status:** ✔ Verified

- Aggregation is deterministic
- Given identical inputs, outputs are identical
- Aggregation does not mutate profile state

Files:

- `living_vote/engine.py::aggregate_issue`

Tests:

- `test_invariant_determinism_same_input_same_output`
- `test_invariant_no_implicit_transitions`

---

## Decision Context

### LVP §8 — Non-Decision Principle

**Status:** ✔ Enforced by design

- System derives legitimacy signals only
- No decisions are executed or enforced
- Output is a pure `DecisionContext`

Files:

- `living_vote/engine.py::DecisionContext`

---

## Invariants Coverage Summary

| Invariant                   | Status                                 |
|-----------------------------|----------------------------------------|
| I-1 One Profile per Citizen | ✔                                      |
| I-2 Persistence             | ✔                                      |
| I-3 Ownership               | ✔                                      |
| I-4 Reversibility           | ✔                                      |
| I-5 Determinism             | ✔                                      |
| I-6 No Implicit Transitions | ✔                                      |
| I-7 Cycle Safety            | ✔                                      |
| I-8 No Decision Authority   | ✔                                      |
| I-9 Identity Separation     | ◐ (conceptual, no public output layer) |
| I-10 Protocol Supremacy     | ✔                                      |

---

## Conclusion

The reference implementation is now compliant with the **complete behavioral
and identity-related core** of the Living Vote Protocol.

What is proven:

- The protocol is internally consistent
- Identity binding does not break aggregation
- Ownership enforcement does not require authentication
- Core legitimacy logic is reproducible and testable

What remains intentionally open:

- Persistence technologies
- Cryptographic identity
- Legal embedding
- Scaling & performance
- UI / UX

---

## Status

**Phase A: COMPLETE**

This repository now constitutes a **full core proof** of the Living Vote Protocol.
