# Living Vote Protocol (LVP)

### Version 0.1 — Normative Specification

---

## 1. Purpose

The **Living Vote Protocol (LVP)** defines a **continuous legitimacy system** in which political power is derived from
the **current configuration of individual political profiles**, rather than from periodic elections.

This document specifies **what must exist** for the protocol to function.
It does **not** prescribe technology, platforms, or institutions.

---

## 2. Core Definition

> **The Living Vote is a political protocol in which each citizen owns a persistent, configurable political profile
whose current state continuously contributes to the legitimacy of collective decisions.**

---

## 3. Fundamental Principles (Normative)

The protocol MUST satisfy all of the following principles:

1. **Persistence**
   A political profile exists continuously and does not expire.

2. **Configurability**
   The profile can be modified at any time by its owner.

3. **Reversibility**
   Any delegation or configuration can be withdrawn immediately.

4. **Direct Effect**
   Profile states directly affect aggregated legitimacy.

5. **Transparency of Aggregation**
   Aggregation rules are deterministic and reproducible.

---

## 4. Political Profile (PP)

### 4.1 Definition

A **Political Profile (PP)** is the sole authoritative representation of a citizen’s political voice.

**Invariant:**

> Each citizen has exactly one political profile.

---

### 4.2 Ownership

* The political profile is owned by the citizen.
* No external actor may alter a profile without explicit consent.

---

### 4.3 Minimal Data Model

A political profile MUST contain at least:

| Field           | Description                |
|-----------------|----------------------------|
| `profile_id`    | unique internal identifier |
| `state`         | current voice state        |
| `delegation`    | optional delegation target |
| `configuration` | optional parameters        |
| `history`       | record of state changes    |

---

## 5. Profile States

A political profile MUST be in exactly one of the following states:

* **NEUTRAL** – exists, but has no active effect
* **DIRECT** – directly contributes to aggregation
* **DELEGATED** – contributes via another profile
* **DORMANT** – intentionally inactive but persistent

States MUST be mutually exclusive.

---

## 6. Delegation

### 6.1 Rules

* Delegation is explicit and revocable.
* Delegation does not transfer ownership.
* Delegation chains MAY exist.
* Delegation cycles MUST invalidate affected weight.

---

### 6.2 Effect

Delegated weight is added to the final **DIRECT** target profile, if resolvable.

---

## 7. Aggregation

### 7.1 General Rule

> **Political legitimacy is the aggregation of all current profile states.**

Aggregation MUST be:

* deterministic
* transparent
* reproducible

---

### 7.2 Non-Decision Principle

The protocol:

* MUST NOT make decisions
* MUST NOT enforce outcomes

It only produces **legitimacy signals**.

---

## 8. Decision Context

The result of aggregation is a **Decision Context**, which MAY include:

* distribution of weights
* leading option
* margin of legitimacy
* volatility indicators

Decision Contexts inform decisions but do not replace them.

---

## 9. Technology Neutrality

This protocol intentionally avoids prescribing:

* databases
* cryptography
* blockchains
* user interfaces
* artificial intelligence

Any compliant implementation MUST preserve protocol semantics.

---

## 10. Scope of Validity

This protocol defines:

* logical structure
* state behavior
* aggregation semantics

It does NOT define:

* legal authority
* political legitimacy
* ethical correctness

---

## 11. Status

This document defines the **normative core** of the Living Vote Protocol.
All implementations MUST remain compatible with it.

---

# 📄 Initial version of `invariants.md`

## Living Vote — System Invariants

These invariants define **conditions that must never be violated**.
If any invariant fails, the system is invalid.

---

## I-1: One Profile per Citizen

> A citizen MUST have exactly one political profile.

No duplication. No merging. No substitution.

---

## I-2: Persistence

> A political profile MUST NOT expire or disappear due to inactivity.

Political silence is not political loss.

---

## I-3: Ownership

> Only the profile owner MAY modify the profile state.

No administrative override.

---

## I-4: Reversibility

> Any delegation MUST be revocable at any time.

No lock-in. No minimum duration.

---

## I-5: Deterministic Aggregation

> Given the same profile states, aggregation MUST always produce the same result.

No randomness. No hidden weighting.

---

## I-6: No Implicit Transitions

> Profile states MUST NOT change without explicit user action.

No automatic decay. No timeout effects.

---

## I-7: Cycle Safety

> Delegation cycles MUST NOT produce voting power.

Cycles invalidate affected weight.

---

## I-8: No Decision Authority

> The system MUST NOT make or enforce political decisions.

It only derives legitimacy signals.

---

## I-9: Identity Separation

> Individual identities MUST NOT be inferable from aggregated results.

Legitimacy without exposure.

---

## I-10: Protocol Supremacy

> No implementation detail may override protocol rules.

Code adapts to protocol, not the other way around.

---

## Status

These invariants are **non-negotiable**.
Any system violating one of them is **not a Living Vote implementation**.

---
