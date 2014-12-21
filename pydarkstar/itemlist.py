"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject
import pydarkstar.item

class ItemList(pydarkstar.darkobject.DarkObject):
    """
    Container for Item objects.
    """
    def __init__(self, *args, **kwargs):
        super(ItemList, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    pass
