from __future__ import absolute_import, annotations

import abc
from enum import Enum
from typing import Dict, Optional


class Scope(Enum):

    ID = "id"
    FIRST_NAME = "first_name"
    MIDDLE_NAME = "middle_name"
    LAST_NAME = "last_name"
    PREFIX_NAME = "prefix_name"
    SUFFIX_NAME = "suffix_name"
    BIRTHDATE = "birthdate"
    GENDER = "gender"
    NATIONALITY = "nationality"
    LOCALE = "locale"
    PHONE_NUMBER = "phone_number"
    WRITE_FEED = "write_feed"
    EMAIL = "email"
    CONVERSATIONS = "conversations"


class AbstractScopeMappings(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def _get_mappings() -> Dict[Scope, str]:
        pass

    @classmethod
    def get_field(cls, scope: Scope) -> Optional[str]:
        return cls._get_mappings().get(scope, None)
