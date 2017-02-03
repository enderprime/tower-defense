"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense creeps class
[E] ender.prime@gmail.com
[F] creeps.py
[V] 02.03.17
"""

from bool import *
from const import *
from grid import *
from creep import *

import math
import random

# --------------------------------------------------------------------------------------------------------------------

class Creeps(object):
    """
    creep collection
    """
    WAVE = 30

    WAVES = \
        {
            1: [(1, 20)]
        }

    # ----------------------------------------

    def __init__(self):

        self._id = 0
        self.active = {}
        self.nextWave = Creeps.WAVE

    # ----------------------------------------

    def spawnCreep(self, ai, x, y):

        self._id = self._id + 1

        creep = Creep(self._id)
        creep.ai = ai
        creep.x = x
        creep.y = y

        if ai == 1:
            creep.image = IMG_CREEP_01
        if ai == 2:
            creep.image = IMG_CREEP_02
        if ai == 3:
            creep.image = IMG_CREEP_03
        if ai == 4:
            creep.image = IMG_CREEP_04
        if ai == 5:
            creep.image = IMG_CREEP_05
        if ai == 6:
            creep.image = IMG_CREEP_06
        if ai == 7:
            creep.image = IMG_CREEP_07
        if ai == 8:
            creep.image = IMG_CREEP_08
        if ai == 9:
            creep.image = IMG_CREEP_09
        if ai == 10:
            creep.image = IMG_CREEP_10
        if ai == 10:
            creep.image = IMG_CREEP_10
        if ai == 10:
            creep.image = IMG_CREEP_10
        if ai == 10:
            creep.image = IMG_CREEP_10
        if ai == 10:
            creep.image = IMG_CREEP_10
        if ai == 10:
            creep.image = IMG_CREEP_10

        self.active.update({self._id: creep})

    # ----------------------------------------

    def spawnWave(self, wave):



        self.nextWave = Creeps.WAVE
