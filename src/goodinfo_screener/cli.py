"""Command-line interface for goodinfo-screener-cli."""

from typing import Annotated

import typer

from goodinfo_screener import __version__

app = typer.Typer(
    help=(
        "Save and run Goodinfo stock screener presets with local Playwright "
        "browser automation."
    ),
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            help="Show the installed version and exit.",
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Run Goodinfo screener automation commands."""


def _planned(command: str, milestone: str) -> None:
    typer.secho(
        f"`goodinfo {command}` is planned for {milestone} and is not implemented yet.",
        fg=typer.colors.YELLOW,
    )
    raise typer.Exit(code=2)


@app.command()
def init() -> None:
    """Create the local preset configuration directory."""
    _planned("init", "Day 2: Preset System")


@app.command(name="import")
def import_preset(
    name: Annotated[str, typer.Argument(help="Preset name, for example `high-margin`.")],
    url: Annotated[str, typer.Argument(help="Goodinfo StockList.asp screener URL.")],
    force: Annotated[
        bool,
        typer.Option("--force", help="Overwrite an existing preset with the same name."),
    ] = False,
) -> None:
    """Save a Goodinfo screener URL as a named preset."""
    _ = (name, url, force)
    _planned("import", "Day 2: Preset System")


@app.command(name="list")
def list_presets() -> None:
    """List saved screener presets."""
    _planned("list", "Day 2: Preset System")


@app.command()
def run(
    name: Annotated[str, typer.Argument(help="Preset name to run.")],
    headful: Annotated[
        bool,
        typer.Option("--headful", help="Run the browser in visible mode for debugging."),
    ] = False,
    timeout: Annotated[
        int,
        typer.Option("--timeout", help="Browser timeout in milliseconds."),
    ] = 30000,
    csv_path: Annotated[
        str | None,
        typer.Option("--csv", help="Write parsed rows to a CSV file."),
    ] = None,
    json_path: Annotated[
        str | None,
        typer.Option("--json", help="Write parsed rows to a JSON file."),
    ] = None,
) -> None:
    """Run a saved preset through browser automation."""
    _ = (name, headful, timeout, csv_path, json_path)
    _planned("run", "Day 3: Browser Runner")


@app.command()
def remove(
    name: Annotated[str, typer.Argument(help="Preset name to remove.")],
) -> None:
    """Remove a saved preset."""
    _ = name
    _planned("remove", "Day 2: Preset System")
