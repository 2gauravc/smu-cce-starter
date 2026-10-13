"""Local Markdown storage for analyses."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


ANALYSES_DIRECTORY = Path(__file__).resolve().parent.parent / "analyses-data"


def _filename_segment(value: str) -> str:
    segment = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-")
    if not segment:
        raise ValueError("Ticker and analysis type must contain letters or numbers.")
    return segment


def generate_analysis_filename(
    ticker: str,
    analysis_type: str,
    created_at: datetime | None = None,
) -> str:
    """Generate a readable, filesystem-safe analysis filename."""
    created_at = created_at or datetime.now(timezone.utc)
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    timestamp = created_at.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    ticker_segment = _filename_segment(ticker.upper())
    type_segment = _filename_segment(analysis_type.lower())
    return f"{ticker_segment}__{type_segment}__{timestamp}.md"


def save_analysis(
    content: str,
    ticker: str,
    analysis_type: str,
    created_at: datetime | None = None,
) -> Path:
    """Save Markdown without overwriting an existing analysis."""
    ANALYSES_DIRECTORY.mkdir(parents=True, exist_ok=True)
    filename = generate_analysis_filename(ticker, analysis_type, created_at)
    path = ANALYSES_DIRECTORY / filename
    counter = 1
    while True:
        try:
            with path.open("x", encoding="utf-8") as analysis_file:
                analysis_file.write(content)
            return path
        except FileExistsError:
            path = ANALYSES_DIRECTORY / f"{Path(filename).stem}-{counter}.md"
            counter += 1


def list_saved_analyses() -> list[Path]:
    """Return saved Markdown files, newest first."""
    ANALYSES_DIRECTORY.mkdir(parents=True, exist_ok=True)
    analyses = [
        path for path in ANALYSES_DIRECTORY.iterdir()
        if path.is_file() and path.suffix.lower() == ".md"
    ]
    return sorted(analyses, key=lambda path: path.stat().st_mtime, reverse=True)


def read_analysis(path: Path) -> str:
    """Read a saved analysis from the configured storage directory."""
    resolved_path = path.resolve()
    if resolved_path.parent != ANALYSES_DIRECTORY.resolve() or resolved_path.suffix.lower() != ".md":
        raise ValueError("The selected file is not a saved analysis.")
    return resolved_path.read_text(encoding="utf-8")


def analysis_label(path: Path) -> str:
    """Build a readable selector label from a generated analysis filename."""
    parts = path.stem.split("__")
    if len(parts) != 3:
        return path.stem.replace("-", " ")

    ticker, analysis_type, timestamp = parts
    timestamp = timestamp.split("-", maxsplit=1)[0]
    try:
        created_at = datetime.strptime(timestamp, "%Y%m%dT%H%M%S%fZ")
        readable_timestamp = created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
    except ValueError:
        readable_timestamp = timestamp
    return f"{ticker} — {analysis_type.replace('-', ' ')} — {readable_timestamp}"
