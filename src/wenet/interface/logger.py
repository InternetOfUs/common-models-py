from __future__ import absolute_import, annotations

import logging
from typing import List, Optional

from wenet.interface.component import ComponentInterface
from wenet.interface.client import RestClient
from wenet.interface.exceptions import AuthenticationException, CreationError
from wenet.model.logging_message.message import BaseMessage


logger = logging.getLogger("wenet.interface.logger")


class LoggerInterface(ComponentInterface):

    def __init__(self, client: RestClient, platform_url: str, component_path: str = "/logger", extra_headers: Optional[dict] = None) -> None:
        base_url = platform_url + component_path
        super().__init__(client, base_url, extra_headers)

    def post_messages(self, messages: List[BaseMessage], headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}/messages", body=[message.to_repr() for message in messages], headers=headers)

        if response.status_code in [200, 201]:
            return response.json()["traceIds"]
        elif response.status_code in [401, 403]:
            raise AuthenticationException("logger", response.status_code, response.text)
        else:
            raise CreationError(response.status_code, response.text)
