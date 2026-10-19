"""Shared checks for source and destination path aliases."""

import os
from pathlib import Path


def paths_alias(source: str | Path, destination: str | Path) -> bool:
    """Return whether two paths name the same file, failing closed on errors.

    ``Path.resolve`` can raise ``RuntimeError`` for symlink loops. Permission
    and other resolution errors are surfaced as a user-facing ``ValueError``
    instead of allowing a possibly unsafe write to proceed.
    """
    source_path = Path(source)
    destination_path = Path(destination)
    try:
        if source_path.resolve() == destination_path.resolve():
            return True
    except (OSError, RuntimeError) as exc:
        raise ValueError("Cannot safely resolve source and output paths.") from exc

    try:
        return os.path.samefile(source_path, destination_path)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise ValueError("Cannot safely verify source and output paths.") from exc
