from typing import Optional, List

import requests

from wenet.common.interface.exceptions import TaskNotFound, UpdateMetadataError, TaskCreationError, \
    TaskTransactionCreationError
from wenet.common.model.task.transaction import TaskTransaction
from wenet.common.model.user.authentication_account import WeNetUserWithAccounts
from wenet.common.model.task.task import Task, TaskPage
from wenet.common.model.user.user_profile import WeNetUserProfile


class ServiceApiInterface:

    USER_ENDPOINT = "/user"
    TASK_ENDPOINT = '/task'

    def __init__(self, base_url: str, app_id: str, api_token: str) -> None:
        self.base_url = base_url
        self.app_id = app_id
        self.headers = {"appToken": api_token, "appId": self.app_id}

    def authenticate_telegram_user(self, telegram_id: int) -> Optional[str]:
        payload = {
            "type": "telegram",
            "appId": self.app_id,
            "telegramId": telegram_id
        }
        req = requests.post(self.base_url + self.USER_ENDPOINT + '/authenticate', json=payload, headers=self.headers)
        if req.status_code == 200:
            return req.json()["userId"]
        else:
            return None

    def get_user_accounts(self, wenet_user_id: str) -> Optional[WeNetUserWithAccounts]:
        req = requests.get(self.base_url + self.USER_ENDPOINT + '/accounts',
                           params={"appId": self.app_id, "userId": wenet_user_id}, headers=self.headers)
        if req.status_code == 200:
            return WeNetUserWithAccounts.from_repr(req.json())
        else:
            return None

    def update_user_metadata_telegram(self, telegram_id: int, wenet_user_id: str, metadata: dict):
        payload = {
            "type": "telegram",
            "appId": self.app_id,
            "metadata": metadata,
            "telegramId": telegram_id,
            "userId": wenet_user_id
        }
        req = requests.post(self.base_url + self.USER_ENDPOINT + "/account/metadata", json=payload, headers=self.headers)
        if req.status_code != 200:
            raise UpdateMetadataError(wenet_user_id, telegram_id)

    def create_task(self, task: Task):
        task_repr = task.to_repr()
        task_repr.pop("id", None)
        req = requests.post(self.base_url + self.TASK_ENDPOINT, json=task_repr, headers=self.headers)
        if req.status_code not in [200, 201]:
            raise TaskCreationError("Service API responded with code %d" % req.status_code)

    def get_task(self, task_id: str) -> Task:
        req = requests.get(self.base_url + self.TASK_ENDPOINT + '/%s' % task_id, headers=self.headers)
        if req.status_code == 404:
            raise TaskNotFound(task_id)
        task = Task.from_repr(req.json(), task_id)
        return task

    def create_task_transaction(self, transaction: TaskTransaction):
        req = requests.post(self.base_url + self.TASK_ENDPOINT + '/transaction', json=transaction.to_repr(), headers=self.headers)
        if req.status_code not in [200, 201]:
            raise TaskTransactionCreationError()

    def get_user_profile(self, wenet_user_id: str) -> Optional[WeNetUserProfile]:
        req = requests.get(self.base_url + self.USER_ENDPOINT + '/profile/%s' % wenet_user_id, headers=self.headers)
        if req.status_code == 200:
            return WeNetUserProfile.from_repr(req.json())
        return None

    def get_tasks_of_user(self, wenet_user_id: str) -> List[Task]:
        tasks = []
        req = requests.get(self.base_url + self.TASK_ENDPOINT + "s", headers=self.headers,
                           params={"appId": self.app_id, "requesterId": wenet_user_id}).json()
        task_page = TaskPage.from_repr(req)
        tasks.extend(task_page.tasks)
        while len(tasks) < task_page.total:
            offset = len(tasks)
            req = requests.get(self.base_url + self.TASK_ENDPOINT + "s", headers=self.headers,
                               params={"appId": self.app_id, "requesterId": wenet_user_id, "offset": offset}).json()
            task_page = TaskPage.from_repr(req)
            tasks.extend(task_page.tasks)
        return tasks
