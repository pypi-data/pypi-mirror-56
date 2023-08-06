"""A colored logger for python

This module wraps around Google's absl logging module and delegates
all actual logging to absl logging. This module simply modifies the
log message passed through to absl logger with color codes from the
colored library based of the log severity.
"""

from absl import logging
from colored import fore, style


def fatal(msg, *args, **kwargs):
    """Logs a fatal message."""
    logging.fatal(fore.RED + msg + style.RESET, *args, **kwargs)


def error(msg, *args, **kwargs):
    """Logs an error message."""
    logging.error(fore.LIGHT_RED + msg + style.RESET, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """Logs a warning message."""
    logging.warning(fore.YELLOW + msg + style.RESET, *args, **kwargs)


def info(msg, *args, **kwargs):
    """Logs an info message."""
    logging.info(fore.DARK_GRAY + msg + style.RESET, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """Logs a debug message."""
    logging.debug(fore.STEEL_BLUE + msg + style.RESET, *args, **kwargs)


def exception(msg, *args):
    """Logs an exception."""
    logging.exception(fore.ORANGE_1 + msg + style.RESET, *args)
