from __future__ import absolute_import, annotations

import abc
from typing import Optional, List

from wenet_service_api.model.app import UserAccountTelegram
from wenet.service_api.common import PlatformType


class AuthenticationAccount(abc.ABC):

    def __init__(self, account_type: PlatformType, user_id: Optional[int]):
        self.user_id = user_id
        self.account_type = account_type

    def to_repr(self) -> dict:
        return {
            "type": self.account_type.value,
            "userId": str(self.user_id) if self.user_id is not None else None
        }

    @staticmethod
    def from_repr(raw_data: dict) -> AuthenticationAccount:
        account_type = PlatformType(raw_data["type"])

        if account_type == PlatformType.TELEGRAM:
            return TelegramAuthenticationAccount.from_repr(raw_data)
        else:
            raise ValueError(f"Unable to build a TelegramAuthenticationAccount from type [{account_type.value}]")

    def __eq__(self, o):
        if not isinstance(o, AuthenticationAccount):
            return False
        return self.account_type == o.account_type

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()


class TelegramAuthenticationAccount(AuthenticationAccount):

    def __init__(self, app_id: str, metadata: Optional[dict], telegram_id: int, user_id: Optional[int] = None):
        super().__init__(PlatformType.TELEGRAM, user_id)
        self.app_id = app_id
        self.metadata = metadata
        self.telegram_id = telegram_id

        if not isinstance(app_id, str):
            raise TypeError("app_id should be a string")

        if metadata:
            if not isinstance(metadata, dict):
                raise TypeError("metadata should be a dictionary")
        else:
            self.metadata = {}

        if not isinstance(telegram_id, int):
            raise TypeError("telegram_id should be an integer")

    def to_repr(self) -> dict:
        base_repr = super().to_repr()
        base_repr.update({
            "appId": self.app_id,
            "metadata": self.metadata,
            "telegramId": self.telegram_id
        })
        return base_repr

    @staticmethod
    def from_repr(raw_data: dict) -> TelegramAuthenticationAccount:
        return TelegramAuthenticationAccount(
            app_id=raw_data["appId"],
            metadata=raw_data.get("metadata", None),
            telegram_id=raw_data["telegramId"],
            user_id=int(raw_data["userId"]) if raw_data.get("userId", None) is not None else None
        )

    def __eq__(self, o):
        if not isinstance(o, TelegramAuthenticationAccount):
            return False
        return self.app_id == o.app_id and self.metadata == o.metadata and self.telegram_id == o.telegram_id

    @staticmethod
    def from_user_account_telegram(account: UserAccountTelegram):
        return TelegramAuthenticationAccount(
            app_id=account.app_id,
            metadata=account.metadata,
            telegram_id=account.telegram_id,
            user_id=account.user_id
        )


class WeNetUserWithAccounts:

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.accounts: List[AuthenticationAccount] = []

    def with_account(self, account: AuthenticationAccount) -> WeNetUserWithAccounts:
        if account.user_id is not None and account.user_id != self.user_id:
            raise ValueError(f"Invalid user_id [{account.user_id}] for WeNetUserWithAccounts with id [{self.user_id}]")
        self.accounts.append(account)
        return self

    def to_repr(self) -> dict:
        return {
            "userId": str(self.user_id),
            "accounts": list(x.to_repr() for x in self.accounts)
        }

    @staticmethod
    def from_repr(raw_data: dict) -> WeNetUserWithAccounts:
        user = WeNetUserWithAccounts(
            user_id=int(raw_data["userId"]),
        )

        for raw_account in raw_data["accounts"]:
            account = AuthenticationAccount.from_repr(raw_account)
            user.with_account(account)

        return user

    def __eq__(self, o) -> bool:
        if not isinstance(o, WeNetUserWithAccounts):
            return False
        return self.user_id == o.user_id and self.accounts == o.accounts

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()
