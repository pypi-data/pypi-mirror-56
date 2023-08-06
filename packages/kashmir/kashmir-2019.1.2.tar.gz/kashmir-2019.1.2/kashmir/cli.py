import click
from kashmir import __version__
from pathlib import Path

from kashmir.providers.gitlab import GitLab
from kashmir.usecases import NewRelease
from kashmir.repositories import ProjectRepository
from kashmir.usecases.new_fix import NewFix


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.group('new')
@click.pass_context
def new(ctx):
    pass


@new.command('release')
@click.argument('PROJECT_ID')
@click.option('--scm', default='https://gitlab.com', help='SCM Server address')
@click.option('--token', help='SCM Token', required=True)
@click.pass_context
def new_release(ctx, project_id, scm, token):
    scm = GitLab(
        server=scm,
        token=token,
        project_id=project_id
    )
    repository = ProjectRepository(scm)
    use_case = NewRelease(repository)
    release = use_case(project_id)
    click.echo(f"New release! {release}")


@new.command('fix')
@click.argument('PROJECT_ID')
@click.option('--scm', default='https://gitlab.com', help='SCM Server address')
@click.option('--token', help='SCM Token', required=True)
@click.pass_context
def new_fix(ctx, project_id, scm, token):
    scm = GitLab(
        server=scm,
        token=token,
        project_id=project_id
    )
    repository = ProjectRepository(scm)
    use_case = NewFix(repository)
    release = use_case(project_id)
    click.echo(f"New release! {release}")
