"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense game class
[E] ender.prime@gmail.com
[F] game.py
[V] 02.03.17
"""

from bool import *
from const import *
from creeps import *
from grid import *
from towers import *

import math
import pygame
from pygame.locals import *
import sys

# --------------------------------------------------------------------------------------------------------------------

class Game(object):
    """
    core game logic
    """
    FPS = 30
    HEADER = 56
    FOOTER = 72
    SIDEBAR = 200

    COLORS = \
        {
            'CELL_BLOCK':  (128, 36, 36),       # red
            'CELL_BUILD':  (32, 64, 128),       # blue
            'CELL_HOVER':  (255, 255, 255),     # white
            'CELL_OPEN':   (51, 102, 51),       # green
            'FOOT_BG':     (0, 0, 0),           # black
            'FOOT_BODY':   (255, 255, 255),     # white
            'FOOT_HEAD':   (255, 255, 255),     # white
            'GRID_BASE':   (255, 255, 255),     # white
            'GRID_BG':     (0, 0, 0),           # black
            'GRID_BODY':   (255, 255, 255),     # white
            'GRID_GRID':   (24, 24, 24),        # grey
            'GRID_HEAD':   (255, 255, 255),     # white
            'GRID_PATH':   (204, 102, 0),       # orange
            'HEAD_BG':     (0, 0, 0),           # black
            'HEAD_BODY':   (255, 255, 255),     # white
            'HEAD_HEAD':   (255, 255, 255),     # white
            'RANK_2':      (51, 102, 51),       # green
            'RANK_3':      (32, 64, 128),       # blue
            'RANK_4':      (102, 0, 102),       # purple
            'RANK_5':      (128, 36, 36),       # red
            'SIDE_BG':     (0, 0, 0),           # black
            'SIDE_BODY':   (255, 255, 255),     # white
            'SIDE_HEAD':   (255, 255, 255),     # white
        }

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

            IMG_PAUSE: pygame.image.load(IMG_PAUSE),
            IMG_PLAY: pygame.image.load(IMG_PLAY),

            IMG_TOWER_0: pygame.image.load(IMG_TOWER_0),
            IMG_TOWER_1_1: pygame.image.load(IMG_TOWER_1_1),
            IMG_TOWER_2_1: pygame.image.load(IMG_TOWER_2_1),
            IMG_TOWER_3_1: pygame.image.load(IMG_TOWER_3_1),
            IMG_TOWER_4_1: pygame.image.load(IMG_TOWER_4_1),
            IMG_TOWER_5_1: pygame.image.load(IMG_TOWER_5_1),
            IMG_TOWER_6_1: pygame.image.load(IMG_TOWER_6_1),
            IMG_TOWER_7_1: pygame.image.load(IMG_TOWER_7_1),
            IMG_TOWER_8_1: pygame.image.load(IMG_TOWER_8_1),
            IMG_TOWER_9: pygame.image.load(IMG_TOWER_9),
        }

    # ----------------------------------------

    def __init__(self):

        self.clock = pygame.time.Clock()
        self.creeps = Creeps()
        self.debug = True
        self.grid = Grid(0, Game.HEADER)
        self.mouse = (0, 0)
        self.showGrid = False
        self.showPath = True
        self.towers = Towers()


        pygame.display.set_icon(Game.IMAGES[IMG_ICON])
        self.window = pygame.display.set_mode((Game.width(), Game.height()))
        pygame.display.set_caption('TOWER DEFENSE')
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
        
        self.building = None
        self.energy = 100
        self.mass = 20
        self.pause = True
        self.select = None
        self.speed = 100
        self.time = 0
        self.wave = 1

    # ----------------------------------------

    @classmethod
    def height(cls):
        """
        :return: height in pixels
        """
        return Game.HEADER + Grid.height() + Game.FOOTER

    # ----------------------------------------

    @classmethod
    def width(cls):
        """
        :return: width in pixels
        """
        return Grid.width() + Game.SIDEBAR

    # ----------------------------------------

    @property
    def btnPlay(self):
        """
        :return: play button bounding box points ((west, north), (east, south))
        """
        x = self.grid.width() + (Game.SIDEBAR // 2) - 12
        y = (Game.HEADER // 2) - 12

        return (x, y), (x + 23, y + 23)

    # ----------------------------------------

    @property
    def fonts(self):
        """
        :return: dictionary of fonts
        """
        return \
            {
                'FOOT_BODY': pygame.font.SysFont('lucida console', 20),
                'FOOT_HEAD': pygame.font.SysFont('lucida console', 28),
                'GRID_BODY': pygame.font.SysFont('lucida console', 20),
                'GRID_HEAD': pygame.font.SysFont('lucida console', 28),
                'HEAD_BODY': pygame.font.SysFont('lucida console', 20),
                'HEAD_HEAD': pygame.font.SysFont('lucida console', 28),
                'SIDE_BODY': pygame.font.SysFont('lucida console', 20),
                'SIDE_HEAD': pygame.font.SysFont('lucida console', 28)
            }

    # ----------------------------------------

    def drawGrid(self):
        """
        draw main game area on screen
        :return: none
        """

        # background
        color = Game.COLORS['GRID_BG']
        rect = pygame.Rect(self.grid.x, self.grid.y, Grid.width(), Grid.height())
        self.window.fill(color, rect)

        # grid lines
        color = Game.COLORS['GRID_GRID']
        if self.showGrid:
            for n in self.grid.base:
                cell = self.grid[n]
                if cell.open:
                    rect = (cell.west, cell.north, Cell.DIM, Cell.DIM)
                    pygame.draw.rect(self.window, color, rect, 1)

        # hover
        index = self.grid.pointToIndex(self.mouse)
        if self.grid.indexIsValid(index):
            cell = self.grid[index]
            if cell.base:
                if notNull(self.building):
                    self.select = None
                    if isNull(cell.build) and cell.open:
                        color = Game.COLORS['CELL_OPEN']
                        rect = pygame.Rect(cell.west + 2, cell.north + 2, Cell.DIM - 4, Cell.DIM - 4)
                    else:
                        color = Game.COLORS['CELL_BLOCK']
                        rect = pygame.Rect(cell.west, cell.north, Cell.DIM, Cell.DIM)
                    self.window.fill(color, rect)

        # selected
        if notNull(self.select):
            cell = self.grid[self.select]
            color = Game.COLORS['CELL_BUILD']
            rect = pygame.Rect(cell.west, cell.north, Cell.DIM, Cell.DIM)
            self.window.fill(color, rect)

        # base border
        color = Game.COLORS['GRID_BASE']
        c1, c2 = Grid.baseBounds()
        west, north = self.grid[c1].NW
        east, south = self.grid[c2].SE
        east = east + 3
        north = north - 4
        south = south + 3
        west = west - 4
        pygame.draw.line(self.window, color, (west, north), (east, north), 2)
        pygame.draw.line(self.window, color, (west, south), (east, south), 2)
        pygame.draw.line(self.window, color, (west, north), (west, north + 11), 2)
        pygame.draw.line(self.window, color, (east, north), (east, north + 11), 2)
        pygame.draw.line(self.window, color, (west, south), (west, south - 11), 2)
        pygame.draw.line(self.window, color, (east, south), (east, south - 11), 2)

        # creep path
        if self.showPath:
            color = Game.COLORS['GRID_PATH']
            for index in self.grid.path:
                p = self.grid[index].xy
                pygame.draw.circle(self.window, color, p, 3)

        # towers
        if bool(self.towers.active):
            for _id, tower in self.towers.active.items():
                x, y = self.grid[tower.index].NW
                rect = pygame.Rect(x, y, Cell.DIM, Cell.DIM)
                img = Game.IMAGES[tower.imgTower]
                if not (tower.angle == 0):
                    img = pygame.transform.rotate(img, math.degrees(tower.angle))
                self.window.blit(img, rect)

        # creeps

    # ----------------------------------------

    def drawHeader(self):
        """
        draw interface header on screen
        :return: none
        """
        color = Game.COLORS['HEAD_BG']
        rect = pygame.Rect(0, 0, Game.width(), Game.HEADER)
        self.window.fill(color, rect)

        # mass
        if self.mass < 10:
            img = PATH_IMG + 'mass-0' + str(self.mass) + '.png'
        else:
            img = PATH_IMG + 'mass-' + str(self.mass) + '.png'

        xCenter, yCenter = self.grid.center
        x = xCenter - 141
        y = (Game.HEADER // 2) - 14
        rect = pygame.Rect(x, y, 282, 28)
        self.window.blit(Game.IMAGES[img], rect)

        ####

    # ----------------------------------------

    def drawFooter(self):
        """
        draw interface footer on screen
        :return: none
        """
        color = Game.COLORS['FOOT_BG']
        rect = pygame.Rect(0, Game.HEADER + Grid.height(), Game.width(), Game.FOOTER)
        self.window.fill(color, rect)

        ####

    # ----------------------------------------

    def drawSidebar(self):
        """
        draw interface sidebar on screen
        :return: none
        """
        color = Game.COLORS['SIDE_BG']
        rect = pygame.Rect(Grid.width(), 0, Game.SIDEBAR, Game.height())
        self.window.fill(color, rect)

        # play button
        if self.pause:
            img = Game.IMAGES[IMG_PLAY]
        else:
            img = Game.IMAGES[IMG_PAUSE]
        nw, se = self.btnPlay
        x1, y1 = nw
        x2, y2 = se
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.window.blit(img, rect)

        # debug info
        if self.debug:
            color = self.COLORS['SIDE_BODY']
            font = self.fonts['SIDE_BODY']

            x = self.width() - 80
            y = self.height() - 30
            p = (x, y)
            text = font.render('FPS', True, color)
            self.window.blit(text, p)

            x = x + 40
            p = (x, y)
            text = font.render(str(int(self.clock.get_fps())), True, color)
            self.window.blit(text, p)
        
    # ----------------------------------------

    def eventClick(self, point, button):
        """
        event handling for mouse clicks
        :param point: mouse (x, y) from pygame event loop
        :param button: mouse button from pygame event loop
        :return: none
        """
        if button == 1:
            index = self.grid.pointToIndex(point)
            if self.grid.indexIsValid(index):
                cell = self.grid[index]
                if cell.base:
                    if notNull(self.building) and isNull(cell.build) and cell.open:
                        col, row = index
                        self.towers.build(self.building, col, row)      # NTS: update with valid path logic
                        cell.build = self.building
                        if not (self.building == 9):
                            cell.open = False
                    elif notNull(cell.build) and (not cell.open):
                        self.select = index
        elif button == 3:
            if notNull(self.building): self.building = None
            if notNull(self.select): self.select = None

    # ----------------------------------------

    def eventKey(self, key):
        """
        event handling for keyboard
        :param key: keyboard input from pygame event loop
        :return: none
        """
        if key == K_ESCAPE:
            if notNull(self.building): self.building = None
            if notNull(self.select): self.select = None
        elif key == K_SPACE: self.pause = not self.pause
        elif key == K_0:
            if self.debug: self.building = 0
        elif key == K_1: self.building = 1
        elif key == K_2: self.building = 2
        elif key == K_3: self.building = 3
        elif key == K_4: self.building = 4
        elif key == K_5: self.building = 5
        elif key == K_6: self.building = 6
        elif key == K_7: self.building = 7
        elif key == K_8: self.building = 8
        elif key == K_9: self.building = 9
        elif key == K_g: self.showGrid = not self.showGrid
        elif key == K_p: self.showPath = not self.showPath

    # ----------------------------------------

    def end(self):
        """
        game over logic
        :return: none
        """

        ####

        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    # ----------------------------------------

    def loop(self):
        """
        main game loop
        :return: none
        """
        new = False
        quit = False
        run = True

        while run:
            if self.mass < 1:
                run = False
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit = True
                        run = False
                    elif event.type == KEYUP:
                        self.eventKey(event.key)
                    elif event.type == MOUSEBUTTONUP:
                        self.eventClick(event.pos, event.button)
                    elif event.type == MOUSEMOTION:
                        self.mouse = event.pos
                    elif event.type == USEREVENT + 1:
                        self.time = self.time + 1

            self.drawGrid()
            self.drawHeader()
            self.drawFooter()
            self.drawSidebar()

            if not self.pause:
                pass

                # towers

                # creeps

            pygame.display.update()
            self.clock.tick(Game.FPS)

        if quit:
            pygame.quit()
            sys.exit()
        elif new:
            self.new()
        else:
            self.end()

    # ----------------------------------------

    def new(self):
        """
        new game logic
        :return: none
        """

        self.building = None
        self.energy = 100
        self.grid.reset()
        self.mass = 20
        self.pause = True
        self.select = None
        self.speed = 100
        self.time = 0
        self.wave = 1

        self.loop()
