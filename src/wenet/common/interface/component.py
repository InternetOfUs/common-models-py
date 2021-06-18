from __future__ import absolute_import, annotations

import logging
from abc import ABC
from typing import Optional

from wenet.common.interface.client import RestClient


logger = logging.getLogger("wenet.common.interface.component")


class ComponentInterface(ABC):

    PRODUCTION_INSTANCE = "https://internetofus.u-hopper.com/prod"
    DEVELOPMENT_INSTANCE = "https://wenet.u-hopper.com/dev"

    def __init__(self, client: RestClient, base_url: str, base_headers: Optional[dict] = None) -> None:
        self._client = client
        self._base_url = base_url
        self._base_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if base_headers:
            self._base_headers.update(base_headers)
