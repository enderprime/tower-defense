"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense cell class
[E] ender.prime@gmail.com
[F] cell.py
[V] 02.03.17
"""

from bool import *
from const import *

import math

# --------------------------------------------------------------------------------------------------------------------

class Cell(object):
    """
    represents a single game board square
    """
    DIM = 48

    # ----------------------------------------

    def __init__(self):

        self.col = 0
        self.row = 0
        self.x = 0
        self.y = 0

        self.base = False
        self.gx = math.inf
        self.hx = math.inf
        self.parent = None

        self.build = None
        self.open = True

    # ----------------------------------------

    def __repr__(self):

        return 'Cell(' + str(self.col) + ', ' + str(self.row) + ', ' + str(self.x) + ', ' + str(self.y) + ')'

    # ----------------------------------------

    def __str__(self):

        return str(self.index)

    # ----------------------------------------
    
    @classmethod
    def half(cls):
        """ 
        :return: size in pixels // 2
        """
        return Cell.DIM // 2
    
    # ----------------------------------------

    @property
    def bounds(self):
        """
        :return: bounding box points: ((west, north), (east, south))
        """
        return self.NW, self.SE

    # ----------------------------------------

    @property
    def fx(self):
        """
        :return: pathfinder fx == gx + hx
        """
        return self.gx + self.hx

    # ----------------------------------------

    @property
    def east(self):
        """
        :return: east x value
        """
        return self.x + Cell.half() - 1

    # ----------------------------------------

    @property
    def index(self):
        """
        :return: grid index: (column, row)
        """
        return self.col, self.row

    # ----------------------------------------

    @property
    def north(self):
        """
        :return: north y value
        """
        return self.y - Cell.half()

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
        return self.y + Cell.half() - 1

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
        return self.x - Cell.half()

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
