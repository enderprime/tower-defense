"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense creeps collection class
[E] ender.prime@gmail.com
[F] creeps.py
[V] 03.08.17
"""

from boolean import *
from constant import *
from creep import *

# --------------------------------------------------------------------------------------------------------------------

class Creeps(object):
    """
    collection of active creep objects
    """

    WAVE_MAX = 100
    WAVE_TIMER = 42     # cooldown in seconds between creep waves

    # creep waves: key = wave number, value = list of creep groups: [(creep ai, creep count)..]
    WAVES = \
        {
            0:   [(1, 20)],
            1:   [(1, 20)],
            2:   [(1, 20)],
            3:   [(1, 20)],
            4:   [(1, 20)],
            5:   [(1, 20)],
            6:   [(1, 20)],
            7:   [(1, 20)],
            8:   [(1, 20)],
            9:   [(1, 20)],
            10:  [(1, 20)],
            11:  [(1, 20)],
            12:  [(1, 20)],
            13:  [(1, 20)],
            14:  [(1, 20)],
            15:  [(1, 20)],
            16:  [(1, 20)],
            17:  [(1, 20)],
            18:  [(1, 20)],
            19:  [(1, 20)],
            20:  [(1, 20)],
            21:  [(1, 20)],
            22:  [(1, 20)],
            23:  [(1, 20)],
            24:  [(1, 20)],
            25:  [(1, 20)],
            26:  [(1, 20)],
            27:  [(1, 20)],
            28:  [(1, 20)],
            29:  [(1, 20)],
            30:  [(1, 20)],
            31:  [(1, 20)],
            32:  [(1, 20)],
            33:  [(1, 20)],
            34:  [(1, 20)],
            35:  [(1, 20)],
            36:  [(1, 20)],
            37:  [(1, 20)],
            38:  [(1, 20)],
            39:  [(1, 20)],
            40:  [(1, 20)],
            41:  [(1, 20)],
            42:  [(1, 20)],
            43:  [(1, 20)],
            44:  [(1, 20)],
            45:  [(1, 20)],
            46:  [(1, 20)],
            47:  [(1, 20)],
            48:  [(1, 20)],
            49:  [(1, 20)],
            50:  [(1, 20)],
            51:  [(1, 20)],
            52:  [(1, 20)],
            53:  [(1, 20)],
            54:  [(1, 20)],
            55:  [(1, 20)],
            56:  [(1, 20)],
            57:  [(1, 20)],
            58:  [(1, 20)],
            59:  [(1, 20)],
            60:  [(1, 20)],
            61:  [(1, 20)],
            62:  [(1, 20)],
            63:  [(1, 20)],
            64:  [(1, 20)],
            65:  [(1, 20)],
            66:  [(1, 20)],
            67:  [(1, 20)],
            68:  [(1, 20)],
            69:  [(1, 20)],
            70:  [(1, 20)],
            71:  [(1, 20)],
            72:  [(1, 20)],
            73:  [(1, 20)],
            74:  [(1, 20)],
            75:  [(1, 20)],
            76:  [(1, 20)],
            77:  [(1, 20)],
            78:  [(1, 20)],
            79:  [(1, 20)],
            80:  [(1, 20)],
            81:  [(1, 20)],
            82:  [(1, 20)],
            83:  [(1, 20)],
            84:  [(1, 20)],
            85:  [(1, 20)],
            86:  [(1, 20)],
            87:  [(1, 20)],
            88:  [(1, 20)],
            89:  [(1, 20)],
            90:  [(1, 20)],
            91:  [(1, 20)],
            92:  [(1, 20)],
            93:  [(1, 20)],
            94:  [(1, 20)],
            95:  [(1, 20)],
            96:  [(1, 20)],
            97:  [(1, 20)],
            98:  [(1, 20)],
            99:  [(1, 20)],
            100: [(1, 20)]
        }

    # ----------------------------------------

    def __init__(self):

        self._id = 0            # unique creep id

        self.active = {}        # active creeps: key = _id, value = creep object reference
        self.byIndex = {}

        self.wave = 0           # current creep wave
        self.waveTimer = 0      # countdown to next creep wave

    # ----------------------------------------

    @property
    def cleared(self):
        """
        :return: true if all creeps cleared from all waves
        """
        if (self.wave == Creeps.WAVE_MAX) and (not (bool(self.active))):
            return True
        else:
            return False

    # ----------------------------------------

    def remove(self, _id):
        pass

    # ----------------------------------------

    def reset(self):
        """
        reset creeps to new game conditions
        :return: none
        """
        self._id = 0

        self.active = {}
        self.byIndex = {}

        self.wave = 0
        self.waveTimer = 0

    # ----------------------------------------

    def spawnCreep(self, ai):
        """
        add creep to game
        :param ai: creep type
        :return: new creep object reference
        """
        self._id = self._id + 1

        if ai == 0:
            creep = CreepScout(self._id)
        else:
            creep = CreepScout(self._id)

        creep.spawn(self.wave)
        self.active.update({self._id: creep})

        return creep

    # ----------------------------------------

    def spawnWave(self):
        """
        add next creep wave to game
        :return: number of creeps spawned
        """
        spawned = 0
        if (self.wave + 1) <= Game.WAVE_MAX:
            if Game.DEBUG:
                self.wave = 0
            else:
                self.wave = self.wave + 1
            for creeps in Creeps.WAVES[self.wave]:
                ai, count = creeps
                for i in range(count):
                    self.spawnCreep(ai)
                spawned = spawned + count

            if self.wave != Creeps.WAVE_MAX:
                self.waveTimer = Creeps.WAVE_TIMER

        return spawned

    # ----------------------------------------

    def update(self):
        """
        update location and target for all active creeps
        :return: none
        """
        self.byIndex = {Grid.PATH_START: []}
        escaped = []
        killed = []

        if bool(self.active):
            for _id, creep in self.active.items():
                if creep.massCurrent <= 0:
                    removeCreeps.append(_id)
                    self.energy = self.energy + creep.energy
                    self.stats['CREEPS_KILLED'] = self.stats['CREEPS_KILLED'] + 1
                else:
                    if creep.x > (Grid.XY_EAST + creep._half):
                        removeCreeps.append(_id)
                        if not Game.DEBUG:
                            self.mass = self.mass - creep.damage
                        self.stats['CREEPS_ESCAPED'] = self.stats['CREEPS_ESCAPED'] + 1
                    else:
                        creep.move(self.grid, self.delta)
                        if bool(creep.index):
                            if creep.index in self.creepsByIndex:
                                self.creepsByIndex[creep.index].append(creep._id)
                            else:
                                self.creepsByIndex.update({creep.index: [creep._id]})

            for n in removeCreeps:
                del self.creeps[n]
