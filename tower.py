"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense tower class
[E] ender.prime@gmail.com
[F] tower.py
[V] 02.03.17
"""

from bool import *
from const import *

# --------------------------------------------------------------------------------------------------------------------

class Tower(object):
    """
    buildable tower
    """

    # ----------------------------------------

    def __init__(self, _id):

        # _id == unique int, assigned from collection
        self._id = _id

        self.ai = 0
        self.angle = 0
        self.col = 0
        self.damage = 0
        self.energy = 0
        self.imgHit = ''
        self.range = 0
        self.rank = 0
        self.row = 0
        self.speed = 100
        self.target = (0, 0)

    # ----------------------------------------

    @property
    def imgTower(self):

        if (self.ai == 0) or (self.ai == 9):
            return PATH_IMG + 'tower-' + str(self.ai) + '.png'
        else:
            return PATH_IMG + 'tower-' + str(self.ai) + '-' + str(self.rank) + '.png'

    # ----------------------------------------

    @property
    def index(self):
        """
        :return: grid index: (column, row)
        """
        return self.col, self.row

    # ----------------------------------------
