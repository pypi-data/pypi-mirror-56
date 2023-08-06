from abc import abstractmethod
from typing import TypeVar
from typing_extensions import Protocol

from kashmir.core.data import Id, Release
from kashmir.core.entities.project import Project
from kashmir.core.protocols import Entity


class PRepository(Protocol):

    @abstractmethod
    def get(self, id: Id) -> Entity:
        raise NotImplementedError


class PProjectRepository(PRepository):

    @abstractmethod
    def get(self, id: Id) -> Project:
        raise NotImplementedError

    @abstractmethod
    def create_release(self, release: Release):
        raise NotImplementedError
