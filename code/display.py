"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense cell class
[E] ender.prime@gmail.com
[F] display.py
[V] 02.19.17
"""

from boolean import *
from constant import *
from grid import *

import math
import pygame
from pygame.locals import *

# --------------------------------------------------------------------------------------------------------------------

class Display(object):
    """
    pygame display
    """

    HEADER = 84         # pixels
    FOOTER = 133        # pixels
    SIDEBAR = 250       # pixels

    WIDTH = Grid.WIDTH + SIDEBAR                # width in pixels
    HEIGHT = HEADER + Grid.HEIGHT + FOOTER      # height in pixels

    # new game button bounds
    BTN_NEW_X = WIDTH - (SIDEBAR // 2) - 64
    BTN_NEW_Y = (HEADER // 2) - 22
    BTN_NEW = (BTN_NEW_X, BTN_NEW_Y, BTN_NEW_X + 128, BTN_NEW_Y + 36)

    # next button bounds
    BTN_NEXT_X = 1100
    BTN_NEXT_Y = (HEADER // 2) - 18
    BTN_NEXT = (BTN_NEXT_X, BTN_NEXT_Y, BTN_NEXT_X + 27, BTN_NEXT_Y + 27)

    # play button bounds
    BTN_PLAY_X = 1050
    BTN_PLAY_Y = (HEADER // 2) - 18
    BTN_PLAY = (BTN_PLAY_X, BTN_PLAY_Y, BTN_PLAY_X + 27, BTN_PLAY_Y + 27)

    COLOR_BLACK =   (0, 0, 0)
    COLOR_BLUE =    (32, 64, 128)
    COLOR_GREEN =   (51, 102, 51)
    COLOR_GREY_1 =  (24, 24, 24)
    COLOR_GREY_2 =  (36, 36, 36)
    COLOR_ORANGE =  (204, 102, 0)
    COLOR_PURPLE =  (102, 0, 102)
    COLOR_RED =     (128, 28, 28)
    COLOR_WHITE =   (255, 255, 255)

    IMAGES = \
        {
            IMG_CREEP_01: pygame.image.load(IMG_CREEP_01),

            IMG_EFFECT_01: pygame.image.load(IMG_EFFECT_01),
            IMG_EFFECT_02: pygame.image.load(IMG_EFFECT_02),
            IMG_EFFECT_03: pygame.image.load(IMG_EFFECT_03),
            IMG_EFFECT_04: pygame.image.load(IMG_EFFECT_04),
            IMG_EFFECT_05: pygame.image.load(IMG_EFFECT_05),
            IMG_EFFECT_06: pygame.image.load(IMG_EFFECT_06),

            IMG_ICON: pygame.image.load(IMG_ICON),

            IMG_MASS_00: pygame.image.load(IMG_MASS_00),
            IMG_MASS_01: pygame.image.load(IMG_MASS_01),
            IMG_MASS_02: pygame.image.load(IMG_MASS_02),
            IMG_MASS_03: pygame.image.load(IMG_MASS_03),
            IMG_MASS_04: pygame.image.load(IMG_MASS_04),
            IMG_MASS_05: pygame.image.load(IMG_MASS_05),
            IMG_MASS_06: pygame.image.load(IMG_MASS_06),
            IMG_MASS_07: pygame.image.load(IMG_MASS_07),
            IMG_MASS_08: pygame.image.load(IMG_MASS_08),
            IMG_MASS_09: pygame.image.load(IMG_MASS_09),
            IMG_MASS_10: pygame.image.load(IMG_MASS_10),
            IMG_MASS_11: pygame.image.load(IMG_MASS_11),
            IMG_MASS_12: pygame.image.load(IMG_MASS_12),
            IMG_MASS_13: pygame.image.load(IMG_MASS_13),
            IMG_MASS_14: pygame.image.load(IMG_MASS_14),
            IMG_MASS_15: pygame.image.load(IMG_MASS_15),
            IMG_MASS_16: pygame.image.load(IMG_MASS_16),
            IMG_MASS_17: pygame.image.load(IMG_MASS_17),
            IMG_MASS_18: pygame.image.load(IMG_MASS_18),
            IMG_MASS_19: pygame.image.load(IMG_MASS_19),
            IMG_MASS_20: pygame.image.load(IMG_MASS_20),

            IMG_NEW: pygame.image.load(IMG_NEW),
            IMG_NEXT_ACTIVE: pygame.image.load(IMG_NEXT_ACTIVE),
            IMG_NEXT_INACTIVE: pygame.image.load(IMG_NEXT_INACTIVE),
            IMG_PATH: pygame.image.load(IMG_PATH),
            IMG_PAUSE: pygame.image.load(IMG_PAUSE),
            IMG_PLAY: pygame.image.load(IMG_PLAY),
            IMG_SPEED_FAST: pygame.image.load(IMG_SPEED_FAST),
            IMG_SPEED_SLOW: pygame.image.load(IMG_SPEED_SLOW),

            IMG_TOWER_1_1: pygame.image.load(IMG_TOWER_1_1),
            IMG_TOWER_2_1: pygame.image.load(IMG_TOWER_2_1),
            IMG_TOWER_3_1: pygame.image.load(IMG_TOWER_3_1),
            IMG_TOWER_4_1: pygame.image.load(IMG_TOWER_4_1),
            IMG_TOWER_5_1: pygame.image.load(IMG_TOWER_5_1),
            IMG_TOWER_6_1: pygame.image.load(IMG_TOWER_6_1),
            IMG_TOWER_7_1: pygame.image.load(IMG_TOWER_7_1),
            IMG_TOWER_8: pygame.image.load(IMG_TOWER_8),
            IMG_TOWER_BASE: pygame.image.load(IMG_TOWER_BASE)
        }

    # ----------------------------------------

    def __init__(self):

        # font dictionary
        self._fonts = \
            {
                'LUCID_16': pygame.font.SysFont('lucida console', 16),
                'LUCID_20': pygame.font.SysFont('lucida console', 20),
                'LUCID_24': pygame.font.SysFont('lucida console', 24)
            }

        # static text dictionary
        self._text = \
            {
                'ENERGY':   self._fonts['LUCID_20'].render('ENERGY', True, Display.COLOR_WHITE),
                'MASS':     self._fonts['LUCID_20'].render('MASS', True, Display.COLOR_WHITE),
                'NEXT':     self._fonts['LUCID_20'].render('NEXT', True, Display.COLOR_WHITE),
                'TICK':     self._fonts['LUCID_20'].render('TICK', True, Display.COLOR_WHITE),
                'WAVE':     self._fonts['LUCID_20'].render('WAVE', True, Display.COLOR_WHITE)
            }

        self.mouse = (0, 0)

        pygame.display.set_icon(Display.IMAGES[IMG_ICON])
        self.window = pygame.display.set_mode((Display.WIDTH, Display.HEIGHT))
        pygame.display.set_caption('TOWER DEFENSE')

    # ----------------------------------------

    @classmethod
    def imgRotate(cls, img, angle):
        """
        rotate image around center
        :param img: image string
        :param angle: angle in radians
        :return: rotated image
        """
        img = Display.IMAGES[img]
        imgRect = img.get_rect()

        rotated = pygame.transform.rotate(img, math.degrees(angle))
        rotatedRect = imgRect.copy()
        rotatedRect.center = rotated.get_rect().center
        rotated = rotated.subsurface(rotatedRect).copy()

        return rotated