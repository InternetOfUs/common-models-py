from __future__ import absolute_import, annotations

import logging
import os
from typing import List, Optional

from wenet.common.interface.component import ComponentInterface
from wenet.common.interface.client import RestClient
from wenet.common.model.user.user_profile import WeNetUserProfile, WeNetUserProfilesPage, UserIdentifiersPage


logger = logging.getLogger("wenet.common.interface.profile_manager")


class ProfileManagerInterface(ComponentInterface):

    COMPONENT_PATH = os.getenv("PROFILE_MANAGER_PATH", "/profile_manager")

    def __init__(self, client: RestClient, instance: str = ComponentInterface.PRODUCTION_INSTANCE, base_headers: Optional[dict] = None) -> None:
        base_url = instance + self.COMPONENT_PATH
        super().__init__(client, base_url, base_headers)

    def get_user_profile(self, user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/profiles/{user_id}", headers=headers)

        if response.status_code in [200, 202]:
            return WeNetUserProfile.from_repr(response.json())
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def update_user_profile(self, profile: WeNetUserProfile, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        profile_repr = profile.to_repr()
        profile_repr.pop("_creationTs", None)
        profile_repr.pop("_lastUpdateTs", None)

        response = self._client.put(f"{self._base_url}/profiles/{profile.profile_id}", body=profile_repr, headers=headers)

        if response.status_code in [200, 202]:
            return
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def create_empty_user_profile(self, user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        profile_repr = {
            "id": user_id
        }

        response = self._client.put(f"{self._base_url}/profiles", body=profile_repr, headers=headers)
        if response.status_code in [200, 201, 202]:
            return WeNetUserProfile.empty(user_id)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def delete_user_profile(self, user_id: str, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.delete(f"{self._base_url}/profiles/{user_id}", headers=headers)

        if response.status_code not in [200, 204]:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def get_profiles(self, headers: Optional[dict] = None) -> List[WeNetUserProfile]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        profiles = []
        has_got_all_profiles = False
        offset = 0
        while not has_got_all_profiles:
            response = self._client.get(f"{self._base_url}/profiles", query_params={"offset": offset}, headers=headers)

            if response.status_code in [200, 202]:
                profiles_page = WeNetUserProfilesPage.from_repr(response.json())
            else:
                raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

            profiles.extend(profiles_page.profiles)
            offset = len(profiles)
            if len(profiles) >= profiles_page.total:
                has_got_all_profiles = True

        return profiles

    def get_profile_user_ids(self, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        user_ids = []
        has_got_all_user_ids = False
        offset = 0
        while not has_got_all_user_ids:
            response = self._client.get(f"{self._base_url}/userIdentifiers", query_params={"offset": offset}, headers=headers)

            if response.status_code in [200, 202]:
                user_ids_page = UserIdentifiersPage.from_repr(response.json())
            else:
                raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

            user_ids.extend(user_ids_page.user_ids)
            offset = len(user_ids)
            if len(user_ids) >= user_ids_page.total:
                has_got_all_user_ids = True

        return user_ids