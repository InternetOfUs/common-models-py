from __future__ import absolute_import, annotations

from typing import List

from wenet.common.model.user.user_profile import CoreWeNetUserProfile


class TokenDetails:

    def __init__(self, profile: CoreWeNetUserProfile, app_id: str, scopes: List[str]):
        self.profile = profile
        self.app_id = app_id
        self.scopes = scopes

    def to_repr(self) -> dict:
        return {
            "profile": self.profile.to_repr(),
            "appId": self.app_id,
            "scopes": self.scopes
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TokenDetails:
        return TokenDetails(
            profile=CoreWeNetUserProfile.from_repr(raw_data["profile"]),
            app_id=raw_data["appId"],
            scopes=raw_data["scopes"]
        )

    def __eq__(self, o):
        if not isinstance(o, TokenDetails):
            return False
        return self.profile == o.profile and self.app_id == o.app_id and self.scopes == o.scopes
