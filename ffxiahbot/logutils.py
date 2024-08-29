import contextlib
import logging.handlers
import warnings

lfmt = "[%(asctime)s][%(processName)s][%(threadName)s][%(levelname)-5s]: %(message)s"
dfmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.ERROR, format=lfmt, datefmt=dfmt)
logging.addLevelName(logging.CRITICAL, "FATAL")
logging.addLevelName(logging.WARNING, "WARN")
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)


def set_level(level):
    logging.getLogger().setLevel(level)


def set_debug():
    set_level(logging.DEBUG)


def set_error():
    set_level(logging.ERROR)


def set_info():
    set_level(logging.INFO)


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
            logging.exception("caught unhandled excetion")
            if fail and not isinstance(e, Warning):
                raise RuntimeError("application failure") from None
    finally:
        if capture_warnings:
            warnings.formatwarning = default_warning_format
            logging.captureWarnings(False)


class LoggingObject:
    """
    Inherit from this to get a bunch of logging functions as class methods.
    """

    def __init__(self):
        self._init_notify()

    def _init_notify(self):
        self.debug("init")

    def debug(self, msg, *args, **kwargs):
        logging.debug(self._preprocess(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logging.error(self._preprocess(msg), *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        logging.fatal(self._preprocess(msg), *args, **kwargs)
        exit(-1)

    def warn(self, msg, *args, **kwargs):
        logging.warning(self._preprocess(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        logging.info(self._preprocess(msg), *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        logging.exception(self._preprocess(msg), *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        logging.log(level, self._preprocess(msg), *args, **kwargs)

    def _preprocess(self, msg):
        return f"{self!r}: {msg}"

    @contextlib.contextmanager
    def capture(self, **kwargs):
        try:
            with capture(**kwargs):
                yield
        finally:
            pass


def add_rotating_file_handler(level=logging.DEBUG, fname="app.log", logger=None, fmt=lfmt, **kwargs):
    """
    Create rotating file handler and add it to logging.

    :param level: logging level
    :param fname: name of file
    :param logger: logger instance
    :param fmt: format
    """

    _kwargs = {"maxBytes": (1048576 * 5), "backupCount": 5}
    _kwargs.update(**kwargs)

    handler = logging.handlers.RotatingFileHandler(fname, **kwargs)
    handler.setLevel(level)

    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    if isinstance(logger, str):
        logger = logging.getLogger(logger)

    elif logger is None:
        logger = logging.getLogger()

    logger.addHandler(handler)

    return logger


def basic_config(verbose=False, silent=False, fname=None):
    """
    Setup logging.
    """
    set_info()

    if verbose:
        set_debug()

    if silent:
        set_error()

    if fname:
        add_rotating_file_handler(fname=fname)


if __name__ == "__main__":
    pass
