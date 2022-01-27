from __future__ import absolute_import, annotations

import abc
from enum import Enum
from typing import Dict, Optional


class Scope(Enum):

    # Legacy scopes
    ID_LEGACY = "id"
    FIRST_NAME_LEGACY = "first_name"
    MIDDLE_NAME_LEGACY = "middle_name"
    LAST_NAME_LEGACY = "last_name"
    PREFIX_NAME_LEGACY = "prefix_name"
    SUFFIX_NAME_LEGACY = "suffix_name"
    BIRTHDATE_LEGACY = "birthdate"
    GENDER_LEGACY = "gender"
    NATIONALITY_LEGACY = "nationality"
    LOCALE_LEGACY = "locale"
    PHONE_NUMBER_LEGACY = "phone_number"
    WRITE_FEED_LEGACY = "write_feed"
    EMAIL_LEGACY = "email"
    CONVERSATIONS_LEGACY = "conversations"

    # public scopes
    ID_READ = "id:read"
    FIRST_NAME_READ = "first_name:read"
    LAST_NAME_READ = "last_name:read"

    # read scopes
    MIDDLE_NAME_READ = "middle_name:read"
    PREFIX_NAME_READ = "prefix_name:read"
    SUFFIX_NAME_READ = "suffix_name:read"
    BIRTHDATE_READ = "birth_date:read"
    GENDER_READ = "gender:read"
    EMAIL_READ = "email:read"
    PHONE_NUMBER_READ = "phone_number:read"
    LOCALE_READ = "locale:read"
    AVATAR_READ = "avatar:read"
    NATIONALITY_READ = "nationality:read"
    OCCUPATION_READ = "occupation:read"
    NORMS_READ = "norms:read"
    ACTIVITIES_READ = "activities:read"
    LOCATIONS_READ = "locations:read"
    RELATIONSHIPS_READ = "relationships:read"
    BEHAVIOURS_READ = "behaviours:read"
    MATERIALS_READ = "materials:read"
    COMPETENCES_READ = "competences:read"
    MEANINGS_READ = "meanings:read"

    # Write Scopes
    FIRST_NAME_WRITE = "first_name:write"
    LAST_NAME_WRITE = "last_name:write"
    MIDDLE_NAME_WRITE = "middle_name:write"
    PREFIX_NAME_WRITE = "prefix_name:write"
    SUFFIX_NAME_WRITE = "suffix_name:write"
    BIRTHDATE_WRITE = "birth_date:write"
    GENDER_WRITE = "gender:write"
    EMAIL_WRITE = "email:write"
    PHONE_NUMBER_WRITE = "phone_number:write"
    LOCALE_WRITE = "locale:write"
    AVATAR_WRITE = "avatar:write"
    NATIONALITY_WRITE = "nationality:write"
    OCCUPATION_WRITE = "occupation:write"
    NORMS_WRITE = "norms:write"
    ACTIVITIES_WRITE = "activities:write"
    LOCATIONS_WRITE = "locations:write"
    RELATIONSHIPS_WRITE = "relationships:write"
    BEHAVIOURS_WRITE = "behaviours:write"
    MATERIALS_WRITE = "materials:write"
    COMPETENCES_WRITE = "competences:write"
    MEANINGS_WRITE = "meanings:write"
    CONVERSATIONS_WRITE = "conversation:write"
    DATA_WRITE = "data:write"


class AbstractScopeMappings(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def _get_read_scope_mappings() -> Dict[Scope, str]:
        """
        retireve the dictionary which maps a read scope on afield
        :return:
        """
        pass

    @classmethod
    def get_field(cls, scope: Scope) -> Optional[str]:
        """
        retrieve the field associated to a read scope.
        :param scope:
        :return:
        """
        return cls._get_read_scope_mappings().get(scope, None)
