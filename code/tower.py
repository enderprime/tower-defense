"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense tower class
[E] ender.prime@gmail.com
[F] tower.py
[V] 03.05.17
"""

from boolean import *
from constant import *
from grid import *

# --------------------------------------------------------------------------------------------------------------------

class Tower(object):
    """
    base class: buildable tower that kills creeps
    """

    RANGE_1 = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))
    RANGE_2 = ((2, 1), (2, 0), (2, -1),
               (1, 2), (1, 1), (1, 0), (1, -1), (1, -2),
               (0, 2), (0, 1), (0, -1), (0, -2),
               (-1, 2), (-1, 1), (-1, 0), (-1, -1), (-1, -2),
               (-2, 1), (-2, 0), (-2, -1))

    # ----------------------------------------

    def __init__(self, _id):

        self._id = _id              # unique int, assigned on spawn

        self.col = 0
        self.row = 0
        self.x = 0
        self.y = 0

        self.ai = 0                 # tower type
        self.angle = 0.0
        self.cooldown = 1000        # time between shots in ms
        self.cooldownLeft = 0
        self.damage = 1             # damage per shot to primary target
        self.description = ''
        self.energy = 1             # energy required to build
        self.imgFire = ''
        self.imgHit = ''
        self.imgTower = ''
        self.name = ''
        self.range = 1              # targeting range in cells
        self.rank = 1               # tower upgrade level
        self.splashDamage = 0       # splash damage to adjacent
        self.splashRadius = 0       # splash radius in cells
        self.target = 0             # creep _id

    # ----------------------------------------

    @property
    def index(self):
        """
        :return: grid index: (column, row)
        """
        return self.col, self.row

    # ----------------------------------------

    @property
    def xy(self):
        """
        :return: base point at center: (x, y)
        """
        return self.x, self.y

    # ----------------------------------------

    def spawn(self, index, point):
        """
        add tower to game
        :param index: (column, row)
        :param point: (x, y)
        :return: none
        """
        self.col, self.row = index
        self.x, self.y = point

    # ----------------------------------------

    def track(self):
        """
        update rotation and target, and fire if cooldown is up
        :return: none
        """

# --------------------------------------------------------------------------------------------------------------------

class TowerBase(Tower):
    """
    base tower, blocks pathing but does not fire
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.imgTower = PATH_IMG + 'tower-base.png'

    # ----------------------------------------

# --------------------------------------------------------------------------------------------------------------------

class TowerGun(Tower):
    """
    tower type 1
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.ai = 1
        self.imgTower = PATH_IMG + 'tower-1-1.png'

    # ----------------------------------------

# --------------------------------------------------------------------------------------------------------------------

class TowerCannon(Tower):
    """
    tower type 2
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.ai = 2
        self.imgTower = PATH_IMG + 'tower-2-1.png'

    # ----------------------------------------

# --------------------------------------------------------------------------------------------------------------------

class TowerMissle(Tower):
    """
    tower type 3
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.ai = 3
        self.imgTower = PATH_IMG + 'tower-3-1.png'

    # ----------------------------------------

# --------------------------------------------------------------------------------------------------------------------

class TowerSlow(Tower):
    """
    tower type 4
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.ai = 4
        self.imgTower = PATH_IMG + 'tower-4-1.png'

    # ----------------------------------------

# --------------------------------------------------------------------------------------------------------------------

class TowerLaser(Tower):
    """
    tower type 5
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.ai = 5
        self.imgTower = PATH_IMG + 'tower-5-1.png'

    # ----------------------------------------

# --------------------------------------------------------------------------------------------------------------------

class TowerRail(Tower):
    """
    tower type 6
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.ai = 6
        self.imgTower = PATH_IMG + 'tower-6-1.png'

    # ----------------------------------------

# --------------------------------------------------------------------------------------------------------------------

class TowerBash(Tower):
    """
    tower type 7
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.ai = 7
        self.imgTower = PATH_IMG + 'tower-7-1.png'

    # ----------------------------------------

# --------------------------------------------------------------------------------------------------------------------

class TowerSupport(Tower):
    """
    tower type 8
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.ai = 8
        self.imgTower = PATH_IMG + 'tower-8-1.png'

    # ----------------------------------------
