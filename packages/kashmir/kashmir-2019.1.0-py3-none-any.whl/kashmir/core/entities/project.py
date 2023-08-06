from dataclasses import dataclass
from datetime import datetime

from kashmir.core.data import Version, Release, Id
from kashmir.core.protocols.entity import Entity


@dataclass
class Project(Entity):

    def __init__(self, id: Id, version: Version):
        self.id = id
        self.version = version

    def new_release(self) -> Release:
        current_year = datetime.now().year
        if self.version and self.version.year == current_year:
            year, release, fix = self.version.year, self.version.release + 1, self.version.fix
        else:
            year, release, fix = current_year, 1, 0
        new_version = Version(year, release, fix)
        return Release(self.id, new_version)

    def new_fix(self) -> Release:
        new_version = Version(self.version.year,
                              self.version.release,
                              self.version.fix + 1)
        return Release(self.id, new_version)

    def __str__(self):
        return f"Project<{self.id}> {self.version}"
