from __future__ import absolute_import, annotations

from typing import List

from wenet.common.model.user.user_profile import CoreWeNetUserProfile


class TokenDetails:

    def __init__(self, profile_id: str, app_id: str, scopes: List[str]):
        self.profile_id = profile_id
        self.app_id = app_id
        self.scopes = scopes

    def to_repr(self) -> dict:
        return {
            "profileId": self.profile_id,
            "appId": self.app_id,
            "scopes": self.scopes
        }

    @staticmethod
    def from_repr(raw_data: dict) -> TokenDetails:
        return TokenDetails(
            profile_id=raw_data["profileId"],
            app_id=raw_data["appId"],
            scopes=raw_data["scopes"]
        )

    def __eq__(self, o):
        if not isinstance(o, TokenDetails):
            return False
        return self.profile_id == o.profile_id and self.app_id == o.app_id and self.scopes == o.scopes
