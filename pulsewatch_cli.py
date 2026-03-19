"""PulseWatch PoC Week 1 CLI."""

from __future__ import annotations

from pathlib import Path

import click

from diff import diff_capture_dirs
from storage import capture_directory_for_url, save_capture_artifacts


@click.group(help="PulseWatch PoC: capture pages and compare captures.")
def cli() -> None:
    pass


@cli.command("capture")
@click.argument("url")
def capture_command(url: str) -> None:
    """Capture URL HTML + screenshot and persist artifacts."""
    from capture import capture_html_and_screenshot

    capture_dir = capture_directory_for_url(url)
    captured = capture_html_and_screenshot(url, capture_dir)
    saved = save_capture_artifacts(
        capture_dir=Path(capture_dir),
        url=url,
        html=captured["html"],
        screenshot_path=captured["screenshot_path"],
    )

    click.echo(f"Capture saved: {saved['capture_dir']}")
    click.echo(f"HTML: {saved['html_path']}")
    click.echo(f"Screenshot: {saved['screenshot_path']}")
    click.echo(f"Metadata: {saved['metadata_path']}")


@cli.command("diff")
@click.argument("old_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("new_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def diff_command(old_dir: Path, new_dir: Path) -> None:
    """Diff two capture directories and write diff.txt to NEW_DIR."""
    result = diff_capture_dirs(old_dir, new_dir)
    click.echo(f"Changed lines: {result['changed_lines_count']}")
    click.echo(f"Diff output: {result['diff_path']}")


if __name__ == "__main__":
    cli()
