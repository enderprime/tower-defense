"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense cell class
[E] ender.prime@gmail.com
[F] cell.py
[V] 01.25.17
"""

from bool import *
from const import *

# --------------------------------------------------------------------------------------------------------------------

class Cell(object):

    DIM = 36
    HALF = 18

    # ----------------------------------------

    def __init__(self, x, y):

        self.col = 0
        self.row = 0

        self.x = x
        self.y = y

        self.base = False
        self.build = None
        self.open = True
        self.path = False

    # ----------------------------------------

    def __len__(self):

        return 1

    # ----------------------------------------

    def __repr__(self):

        return 'Cell' + str(self.xy)

    # ----------------------------------------

    def __str__(self):

        return str(self.index)

    # ----------------------------------------

    @property
    def bounds(self):
        """
        :return: bounding box points: ((west, north), (east, south))
        """
        return self.NW, self.SE

    # ----------------------------------------

    @property
    def index(self):
        """
        :return: grid index: (col, row)
        """
        return self.col, self.row

    # ----------------------------------------

    @property
    def east(self):
        """
        :return: east x value
        """
        return self.x + Cell.HALF - 1

    # ----------------------------------------

    @property
    def north(self):
        """
        :return: north y value
        """
        return self.y - Cell.HALF

    # ----------------------------------------

    @property
    def NE(self):
        """
        :return: northeast point: (x, y)
        """
        return self.east, self.north

    # ----------------------------------------

    @property
    def NW(self):
        """
        :return: northwest point: (x, y)
        """
        return self.west, self.north

    # ----------------------------------------

    @property
    def south(self):
        """
        :return: south y value
        """
        return self.y + Cell.HALF - 1

    # ----------------------------------------

    @property
    def SE(self):
        """
        :return: southeast point: (x, y)
        """
        return self.east, self.south

    # ----------------------------------------

    @property
    def SW(self):
        """
        :return: southwest point: (x, y)
        """
        return self.west, self.south

    # ----------------------------------------

    @property
    def west(self):
        """
        :return: west x value
        """
        return self.x - Cell.HALF

    # ----------------------------------------

    @property
    def xy(self):
        """
        :return: base point at center: (x, y)
        """
        return self.x, self.y

    # ----------------------------------------

    def reset(self):
        """
        :return: reset cell to new game conditions
        """
        self.build = None
        self.open = True
        self.path = False
