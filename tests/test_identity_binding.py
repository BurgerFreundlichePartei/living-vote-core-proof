import pytest

from living_vote.model import Issue, State
from living_vote.registry import CitizenRegistry, IdentityError, AuthorizationError


def test_invariant_one_profile_per_citizen():
    reg = CitizenRegistry()
    reg.create_profile("C1", "P1")

    with pytest.raises(IdentityError):
        reg.create_profile("C1", "P1b")  # same citizen cannot create second profile


def test_invariant_owner_only_can_update_state():
    reg = CitizenRegistry()
    reg.create_profile("C1", "P1")
    reg.create_profile("C2", "P2")

    # C2 tries to modify C1 -> forbidden
    with pytest.raises(AuthorizationError):
        reg.update_state(actor_citizen_id="C2", target_citizen_id="C1", new_state=State.DIRECT)

    # C1 modifies own profile -> ok
    reg.update_state(actor_citizen_id="C1", target_citizen_id="C1", new_state=State.DIRECT)
    assert reg.get_profile("C1").state == State.DIRECT


def test_owner_only_can_set_preference():
    issue = Issue("EU_EXIT", "Soll das Land aus der EU austreten?", ["JA", "NEIN"])
    reg = CitizenRegistry()
    reg.create_profile("C1", "P1")
    reg.create_profile("C2", "P2")

    with pytest.raises(AuthorizationError):
        reg.set_preference(actor_citizen_id="C2", target_citizen_id="C1", issue=issue, option="JA")

    reg.set_preference(actor_citizen_id="C1", target_citizen_id="C1", issue=issue, option="NEIN")
    assert reg.get_profile("C1").preference["EU_EXIT"] == "NEIN"
