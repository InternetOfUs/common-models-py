from __future__ import absolute_import, annotations

import logging
from typing import List, Optional

from wenet.interface.component import ComponentInterface
from wenet.interface.client import RestClient
from wenet.model.user.profile import WeNetUserProfile, WeNetUserProfilesPage, UserIdentifiersPage, PatchWeNetUserProfile
from wenet.model.user.relationship import RelationshipPage, Relationship

logger = logging.getLogger("wenet.interface.profile_manager")


class ProfileManagerInterface(ComponentInterface):

    def __init__(self, client: RestClient, platform_url: str, component_path: str = "/profile_manager",
                 extra_headers: Optional[dict] = None) -> None:
        base_url = platform_url + component_path
        super().__init__(client, base_url, extra_headers)

    def get_user_profile(self, user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/profiles/{user_id}", headers=headers)

        if response.status_code in [200, 202]:
            return WeNetUserProfile.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def update_user_profile(self, profile: WeNetUserProfile, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        profile_repr = profile.to_repr()
        profile_repr.pop("_creationTs", None)
        profile_repr.pop("_lastUpdateTs", None)

        response = self._client.put(f"{self._base_url}/profiles/{profile.profile_id}", body=profile_repr,
                                    headers=headers)

        if response.status_code in [200, 202]:
            return WeNetUserProfile.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def patch_user_profile(self, profile_patch: PatchWeNetUserProfile,
                           headers: Optional[dict] = None) -> WeNetUserProfile:
        """
        Only the fields with value different from None in the profile_patch will be patched
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.patch(f"{self._base_url}/profiles/{profile_patch.profile_id}",
                                      body=profile_patch.to_patch(), headers=headers)

        if response.status_code in [200, 202]:
            return WeNetUserProfile.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def create_empty_user_profile(self, user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        profile_repr = {
            "id": user_id
        }

        response = self._client.post(f"{self._base_url}/profiles", body=profile_repr, headers=headers)
        if response.status_code in [200, 201, 202]:
            return WeNetUserProfile.empty(user_id)
        else:
            raise self.get_api_exception_for_response(response)

    def delete_user_profile(self, user_id: str, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.delete(f"{self._base_url}/profiles/{user_id}", headers=headers)

        if response.status_code not in [200, 204]:
            raise self.get_api_exception_for_response(response)

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
                raise self.get_api_exception_for_response(response)

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
            response = self._client.get(f"{self._base_url}/userIdentifiers", query_params={"offset": offset},
                                        headers=headers)

            if response.status_code in [200, 202]:
                user_ids_page = UserIdentifiersPage.from_repr(response.json())
            else:
                raise self.get_api_exception_for_response(response)

            user_ids.extend(user_ids_page.user_ids)
            offset = len(user_ids)
            if len(user_ids) >= user_ids_page.total:
                has_got_all_user_ids = True

        return user_ids

    def get_relationship_page(self,
                              app_id: Optional[str],
                              source_id: Optional[str] = None,
                              target_id: Optional[str] = None,
                              relation_type: Optional[str] = None,
                              weight_from: Optional[float] = None,
                              weight_to: Optional[float] = None,
                              order: Optional[str] = None,
                              offset: int = 0,
                              limit: int = 10,
                              headers: Optional[dict] = None
                              ) -> RelationshipPage:
        """
        Get all the relationships that match the request parameters
        :param app_id: An application identifier to be equals on the social network relationships to return.
        You can use a Perl compatible regular expressions (PCRE) that has to match the application identifier of
        the relationships if you write between '/'. For example to get the relationships for the applications '1' and '2' you must pass as 'appId' '/^[1|2]$/'.
        :param source_id: A user identifier to be equals on the relationships source to return. You can use a Perl
        compatible regular expressions (PCRE) that has to match the user identifier of the relationships source if you
        write between '/'. For example to get the relationships with the source users '1' and '2' you must pass as 'source' '/^[1|2]$/'.
        :param target_id: A user identifier to be equals on the relationships target to return. You can use a Perl compatible regular expressions (PCRE) that has to match the user identifier of the relationships target if you write between '/'. For example to get the relationships with the target users '1' and '2' you must pass as 'target' '/^[1|2]$/'.
        :param relation_type: The type for the relationships to return. You can use a Perl compatible regular expressions (PCRE) that has to match the type of the relationships if you write between '/'. For example to get the relationships with the types 'friend' and 'colleague' you must pass as 'type' '/^[friend|colleague]$/'.
        :param weight_from: The minimal weight, inclusive, of the relationships to return.
        :param weight_to: The maximal weight, inclusive, of the relationships to return.
        :param order: The order in witch the relationships has to be returned. For each field it has be separated by a ',' and each field can start with '+' (or without it) to order on ascending order, or with the prefix '-' to do on descendant order.
        :param offset: The index of the first social network relationship to return.
        :param limit: The number maximum of social network relationships to return
        :param headers: Additional headers to add in the http request
        :return: An object representing a relationships page.
        :raise: ApiException if the request does not return a 200 code. KeyError if the methods is not able to create a RelationshipPage object
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        query_params_temp = {
            "appId": app_id,
            "sourceId": source_id,
            "targetId": target_id,
            "type": relation_type,
            "weightFrom": weight_from,
            "weightTo": weight_to,
            "order": order,
            "offset": offset,
            "limit": limit
        }

        query_params = {}

        for param, value in query_params_temp.items():
            if value is not None:
                query_params[param] = value

        response = self._client.get(f"{self._base_url}/relationships", query_params=query_params, headers=headers)

        if response.status_code == 200:
            return RelationshipPage.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def get_relationships(self,
                          app_id: Optional[str],
                          source_id: Optional[str] = None,
                          target_id: Optional[str] = None,
                          relation_type: Optional[str] = None,
                          weight_from: Optional[float] = None,
                          weight_to: Optional[float] = None,
                          order: Optional[str] = None,
                          headers: Optional[dict] = None
                          ) -> List[Relationship]:
        relationships = []
        has_got_all_relationships = False
        offset = 0
        limit = 100
        while not has_got_all_relationships:
            relationship_page = self.get_relationship_page(
                app_id=app_id,
                source_id=source_id,
                target_id=target_id,
                relation_type=relation_type,
                weight_from=weight_from,
                weight_to=weight_to,
                order=order,
                headers=headers,
                offset=offset,
                limit=limit
            )

            relationships.extend(relationship_page.relationships)
            offset += len(relationship_page.relationships)
            if len(relationship_page.relationships) < limit:
                has_got_all_relationships = True

        return relationships
