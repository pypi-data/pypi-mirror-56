from typing import Optional

import gitlab  # type: ignore

from kashmir.core.data import Version, Release
from kashmir.core.providers import SCMProvider


class GitLab(SCMProvider):

    def __init__(self, server: str, token: str, project_id: str):
        gl = gitlab.Gitlab(server, token)
        self.project = gl.projects.get(project_id)

    @property
    def version(self) -> Optional[Version]:
        """
        This method tries to find the last version for the project.

        In order for this tho work, it's expected that the version match the
        following pattern <<YEAR>>.<<MILESTONE>>.<<FIX>>
        :return: Version
        """
        releases = self.project.releases.list()
        try:
            last_release = releases[0]
            version_components = map(int, last_release.name.split('.'))
            return Version(*version_components)
        except (IndexError, TypeError):
            return None

    def new_release(self, release: Release):
        branch_body = {
            "branch": f"release-{release.version}",
            "ref": "master"
        }
        release_body = {
            "name": str(release.version),
            "tag_name": str(release.version),
            "description": f"Release {release.version}",
            "ref": f"release-{release.version}"
        }
        self.project.branches.create(branch_body)
        self.project.releases.create(release_body)
