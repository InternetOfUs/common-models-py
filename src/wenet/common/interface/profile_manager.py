from __future__ import absolute_import, annotations

import json
import logging
from typing import List

import requests

from wenet.common.model.user.user_profile import WeNetUserProfile, WeNetUserProfilesPage, UserIdentifiersPage


logger = logging.getLogger("wenet.common.interface.profile_manager")


class ProfileManagerInterface:

    def __init__(self, base_url: str, apikey: str) -> None:
        self._base_url = base_url
        self._apikey = apikey

    def _create_apikey_header(self) -> dict:
        return {"x-wenet-component-apikey": self._apikey}

    def get_user_profile(self, user_id: str) -> WeNetUserProfile:
        result = requests.get(self._base_url + "/profiles/" + user_id, headers=self._create_apikey_header())

        if result.status_code == 200:
            return WeNetUserProfile.from_repr(json.loads(result.content))
        else:
            raise Exception(f"request has return a code {result.status_code} with content {result.content}")

    def delete_user_profile(self, user_id: str) -> None:
        result = requests.delete(self._base_url + "/profiles/" + user_id, headers=self._create_apikey_header())

        if result.status_code == 204:
            return
        else:
            raise Exception(f"request has return a code {result.status_code} with content {result.content}")

    def get_profiles(self) -> List[WeNetUserProfile]:
        profiles = []
        has_got_all_profiles = False
        offset = 0
        while not has_got_all_profiles:
            result = requests.get(self._base_url + "/profiles", headers=self._create_apikey_header(), params={"offset": offset})

            if result.status_code == 200:
                profiles_page = WeNetUserProfilesPage.from_repr(json.loads(result.content))
            else:
                raise Exception(f"request has return a code {result.status_code} with content {result.content}")

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
            result = requests.get(self._base_url + "/userIdentifiers", headers=self._create_apikey_header(), params={"offset": offset})

            if result.status_code == 200:
                user_ids_page = UserIdentifiersPage.from_repr(json.loads(result.content))
            else:
                raise Exception(f"request has return a code {result.status_code} with content {result.content}")

            user_ids.extend(user_ids_page.user_ids)
            offset = len(user_ids)
            if len(user_ids) >= user_ids_page.total:
                has_got_all_user_ids = True

        return user_ids
