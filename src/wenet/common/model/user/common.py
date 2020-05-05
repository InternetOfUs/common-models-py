from __future__ import absolute_import, annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from iso639 import is_valid639_1


class PlatformType(Enum):

    TELEGRAM = "telegram"


class Gender(Enum):

    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class Date:

    def __init__(self, year: Optional[int], month: Optional[int], day: Optional[int]):
        """

        @param year:
        @param month: the month form 1 to 12 (1: Jan, 12: Dec)
        @param day:
        """
        self.year = year
        self.month = month
        self.day = day

        if day is not None and not isinstance(day, int):
            raise TypeError("Day should be a string")
        if month is not None and not isinstance(month, int):
            raise TypeError("Month should be a string")
        if year is not None and not isinstance(year, int):
            raise TypeError("Year should be a string")

        if not self._validate():
            raise ValueError("date %s is not valid" % self)

    def _validate(self) -> bool:

        if self.year is not None and self.month is not None and self.day is not None:
            return self.date_dt is not None
        elif self.year is not None and self.month is not None and self.day is None:
            return 1 <= self.month <= 12
        elif self.year is not None and self.month is None and self.day is None:
            return True
        elif self.year is None and self.month is None and self.day is None:
            return True
        else:
            return False

    def to_repr(self) -> dict:
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day
        }

    @staticmethod
    def from_repr(raw_data: dict) -> Date:
        return Date(
            year=raw_data.get("year", None),
            month=raw_data.get("month", None),
            day=raw_data.get("day", None)
        )

    @property
    def date_dt(self) -> Optional[datetime]:
        if self.year is None or self.month is None or self.day is None:
            return None
        else:
            return datetime(year=self.year, month=self.month, day=self.day)

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, Date):
            return False
        return self.year == o.year and self.month == o.month and self.day == o.day

    @staticmethod
    def empty() -> Date:
        return Date(
            year=None,
            month=None,
            day=None
        )


class UserLanguage:

    def __init__(self, name: str, level: str, code: str):
        self.name = name
        self.level = level
        self.code = code

        if not isinstance(name, str):
            raise TypeError("Name should be a string")
        if not isinstance(level, str):
            raise TypeError("Level should be a string")
        if not isinstance(code, str):
            raise TypeError("Code should be a string")

        if not is_valid639_1(self.code):
            raise ValueError("[%s] is not a valid iso639-1 language" % self.code)

    def to_repr(self) -> dict:
        return {
            "name": self.name,
            "level": self.level,
            "code": self.code
        }

    @staticmethod
    def from_repr(raw_data: dict) -> UserLanguage:
        return UserLanguage(
            name=raw_data["name"],
            level=raw_data["level"],
            code=raw_data["code"]
        )

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, UserLanguage):
            return False
        return self.name == o.name and self.code == o.code and self.level == o.level
