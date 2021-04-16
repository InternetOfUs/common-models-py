from __future__ import absolute_import, annotations

import logging
from typing import List

from wenet.common.interface.base import BaseInterface
from wenet.common.interface.client import RestClient
from wenet.common.model.app.app_dto import HubApp


logger = logging.getLogger("wenet.common.interface.hub")


class HubInterface(BaseInterface):

    def __init__(self, client: RestClient, instance: str = BaseInterface.PRODUCTION_INSTANCE) -> None:
        base_url = instance + "/hub/frontend"
        super().__init__(client, base_url)

    def get_user_ids_for_app(self, app_id: str) -> List[str]:
        response = self._client.get(f"{self._base_url}/data/app/{app_id}/user")

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

    def get_app_details(self, app_id: str) -> HubApp:
        response = self._client.get(f"{self._base_url}/data/app/{app_id}")

        if response.status_code == 200:
            return HubApp.from_repr(response.json())
        else:
            raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

    def get_user_ids(self) -> List[str]:
        response = self._client.get(f"{self._base_url}/data/user")

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request has return a code {response.status_code} with content {response.text}")

    # def delete_user(self, user_id: str) -> None:
    #     response = self._client.delete(f"{self._base_url}/data/user/{user_id}")  # TODO this endpoint should be implemented
    #
    #     if response.status_code not in [200, 204]:
    #         raise Exception(f"Request has return a code {response.status_code} with content {response.text}")
