from __future__ import absolute_import, annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

from wenet.common.interface.component import ComponentInterface
from wenet.common.interface.client import RestClient
from wenet.common.model.task.task import TaskPage, Task
from wenet.common.model.task.transaction import TaskTransaction, TaskTransactionPage


logger = logging.getLogger("wenet.common.interface.task_manager")


class TaskManagerInterface(ComponentInterface):

    COMPONENT_PATH = os.getenv("TASK_MANAGER_PATH", "/task_manager")

    def __init__(self, client: RestClient, instance: str = ComponentInterface.PRODUCTION_INSTANCE, base_headers: Optional[dict] = None):
        base_url = instance + self.COMPONENT_PATH
        super().__init__(client, base_url, base_headers)

    def get_tasks(self, app_id: str, created_from: datetime, created_to: datetime, headers: Optional[dict] = None) -> List[Task]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        tasks = []
        has_got_all_tasks = False
        offset = 0
        while not has_got_all_tasks:
            response = self._client.get(f"{self._base_url}/tasks",
                                        query_params={"appId": app_id, "creationFrom": int(created_from.timestamp()),
                                                      "creationTo": int(created_to.timestamp()), "offset": offset},
                                        headers=headers)

            if response.status_code == 200:
                task_page = TaskPage.from_repr(response.json())
            else:
                raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

            tasks.extend(task_page.tasks)
            offset = len(tasks)
            if len(tasks) >= task_page.total:
                has_got_all_tasks = True

        return tasks

    def get_transactions(self, app_id: str, created_from: datetime, created_to: datetime, headers: Optional[dict] = None) -> List[TaskTransaction]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        transactions = []
        has_got_all_transactions = False
        offset = 0
        while not has_got_all_transactions:
            response = self._client.get(f"{self._base_url}/taskTransactions",
                                        query_params={"appId": app_id, "creationFrom": int(created_from.timestamp()),
                                                      "creationTo": int(created_to.timestamp()), "offset": offset},
                                        headers=headers)

            if response.status_code == 200:
                transaction_page = TaskTransactionPage.from_repr(response.json())
            else:
                raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

            transactions.extend(transaction_page.transactions)
            offset = len(transactions)
            if len(transactions) >= transaction_page.total:
                has_got_all_transactions = True

        return transactions

    def get_task(self, task_id: str, headers: Optional[dict] = None) -> Task:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/tasks/{task_id}", headers=headers)

        if response.status_code == 200:
            return Task.from_repr(response.json())
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def get_task_page(self,
                      app_id: Optional[str] = None,
                      requester_id: Optional[str] = None,
                      task_type_id: Optional[str] = None,
                      goal_name: Optional[str] = None,
                      goal_description: Optional[str] = None,
                      start_from: Optional[int] = None,
                      start_to: Optional[int] = None,
                      end_from: Optional[int] = None,
                      end_to: Optional[int] = None,
                      deadline_from: Optional[int] = None,
                      deadline_to: Optional[int] = None,
                      offset: Optional[int] = None,
                      limit: Optional[int] = None,
                      has_close_ts: Optional[dict] = None,
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
            "startFrom": start_from,
            "startTo": start_to,
            "endFrom": end_from,
            "endTo": end_to,
            "deadlineFrom": deadline_from,
            "deadlineTo": deadline_to,
            "offset": offset,
            "limit": limit,
            "hasCloseTs": has_close_ts
        }

        query_params = {}

        for key in query_params_temp:
            if query_params_temp[key] is not None:
                query_params[key] = query_params_temp[key]

        response = self._client.get(f"{self._base_url}/tasks", query_params=query_params, headers=headers)

        if response.status_code == 200:
            return TaskPage.from_repr(response.json())
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def create_task(self, task: Task, headers: Optional[dict] = None) -> Task:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        task_repr = task.prepare_task()
        task_repr.pop("id", None)
        response = self._client.post(f"{self._base_url}/tasks", body=task_repr, headers=headers)

        if response.status_code in [200, 201, 202]:
            return Task.from_repr(response.json())
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def update_task(self, task: Task, headers: Optional[dict] = None) -> Task:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.put(f"{self._base_url}/tasks/{task.task_id}", body=task.prepare_task(), headers=headers)

        if response.status_code in [200, 201, 202]:
            return Task.from_repr(response.json())
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def post_task_transaction(self, task_transaction: TaskTransaction, headers: Optional[dict] = None):
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}/tasks/transactions", body=task_transaction.to_repr(), headers=headers)

        if response.status_code in [200, 201, 202]:
            return
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")
