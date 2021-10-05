from __future__ import absolute_import, annotations

import logging
from datetime import datetime
from typing import List, Optional

from wenet.interface.client import RestClient, Oauth2Client
from wenet.interface.component import ComponentInterface
from wenet.interface.exceptions import NotFound, CreationError, AuthenticationException
from wenet.model.app import AppDTO
from wenet.model.logging_message.message import BaseMessage
from wenet.model.task.task import Task, TaskPage
from wenet.model.task.transaction import TaskTransaction
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
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def get_app_details(self, app_id: str, headers: Optional[dict] = None) -> AppDTO:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.APP_ENDPOINT}/{app_id}", headers=headers)

        if response.status_code == 200:
            return AppDTO.from_repr(response.json())
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("App", app_id, response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def get_app_users(self, app_id: str, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.APP_ENDPOINT}/{app_id}/users", headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("App", app_id, response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

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
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        else:
            raise CreationError(response.status_code, response.text)

    def get_task(self, task_id: str, headers: Optional[dict] = None) -> Task:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}/{task_id}", headers=headers)

        if response.status_code == 200:
            return Task.from_repr(response.json(), task_id)
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("Task", task_id, response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def create_task_transaction(self, transaction: TaskTransaction, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.TASK_ENDPOINT}/transaction", body=transaction.to_repr(), headers=headers)

        if response.status_code not in [200, 201]:
            if response.status_code in [401, 403]:
                raise AuthenticationException("service api", response.status_code, response.text)
            else:
                raise CreationError(response.status_code, response.text)

    def get_user_profile(self, wenet_user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", headers=headers)

        if response.status_code == 200:
            return WeNetUserProfile.from_repr(response.json())
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("User", wenet_user_id, response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def create_user_profile(self, wenet_user_id: str, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", {}, headers=headers)

        if response.status_code not in [200, 201]:
            if response.status_code in [401, 403]:
                raise AuthenticationException("service api", response.status_code, response.text)
            else:
                raise CreationError(response.status_code, response.text)

    def update_user_profile(self, wenet_user_id: str, profile: CoreWeNetUserProfile, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", profile.to_repr(), headers=headers)

        if response.status_code == 200:
            return WeNetUserProfile.from_repr(response.json())
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("User", wenet_user_id, response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

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
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("User", wenet_user_id, response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

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
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

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
        elif response.status_code in [401, 403]:
            raise AuthenticationException("service api", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("App", app_id, response.status_code, response.text)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def log_message(self, message: BaseMessage, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.LOG_ENDPOINT}", body=message.to_repr(), headers=headers)

        if response.status_code not in [200, 201]:
            if response.status_code in [401, 403]:
                raise AuthenticationException("service api", response.status_code, response.text)
            else:
                raise CreationError(response.status_code, response.text)
