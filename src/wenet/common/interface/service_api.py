from typing import Optional, List

from wenet.common.interface.client import Oauth2Client
from wenet.common.interface.exceptions import TaskNotFound, UpdateMetadataError, TaskCreationError, \
    TaskTransactionCreationError
from wenet.common.model.task.transaction import TaskTransaction
from wenet.common.model.user.authentication_account import WeNetUserWithAccounts
from wenet.common.model.task.task import Task, TaskPage
from wenet.common.model.user.user_profile import WeNetUserProfile

import logging

logger = logging.getLogger("uhopper.service_api_interface")


class ServiceApiInterface:

    USER_ENDPOINT = "/user"
    TASK_ENDPOINT = '/task'

    def __init__(self, base_url: str, oauth2_client: Oauth2Client) -> None:
        self.base_url = base_url
        self.client = oauth2_client

    def get_user_accounts(self, wenet_user_id: str, app_id) -> Optional[WeNetUserWithAccounts]:
        req = self.client.get(self.base_url + self.USER_ENDPOINT + '/accounts', query_params={"appId": app_id, "userId": wenet_user_id})
        if req.status_code == 200:
            return WeNetUserWithAccounts.from_repr(req.json())
        else:
            return None

    def create_task(self, task: Task):
        task_repr = task.to_repr()
        task_repr.pop("id", None)
        req = self.client.post(self.base_url + self.TASK_ENDPOINT, body=task_repr)
        if req.status_code not in [200, 201]:
            raise TaskCreationError(req.status_code, req.json())

    def get_task(self, task_id: str) -> Task:
        req = self.client.get(self.base_url + self.TASK_ENDPOINT + '/%s' % task_id)
        if req.status_code == 404:
            raise TaskNotFound(task_id)
        task = Task.from_repr(req.json(), task_id)
        return task

    def create_task_transaction(self, transaction: TaskTransaction):
        req = self.client.post(self.base_url + self.TASK_ENDPOINT + '/transaction', body=transaction.to_repr())
        if req.status_code not in [200, 201]:
            raise TaskTransactionCreationError(req.status_code, req.json())

    def get_user_profile(self, wenet_user_id: Optional[str] = None) -> Optional[WeNetUserProfile]:
        if wenet_user_id is not None:
            req = self.client.get(self.base_url + self.USER_ENDPOINT + '/profile/%s' % wenet_user_id)
        else:
            req = self.client.get(self.base_url + self.USER_ENDPOINT + '/profile')
        if req.status_code == 200:
            return WeNetUserProfile.from_repr(req.json())
        logger.warning(f"Unable to retrieve the user profile, service api respond with: {req.status_code} {req.text}")
        return None

    def get_opened_tasks_of_user(self, wenet_user_id: str, app_id: str) -> List[Task]:
        tasks = []
        req = self.client.get(self.base_url + self.TASK_ENDPOINT + "s", query_params={"appId": app_id, "requesterId": wenet_user_id, "hasCloseTs": False})

        if req.status_code == 200:
            task_page = TaskPage.from_repr(req.json())
            tasks.extend(task_page.tasks)
            while len(tasks) < task_page.total:
                offset = len(tasks)
                req = self.client.get(self.base_url + self.TASK_ENDPOINT + "s", query_params={"appId": app_id, "requesterId": wenet_user_id, "offset": offset}).json()
                task_page = TaskPage.from_repr(req)
                tasks.extend(task_page.tasks)
            return tasks
        else:
            logger.warning(f"Unable to retrieve the list of task, server respond with [{req.status_code}], [{req.text}]")
            return []
