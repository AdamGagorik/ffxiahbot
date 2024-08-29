from ffxiahbot.logutils import LoggingObject


class DarkObject(LoggingObject):
    """
    Base class for all objects in ffxiahbot.
    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"({hex(id(self))}) {self.__class__.__name__}"


if __name__ == "__main__":
    pass
