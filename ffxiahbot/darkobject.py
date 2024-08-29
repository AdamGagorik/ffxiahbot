from dataclasses import dataclass


@dataclass()
class DarkObject:
    """
    Base class for all objects.
    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"({hex(id(self))}) {self.__class__.__name__}"
