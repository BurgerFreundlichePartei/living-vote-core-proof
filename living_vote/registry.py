from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .model import PoliticalProfile, State, Issue


class IdentityError(ValueError):
    pass


class AuthorizationError(PermissionError):
    pass


@dataclass
class CitizenRegistry:
    """
    Minimal identity binding layer (Phase A+):
    - Enforces I-1: one profile per citizen
    - Enforces I-3: only owner can mutate their profile (domain-level, no auth system)
    """
    _profiles_by_citizen: Dict[str, PoliticalProfile]

    def __init__(self) -> None:
        self._profiles_by_citizen = {}

    def create_profile(self, citizen_id: str, profile_id: str) -> PoliticalProfile:
        if citizen_id in self._profiles_by_citizen:
            raise IdentityError(f"Citizen '{citizen_id}' already has a profile.")
        profile = PoliticalProfile(profile_id=profile_id, state=State.NEUTRAL)
        self._profiles_by_citizen[citizen_id] = profile
        return profile

    def get_profile(self, citizen_id: str) -> PoliticalProfile:
        if citizen_id not in self._profiles_by_citizen:
            raise IdentityError(f"No profile for citizen '{citizen_id}'.")
        return self._profiles_by_citizen[citizen_id]

    def find_owner(self, profile_id: str) -> Optional[str]:
        for cid, p in self._profiles_by_citizen.items():
            if p.profile_id == profile_id:
                return cid
        return None

    def update_state(
            self,
            actor_citizen_id: str,
            target_citizen_id: str,
            new_state: State,
            delegated_to_profile_id: Optional[str] = None,
    ) -> None:
        if actor_citizen_id != target_citizen_id:
            raise AuthorizationError("Only the profile owner may modify their profile.")
        profile = self.get_profile(target_citizen_id)
        profile.state = new_state
        profile.delegated_to = delegated_to_profile_id

    def set_preference(
            self,
            actor_citizen_id: str,
            target_citizen_id: str,
            issue: Issue,
            option: str,
    ) -> None:
        if actor_citizen_id != target_citizen_id:
            raise AuthorizationError("Only the profile owner may modify their profile.")
        profile = self.get_profile(target_citizen_id)
        profile.set_preference(issue, option)

    def all_profiles(self) -> list[PoliticalProfile]:
        return list(self._profiles_by_citizen.values())
