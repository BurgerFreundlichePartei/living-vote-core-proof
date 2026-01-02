# Protocol Compliance — living-vote-core-proof

This document maps the Living Vote Protocol (LVP) specification to the current codebase
(`living_vote/model.py`, `living_vote/engine.py`) and the unit tests.

## Scope

This repository is a **Phase A proof**. It implements:
- Political Profiles (minimal data model)
- State machine (NEUTRAL/DIRECT/DELEGATED/DORMANT)
- Delegation resolution (including cycle invalidation)
- Deterministic aggregation
- Decision Context derivation (non-decision)

Out of scope (by design):
- Identity management, authentication, cryptography, databases, UI, networking, AI

---

## LVP Sections → Implementation Mapping

### 2. Core Definition
**Spec:** profiles persist and contribute to legitimacy by current state  
**Code:** `PoliticalProfile` stores persistent state (in-memory for the proof)
- `living_vote/model.py: PoliticalProfile`

### 3. Fundamental Principles
1) Persistence
- **Proof:** profiles exist independent of participation state
- **Code:** profiles always remain in list; NEUTRAL/DORMANT contribute zero weight
- **Tests:** `test_*` cover NEUTRAL/DORMANT -> weight 0

2) Configurability
- **Proof:** profile state and delegation can be changed at any time
- **Code:** mutable dataclass fields `state`, `delegated_to`, `preference`
- **Tests:** `test_reversibility_with_withdraw_delegation`

3) Reversibility
- **Proof:** delegation withdrawal has immediate effect
- **Code:** state changes affect next aggregation call deterministically
- **Tests:** `test_reversibility_with_withdraw_delegation`

4) Direct Effect
- **Proof:** DIRECT profiles contribute weight directly to issue option
- **Code:** `aggregate_issue()` adds weight for DIRECT preference
- **File:** `living_vote/engine.py: aggregate_issue`

5) Transparency of Aggregation
- **Proof:** deterministic totals, winner selection defined and reproducible
- **Code:** totals computed deterministically; tie-break by issue option order
- **File:** `living_vote/engine.py: aggregate_issue`

---

## 4. Political Profile (PP)
### 4.3 Minimal Data Model
**Spec:** `profile_id`, `state`, `delegation`, `configuration`, `history`  
**Code (Phase A):**
- Implemented: `profile_id`, `state`, `delegated_to`, `preference` (acts as minimal config for issues)
- Not implemented (explicitly out of scope): `history`, generalized `configuration`

**Rationale:** Phase A is proof-of-mechanics. Persistence/history is a later phase.

---

## 5. Profile States
**Spec:** exactly one state at any time  
**Code:** `state: State` Enum in `PoliticalProfile`
- `living_vote/model.py: State`

---

## 6. Delegation
### 6.1 Rules
- Revocable: implemented via state/delegation change
- Chains: supported through `_resolve_delegation_chain()`
- Cycles invalid: cycles return `None` → delegated weight not counted

**Code:** `living_vote/engine.py: _resolve_delegation_chain`

**Tests:** `test_cycle_delegation_is_invalid`

---

## 7. Aggregation
### 7.1 Deterministic
**Code:** deterministic loop + deterministic winner selection  
**Tests:** covered by explicit numeric assertions

### 7.2 Non-Decision Principle
**Spec:** protocol must not enforce outcomes  
**Code:** returns `DecisionContext` only; no side effects, no persistence, no enforcement
- `living_vote/engine.py: DecisionContext`, `aggregate_issue()`

---

## 8. Decision Context
**Spec:** derived signals (winner, margin, close-call)  
**Code:** `DecisionContext` includes winner, margin, close_call, totals

---

## Invariants → Tests Mapping

- I-5 Deterministic Aggregation:
    - `test_*` asserts exact totals and winner
- I-4 Reversibility:
    - `test_reversibility_with_withdraw_delegation`
- I-7 Cycle Safety:
    - `test_cycle_delegation_is_invalid`
- I-8 No Decision Authority:
    - enforced by design: engine returns context only (no effects)
- I-2 Persistence:
    - demonstrated by NEUTRAL/DORMANT contributing 0, not disappearing

Note: I-1 (One profile per citizen) and I-3 (Ownership) are out of scope for Phase A,
because identity/auth are intentionally not implemented. They become testable once
identity binding exists.

---

## Status

This repository is compliant with the **behavioral core** of LVP:
- states, delegation, aggregation, determinism, non-decision

Identity binding, persistence layers, and security constraints are explicitly deferred.
