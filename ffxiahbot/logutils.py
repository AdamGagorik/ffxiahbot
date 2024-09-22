import contextlib
import logging
import warnings
from collections.abc import Iterator
from typing import Any

logger = logging.getLogger("ffxiahbot")


# noinspection PyUnusedLocal
def custom_warning_format(
    message: Warning | str, category: type[Warning], filename: str, lineno: int, *args: Any, **kwargs: Any
) -> str:
    return f"{filename}:{lineno}\n{category.__name__}: {message}"


@contextlib.contextmanager
def capture(capture_warnings: bool = True, fail: bool = False) -> Iterator:
    """
    Log exceptions and warnings.
    """
    default_warning_format = warnings.formatwarning
    try:
        if capture_warnings:
            warnings.formatwarning = custom_warning_format
            logging.captureWarnings(True)
        try:
            yield
        except Exception as e:
            logging.exception("caught unhandled exception")
            if fail and not isinstance(e, Warning):
                raise RuntimeError("application failure") from None
    finally:
        if capture_warnings:
            warnings.formatwarning = default_warning_format
            logging.captureWarnings(False)
