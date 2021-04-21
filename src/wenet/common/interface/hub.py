from __future__ import absolute_import, annotations

import logging
import os
from typing import List, Optional

from wenet.common.interface.component import ComponentInterface
from wenet.common.interface.client import RestClient
from wenet.common.model.app.app_dto import App


logger = logging.getLogger("wenet.common.interface.hub")


class HubInterface(ComponentInterface):

    COMPONENT_PATH = os.getenv("HUB_PATH", "/hub/frontend")

    def __init__(self, client: RestClient, instance: str = ComponentInterface.PRODUCTION_INSTANCE, base_headers: Optional[dict] = None) -> None:
        base_url = instance + self.COMPONENT_PATH
        super().__init__(client, base_url, base_headers)

    def get_user_ids_for_app(self, app_id: str, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/data/app/{app_id}/user", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def get_app_details(self, app_id: str, headers: Optional[dict] = None) -> App:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/data/app/{app_id}", headers=headers)

        if response.status_code == 200:
            return App.from_repr(response.json())
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def get_app_developers(self, app_id: str, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/data/app/{app_id}/developer", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    def get_user_ids(self, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.get(f"{self._base_url}/data/user", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")

    # def delete_user(self, user_id: str, headers: Optional[dict] = None) -> None:
    #     if headers is not None:
    #         headers.update(self._base_headers)
    #     else:
    #         headers = self._base_headers
    #
    #     response = self._client.delete(f"{self._base_url}/data/user/{user_id}", headers=headers)  # TODO this endpoint should be implemented
    #
    #     if response.status_code not in [200, 204]:
    #         raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")
