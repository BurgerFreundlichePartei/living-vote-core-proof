import pytest

from living_vote.model import PoliticalProfile, Issue, State
from living_vote.engine import aggregate_issue


@pytest.fixture
def issues():
    eu_exit = Issue(
        issue_id="EU_EXIT",
        title="Soll das Land aus der EU austreten?",
        options=["JA", "NEIN"],
    )
    arms_israel = Issue(
        issue_id="ARMS_ISRAEL",
        title="Soll das Land Waffen an Israel liefern?",
        options=["JA", "NEIN"],
    )
    return eu_exit, arms_israel


def make_profiles_for_demo(eu_exit: Issue, arms_israel: Issue):
    """
    7 profiles: mix of DIRECT / DELEGATED / NEUTRAL / DORMANT
    """
    p1 = PoliticalProfile("P1", State.DIRECT)
    p2 = PoliticalProfile("P2", State.DIRECT)
    p3 = PoliticalProfile("P3", State.DIRECT)
    p4 = PoliticalProfile("P4", State.DELEGATED, delegated_to="P1")
    p5 = PoliticalProfile("P5", State.DELEGATED, delegated_to="P2")
    p6 = PoliticalProfile("P6", State.NEUTRAL)
    p7 = PoliticalProfile("P7", State.DORMANT)

    # preferences
    # EU_EXIT: P1=NEIN, P2=NEIN, P3=JA
    p1.set_preference(eu_exit, "NEIN")
    p2.set_preference(eu_exit, "NEIN")
    p3.set_preference(eu_exit, "JA")

    # ARMS_ISRAEL: P1=JA, P2=NEIN, P3=NEIN
    p1.set_preference(arms_israel, "JA")
    p2.set_preference(arms_israel, "NEIN")
    p3.set_preference(arms_israel, "NEIN")

    return [p1, p2, p3, p4, p5, p6, p7]


def test_eu_exit_aggregation_with_delegation(issues):
    eu_exit, arms_israel = issues
    profiles = make_profiles_for_demo(eu_exit, arms_israel)

    ctx = aggregate_issue(eu_exit, profiles)

    # Expected:
    # DIRECT votes: P1->NEIN, P2->NEIN, P3->JA  => NEIN=2, JA=1
    # DELEGATED: P4->P1 => NEIN +1, P5->P2 => NEIN +1 => NEIN=4
    assert ctx.totals["NEIN"] == 4.0
    assert ctx.totals["JA"] == 1.0
    assert ctx.winner == "NEIN"
    assert ctx.active_weight == 5.0
    assert ctx.dormant_or_neutral == 2  # P6 + P7


def test_arms_israel_aggregation_with_delegation(issues):
    eu_exit, arms_israel = issues
    profiles = make_profiles_for_demo(eu_exit, arms_israel)

    ctx = aggregate_issue(arms_israel, profiles)

    # DIRECT: P1->JA, P2->NEIN, P3->NEIN => JA=1, NEIN=2
    # DELEGATED: P4->P1 => JA +1, P5->P2 => NEIN +1 => JA=2, NEIN=3
    assert ctx.totals["JA"] == 2.0
    assert ctx.totals["NEIN"] == 3.0
    assert ctx.winner == "NEIN"
    assert ctx.active_weight == 5.0


def test_reversibility_with_withdraw_delegation(issues):
    eu_exit, arms_israel = issues
    profiles = make_profiles_for_demo(eu_exit, arms_israel)

    # withdraw P4 delegation
    p4 = next(p for p in profiles if p.profile_id == "P4")
    p4.state = State.NEUTRAL
    p4.delegated_to = None

    ctx = aggregate_issue(eu_exit, profiles)

    # Previously NEIN=4, JA=1; now remove P4's delegated weight => NEIN=3
    assert ctx.totals["NEIN"] == 3.0
    assert ctx.totals["JA"] == 1.0
    assert ctx.winner == "NEIN"
    assert ctx.active_weight == 4.0


def test_cycle_delegation_is_invalid(issues):
    eu_exit, arms_israel = issues
    profiles = make_profiles_for_demo(eu_exit, arms_israel)

    # create cycle: P4 -> P5, P5 -> P4
    p4 = next(p for p in profiles if p.profile_id == "P4")
    p5 = next(p for p in profiles if p.profile_id == "P5")
    p4.delegated_to = "P5"
    p5.delegated_to = "P4"

    ctx = aggregate_issue(eu_exit, profiles)

    # cycle invalidates both delegated weights => only DIRECT counts: NEIN=2, JA=1
    assert ctx.totals["NEIN"] == 2.0
    assert ctx.totals["JA"] == 1.0
    assert ctx.active_weight == 3.0
