from __future__ import absolute_import, annotations

import logging
import os
from typing import List, Optional

from wenet.common.interface.component import ComponentInterface
from wenet.common.interface.client import RestClient, ApikeyClient
from wenet.common.interface.exceptions import AuthenticationException
from wenet.common.model.logging_messages.messages import BaseMessage


logger = logging.getLogger("wenet.common.interface.logger")


class LoggerInterface(ComponentInterface):

    COMPONENT_PATH = os.getenv("LOGGER_PATH", "/logger")

    def __init__(self, client: RestClient, instance: str = ComponentInterface.PRODUCTION_INSTANCE, base_headers: Optional[dict] = None) -> None:
        if isinstance(client, ApikeyClient):
            base_url = instance + self.COMPONENT_PATH
        else:
            raise AuthenticationException("logger")

        super().__init__(client, base_url, base_headers)

    def post_messages(self, messages: List[BaseMessage], headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._base_headers)
        else:
            headers = self._base_headers

        response = self._client.post(f"{self._base_url}/messages", body=[message.to_repr() for message in messages], headers=headers)

        if response.status_code in [200, 201]:
            return response.json()["traceIds"]
        else:
            raise Exception(f"Request has return a code [{response.status_code}] with content [{response.text}]")
