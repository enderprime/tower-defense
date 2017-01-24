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

# --------------------------------------------------------------------------------------------------------------------

class Cell(object):

    DIM = 36

    # ----------------------------------------

    def __init__(self):

        self.col = 0
        self.row = 0
        self.index = (0, 0)

        self.x = 0
        self.y = 0
        self.xy = (0, 0)

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

    def reset(self):

        self.build = None
        self.empty = True
        self.path = False
