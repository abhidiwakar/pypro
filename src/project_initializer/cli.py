from typing import Annotated

import typer

from project_initializer import __version__

app = typer.Typer(
    name="project-init",
    help="Create production-ready Python web projects from interactive prompts.",
    no_args_is_help=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"project-init {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the installed project-init version.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    return None


@app.command()
def new() -> None:
    typer.echo("Project generation is not wired yet.")
