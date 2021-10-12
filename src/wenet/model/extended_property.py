from __future__ import absolute_import, annotations

from abc import ABC, abstractmethod


class ExtendedProperty(ABC):

    @abstractmethod
    def to_repr(self) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def from_repr(raw_data: dict) -> ExtendedProperty:
        pass

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()
