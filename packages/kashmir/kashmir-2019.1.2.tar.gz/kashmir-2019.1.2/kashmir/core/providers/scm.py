from abc import abstractmethod
from typing import Any
from typing_extensions import Protocol

from kashmir.core.data import Version, Release, Id


class SCMProvider(Protocol):
    """
    A Source Control Management provider.
    """
    project: Any

    @property
    @abstractmethod
    def version(self):
        raise NotImplementedError

    @abstractmethod
    def new_release(self, release: Release):
        raise NotImplementedError
