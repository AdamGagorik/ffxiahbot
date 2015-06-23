from .logutils import LoggingObject


class DarkObject(LoggingObject):
    """
    Base class for all objects in pydarkstar.
    """

    def __init__(self):
        super(DarkObject, self).__init__()

    def __repr__(self):
        return '({}) {}'.format(hex(id(self)), self.__class__.__name__)


if __name__ == '__main__':
    pass
