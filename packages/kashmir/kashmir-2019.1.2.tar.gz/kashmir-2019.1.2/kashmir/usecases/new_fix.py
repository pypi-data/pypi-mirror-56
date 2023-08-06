from dataclasses import dataclass

from kashmir.core.data import Id
from kashmir.core.protocols import PProjectRepository


@dataclass
class NewFix:
    repository: PProjectRepository

    def __call__(self, project_id: Id):
        project = self.repository.get(project_id)
        new_release = project.new_fix()
        self.repository.create_release(new_release)
        return new_release
