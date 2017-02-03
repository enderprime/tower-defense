"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense creep class
[E] ender.prime@gmail.com
[F] creep.py
[V] 02.03.17
"""

from bool import *
from const import *

# --------------------------------------------------------------------------------------------------------------------

class Creep(object):
    """
    killable enemy
    """
    def __init__(self, _id):

        # _id == unique int, assigned from collection
        self._id = _id

        self.ai = 0
        self.angle = 0
        self.damage = 0
        self.energy = 0
        self.image = ''
        self.mass = 0
        self.rank = 0
        self.size = 16
        self.speed = 100
        self.target = (0, 0)
        self.x = 0
        self.y = 0

    # ----------------------------------------

    @property
    def xy(self):
        """
        :return: base point at center: (x, y)
        """
        return self.x, self.y

    # ----------------------------------------
