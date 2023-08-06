from kashmir.core.data import Id, Release
from kashmir.core.entities.project import Project
from kashmir.core.protocols.repository import PProjectRepository
from kashmir.core.providers import SCMProvider


class ProjectRepository(PProjectRepository):

    def __init__(self, scm: SCMProvider):
        self.scm = scm

    def get(self, id: Id) -> Project:
        return Project(
            id=self.scm.project.id,
            version=self.scm.version
        )

    def create_release(self, release: Release) -> Release:
        return self.scm.new_release(release)
