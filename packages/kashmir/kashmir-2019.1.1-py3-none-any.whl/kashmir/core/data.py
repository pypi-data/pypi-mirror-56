from dataclasses import dataclass
from datetime import datetime
from typing import Union

Id = Union[int, str]


@dataclass(frozen=True)
class Version:
    year: int  # AAAA
    release: int  # Non-negative integer
    fix: int  # Non-negative integer

    def __str__(self):
        return f"{self.year}.{self.release}.{self.fix}"

    @classmethod
    def new(cls) -> 'Version':
        return cls(datetime.now().year, 1, 0)


@dataclass(frozen=True)
class Release:
    project: Id
    version: Version

    def __str__(self):
        return f"Release {self.version}"
