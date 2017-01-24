"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense cell class
[E] ender.prime@gmail.com
[F] cell.py
[V] 01.23.17
"""

from bool import *
from const import *

import pygame

# --------------------------------------------------------------------------------------------------------------------

class Cell(object):

    DIM = 36

    # ----------------------------------------

    def __init__(self, x, y):

        self.col = 0
        self.row = 0

        self.x = x
        self.y = y

        self.base = False
        self.build = None
        self.empty = True
        self.path = False

    # ----------------------------------------

    def __len__(self):

        return 1

    # ----------------------------------------

    def __repr__(self):

        return 'Cell(' + str(self.index) + ')'

    # ----------------------------------------

    def __str__(self):

        return str(self.index)

    # ----------------------------------------

    @property
    def index(self):

        return self.col, self.row

    # ----------------------------------------

    @property
    def rect(self):

        return pygame.Rect(self.x, self.y, Cell.DIM, Cell.DIM)

    # ----------------------------------------

    @property
    def xy(self):

        return self.x, self.y

    # ----------------------------------------

    def reset(self):

        self.build = None
        self.empty = True
        self.path = False
