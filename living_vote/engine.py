from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from .model import PoliticalProfile, Issue, State


@dataclass(frozen=True)
class DecisionContext:
    issue_id: str
    title: str
    totals: Dict[str, float]          # option -> aggregated weight
    winner: str                       # option name
    margin: float                     # winner - runner_up
    close_call: bool                  # margin below threshold
    active_weight: float              # total weight participating (DIRECT+DELEGATED effective)
    dormant_or_neutral: int           # count of profiles not participating


def _resolve_delegation_chain(
    start_id: str,
    profiles: Dict[str, PoliticalProfile],
    max_hops: int = 10
) -> Optional[str]:
    """
    Resolve where voting weight ultimately lands.
    Returns final target profile_id if resolvable, else None.
    Rules:
      - Delegation must land on a profile that is DIRECT (to be effective).
      - Cycles or too deep chains => invalid => weight becomes inactive.
    """
    seen: Set[str] = set()
    cur = start_id
    hops = 0

    while True:
        if cur in seen:
            return None  # cycle
        seen.add(cur)

        p = profiles.get(cur)
        if not p:
            return None

        if p.state == State.DIRECT:
            return cur

        if p.state != State.DELEGATED:
            return None  # delegated weight cannot land on NEUTRAL/DORMANT

        if p.delegated_to is None:
            return None

        cur = p.delegated_to
        hops += 1
        if hops > max_hops:
            return None


def aggregate_issue(
    issue: Issue,
    profiles_list: List[PoliticalProfile],
    close_call_threshold: float = 0.5
) -> DecisionContext:
    """
    Deterministic aggregation:
      - DIRECT profile contributes weight 1 to its chosen option (if preference set).
      - DELEGATED profile contributes weight 1 to the final DIRECT target's option,
        but only if delegation resolves and target has a preference.
      - NEUTRAL and DORMANT contribute 0.
    """
    profiles: Dict[str, PoliticalProfile] = {p.profile_id: p for p in profiles_list}

    totals: Dict[str, float] = {opt: 0.0 for opt in issue.options}
    active_weight = 0.0
    dormant_or_neutral = 0

    def add_vote(option: Optional[str], weight: float) -> None:
        nonlocal active_weight
        if option is None:
            return
        if option not in totals:
            return
        totals[option] += weight
        active_weight += weight

    for p in profiles_list:
        if p.state in (State.NEUTRAL, State.DORMANT):
            dormant_or_neutral += 1
            continue

        if p.state == State.DIRECT:
            opt = p.preference.get(issue.issue_id)
            add_vote(opt, 1.0)
            continue

        if p.state == State.DELEGATED:
            target_id = _resolve_delegation_chain(p.profile_id, profiles)
            if not target_id:
                continue
            target = profiles[target_id]
            opt = target.preference.get(issue.issue_id)
            add_vote(opt, 1.0)
            continue

    # determine winner deterministically: max total, tie-break by option order
    ordered = [(opt, totals[opt]) for opt in issue.options]
    ordered.sort(key=lambda x: (-x[1], issue.options.index(x[0])))
    winner, winner_val = ordered[0]
    runner_up_val = ordered[1][1] if len(ordered) > 1 else 0.0
    margin = winner_val - runner_up_val
    close_call = margin < close_call_threshold

    return DecisionContext(
        issue_id=issue.issue_id,
        title=issue.title,
        totals=totals,
        winner=winner,
        margin=margin,
        close_call=close_call,
        active_weight=active_weight,
        dormant_or_neutral=dormant_or_neutral,
    )
