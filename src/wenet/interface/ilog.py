from __future__ import absolute_import, annotations

import logging
from datetime import datetime
from typing import Optional

from wenet.interface.client import RestClient
from wenet.interface.component import ComponentInterface

logger = logging.getLogger("wenet.interface.ilog")


class IlogInterface(ComponentInterface):

    def __init__(self, client: RestClient, platform_url: str, component_path: str = "/streambase", extra_headers: Optional[dict] = None) -> None:
        base_url = platform_url + component_path
        super().__init__(client, base_url, extra_headers)

    def delete_user_data(self, user_id: str, from_date: datetime, to_date: datetime, headers: Optional[dict] = None) -> None:
        if headers is not None:
            headers.update(self._json_body_headers)
        else:
            headers = self._json_body_headers

        params = {
            "from": from_date.strftime("%Y%m%d%H%M%S"),
            "to": to_date.strftime("%Y%m%d%H%M%S")
        }

        response = self._client.delete(f"{self._base_url}/data/{user_id}", headers=headers, query_params=params)

        if response.status_code == 200:
            return
        else:
            raise self.get_api_exception_for_response(response)
