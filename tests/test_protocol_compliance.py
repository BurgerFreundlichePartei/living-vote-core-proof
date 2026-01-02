from living_vote.model import PoliticalProfile, Issue, State
from living_vote.engine import aggregate_issue


def test_invariant_determinism_same_input_same_output():
    issue = Issue("EU_EXIT", "Soll das Land aus der EU austreten?", ["JA", "NEIN"])

    p1 = PoliticalProfile("P1", State.DIRECT); p1.set_preference(issue, "NEIN")
    p2 = PoliticalProfile("P2", State.DIRECT); p2.set_preference(issue, "JA")
    p3 = PoliticalProfile("P3", State.DELEGATED, delegated_to="P1")
    p4 = PoliticalProfile("P4", State.DORMANT)
    profiles = [p1, p2, p3, p4]

    ctx1 = aggregate_issue(issue, profiles)
    ctx2 = aggregate_issue(issue, profiles)

    assert ctx1.totals == ctx2.totals
    assert ctx1.winner == ctx2.winner
    assert ctx1.margin == ctx2.margin
    assert ctx1.close_call == ctx2.close_call


def test_invariant_no_implicit_transitions():
    issue = Issue("ARMS_ISRAEL", "Soll das Land Waffen an Israel liefern?", ["JA", "NEIN"])

    p1 = PoliticalProfile("P1", State.NEUTRAL)
    p2 = PoliticalProfile("P2", State.DORMANT)
    profiles = [p1, p2]

    # Aggregation must not mutate profile states
    _ = aggregate_issue(issue, profiles)

    assert p1.state == State.NEUTRAL
    assert p2.state == State.DORMANT


def test_invariant_cycle_safety_invalidates_weight():
    issue = Issue("EU_EXIT", "Soll das Land aus der EU austreten?", ["JA", "NEIN"])

    p1 = PoliticalProfile("P1", State.DIRECT); p1.set_preference(issue, "NEIN")
    p2 = PoliticalProfile("P2", State.DELEGATED, delegated_to="P3")
    p3 = PoliticalProfile("P3", State.DELEGATED, delegated_to="P2")  # cycle with P2
    profiles = [p1, p2, p3]

    ctx = aggregate_issue(issue, profiles)

    # only P1 counts
    assert ctx.totals["NEIN"] == 1.0
    assert ctx.totals["JA"] == 0.0
    assert ctx.active_weight == 1.0
