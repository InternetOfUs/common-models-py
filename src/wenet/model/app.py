from __future__ import absolute_import, annotations

from enum import Enum
from numbers import Number
from typing import Optional


class AppStatus(Enum):

    STATUS_NOT_ACTIVE = 0
    STATUS_ACTIVE = 1
    STATUS_DELETED = 2


class App:

    def __init__(self, creation_ts: Optional[Number], last_update_ts: Optional[Number], app_id: str, status: AppStatus,
                 name: str, owner_id: int, image_url: Optional[str], message_callback_url: Optional[str],
                 metadata: Optional[dict]) -> None:
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.app_id = app_id
        self.status = status
        self.name = name
        self.owner_id = owner_id
        self.image_url = image_url
        self.message_callback_url = message_callback_url
        self.metadata = metadata

        if not self.metadata:
            self.metadata = {}

        if self.creation_ts is not None:
            if not isinstance(self.creation_ts, Number):
                raise TypeError("creationTs should be a number")

        if self.last_update_ts is not None:
            if not isinstance(self.last_update_ts, Number):
                raise TypeError("lastUpdateTs should be a number")

        if not isinstance(self.app_id, str):
            raise TypeError("id should be a string")

        if not isinstance(self.name, str):
            raise TypeError("name should be a string")

        if not isinstance(self.owner_id, int):
            raise TypeError("ownerId should be an integer")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata should be a dictionary")

    def to_repr(self) -> dict:
        return {
            "id": self.app_id,
            "name": self.name,
            "status": self.status.value,
            "ownerId": self.owner_id,
            "image_url": self.image_url,
            "createdAt": self.creation_ts,
            "updatedAt": self.last_update_ts,
            "metadata": self.metadata,
            "messageCallbackUrl": self.message_callback_url
        }

    @staticmethod
    def from_repr(raw_data: dict) -> App:
        return App(
            creation_ts=raw_data.get("createdAt", None),
            last_update_ts=raw_data.get("updatedAt", None),
            app_id=raw_data["id"],
            status=AppStatus(raw_data["status"]),
            name=raw_data["name"],
            owner_id=raw_data["ownerId"],
            image_url=raw_data.get("image_url", None),
            message_callback_url=raw_data.get("messageCallbackUrl", None),
            metadata=raw_data.get("metadata", None)
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, App):
            return False
        return self.app_id == o.app_id and self.status == o.status and self.name == o.name \
            and self.owner_id == o.owner_id and self.image_url == o.image_url \
            and self.creation_ts == o.creation_ts and self.last_update_ts == o.last_update_ts \
            and self.message_callback_url == o.message_callback_url and self.metadata == o.metadata

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()


class AppDTO:

    def __init__(self, creation_ts: Optional[Number], last_update_ts: Optional[Number], app_id: str,
                 message_callback_url: Optional[str], metadata: Optional[dict]) -> None:
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.app_id = app_id
        self.message_callback_url = message_callback_url
        self.metadata = metadata

        if not self.metadata:
            self.metadata = {}

        if self.creation_ts is not None:
            if not isinstance(self.creation_ts, Number):
                raise TypeError("creationTs should be a number")

        if self.last_update_ts is not None:
            if not isinstance(self.last_update_ts, Number):
                raise TypeError("lastUpdateTs should be a number")

        if not isinstance(self.app_id, str):
            raise TypeError("appId should be a string")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata should be a dictionary")

    def to_repr(self) -> dict:
        return {
            "creationTs": self.creation_ts,
            "lastUpdateTs": self.last_update_ts,
            "appId": self.app_id,
            "messageCallbackUrl": self.message_callback_url,
            "metadata": self.metadata
        }

    @staticmethod
    def from_repr(raw_data: dict) -> AppDTO:
        return AppDTO(
            creation_ts=raw_data.get("creationTs", None),
            last_update_ts=raw_data.get("lastUpdateTs", None),
            app_id=raw_data["appId"],
            message_callback_url=raw_data.get("messageCallbackUrl", None),
            metadata=raw_data.get("metadata", None)
        )

    @staticmethod
    def from_app(app: App) -> AppDTO:
        return AppDTO(
            creation_ts=app.creation_ts,
            last_update_ts=app.last_update_ts,
            app_id=app.app_id,
            message_callback_url=app.message_callback_url,
            metadata=app.metadata
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, AppDTO):
            return False
        return self.app_id == o.app_id and self.creation_ts == o.creation_ts and self.last_update_ts == o.last_update_ts \
            and self.message_callback_url == o.message_callback_url and self.metadata == o.metadata

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
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

    def __eq__(self, o) -> bool:
        if not isinstance(o, AppDeveloper):
            return False
        return self.app_id == o.app_id and self.user_id == o.user_id

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()
