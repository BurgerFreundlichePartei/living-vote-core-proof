from living_vote.model import Issue, State
from living_vote.engine import aggregate_issue
from living_vote.registry import CitizenRegistry


def test_registry_profiles_work_with_engine():
    issue = Issue("EU_EXIT", "Soll das Land aus der EU austreten?", ["JA", "NEIN"])
    reg = CitizenRegistry()

    reg.create_profile("C1", "P1")
    reg.create_profile("C2", "P2")
    reg.create_profile("C3", "P3")

    reg.update_state("C1", "C1", State.DIRECT)
    reg.update_state("C2", "C2", State.DIRECT)
    reg.update_state("C3", "C3", State.DELEGATED, delegated_to_profile_id="P1")

    reg.set_preference("C1", "C1", issue, "NEIN")
    reg.set_preference("C2", "C2", issue, "JA")

    ctx = aggregate_issue(issue, reg.all_profiles())
    # P1 gets delegated weight from P3 => NEIN=2, JA=1
    assert ctx.totals["NEIN"] == 2.0
    assert ctx.totals["JA"] == 1.0
    assert ctx.winner == "NEIN"
