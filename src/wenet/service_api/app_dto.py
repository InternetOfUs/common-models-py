from __future__ import absolute_import, annotations

from typing import Optional, List

from wenet.service_api.platform_dto import PlatformDTO, TelegramPlatformDTO


class AppDTO:

    def __init__(self, creation_ts: Optional[int], last_update_ts: Optional[int], app_id: str, app_token: str, allowed_platforms: List[PlatformDTO], message_callback_url: Optional[str], metadata: Optional[dict]):
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.app_id = app_id
        self.app_token = app_token
        self.allowed_platforms = allowed_platforms
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
        if isinstance(self.allowed_platforms, list):
            for platforms in self.allowed_platforms:
                if not isinstance(platforms, PlatformDTO):
                    raise TypeError("AllowedPlatforms should be a list of Platforms")
        else:
            raise TypeError("AllowedPlatforms should be a list of Platforms")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata should be a dictionary")

    def to_repr(self) -> dict:
        return {
            "creationTs": self.creation_ts,
            "lastUpdateTs": self.last_update_ts,
            "appId": self.app_id,
            "appToken": self.app_token,
            "allowedPlatforms": list(x.to_repr() for x in self.allowed_platforms),
            "messageCallbackUrl": self.message_callback_url,
            "metadata": self.metadata
        }

    @staticmethod
    def from_repr(raw_data: dict) -> AppDTO:
        return AppDTO(
            creation_ts=raw_data.get("creationTs", None),
            last_update_ts=raw_data.get("lastUpdateTs", None),
            app_id=raw_data["appId"],
            app_token=raw_data["appToken"],
            allowed_platforms=list(PlatformDTO.from_repr(x) for x in raw_data["allowedPlatforms"]),
            message_callback_url=raw_data.get("messageCallbackUrl", None),
            metadata=raw_data.get("metadata", None)
        )

    def __eq__(self, o):
        if not isinstance(o, AppDTO):
            return False
        return self.app_id == o.app_id and self.app_token == o.app_token and self.allowed_platforms == o.allowed_platforms \
            and self.message_callback_url == o.message_callback_url and self.metadata == o.metadata

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__str__()

    @staticmethod
    def from_app(app) -> AppDTO:
        from wenet_service_api.model.app import App

        if not isinstance(app, App):
            raise TypeError(f"Unable to build an AppDTO from type [{type(app)}]")

        if app.platform_telegram:
            allowed_platforms = [
                TelegramPlatformDTO.from_platform_telegram(app.platform_telegram)
            ]
        else:
            allowed_platforms = []

        return AppDTO(
            creation_ts=app.creation_ts,
            last_update_ts=app.last_update_ts,
            app_id=app.app_id,
            app_token=app.app_token,
            allowed_platforms=allowed_platforms,
            message_callback_url=app.message_call_back_url,
            metadata=app.metadata
        )
