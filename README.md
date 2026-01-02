# living-vote-core-proof

Minimal reference implementation proving the core mechanics of the **Living Vote** protocol
via deterministic aggregation and unit tests.

This repository is **not a product**, **not a platform**, and **not a political application**.
It exists solely to **prove the internal consistency and reversibility** of the Living Vote
model at the smallest possible scale.

---

## Purpose

The goal of this repository is to demonstrate that:

- political profiles can exist as persistent state
- profiles can be configured, delegated, and reverted
- aggregation of profiles produces deterministic legitimacy outcomes
- delegation chains are resolvable and cycle-safe
- decision contexts can be *derived*, not *decided*
- all of the above can be **verified by unit tests**

If the tests pass, the theory holds.

---

## What This Is **Not**

This repository deliberately does **not** include:

- ❌ user interfaces
- ❌ authentication or identity management
- ❌ cryptography or encryption
- ❌ databases or persistence layers
- ❌ network or API layers
- ❌ AI-based decision making
- ❌ voting apps or e-democracy tooling

Any of the above would obscure the proof.

---

## Conceptual Model (Minimal)

- **PoliticalProfile**
  - persistent
  - configurable
  - reversible
- **State Machine**
  - NEUTRAL
  - DIRECT
  - DELEGATED
  - DORMANT
- **Delegation**
  - explicit
  - revocable
  - cycle-safe
- **Aggregation**
  - deterministic
  - transparent
  - reproducible
- **DecisionContext**
  - winner
  - margin
  - close-call indicator
  - active vs inactive weight

The system **never decides**.
It only computes legitimacy signals.

---

## Example Issues Used in Tests

The test suite uses realistic but neutral example issues, such as:

- “Should the country leave the EU?”
- “Should weapons be supplied to Israel?”

These labels are **placeholders only**.
The system treats all issues identically and does not encode ideology.

---

## Project Structure

```

living_vote/
model.py        # domain objects (profiles, issues, states)
engine.py       # aggregation and decision-context logic
tests/
test_engine.py  # unit tests proving invariants

````

---

## How the Proof Works

The proof is entirely contained in the unit tests:

- delegation increases effective weight
- delegation withdrawal is immediate
- neutral and dormant profiles have zero weight
- delegation cycles invalidate affected weights
- aggregation results are deterministic
- decision contexts are reproducible

If any test fails, the model is invalid.

---

## Running the Tests

```bash
pip install pytest
pytest -q
````

No additional setup is required.

---

## Design Principle

> The system is not explained.
> It is demonstrated.

---

## Scope of Validity

This repository proves:

* logical consistency
* reversibility
* minimal scalability of the model

It does **not** claim:

* political legitimacy
* legal validity
* societal desirability

Those questions come **after** the proof.

---

## Status

This repository represents **Phase A: Core Proof**.

Subsequent phases (out of scope here):

* protocol formalization
* larger-scale simulation
* legal mapping
* technical implementations

---

## License / Usage

This code is intended as a **reference proof**.
Reuse, fork, and critique are explicitly encouraged.

```
