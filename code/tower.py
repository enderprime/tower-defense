"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense tower class
[E] ender.prime@gmail.com
[F] tower.py
[V] 02.14.17
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

        self._id = _id              # unique int, assigned on spawn

        self.ai = 0                 # tower type
        self.angle = 0.0
        self.col = 0
        self.cooldown = 1.0         # time between shots
        self.cooldownLeft = 1.0
        self.damage = 1             # damage per shot
        self.description = ''
        self.energy = 1             # energy required to build
        self.imgFire = ''
        self.imgHit = ''
        self.name = ''
        self.range = 1              # shot radius in cells
        self.rank = 1               # tower upgrade level
        self.row = 0
        self.splash = 0             # damage splash radius in cells
        self.target = 0             # creep _id

    # ----------------------------------------

    @property
    def imgTower(self):
        """
        :return: image path
        """
        if 0 < self.ai < 8:
            return PATH_IMG + 'tower-' + str(self.ai) + '-' + str(self.rank) + '.png'
        else:
            return PATH_IMG + 'tower-' + str(self.ai) + '.png'

    # ----------------------------------------

    @property
    def index(self):
        """
        :return: grid index: (column, row)
        """
        return self.col, self.row

    # ----------------------------------------
