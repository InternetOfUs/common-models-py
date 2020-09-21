from __future__ import absolute_import, annotations

from wenet.common.model.user.common import PlatformType

# TODO remove
class PlatformDTO:

    def __init__(self, platform_type: PlatformType):
        self.platform_type = platform_type

    def to_repr(self) -> dict:
        return {
            "type": self.platform_type.value
        }

    @staticmethod
    def from_repr(raw_data: dict) -> PlatformDTO:
        platform_type = PlatformType(raw_data["type"])

        if platform_type == PlatformType.TELEGRAM:
            return TelegramPlatformDTO.from_repr(raw_data)
        else:
            raise ValueError(f"Unable to build a Platform from type {platform_type.value}")

    def __eq__(self, o):
        if not isinstance(o, PlatformDTO):
            return False
        return self.platform_type == o.platform_type

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()


class TelegramPlatformDTO(PlatformDTO):

    def __init__(self, bot_id: str):
        super().__init__(PlatformType.TELEGRAM)
        self.bot_id = bot_id

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "botId": self.bot_id
        })
        return base_repr

    @staticmethod
    def from_repr(raw_data: dict) -> PlatformDTO:
        return TelegramPlatformDTO(
            bot_id=raw_data["botId"]
        )
