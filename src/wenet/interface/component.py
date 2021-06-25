from __future__ import absolute_import, annotations

import logging
from abc import ABC
from typing import Optional

from wenet.interface.client import RestClient


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
