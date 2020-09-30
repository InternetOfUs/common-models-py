from __future__ import absolute_import, annotations

from enum import Enum
from typing import Optional, List

from wenet.common.model.app.platform_dto import PlatformDTO


class AppStatus(Enum):

    ACTIVE = 1
    DEVELOPMENT = 0

# TODO rename in app
class AppDTO:

    def __init__(self, creation_ts: Optional[int], last_update_ts: Optional[int], app_id: str, app_token: Optional[str], status: AppStatus, message_callback_url: Optional[str], metadata: Optional[dict]):
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.app_id = app_id
        self.status = status
        self.app_token = app_token
        self.message_callback_url = message_callback_url
        self.metadata = metadata

        if not self.metadata:
            self.metadata = {}

        if self.creation_ts is not None:
            if not isinstance(self.creation_ts, int):
                raise TypeError("creationTs should be a int")
        if self.last_update_ts is not None:
            if not isinstance(self.last_update_ts, int):
                raise TypeError("lastUpdateTs should be a int")

        if not isinstance(self.app_id, str):
            raise TypeError("App id should be a string")
        if not isinstance(self.app_token, str):
            raise TypeError("AppToken should be a string")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata should be a dictionary")

    def to_repr(self) -> dict:
        return {
            "creationTs": self.creation_ts,
            "lastUpdateTs": self.last_update_ts,
            "appId": self.app_id,
            "status": self.status.value,
            "token": self.app_token,
            "messageCallbackUrl": self.message_callback_url,
            "metadata": self.metadata
        }

    @staticmethod
    def from_repr(raw_data: dict) -> AppDTO:
        return AppDTO(
            creation_ts=raw_data.get("creationTs", None),
            last_update_ts=raw_data.get("lastUpdateTs", None),
            app_id=raw_data["appId"],
            status=AppStatus(raw_data["status"]),
            app_token=raw_data.get("token", None),
            message_callback_url=raw_data.get("messageCallbackUrl", None),
            metadata=raw_data.get("metadata", None)
        )

    def __eq__(self, o):
        if not isinstance(o, AppDTO):
            return False
        return self.app_id == o.app_id and self.app_token == o.app_token \
            and self.message_callback_url == o.message_callback_url and self.metadata == o.metadata

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()


class AppDeveloper:

    def __init__(self, app_id: str, user_id: str):
        self.app_id = app_id
        self.user_id = user_id

    def to_repr(self) -> dict:
        return {
            "appId": self.app_id,
            "userId": self.user_id
        }

    @staticmethod
    def from_repr(raw_data: dict) -> AppDeveloper:
        return AppDeveloper(
            app_id=raw_data["appId"],
            user_id=raw_data["userId"]
        )
