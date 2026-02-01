"""Centralized logging configuration for SudaPy."""

from __future__ import annotations

import logging

from rich.console import Console
from rich.logging import RichHandler

console = Console(stderr=True)

_LOG_FORMAT = "%(message)s"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger with Rich handler.

    Args:
        name: Logger name (typically ``__name__``).
        level: Logging level.

    Returns:
        Configured :class:`logging.Logger`.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            markup=True,
        )
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def setup_logging(verbose: bool = False) -> None:
    """Configure root logging for the CLI.

    Args:
        verbose: If ``True``, set level to DEBUG.
    """
    level = logging.DEBUG if verbose else logging.INFO
    root = logging.getLogger("sudapy")
    root.setLevel(level)
    if not root.handlers:
        handler = RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            markup=True,
        )
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        root.addHandler(handler)
