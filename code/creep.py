"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense creep class
[E] ender.prime@gmail.com
[F] creep.py
[V] 02.14.17
"""

from bool import *
from const import *

# --------------------------------------------------------------------------------------------------------------------

class Creep(object):
    """
    killable enemy
    """

    def __init__(self, _id):

        self._id = _id          # unique int, assigned on spawn
        self._size = 48         # creep size in pixels
        self._half = 24         # half size in pixels

        self.ai = 0             # creep type
        self.angle = 0.0
        self.damage = 1         # mass lost if escaped
        self.description = ''
        self.energy = 1         # energy gained if killed
        self.goal = ()          # used in pathfinding
        self.index = ()
        self.mass = 1           # damage required to kill
        self.name = ''
        self.rank = 1           # creep level
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
        return self.x + self._half - 1

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
        :return: north y value
        """
        return self.y - self._half

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
        return self.y + self._half - 1

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
        return self.x - self._half

    # ----------------------------------------

    @property
    def xy(self):
        """
        :return: base point at center: (x, y)
        """

        return self.x, self.y

    # ----------------------------------------
