"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject

class Item(pydarkstar.darkobject.DarkObject):
    """
    Item properties.
    """
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    pass
