"""Logging setup for the application."""

import logging


def configure_logging() -> None:
    """Configure concise operational logs without user-submitted content."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
