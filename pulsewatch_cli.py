"""PulseWatch PoC Week 1 CLI."""

from __future__ import annotations

from pathlib import Path

import click
import yaml

from diff import diff_capture_dirs
from storage import capture_directory_for_url, save_capture_artifacts


def _load_urls_from_config(config_path: Path) -> list[str]:
    """Load target URLs from YAML file.

    Supports either:
    - A top-level list of URLs
    - A mapping with a `urls` key containing the list
    """
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise click.ClickException(f"Config file not found: {config_path}") from exc

    urls: list[str]
    if isinstance(data, list):
        urls = [u for u in data if isinstance(u, str) and u.strip()]
    elif isinstance(data, dict) and isinstance(data.get("urls"), list):
        urls = [u for u in data["urls"] if isinstance(u, str) and u.strip()]
    else:
        raise click.ClickException("Invalid config format. Expected a list of URLs or {urls: [...]}.")

    if not urls:
        raise click.ClickException("Config contains no valid URLs.")

    return urls


@click.group(help="PulseWatch PoC: capture pages and compare captures.")
def cli() -> None:
    pass


@cli.command("capture")
@click.argument("url", required=False)
@click.option("--config", "config_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), help="YAML file with target URLs.")
def capture_command(url: str | None, config_path: Path | None) -> None:
    """Capture URL HTML + screenshot and persist artifacts."""
    from capture import capture_batch, capture_html_and_screenshot

    if not url and not config_path:
        raise click.ClickException("Provide either URL or --config.")

    if url and config_path:
        raise click.ClickException("Use either URL or --config, not both.")

    if config_path:
        urls = _load_urls_from_config(config_path)
        result = capture_batch(urls=urls, output_dir="data")
        click.echo(
            f"Captured {result['captured']}/{result['total']} pages. "
            f"Summarized: {result.get('summarized', 0)}. Failed: {result['failed']}"
        )
        return

    assert url is not None
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
