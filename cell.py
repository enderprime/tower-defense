"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense cell class
[E] ender.prime@gmail.com
[F] cell.py
[V] 02.13.17
"""

from bool import *
from const import *

import math

# --------------------------------------------------------------------------------------------------------------------

class Cell(object):
    """
    represents a single game board square
    """
    DIM = 48            # cell size in pixels
    HALF = DIM // 2     # half size in pixels

    # ----------------------------------------

    def __init__(self):

        self.col = 0
        self.row = 0
        self.x = 0
        self.y = 0

        self.base = False       # true if cell within base bounds
        self.gx = math.inf      # used for pathfinding
        self.hx = math.inf      # used for pathfinding
        self.parent = None      # used for pathfinding

        self.build = None       # if a tower is built here, holds tower _id
        self.open = True        # true if cell is open for building
        self.path = False       # true if cell location is being used in pathing

    # ----------------------------------------

    def __repr__(self):

        return 'Cell()'

    # ----------------------------------------

    def __str__(self):

        return str(self.index)
    
    # ----------------------------------------

    @property
    def bounds(self):
        """
        :return: bounding box points: (west, north, east, south)
        """
        return self.NW + self.SE

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
        return self.x + Cell.HALF - 1

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