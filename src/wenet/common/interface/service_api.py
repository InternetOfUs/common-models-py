from typing import Optional

import requests

from wenet.common.model.task.transaction import TaskTransaction
from wenet.common.model.user.authentication_account import WeNetUserWithAccounts
from wenet.common.model.task.task import Task


class ServiceApiInterface:

    USER_ENDPOINT = "/user"
    TASK_ENDPOINT = '/task'

    def __init__(self, base_url: str, app_id: str) -> None:
        self.base_url = base_url
        self.app_id = app_id

    def authenticate_telegram_user(self, telegram_id: int) -> Optional[str]:
        payload = {
            "type": "telegram",
            "appId": self.app_id,
            "telegramId": telegram_id
        }
        req = requests.post(self.base_url + self.USER_ENDPOINT + '/authenticate', json=payload)
        if req.status_code == 200:
            return req.json()["userId"]
        else:
            return None

    def get_user_accounts(self, wenet_user_id: str) -> Optional[WeNetUserWithAccounts]:
        req = requests.get(self.base_url + self.USER_ENDPOINT + '/accounts',
                           params={"appId": self.app_id, "userId": wenet_user_id})
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
        req = requests.post(self.base_url + self.USER_ENDPOINT + "/account/metadata", json=payload)
        if req.status_code != 200:
            raise ValueError(f"No WeNet user [{wenet_user_id}] associated with Telegram id [{telegram_id}]")

    def create_task(self, task: Task):
        requests.post(self.base_url + self.TASK_ENDPOINT, json=task.to_repr())

    def get_task(self, task_id: str) -> Task:
        req = requests.get(self.base_url + self.TASK_ENDPOINT + '/%s' % task_id)
        task = Task.from_repr(req.json(), task_id)
        if req.status_code == 404:
            raise ValueError(f"Task [{task_id}] does not exist")
        return task

    def create_task_transaction(self, transaction: TaskTransaction):
        requests.post(self.base_url + self.TASK_ENDPOINT + '/transaction', json=transaction.to_repr())
