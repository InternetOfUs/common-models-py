from __future__ import absolute_import, annotations

import logging
from typing import List

from wenet.common.interface.base import BaseInterface
from wenet.common.interface.client import RestClient
from wenet.common.model.user.user_profile import WeNetUserProfile, WeNetUserProfilesPage, UserIdentifiersPage


logger = logging.getLogger("wenet.common.interface.profile_manager")


class ProfileManagerInterface(BaseInterface):

    def __init__(self, client: RestClient, instance: str = BaseInterface.PRODUCTION_INSTANCE) -> None:
        base_url = instance + "/profile_manager"
        super().__init__(client, base_url)

    def get_user_profile(self, user_id: str) -> WeNetUserProfile:
        response = self._client.get(self._base_url + "/profiles/" + user_id)

        if response.status_code == 200:
            return WeNetUserProfile.from_repr(response.json())
        else:
            raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

    def delete_user_profile(self, user_id: str) -> None:
        response = self._client.delete(self._base_url + "/profiles/" + user_id)

        if response.status_code not in [200, 204]:
            raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

    def get_profiles(self) -> List[WeNetUserProfile]:
        profiles = []
        has_got_all_profiles = False
        offset = 0
        while not has_got_all_profiles:
            response = self._client.get(self._base_url + "/profiles", query_params={"offset": offset})

            if response.status_code == 200:
                profiles_page = WeNetUserProfilesPage.from_repr(response.json())
            else:
                raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

            profiles.extend(profiles_page.profiles)
            offset = len(profiles)
            if len(profiles) >= profiles_page.total:
                has_got_all_profiles = True

        return profiles

    def get_profile_user_ids(self) -> List[str]:
        user_ids = []
        has_got_all_user_ids = False
        offset = 0
        while not has_got_all_user_ids:
            response = self._client.get(self._base_url + "/userIdentifiers", query_params={"offset": offset})

            if response.status_code == 200:
                user_ids_page = UserIdentifiersPage.from_repr(response.json())
            else:
                raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

            user_ids.extend(user_ids_page.user_ids)
            offset = len(user_ids)
            if len(user_ids) >= user_ids_page.total:
                has_got_all_user_ids = True

        return user_ids
