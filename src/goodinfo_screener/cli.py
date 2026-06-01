"""Command-line interface for goodinfo-screener-cli."""

from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from goodinfo_screener import __version__
from goodinfo_screener.presets import (
    PresetError,
    add_preset,
    init_store,
    load_presets,
    remove_preset,
)

console = Console()

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


def _exit_with_error(message: str) -> None:
    typer.secho(message, fg=typer.colors.RED, err=True)
    raise typer.Exit(code=1)


def _planned(command: str, milestone: str) -> None:
    typer.secho(
        f"`goodinfo {command}` is planned for {milestone} and is not implemented yet.",
        fg=typer.colors.YELLOW,
    )
    raise typer.Exit(code=2)


@app.command()
def init() -> None:
    """Create the local preset configuration directory."""
    path = init_store()
    typer.echo(f"Preset store ready: {path}")


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
    try:
        existed = name in load_presets()
        add_preset(name, url, force=force)
    except PresetError as exc:
        _exit_with_error(str(exc))
    action = "Updated" if existed else "Saved"
    typer.echo(f"{action} preset `{name}`.")


@app.command(name="list")
def list_presets() -> None:
    """List saved screener presets."""
    presets = load_presets()
    if not presets:
        typer.echo("No presets found. Add one with `goodinfo import <name> <url>`.")
        return

    table = Table(title="Goodinfo Presets")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Source")
    table.add_column("Created")
    table.add_column("URL", overflow="fold")

    for name, preset in sorted(presets.items()):
        table.add_row(name, preset.source, preset.created_at.isoformat(), preset.url)

    console.print(table)


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
    try:
        remove_preset(name)
    except PresetError as exc:
        _exit_with_error(str(exc))
    typer.echo(f"Removed preset `{name}`.")
