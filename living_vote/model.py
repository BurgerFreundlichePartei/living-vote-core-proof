from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, List


class State(str, Enum):
    NEUTRAL = "NEUTRAL"      # exists but not used
    DIRECT = "DIRECT"        # votes directly
    DELEGATED = "DELEGATED"  # delegates voting power
    DORMANT = "DORMANT"      # intentionally not used (still exists)


@dataclass(frozen=True)
class Issue:
    """
    A single decision topic with named options.
    Example: "EU Austritt" -> ["JA", "NEIN"]
    """
    issue_id: str
    title: str
    options: List[str]

    def __post_init__(self) -> None:
        if len(self.options) < 2:
            raise ValueError("Issue must have at least two options.")
        if len(set(self.options)) != len(self.options):
            raise ValueError("Issue options must be unique.")


@dataclass
class PoliticalProfile:
    """
    Minimal political profile: state + optional delegation + per-issue preference.
    preference[issue_id] = option string (must be one of Issue.options)
    """
    profile_id: str
    state: State = State.NEUTRAL
    delegated_to: Optional[str] = None
    preference: Dict[str, str] = field(default_factory=dict)

    def set_preference(self, issue: Issue, option: str) -> None:
        if option not in issue.options:
            raise ValueError(f"Invalid option '{option}' for issue '{issue.title}'.")
        self.preference[issue.issue_id] = option
