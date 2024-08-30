import contextlib
import logging
import warnings

logger = logging.getLogger("ffxiahbot")


# noinspection PyUnusedLocal
def custom_warning_format(message, category, filename, lineno, *args, **kwargs):
    return f"{filename}:{lineno}\n{category.__name__}: {message}"


@contextlib.contextmanager
def capture(capture_warnings=True, fail=False):
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
