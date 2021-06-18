from __future__ import absolute_import, annotations

import logging
import os
from typing import List, Optional

from wenet.common.interface.client import RestClient, ApikeyClient, Oauth2Client
from wenet.common.interface.component import ComponentInterface
from wenet.common.interface.exceptions import NotFound, CreationError, AuthenticationException
from wenet.common.model.app.app_dto import AppDTO
from wenet.common.model.logging_messages.messages import BaseMessage
from wenet.common.model.task.task import Task, TaskPage
from wenet.common.model.task.transaction import TaskTransaction
from wenet.common.model.user.token_details import TokenDetails
from wenet.common.model.user.user_profile import WeNetUserProfile, CoreWeNetUserProfile


logger = logging.getLogger("wenet.common.interface.service_api")


class ServiceApiInterface(ComponentInterface):

    COMPONENT_PATH_INTERNAL_USAGE = os.getenv("SERVICE_API_PATH_INTERNAL_USAGE", "/service")
    COMPONENT_PATH_EXTERNAL_USAGE = os.getenv("SERVICE_API_PATH_EXTERNAL_USAGE", "/api/service")

    APP_ENDPOINT = "/app"
    USER_ENDPOINT = "/user"
    TASK_ENDPOINT = "/task"
    TOKEN_ENDPOINT = "/token"
    LOG_ENDPOINT = "/log/messages"

    def __init__(self, client: RestClient, instance: str = ComponentInterface.PRODUCTION_INSTANCE, base_headers: Optional[dict] = None) -> None:
        if isinstance(client, ApikeyClient):
            base_url = instance + self.COMPONENT_PATH_INTERNAL_USAGE
        elif isinstance(client, Oauth2Client):
            base_url = instance + self.COMPONENT_PATH_EXTERNAL_USAGE
        else:
            raise AuthenticationException("service api")

        super().__init__(client, base_url, base_headers)

    def get_token_details(self, headers: Optional[dict] = None) -> TokenDetails:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.TOKEN_ENDPOINT}", headers=headers)

        if response.status_code == 200:
            return TokenDetails.from_repr(response.json())
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
        elif response.status_code == 404:
            raise NotFound("App", app_id)
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
        elif response.status_code == 404:
            raise NotFound("App", app_id)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def create_task(self, task: Task, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        task_repr = task.to_repr()
        task_repr.pop("id", None)
        response = self._client.post(f"{self._base_url}{self.TASK_ENDPOINT}", body=task_repr, headers=headers)

        if response.status_code not in [200, 201]:
            raise CreationError(response.status_code, response.json())

    def get_task(self, task_id: str, headers: Optional[dict] = None) -> Task:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}/{task_id}", headers=headers)

        if response.status_code == 200:
            return Task.from_repr(response.json(), task_id)
        elif response.status_code == 404:
            raise NotFound("Task", task_id)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def create_task_transaction(self, transaction: TaskTransaction, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.TASK_ENDPOINT}/transaction", body=transaction.to_repr(), headers=headers)

        if response.status_code not in [200, 201]:
            raise CreationError(response.status_code, response.json())

    def get_user_profile(self, wenet_user_id: str, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", headers=headers)

        if response.status_code == 200:
            return WeNetUserProfile.from_repr(response.json())
        elif response.status_code == 404:
            raise NotFound("User", wenet_user_id)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def create_user_profile(self, wenet_user_id: str, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", {}, headers=headers)

        if response.status_code not in [200, 201]:
            raise CreationError(response.status_code, response.json())

    def update_user_profile(self, wenet_user_id: str, profile: CoreWeNetUserProfile, headers: Optional[dict] = None) -> WeNetUserProfile:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.put(f"{self._base_url}{self.USER_ENDPOINT}/profile/{wenet_user_id}", profile.to_repr(), headers=headers)

        if response.status_code == 200:
            return WeNetUserProfile.from_repr(response.json())
        elif response.status_code == 404:
            raise NotFound("User", wenet_user_id)
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
                                            query_params={"appId": app_id, "requesterId": wenet_user_id, "offset": offset},
                                            headers=headers)
                task_page = TaskPage.from_repr(response.json())
                tasks.extend(task_page.tasks)
            return tasks
        elif response.status_code == 404:
            raise NotFound("User", wenet_user_id)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def get_tasks(self, app_id: str, requester_id: Optional[str] = None, has_close_ts: Optional[bool] = None,
                  limit: Optional[int] = None, offset: Optional[int] = None, headers: Optional[dict] = None) -> List[Task]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        params = {
            "appId": app_id
        }
        if requester_id:
            params["requesterId"] = requester_id
        if has_close_ts is not None:
            params["hasCloseTs"] = has_close_ts
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client.get(f"{self._base_url}{self.TASK_ENDPOINT}s", query_params=params, headers=headers)

        if response.status_code == 200:
            return [Task.from_repr(task) for task in response.json()["tasks"]]
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
                                            query_params={"appId": app_id, "offset": offset},
                                            headers=headers)
                task_page = TaskPage.from_repr(response.json())
                tasks.extend(task_page.tasks)
            return tasks
        elif response.status_code == 404:
            raise NotFound("App", app_id)
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def log_message(self, message: BaseMessage, headers: Optional[dict] = None) -> None:
        """
        Log a message to the service API, either a request, response or notification.
        Returns True if the operation is successful, False otherwise
        """
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}{self.LOG_ENDPOINT}", body=message.to_repr(), headers=headers)

        if response.status_code not in [200, 201]:
            raise CreationError(response.status_code, response.json())
