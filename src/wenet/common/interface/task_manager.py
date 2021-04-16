from __future__ import absolute_import, annotations

import logging
from datetime import datetime
from typing import List

from wenet.common.interface.base import BaseInterface
from wenet.common.interface.client import RestClient
from wenet.common.model.task.task import TaskPage, Task
from wenet.common.model.task.transaction import TaskTransaction, TaskTransactionPage


logger = logging.getLogger("wenet.common.interface.task_manager")


class TaskManagerInterface(BaseInterface):

    def __init__(self, client: RestClient, instance: str = BaseInterface.PRODUCTION_INSTANCE):
        base_url = instance + "/task_manager"
        super().__init__(client, base_url)

    def get_tasks(self, app_id: str, created_from: datetime, created_to: datetime) -> List[Task]:
        tasks = []
        has_got_all_tasks = False
        offset = 0
        while not has_got_all_tasks:
            response = self._client.get(self._base_url + "/tasks",
                                        query_params={"appId": app_id, "creationFrom": int(created_from.timestamp()),
                                                      "creationTo": int(created_to.timestamp()), "offset": offset})

            if response.status_code == 200:
                task_page = TaskPage.from_repr(response.json())
            else:
                raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

            tasks.extend(task_page.tasks)
            offset = len(tasks)
            if len(tasks) >= task_page.total:
                has_got_all_tasks = True

        return tasks

    def get_transactions(self, app_id: str, created_from: datetime, created_to: datetime) -> List[TaskTransaction]:
        transactions = []
        has_got_all_transactions = False
        offset = 0
        while not has_got_all_transactions:
            response = self._client.get(self._base_url + "/taskTransactions",
                                        query_params={"appId": app_id, "creationFrom": int(created_from.timestamp()),
                                                      "creationTo": int(created_to.timestamp()), "offset": offset})

            if response.status_code == 200:
                transaction_page = TaskTransactionPage.from_repr(response.json())
            else:
                raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

            transactions.extend(transaction_page.transactions)
            offset = len(transactions)
            if len(transactions) >= transaction_page.total:
                has_got_all_transactions = True

        return transactions
