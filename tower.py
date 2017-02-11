"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense tower class
[E] ender.prime@gmail.com
[F] tower.py
[V] 02.10.17
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

        # _id == unique int, assigned on spawn
        self._id = _id

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
        if self.ai == 0:
            return PATH_IMG + 'tower-0.png'
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
