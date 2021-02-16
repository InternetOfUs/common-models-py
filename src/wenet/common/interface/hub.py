from __future__ import absolute_import, annotations

import logging
from typing import List

import requests

logger = logging.getLogger("wenet.common.interface.hub")


class HubInterface:

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_user_ids_for_app(self, app_id: str) -> List[str]:
        response = requests.get(f"{self.base_url}/data/app/{app_id}/user")
        return response.json()

    def get_app_details(self, app_id: str) -> dict:
        response = requests.get(f"{self.base_url}/data/app/{app_id}")
        return response.json()
