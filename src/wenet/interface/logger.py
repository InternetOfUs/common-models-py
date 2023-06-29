from __future__ import absolute_import, annotations

import logging
from typing import List, Optional

from wenet.interface.component import ComponentInterface
from wenet.interface.client import RestClient
from wenet.model.logging_message.message import BaseMessage


logger = logging.getLogger("wenet.interface.logger")


class LoggerInterface(ComponentInterface):

    def __init__(self, client: RestClient, platform_url: str, component_path: str = "/logger", extra_headers: Optional[dict] = None) -> None:
        base_url = platform_url + component_path
        super().__init__(client, base_url, extra_headers)

    def post_messages(self, messages: List[BaseMessage], headers: Optional[dict] = None) -> List[str]:
        if headers is not None:
            headers.update(self._json_body_headers)
        else:
            headers = self._json_body_headers

        response = self._client.post(f"{self._base_url}/messages", body=[message.to_repr() for message in messages], headers=headers)

        if response.status_code in [200, 201]:
            return response.json()["traceIds"]
        else:
            raise self.get_api_exception_for_response(response)

    def delete_user_messages(self, user_id: Optional[str] = None,
                             message_id: Optional[str] = None,
                             project: Optional[str] = None,
                             trace_id: Optional[str] = None,
                             headers: Optional[dict] = None):

        if headers is not None:
            headers.update(self._json_body_headers)
        else:
            headers = self._json_body_headers

        parmas = {
            "userId": user_id,
            "messageId": message_id,
            "project": project,
            "traceId": trace_id
        }

        response = self._client.delete(f"{self._base_url}/messages", query_params=parmas, headers=headers)

        if response.status_code not in [200, 201]:
            raise self.get_api_exception_for_response(response)
