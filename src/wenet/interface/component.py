from __future__ import absolute_import, annotations

import logging
from abc import ABC
from typing import Optional

from requests import Response

from wenet.interface.client import RestClient
from wenet.interface.exceptions import AuthenticationException, NotFound, BadRequest, BadGateway, ApiException

logger = logging.getLogger("wenet.interface.component")


class ComponentInterface(ABC):

    def __init__(self, client: RestClient, base_url: str, extra_headers: Optional[dict] = None) -> None:
        self._client = client
        self._base_url = base_url
        self._base_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if extra_headers:
            self._base_headers.update(extra_headers)

    @staticmethod
    def get_api_exception_for_response(response: Response) -> ApiException:
        if response.status_code in [401, 403]:
            return AuthenticationException(response.status_code, response.text)
        elif response.status_code == 404:
            return NotFound(response.text)
        elif response.status_code == 400:
            return BadRequest(response.text)
        elif response.status_code == 502:
            return BadGateway(response.text)
        else:
            return ApiException(response.status_code, response.text)
