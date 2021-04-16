from __future__ import absolute_import, annotations

import logging
from abc import ABC

from wenet.common.interface.client import RestClient


logger = logging.getLogger("wenet.common.interface.base")


class BaseInterface(ABC):

    PRODUCTION_INSTANCE = "https://internetofus.u-hopper.com/prod"
    DEVELOPMENT_INSTANCE = "https://wenet.u-hopper.com/dev"

    def __init__(self, client: RestClient, base_url: str) -> None:
        self._client = client
        self._base_url = base_url
