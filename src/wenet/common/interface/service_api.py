from __future__ import absolute_import, annotations

import logging
import os
from datetime import datetime
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

    def get_tasks(self,
                  app_id: Optional[str] = None,
                  requester_id: Optional[str] = None,
                  task_type_id: Optional[str] = None,
                  goal_name: Optional[str] = None,
                  goal_description: Optional[str] = None,
                  start_from: Optional[datetime] = None,
                  start_to: Optional[datetime] = None,
                  end_from: Optional[datetime] = None,
                  end_to: Optional[datetime] = None,
                  has_close_ts: Optional[dict] = None,
                  deadline_from: Optional[datetime] = None,
                  deadline_to: Optional[datetime] = None,
                  offset: int = 0,
                  limit: Optional[int] = 100,
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
            start_from: the minimum start date time of the task
            start_to: the maximum start date time of the task
            end_from: the minimum end date time of the task
            end_to: the maximum end date time of the task
            has_close_ts: get the closed or open tasks
            deadline_from: the minimum deadline date time of the task
            deadline_to: the maximum deadline date time of the task
            offset: The index of the first task to return. Default value is set to 0
            limit: the number maximum of tasks to return. Default value is set to 100. If set to None it will return all the tasks
            headers: additional headers

        Returns:
            the list of tasks

        Raises:
            Exception: if response from the component returns an unexpected code
        """
        if limit is not None:
            task_page = self.get_task_page(
                app_id=app_id,
                requester_id=requester_id,
                task_type_id=task_type_id,
                goal_name=goal_name,
                goal_description=goal_description,
                start_from=start_from,
                start_to=start_to,
                end_from=end_from,
                end_to=end_to,
                has_close_ts=has_close_ts,
                deadline_from=deadline_from,
                deadline_to=deadline_to,
                offset=offset,
                limit=limit,
                headers=headers
            )
            return task_page.tasks
        else:
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
                    start_from=start_from,
                    start_to=start_to,
                    end_from=end_from,
                    end_to=end_to,
                    has_close_ts=has_close_ts,
                    deadline_from=deadline_from,
                    deadline_to=deadline_to,
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
                      start_from: Optional[datetime] = None,
                      start_to: Optional[datetime] = None,
                      end_from: Optional[datetime] = None,
                      end_to: Optional[datetime] = None,
                      has_close_ts: Optional[dict] = None,
                      deadline_from: Optional[datetime] = None,
                      deadline_to: Optional[datetime] = None,
                      offset: int = 0,
                      limit: Optional[int] = 100,
                      headers: Optional[dict] = None
                      ) -> TaskPage:
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
            "startFrom": int(start_from.timestamp()) if start_from is not None else None,
            "startTo": int(start_to.timestamp()) if start_to is not None else None,
            "endFrom": int(end_from.timestamp()) if end_from is not None else None,
            "endTo": int(end_to.timestamp()) if end_to is not None else None,
            "hasCloseTs": has_close_ts,
            "deadlineFrom": int(deadline_from.timestamp()) if deadline_from is not None else None,
            "deadlineTo": int(deadline_to.timestamp()) if deadline_to is not None else None,
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
