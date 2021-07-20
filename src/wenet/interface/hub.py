from __future__ import absolute_import, annotations

import logging
from datetime import datetime
from typing import List, Optional

from wenet.interface.component import ComponentInterface
from wenet.interface.client import RestClient
from wenet.interface.exceptions import AuthenticationException, NotFound
from wenet.model.app import App


logger = logging.getLogger("wenet.interface.hub")


class HubInterface(ComponentInterface):

    def __init__(self, client: RestClient, platform_url: str, component_path: str = "/hub/frontend", extra_headers: Optional[dict] = None) -> None:
        base_url = platform_url + component_path
        super().__init__(client, base_url, extra_headers)

    def get_user_ids_for_app(self, app_id: str, from_datetime: Optional[datetime] = None, to_datetime: Optional[datetime] = None, headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        query_params_temp = {
            "fromTs": int(from_datetime.timestamp()) if from_datetime is not None else None,
            "toTs": int(to_datetime.timestamp()) if to_datetime is not None else None
        }

        query_params = {}

        for key in query_params_temp:
            if query_params_temp[key] is not None:
                query_params[key] = query_params_temp[key]

        response = self._client.get(f"{self._base_url}/data/app/{app_id}/user", query_params=query_params, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code in [401, 403]:
            raise AuthenticationException("hub", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("App", app_id, response.status_code, response.text)
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
        elif response.status_code in [401, 403]:
            raise AuthenticationException("hub", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("App", app_id, response.status_code, response.text)
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
        elif response.status_code in [401, 403]:
            raise AuthenticationException("hub", response.status_code, response.text)
        elif response.status_code == 404:
            raise NotFound("App", app_id, response.status_code, response.text)
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
        elif response.status_code in [401, 403]:
            raise AuthenticationException("hub", response.status_code, response.text)
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
    #         if response.status_code in [401, 403]:
    #             raise AuthenticationException("hub", response.status_code, response.text)
    #         elif response.status_code == 404:
    #             raise NotFound("User", user_id, response.status_code, response.text)
    #         else:
    #             raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")
