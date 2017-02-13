"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense creep class
[E] ender.prime@gmail.com
[F] creep.py
[V] 02.13.17
"""

from bool import *
from const import *

# --------------------------------------------------------------------------------------------------------------------

class Creep(object):
    """
    killable enemy
    """
    def __init__(self, _id):

        # _id == unique int, assigned on spawn
        self._id = _id

        self.ai = 0             # creep type
        self.angle = 0.0
        self.damage = 1         # mass lost if escaped
        self.description = ''
        self.energy = 1         # energy gained if killed
        self.goal = ()          # used in pathfinding
        self.index = ()
        self.mass = 1           # damage required to kill
        self.name = ''
        self.path = []
        self.rank = 1           # creep level, used for generating stat values
        self.size = 48          # pixels
        self.speed = 48         # pixels per second, roughly
        self.target = ()        # index of next cell to visit
        self.x = 0
        self.y = 0

    # ----------------------------------------

    @property
    def bounds(self):
        """
        :return: bounding box points: (west, north, east, south)
        """
        return self.NW + self.SE

    # ----------------------------------------

    @property
    def east(self):
        """
        :return: east x value
        """
        return self.x + self.half - 1

     # ----------------------------------------

    @property
    def half(self):
        """
        :return: size in pixels // 2
        """
        return self.size // 2

    # ----------------------------------------

    @property
    def image(self):
        """
        :return: image path
        """
        if self.ai < 10:
            return PATH_IMG + 'creep-0' + str(self.ai) + '.png'
        else:
            return PATH_IMG + 'creep-' + str(self.ai) + '.png'

    # ----------------------------------------

    @property
    def north(self):
        """
        :return: north y value rounded to nearest int
        """
        return int(round(self.y, 0)) - self.half

    # ----------------------------------------

    @property
    def NE(self):
        """
        :return: northeast point: (x, y) rounded to nearest ints
        """
        return self.east, self.north

    # ----------------------------------------

    @property
    def NW(self):
        """
        :return: northwest point: (x, y) rounded to nearest ints
        """
        return self.west, self.north

    # ----------------------------------------

    @property
    def south(self):
        """
        :return: south y value rounded to nearest int
        """
        return int(round(self.y, 0)) + self.half - 1

    # ----------------------------------------

    @property
    def SE(self):
        """
        :return: southeast point: (x, y) rounded to nearest ints
        """
        return self.east, self.south

    # ----------------------------------------

    @property
    def SW(self):
        """
        :return: southwest point: (x, y) rounded to nearest ints
        """
        return self.west, self.south

    # ----------------------------------------

    @property
    def west(self):
        """
        :return: west x value rounded to nearest int
        """
        return int(round(self.x, 0)) - self.half

    # ----------------------------------------

    @property
    def xy(self):
        """
        :return: base point at center: (x, y) rounded to nearest ints
        """
        x = int(round(self.x, 0))
        y = int(round(self.y, 0))

        return x, y

    # ----------------------------------------
