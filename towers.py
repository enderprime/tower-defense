"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense towers class
[E] ender.prime@gmail.com
[F] towers.py
[V] 02.03.17
"""

from bool import *
from const import *
from grid import *
from tower import *

import math

# --------------------------------------------------------------------------------------------------------------------

class Towers(object):
    """
    tower collection
    """
    def __init__(self):

        self._id = 0
        self.active = {}

    # ----------------------------------------

    def build(self, ai, col, row):

        self._id = self._id + 1

        tower = Tower(self._id)
        tower.ai = ai
        tower.col = col
        tower.row = row

        if 0 < ai < 9:
            tower.rank = 1

        self.active.update({self._id: tower})
