import pydarkstar.logutils

class DarkObject(pydarkstar.logutils.LoggingObject):
    """
    Base class for all objects in pydarkstar.
    """
    def __init__(self, *args, **kwargs):
        super(DarkObject, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '({}) {}'.format(hex(id(self)), self.__class__.__name__)

if __name__ == '__main__':
    pass