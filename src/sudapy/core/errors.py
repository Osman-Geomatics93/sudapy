"""Custom exceptions for SudaPy."""

from __future__ import annotations


class SudaPyError(Exception):
    """Base exception for all SudaPy errors."""

    def __init__(self, message: str, hint: str | None = None) -> None:
        self.hint = hint
        full = message
        if hint:
            full += f"\n  Hint: {hint}"
        super().__init__(full)


class CRSError(SudaPyError):
    """Raised for CRS-related issues (invalid EPSG, unsupported datum, etc.)."""


class FileFormatError(SudaPyError):
    """Raised when an input file has an unsupported or invalid format."""


class DependencyError(SudaPyError):
    """Raised when a required optional dependency is missing."""


def check_import(module: str, extra: str = "") -> None:
    """Import *module* or raise :class:`DependencyError` with install hint.

    Args:
        module: Dotted module name.
        extra: The pip extra that provides this module (e.g. ``"viz"``).
    """
    try:
        __import__(module)
    except ImportError as exc:
        hint = f'pip install "sudapy[{extra}]"' if extra else f"pip install {module}"
        raise DependencyError(
            f"Missing dependency: {module}",
            hint=hint,
        ) from exc
