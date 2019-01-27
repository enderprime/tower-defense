"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense towers collection class
[E] ender.prime@gmail.com
[F] towers.py
[V] 03.08.17
"""

from boolean import *
from constant import *
from tower import *

# --------------------------------------------------------------------------------------------------------------------

class Towers(object):
    """
    collection of active tower objects
    """

    # tower stats: key = (ai, rank), value = (cooldown, damage, energy, range, splash damage, splash range)
    STATS = \
        {
            (0, 1): (0, 0, 5, 0, 0, 0),
            (1, 1): (333, 5, 10, 2, 0, 0),
            (2, 1): (1000, 10, 253, 5, 2),
            (3, 1): (500, 20, 50, 2, 10, 1),
            (4, 1): (0, 0, 50, 1, 0, 0),
            (5, 1): (333, 25, 50, 2, 12, 1),
            (6, 1): (4000, 50, 100, 0, 0, 0),
            (7, 1): (1000, 50, 100, 1, 0, 0),
            (8, 1): (0, 0, 50, 0, 0, 0)
        }

    # ----------------------------------------

    def __init__(self):

        self._id = 0        # unique tower id
        self.active = {}    # active towers: key = _id, value = tower object reference

    # ----------------------------------------
    
    @classmethod
    def getCooldown(cls, ai, rank):
        return Towers.STATS[(ai, rank)][0]
    
    # ----------------------------------------
    
    @classmethod
    def getDamage(cls, ai, rank):
        return Towers.STATS[(ai, rank)][1]
    
    # ----------------------------------------
    
    @classmethod
    def getEnergy(cls, ai, rank):
        return Towers.STATS[(ai, rank)][2]
    
    # ----------------------------------------
    
    @classmethod
    def getRange(cls, ai, rank):
        return Towers.STATS[(ai, rank)][3]
    
    # ----------------------------------------
    
    @classmethod
    def getSplashDamage(cls, ai, rank):
        return Towers.STATS[(ai, rank)][4]
    
    # ----------------------------------------
    
    @classmethod
    def getSplashRange(cls, ai, rank):
        return Towers.STATS[(ai, rank)][5]
    
    # ----------------------------------------

    def reset(self):
        """
        reset towers to new game conditions
        :return: none
        """
        self._id = 0
        self.active = {}

    # ----------------------------------------

    def spawn(self, grid, ai, index):
        """
        add tower to game
        :param grid: current game grid
        :param ai: tower type
        :param index: (column, row)
        :return: new tower object reference
        """
        self._id = self._id + 1

        if ai == 0:     tower = TowerBase(self._id)
        elif ai == 1:   tower = TowerGun(self._id)
        elif ai == 2:   tower = TowerCannon(self._id)
        elif ai == 3:   tower = TowerMissle(self._id)
        elif ai == 4:   tower = TowerSlow(self._id)
        elif ai == 5:   tower = TowerLaser(self._id)
        elif ai == 6:   tower = TowerRail(self._id)
        elif ai == 7:   tower = TowerBash(self._id)
        elif ai == 8:   tower = TowerSupport(self._id)
        else:           tower = TowerBase(self._id)

        col, row = index
        point = grid.indexToPoint(index)
        tower.spawn(index, point)

        cell = grid.cells[col][row]
        cell.build = tower
        cell.pathable = False
        cell.path = None

        self.active.update({self._id: tower})
        self.stats['TOWERS_BUILT'] = self.stats['TOWERS_BUILT'] + 1

        return tower

    # ----------------------------------------

    def update(self):
        """
        update target tracking for all towers, and fire if cooldown is up
        :return: none
        """
        if bool(self.towers):
            for _id, tower in self.towers.items():
                if tower.ai > 0:
                    tower.track(self.creeps, self.creepsByIndex)
                    tower.cooldownLeft = tower.cooldownLeft - self.delta
                    if tower.cooldownLeft <= 0:
                        tower.fire()
                        tower.cooldownLeft = tower.cooldown
