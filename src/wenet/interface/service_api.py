from __future__ import absolute_import, annotations

import logging
from datetime import datetime
from typing import List, Optional, Union

from wenet.interface.client import RestClient, Oauth2Client
from wenet.interface.component import ComponentInterface
from wenet.model.app import AppDTO
from wenet.model.logging_message.message import BaseMessage
from wenet.model.protocol_norm import ProtocolNorm
from wenet.model.task.task import Task, TaskPage
from wenet.model.task.transaction import TaskTransaction
from wenet.model.user.competence import Competence
from wenet.model.user.material import Material
from wenet.model.user.meaning import Meaning
from wenet.model.user.personal_behaviors import PersonalBehavior
from wenet.model.user.planned_activity import PlannedActivity
from wenet.model.user.relationship import Relationship, RelationshipPage
from wenet.model.user.relevant_location import RelevantLocation
from wenet.model.user.token import TokenDetails
from wenet.model.user.profile import WeNetUserProfile, CoreWeNetUserProfile


logger = logging.getLogger("wenet.interface.service_api")


class ServiceApiInterface(ComponentInterface):

    APP_ENDPOINT = "/app"
    USER_ENDPOINT = "/user"
    TASK_ENDPOINT = "/task"
    TOKEN_ENDPOINT = "/token"
    LOG_ENDPOINT = "/log/messages"

    def __init__(self, client: RestClient, platform_url: str, component_path: str = "/service", component_path_oauth: str = "/api/service", extra_headers: Optional[dict] = None) -> None:
        if isinstance(client, Oauth2Client):
            base_url = platform_url + component_path_oauth
        else:
            base_url = platform_url + component_path
        super().__init__(client, base_url, extra_headers)

    def get_token_details(self, headers: Optional[dict] = None) -> TokenDetails:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.TOKEN_ENDPOINT}", headers=headers)

        if response.status_code == 200:
            return TokenDetails.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def get_app_details(self, app_id: str, headers: Optional[dict] = None) -> AppDTO:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.APP_ENDPOINT}/{app_id}", headers=headers)

        if response.status_code == 200:
            return AppDTO.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def get_app_users(self, app_id: str, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.APP_ENDPOINT}/{app_id}/users", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def create_task(self, task: Task, headers: Optional[dict] = None) -> Task:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        task_repr = task.to_repr()
        task_repr.pop("id", None)
        response = self._client.post(f"{self._base_url}{self.TASK_ENDPOINT}", body=task_repr, headers=headers)

        if response.status_code in [200, 201]:
            return Task.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def get_task(self, task_id: str, headers: Optional[dict] = None) -> Task:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}/{task_id}", headers=headers)

        if response.status_code == 200:
            return Task.from_repr(response.json(), task_id)
        else:
            raise self.get_api_exception_for_response(response)

    def create_task_transaction(self, transaction: TaskTransaction, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.TASK_ENDPOINT}/transaction", body=transaction.to_repr(), headers=headers)

        if response.status_code not in [200, 201]:
            raise self.get_api_exception_for_response(response)

    def get_user_profile(self, wenet_user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", headers=headers)

        if response.status_code == 200:
            return WeNetUserProfile.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def create_user_profile(self, wenet_user_id: str, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", {}, headers=headers)

        if response.status_code not in [200, 201]:
            raise self.get_api_exception_for_response(response)

    def update_user_profile(self, wenet_user_id: str, profile: CoreWeNetUserProfile, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", profile.to_repr(), headers=headers)

        if response.status_code == 200:
            return WeNetUserProfile.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def get_user_competences(self, wenet_user_id: str, headers: Optional[dict] = None) -> List[dict]:
        """
        Get all the competences defined into a profile

        Args:
            wenet_user_id: The Id of the wenet user
            headers: Additional headers to add to the call

        Returns:
            The competences defined into the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/competences", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def update_user_competences(self, wenet_user_id: str, competences: Union[List[dict], List[Competence]], headers: Optional[dict] = None) -> List[dict]:
        """
        Update all the competences of a profile overwriting the existing ones

        Args:
            wenet_user_id: The Id of the wenet user
            competences: The new competences
            headers: Additional headers to add to the call

        Returns:
            The updated competences of the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        raw_competences = [competence.to_repr() if isinstance(competence, Competence) else competence for competence in competences]
        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/competences", raw_competences, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def get_user_materials(self, wenet_user_id: str, headers: Optional[dict] = None) -> List[dict]:
        """
        Get all the materials defined into a profile

        Args:
            wenet_user_id: The Id of the wenet user
            headers: Additional headers to add to the call

        Returns:
            The materials defined into the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/materials", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def update_user_materials(self, wenet_user_id: str, materials: Union[List[dict], List[Material]], headers: Optional[dict] = None) -> List[dict]:
        """
        Update all the materials of a profile overwriting the existing ones

        Args:
            wenet_user_id: The Id of the wenet user
            materials: The new materials
            headers: Additional headers to add to the call

        Returns:
            The updated materials of the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        raw_materials = [material.to_repr() if isinstance(material, Material) else material for material in materials]
        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/materials", raw_materials, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def get_user_meanings(self, wenet_user_id: str, headers: Optional[dict] = None) -> List[dict]:
        """
        Get all the meanings defined into a profile

        Args:
            wenet_user_id: The Id of the wenet user
            headers: Additional headers to add to the call

        Returns:
            The meanings defined into the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/meanings", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def update_user_meanings(self, wenet_user_id: str, meanings: Union[List[dict], List[Meaning]], headers: Optional[dict] = None) -> List[dict]:
        """
        Update all the meanings of a profile overwriting the existing ones

        Args:
            wenet_user_id: The Id of the wenet user
            meanings: The new meanings
            headers: Additional headers to add to the call

        Returns:
            The updated meanings of the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        raw_meanings = [meaning.to_repr() if isinstance(meaning, Meaning) else meaning for meaning in meanings]
        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/meanings", raw_meanings, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def get_user_norms(self, wenet_user_id: str, headers: Optional[dict] = None) -> List[dict]:
        """
        Get all the norms defined into a profile

        Args:
            wenet_user_id: The Id of the wenet user
            headers: Additional headers to add to the call

        Returns:
            The norms defined into the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/norms", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def update_user_norms(self, wenet_user_id: str, norms: Union[List[dict], List[ProtocolNorm]], headers: Optional[dict] = None) -> List[dict]:
        """
        Update all the norms of a profile overwriting the existing ones

        Args:
            wenet_user_id: The Id of the wenet user
            norms: The new norms
            headers: Additional headers to add to the call

        Returns:
            The updated norms of the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        raw_norms = [norm.to_repr() if isinstance(norm, ProtocolNorm) else norm for norm in norms]
        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/norms", raw_norms, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def get_user_personal_behaviors(self, wenet_user_id: str, headers: Optional[dict] = None) -> List[dict]:
        """
        Get all the personal behaviors defined into a profile

        Args:
            wenet_user_id: The Id of the wenet user
            headers: Additional headers to add to the call

        Returns:
            The personal behaviors defined into the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/personalBehaviors", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def update_user_personal_behaviors(self, wenet_user_id: str, personal_behaviors: Union[List[dict], List[PersonalBehavior]], headers: Optional[dict] = None) -> List[dict]:
        """
        Update all the personal behaviors of a profile overwriting the existing ones

        Args:
            wenet_user_id: The Id of the wenet user
            personal_behaviors: The new personal behaviors
            headers: Additional headers to add to the call

        Returns:
            The updated personal behaviors of the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        raw_personal_behaviors = [personal_behavior.to_repr() if isinstance(personal_behavior, PersonalBehavior) else personal_behavior for personal_behavior in personal_behaviors]
        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/personalBehaviors", raw_personal_behaviors, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def get_user_planned_activities(self, wenet_user_id: str, headers: Optional[dict] = None) -> List[dict]:
        """
        Get all the planned activities defined into a profile

        Args:
            wenet_user_id: The Id of the wenet user
            headers: Additional headers to add to the call

        Returns:
            The planned activities defined into the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/plannedActivities", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def update_user_planned_activities(self, wenet_user_id: str, planned_activities: Union[List[dict], List[PlannedActivity]], headers: Optional[dict] = None) -> List[dict]:
        """
        Update all the planned activities of a profile overwriting the existing ones

        Args:
            wenet_user_id: The Id of the wenet user
            planned_activities: The new planned activities
            headers: Additional headers to add to the call

        Returns:
            The updated planned activities of the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        raw_planned_activities = [planned_activity.to_repr() if isinstance(planned_activity, PlannedActivity) else planned_activity for planned_activity in planned_activities]
        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/plannedActivities", raw_planned_activities, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def get_relationship_page(self,
                              wenet_user_id: str,
                              target_id: Optional[str] = None,
                              relation_type: Optional[str] = None,
                              weight_from: Optional[float] = None,
                              weight_to: Optional[float] = None,
                              order: Optional[str] = None,
                              offset: int = 0,
                              limit: int = 10,
                              headers: Optional[dict] = None) -> RelationshipPage:
        """

        :param wenet_user_id: The Id of the wenet user
        :param target_id: A user identifier to be equals on the relationships target to return. You can use a Perl compatible regular expressions (PCRE) that has to match the user identifier of the relationships target if you write between '/'. For example to get the relationships with the target users '1' and '2' you must pass as 'target' '/^[1|2]$/'.
        :param relation_type: The type for the relationships to return. You can use a Perl compatible regular expressions (PCRE) that has to match the type of the relationships if you write between '/'. For example to get the relationships with the types 'friend' and 'colleague' you must pass as 'type' '/^[friend|colleague]$/'.
        :param weight_from: The minimal weight, inclusive, of the relationships to return.
        :param weight_to: The maximal weight, inclusive, of the relationships to return.
        :param order: The order in witch the relationships has to be returned. For each field it has be separated by a ',' and each field can start with '+' (or without it) to order on ascending order, or with the prefix '-' to do on descendant order.
        :param offset: The index of the first social network relationship to return.
        :param limit: The number maximum of social network relationships to return
        :param headers: Additional headers to add to the call
        :return: An object representing a relationships page.
        """
        query_params_temp = {
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

        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/relationships",
                                    query_params=query_params, headers=headers)

        if response.status_code == 200:
            return RelationshipPage.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def get_user_relationships(self,
                               wenet_user_id: str,
                               target_id: Optional[str] = None,
                               relation_type: Optional[str] = None,
                               weight_from: Optional[float] = None,
                               weight_to: Optional[float] = None,
                               order: Optional[str] = None,
                               headers: Optional[dict] = None) -> List[Relationship]:
        """
        Get all the relationships defined into a profile

        :param wenet_user_id: The Id of the wenet user
        :param target_id: A user identifier to be equals on the relationships target to return. You can use a Perl compatible regular expressions (PCRE) that has to match the user identifier of the relationships target if you write between '/'. For example to get the relationships with the target users '1' and '2' you must pass as 'target' '/^[1|2]$/'.
        :param relation_type: The type for the relationships to return. You can use a Perl compatible regular expressions (PCRE) that has to match the type of the relationships if you write between '/'. For example to get the relationships with the types 'friend' and 'colleague' you must pass as 'type' '/^[friend|colleague]$/'.
        :param weight_from: The minimal weight, inclusive, of the relationships to return.
        :param weight_to: The maximal weight, inclusive, of the relationships to return.
        :param order: The order in witch the relationships has to be returned. For each field it has be separated by a ',' and each field can start with '+' (or without it) to order on ascending order, or with the prefix '-' to do on descendant order.
        :param headers: Additional headers to add to the call
        :return: The list of relationships of the given user
        """
        relationships: List[Relationship] = []
        has_got_all_relationships = False
        offset = 0
        limit = 100
        while not has_got_all_relationships:
            relationship_page = self.get_relationship_page(
                wenet_user_id=wenet_user_id,
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

    def update_user_relationships(self, wenet_user_id: str, relationships: Union[List[Relationship]], headers: Optional[dict] = None) -> List[Relationship]:
        """
        Update The user relationships in batch
        :param wenet_user_id: The id of the user
        :param relationships: The list of relationships to update
        :param headers: Additional headers to add to the call
        :return:
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        raw_relationships = [relationship.to_repr() for relationship in relationships]
        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/relationships", raw_relationships, headers=headers)

        if response.status_code == 200:
            return [Relationship.from_repr(x) for x in response.json()]
        else:
            raise self.get_api_exception_for_response(response)

    def get_user_relevant_locations(self, wenet_user_id: str, headers: Optional[dict] = None) -> List[dict]:
        """
        Get all the relevant locations defined into a profile

        Args:
            wenet_user_id: The Id of the wenet user
            headers: Additional headers to add to the call

        Returns:
            The relevant locations defined into the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/relevantLocations", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def update_user_relevant_locations(self, wenet_user_id: str, relevant_locations: Union[List[dict], List[RelevantLocation]], headers: Optional[dict] = None) -> List[dict]:
        """
        Update all the relevant locations of a profile overwriting the existing ones

        Args:
            wenet_user_id: The Id of the wenet user
            relevant_locations: The new relevant locations
            headers: Additional headers to add to the call

        Returns:
            The updated relevant locations of the profile
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        raw_relevant_locations = [relevant_location.to_repr() if isinstance(relevant_location, RelevantLocation) else relevant_location for relevant_location in relevant_locations]
        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}/relevantLocations", raw_relevant_locations, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise self.get_api_exception_for_response(response)

    def get_opened_tasks_of_user(self, wenet_user_id: str, app_id: str, headers: Optional[dict] = None) -> List[Task]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        tasks = []
        response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}s",
                                    query_params={"appId": app_id, "requesterId": wenet_user_id, "hasCloseTs": False},
                                    headers=headers)

        if response.status_code == 200:
            task_page = TaskPage.from_repr(response.json())
            tasks.extend(task_page.tasks)
            while len(tasks) < task_page.total:
                offset = len(tasks)
                response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}s",
                                            query_params={"appId": app_id, "requesterId": wenet_user_id, "hasCloseTs": False, "offset": offset},
                                            headers=headers)
                task_page = TaskPage.from_repr(response.json())
                tasks.extend(task_page.tasks)
            return tasks
        else:
            raise self.get_api_exception_for_response(response)

    def get_all_tasks(self,
                      app_id: Optional[str] = None,
                      requester_id: Optional[str] = None,
                      task_type_id: Optional[str] = None,
                      goal_name: Optional[str] = None,
                      goal_description: Optional[str] = None,
                      creation_from: Optional[datetime] = None,
                      creation_to: Optional[datetime] = None,
                      update_from: Optional[datetime] = None,
                      update_to: Optional[datetime] = None,
                      has_close_ts: Optional[bool] = None,
                      closed_from: Optional[datetime] = None,
                      closed_to: Optional[datetime] = None,
                      order: Optional[str] = None,
                      offset: int = 0,
                      headers: Optional[dict] = None
                      ) -> List[Task]:
        """
        Get the tasks specifying parameters

        Args:
            app_id: an application identifier to be equals on the tasks to return
            requester_id: an user identifier to be equals on the tasks to return
            task_type_id: a task type identifier to be equals on the tasks to return
            goal_name: a goal name to be equals on the tasks to return
            goal_description: a goal description to be equals on the tasks to return
            creation_from: the minimum creation date time of the tasks to return
            creation_to: the maximum creation date time of the tasks to return
            update_from: the minimum update date time of the tasks to return
            update_to: the maximum update date time of the tasks to return
            has_close_ts: get the closed or open tasks
            closed_from: the minimum close date time of the task
            closed_to: the maximum close date time of the task
            order: the order in witch the tasks have to be returned. For each field it has be separated by a ',' and each field can start with '+' (or without it) to order on ascending order, or with the prefix '-' to do on descendant order
            offset: The index of the first task to return. Default value is set to 0
            headers: additional headers

        Returns:
            The list of tasks

        Raises:
            AuthenticationException: if unauthorized for the request
            Exception: if response from the component returns an unexpected code
        """
        tasks = []
        limit = 100
        has_got_all_tasks = False
        while not has_got_all_tasks:
            task_page = self.get_task_page(
                app_id=app_id,
                requester_id=requester_id,
                task_type_id=task_type_id,
                goal_name=goal_name,
                goal_description=goal_description,
                creation_from=creation_from,
                creation_to=creation_to,
                update_from=update_from,
                update_to=update_to,
                has_close_ts=has_close_ts,
                closed_from=closed_from,
                closed_to=closed_to,
                order=order,
                offset=offset,
                limit=limit,
                headers=headers
            )
            tasks.extend(task_page.tasks)
            offset += len(task_page.tasks)
            if len(task_page.tasks) < limit:
                has_got_all_tasks = True

        return tasks

    def get_task_page(self,
                      app_id: Optional[str] = None,
                      requester_id: Optional[str] = None,
                      task_type_id: Optional[str] = None,
                      goal_name: Optional[str] = None,
                      goal_description: Optional[str] = None,
                      creation_from: Optional[datetime] = None,
                      creation_to: Optional[datetime] = None,
                      update_from: Optional[datetime] = None,
                      update_to: Optional[datetime] = None,
                      has_close_ts: Optional[bool] = None,
                      closed_from: Optional[datetime] = None,
                      closed_to: Optional[datetime] = None,
                      order: Optional[str] = None,
                      offset: int = 0,
                      limit: int = 100,
                      headers: Optional[dict] = None
                      ) -> TaskPage:
        """
        Get a page of tasks specifying parameters

        Args:
            app_id: an application identifier to be equals on the tasks to return
            requester_id: an user identifier to be equals on the tasks to return
            task_type_id: a task type identifier to be equals on the tasks to return
            goal_name: a goal name to be equals on the tasks to return
            goal_description: a goal description to be equals on the tasks to return
            creation_from: the minimum creation date time of the tasks to return
            creation_to: the maximum creation date time of the tasks to return
            update_from: the minimum update date time of the tasks to return
            update_to: the maximum update date time of the tasks to return
            has_close_ts: get the closed or open tasks
            closed_from: the minimum close date time of the task
            closed_to: the maximum close date time of the task
            order: the order in witch the tasks have to be returned. For each field it has be separated by a ',' and each field can start with '+' (or without it) to order on ascending order, or with the prefix '-' to do on descendant order
            offset: The index of the first task to return. Default value is set to 0
            limit: the number maximum of tasks to return. Default value is set to 100
            headers: additional headers

        Returns:
            A page of tasks

        Raises:
            AuthenticationException: if unauthorized for the request
            Exception: if response from the component returns an unexpected code
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        query_params_temp = {
            "appId": app_id,
            "requesterId": requester_id,
            "taskTypeId": task_type_id,
            "goalName": goal_name,
            "goalDescription": goal_description,
            "creationFrom": int(creation_from.timestamp()) if creation_from is not None else None,
            "creationTo": int(creation_to.timestamp()) if creation_to is not None else None,
            "updateFrom": int(update_from.timestamp()) if update_from is not None else None,
            "updateTo": int(update_to.timestamp()) if update_to is not None else None,
            "hasCloseTs": has_close_ts,
            "closeFrom": int(closed_from.timestamp()) if closed_from is not None else None,
            "closeTo": int(closed_to.timestamp()) if closed_to is not None else None,
            "order": order,
            "offset": offset,
            "limit": limit
        }

        query_params = {}

        for key in query_params_temp:
            if query_params_temp[key] is not None:
                query_params[key] = query_params_temp[key]

        response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}s", query_params=query_params, headers=headers)

        if response.status_code == 200:
            return TaskPage.from_repr(response.json())
        else:
            raise self.get_api_exception_for_response(response)

    def get_all_tasks_of_application(self, app_id: str, headers: Optional[dict] = None) -> List[Task]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        tasks = []
        response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}s",
                                    query_params={"appId": app_id, "hasCloseTs": False},
                                    headers=headers)

        if response.status_code == 200:
            task_page = TaskPage.from_repr(response.json())
            tasks.extend(task_page.tasks)
            while len(tasks) < task_page.total:
                offset = len(tasks)
                response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}s",
                                            query_params={"appId": app_id, "hasCloseTs": False, "offset": offset},
                                            headers=headers)
                task_page = TaskPage.from_repr(response.json())
                tasks.extend(task_page.tasks)
            return tasks
        else:
            raise self.get_api_exception_for_response(response)

    def log_message(self, message: BaseMessage, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.LOG_ENDPOINT}", body=message.to_repr(), headers=headers)

        if response.status_code not in [200, 201]:
            raise self.get_api_exception_for_response(response)
