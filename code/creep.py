"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense creep class
[E] ender.prime@gmail.com
[F] creep.py
[V] 03.05.17
"""

from boolean import *
from constant import *
from grid import *

import random

# --------------------------------------------------------------------------------------------------------------------

class Creep(object):
    """
    base class: killable enemy that traverses the grid
    """

    def __init__(self, _id):

        self._id = _id              # unique int, assigned on spawn
        self._size = 48             # creep size in pixels
        self._half = 24             # half size in pixels

        self.index = None
        self.x = 0.0
        self.y = 0.0

        self.ai = 0                 # creep type
        self.angle = 0.0
        self.damage = 1             # mass lost if escaped
        self.description = ''
        self.energy = 1             # energy gained if killed
        self.image = ''
        self.massCurrent = 1        # current health remaining
        self.massMax = 1            # total damage required to kill
        self.name = ''
        self.rank = 1               # creep level
        self.speedCurrent = 50      # pixels per second
        self.speedMax = 50
        self.target = None          # index of next cell to visit

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
    
    def move(self, grid, delta):
        """
        update creep location and target
        :param grid: current grid reference
        :param delta: game loop delta time in ms
        :return: none
        """
        distMove = max(1, self.speedCurrent) * delta / 1000

        if (self.x <= 0) or (self.x > Grid.XY_BASE_EAST):
            self.angle = 0.0
            self.x = self.x + distMove
        else:
            self.index = Grid.pointToIndex(self.xy)
            if not bool(self.target):
                self.target = grid[self.index].path
            xTarget, yTarget = grid.indexToPoint(self.target)
            a = xTarget - self.x
            b = self.y - yTarget
            self.angle = math.atan2(b, a)
            distTarget = math.hypot(a, b)

            if distMove < distTarget:
                x = distMove * math.cos(self.angle)
                y = distMove * math.sin(self.angle)
                self.x = self.x + x
                self.y = self.y - y
            else:
                self.x = xTarget
                self.y = yTarget
                distMove = distMove - distTarget
                self.index = Grid.pointToIndex(self.xy)
                self.target = grid[self.index].path
                xTarget, yTarget = grid.indexToPoint(self.target)
                a = xTarget - self.x
                b = self.y - yTarget
                self.angle = math.atan2(b, a)
                x = distMove * math.cos(self.angle)
                y = distMove * math.sin(self.angle)
                self.x = self.x + x
                self.y = self.y - y

    # ----------------------------------------

    def spawn(self, wave):
        """
        add creep to game
        :return: none
        """
        self.x = - random.randint(100, 800)
        self.y = random.randint(Grid.XY_NORTH + 100, Grid.XY_SOUTH - 100)

# --------------------------------------------------------------------------------------------------------------------

class CreepScout(Creep):
    """
    creep type 1
    """

    def __init__(self, _id):
        super(self.__class__, self).__init__(_id)

        self.image = PATH_IMG + 'creep-01.png'

    # ----------------------------------------

    def move(self, grid, delta):
        """
        update creep location and target
        :param grid: current grid reference
        :param delta: game loop delta time in ms
        :return: none
        """
        distMove = max(1, self.speedCurrent) * delta / 1000

        if (self.x <= 0) or (self.x > Grid.XY_BASE_EAST):
            self.angle = 0.0
            self.x = self.x + distMove
        else:
            self.index = Grid.pointToIndex(self.xy)
            self.target = grid[self.index].path
            xTarget, yTarget = grid.indexToPoint(self.target)
            a = xTarget - self.x
            b = self.y - yTarget
            self.angle = math.atan2(b, a)
            x = distMove * math.cos(self.angle)
            y = distMove * math.sin(self.angle)
            self.x = self.x + x
            self.y = self.y - y

    # ----------------------------------------

    def spawn(self, wave):
        """
        add creep to game
        :return: none
        """
        super(self.__class__, self).spawn(wave)

        self.rank = wave
        self.energy = (self.rank // 5) + 1
        self.massMax = (5 * self.rank) + 20
        self.massCurrent = self.massMax
