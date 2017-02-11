"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense game class
[E] ender.prime@gmail.com
[F] game.py
[V] 02.10.17
"""

from bool import *
from const import *
from creep import *
from grid import *
from tower import *

import math
import pygame
from pygame.locals import *
import random
import sys

# --------------------------------------------------------------------------------------------------------------------

class Game(object):
    """
    core game logic
    """
    FPS = 25            # frames per second
    TICK = 1000 // 25   # time in ms per game loop

    HEADER = 84         # pixels
    FOOTER = 133        # pixels
    SIDEBAR = 250       # pixels

    WAVE_MAX = 100
    WAVE_TIMER = 30     # seconds

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

            IMG_NEXT: pygame.image.load(IMG_NEXT),
            IMG_PAUSE: pygame.image.load(IMG_PAUSE),
            IMG_PLAY: pygame.image.load(IMG_PLAY),
            IMG_SPEED_FAST: pygame.image.load(IMG_SPEED_FAST),
            IMG_SPEED_SLOW: pygame.image.load(IMG_SPEED_SLOW),

            IMG_TOWER_0: pygame.image.load(IMG_TOWER_0),
            IMG_TOWER_1_1: pygame.image.load(IMG_TOWER_1_1),
            IMG_TOWER_2_1: pygame.image.load(IMG_TOWER_2_1),
            IMG_TOWER_3_1: pygame.image.load(IMG_TOWER_3_1),
            IMG_TOWER_4_1: pygame.image.load(IMG_TOWER_4_1),
            IMG_TOWER_5_1: pygame.image.load(IMG_TOWER_5_1),
            IMG_TOWER_6_1: pygame.image.load(IMG_TOWER_6_1),
            IMG_TOWER_7_1: pygame.image.load(IMG_TOWER_7_1),
            IMG_TOWER_8_1: pygame.image.load(IMG_TOWER_8_1),
            # IMG_TOWER_9: pygame.image.load(IMG_TOWER_9),
        }

    WAVES = \
        {
            0: [(1, 20)],   # wave number: list of (creep ai, creep count)
            1: [(1, 20)]
        }

    # ----------------------------------------

    def __init__(self):

        self.debug = True

        self.clock = pygame.time.Clock()
        self.grid = Grid(0, Game.HEADER)
        self.mouse = (0, 0)
        self.showGrid = False
        self.showPath = True

        pygame.display.set_icon(Game.IMAGES[IMG_ICON])
        self.window = pygame.display.set_mode((Game.width(), Game.height()))
        pygame.display.set_caption('TOWER DEFENSE')
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

        self._idCreep = 0           # creep id int, increments by 1 for every creep spawn
        self._idTower = 0           # tower id int, increments by 1 for every tower spawn

        self.building = None        # if player is in build mode, holds tower type (0-9)
        self.creeps = {}            # dictionary of active creeps in game
        self.delta = 0              # time in ms of last game loop
        self.energy = 100           # main player resource used to buy towers and upgrades
        self.mass = 20              # player health, game over if this reaches zero
        self.pause = True
        self.select = None          # index of selected cell (cell clicked while hovering)
        self.tick = 0               # time in ms of last clock tick

        self.statCreepsEscaped = 0
        self.statCreepsKilled = 0
        self.statCreepsSpawned = 0
        self.statTowersBuilt = 0
        self.statTowersSold = 0

        self.time = 0               # running count from start of new game, only increases
        self.towers = {}            # dictionary of active towers in game
        self.wave = 0               # current creep wave, increments on spawnWave()
        self.waveTimer = 0          # countdown to next creep wave, resets to WAVE_TIMER on spawnWave()

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
    def btnNext(self):
        """
        :return: next button bounding box points (west, north, east, south)
        """
        x = 1100
        y = (Game.HEADER // 2) - 18

        return x, y, x + 27, y + 27

    # ----------------------------------------

    @property
    def btnPlay(self):
        """
        :return: play button bounding box points (west, north, east, south)
        """
        x = 1050
        y = (Game.HEADER // 2) - 18

        return x, y, x + 27, y + 27

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

    @property
    def creepsCleared(self):
        """
        :return: true if all creeps cleared from all waves
        """
        if (self.wave == Game.WAVE_MAX) and (not (bool(self.creeps))):
            return True
        else:
            return False

    # ----------------------------------------

    def creepsAtIndex(self, index):
        """
        :param index: (column, row)
        :return: list of creeps ids at index
        """
        creeps = []

        if bool(self.creeps):
            for _id, creep in self.creeps.items():
                if creep.index == index:
                    creeps.append(creep._id)

        return creeps

    # ----------------------------------------

    def creepsByIndex(self):
        """
        :return: dict: key = index, value = list of creep ids at key index
        """
        indexes = {}

        if bool(self.creeps):
            for _id, creep in self.creeps.items():
                if creep.index in indexes:
                    indexes[index] = indexes[index].append(creep._id)
                else:
                    indexes.update({creep.index: [creep._id]})

        return indexes

    # ----------------------------------------

    def drawHeader(self):
        """
        draw interface header on screen
        :return: none
        """
        color = Game.COLORS['HEAD_BG']
        rect = pygame.Rect(0, 0, Game.width(), Game.HEADER)
        self.window.fill(color, rect)

        color = self.COLORS['HEAD_BODY']
        font = self.fonts['HEAD_BODY']

        # mass
        x = 160
        y = (Game.HEADER // 2) - 14
        p = (x, y)
        text = font.render('MASS', True, color)
        self.window.blit(text, p)

        if self.mass < 10:
            img = PATH_IMG + 'mass-0' + str(self.mass) + '.png'
        else:
            img = PATH_IMG + 'mass-' + str(self.mass) + '.png'

        x = x + 60
        y = (Game.HEADER // 2) - 18
        rect = pygame.Rect(x, y, 282, 28)
        self.window.blit(Game.IMAGES[img], rect)

        # energy
        x = x + 330
        y = (Game.HEADER // 2) - 14
        p = (x, y)
        text = font.render('ENERGY', True, color)
        self.window.blit(text, p)

        x = x + 90
        p = (x, y)
        text = font.render(str(self.energy), True, color)
        self.window.blit(text, p)

        # wave
        x = x + 100
        p = (x, y)
        text = font.render('WAVE', True, color)
        self.window.blit(text, p)

        x = x + 70
        p = (x, y)
        if self.wave == 0:
            text = font.render('--', True, color)
        else:
            text = font.render(str(self.wave), True, color)
        self.window.blit(text, p)

        # wave timer
        x = x + 90
        p = (x, y)
        text = font.render('NEXT', True, color)
        self.window.blit(text, p)

        x = x + 70
        p = (x, y)
        if self.waveTimer == 0:
            text = font.render('--', True, color)
        else:
            text = font.render(str(int(self.waveTimer)), True, color)
        self.window.blit(text, p)

        # play button
        if self.pause:
            img = Game.IMAGES[IMG_PLAY]
        else:
            img = Game.IMAGES[IMG_PAUSE]

        x1, y1, x2, y2 = self.btnPlay
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.window.blit(img, rect)

        # next button
        img = Game.IMAGES[IMG_NEXT]
        x1, y1, x2, y2 = self.btnNext
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.window.blit(img, rect)

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
            for lst in self.grid.cells:
                for cell in lst:
                    if cell.base and cell.open:
                        rect = (cell.west, cell.north, Cell.DIM, Cell.DIM)
                        pygame.draw.rect(self.window, color, rect, 1)

        # hover
        if self.grid.pointIsValid(self.mouse):
            index = self.grid.pointToIndex(self.mouse)
            if bool(index):
                cell = self.grid[index]
                if cell.base:
                    if notNull(self.building):
                        self.select = None
                        if (not cell.path) and cell.open:
                            color = Game.COLORS['CELL_OPEN']
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
        west, north, east, south = Grid.baseBounds()
        west, north = self.grid.cells[west][north].NW
        east, south = self.grid.cells[east][south].SE
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

        # path
        if self.showPath:
            color = Game.COLORS['GRID_PATH']
            for index in self.grid.path:
                p = self.grid[index].xy
                pygame.draw.circle(self.window, color, p, 3)

        # towers
        if bool(self.towers):
            for _id, tower in self.towers.items():
                x, y = self.grid[tower.index].NW
                rect = pygame.Rect(x, y, Cell.DIM, Cell.DIM)
                img = Game.IMAGES[tower.imgTower]
                if not (tower.angle == 0):
                    img = pygame.transform.rotate(img, math.degrees(tower.angle))
                self.window.blit(img, rect)

        # creeps
        if bool(self.creeps):
            for _id, creep in self.creeps.items():
                x, y = creep.NW
                rect = pygame.Rect(x, y, creep.size, creep.size)
                img = Game.IMAGES[creep.image]
                if not (creep.angle == 0):
                    img = pygame.transform.rotate(img, math.degrees(creep.angle))
                self.window.blit(img, rect)

    # ----------------------------------------

    def drawSidebar(self):
        """
        draw interface sidebar on screen
        :return: none
        """
        color = Game.COLORS['SIDE_BG']
        rect = pygame.Rect(Grid.width(), 0, Game.SIDEBAR, Game.height())
        self.window.fill(color, rect)

        ####

        # debug info
        if self.debug:
            color = self.COLORS['SIDE_BODY']
            font = self.fonts['SIDE_BODY']
            x = self.width() - 130
            y = self.height() - 30
            p = (x, y)
            text = font.render('TICK', True, color)
            self.window.blit(text, p)

            x = x + 70
            p = (x, y)
            if self.tick < Game.TICK:
                color = self.COLORS['RANK_2']
            else:
                color = self.COLORS['RANK_5']
            text = font.render(str(self.tick), True, color)
            self.window.blit(text, p)

    # ----------------------------------------

    def eventClick(self, point, button):
        """
        event handling for mouse clicks
        :param point: mouse (x, y) from pygame event loop
        :param button: mouse button from pygame event loop
        :return: none
        """
        x, y = point

        if button == 1:
            index = self.grid.pointToIndex(point)
            if bool(index):
                cell = self.grid[index]
                if cell.base:
                    if notNull(self.building) and (cell.open or (cell.build == 0)):
                        col, row = index
                        self.spawnTower(self.building, col, row)      # NTS: update with valid path logic
                        cell.build = self.building
                        cell.open = False
                        self.grid.pathMain()
                    elif notNull(cell.build):
                        self.select = index
            else:
                playWest, playNorth, playEast, playSouth = self.btnPlay
                if (playWest <= x <= playEast) and (playNorth <= y <= playSouth):
                    self.pause = not self.pause

                nextWest, nextNorth, nextEast, nextSouth = self.btnNext
                if (nextWest <= x <= nextEast) and (nextNorth <= y <= nextSouth):
                    self.spawnWave()

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
        elif key == K_0: self.building = 0
        elif key == K_1: self.building = 1
        elif key == K_2: self.building = 2
        elif key == K_3: self.building = 3
        elif key == K_4: self.building = 4
        elif key == K_5: self.building = 5
        elif key == K_6: self.building = 6
        elif key == K_7: self.building = 7
        elif key == K_8: self.building = 8
        elif key == K_g: self.showGrid = not self.showGrid
        elif key == K_n: self.spawnWave()
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
        while True:

            if (self.mass < 1) or self.creepsCleared:
                break

            if not self.pause:
                self.updateCreeps()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP:
                    self.eventKey(event.key)
                elif event.type == MOUSEBUTTONUP:
                    self.eventClick(event.pos, event.button)
                elif event.type == MOUSEMOTION:
                    self.mouse = event.pos
                elif event.type == USEREVENT + 1:
                    self.time = self.time + 1
                    if not self.pause:
                        self.waveTimer = self.waveTimer - 1
                        if self.waveTimer < 1:
                            self.spawnWave()

            self.drawHeader()
            self.drawFooter()
            self.drawGrid()
            self.drawSidebar()

            pygame.display.update()
            self.delta = self.clock.tick(Game.FPS)
            self.tick = self.clock.get_rawtime()

        self.end()

    # ----------------------------------------

    def new(self):
        """
        new game logic
        :return: none
        """
        self._idCreep = 0
        self._idTower = 0

        self.building = None
        self.creeps = {}
        self.delta = 0
        self.energy = 100
        self.mass = 20
        self.pause = True
        self.select = None

        self.statCreepsSpawned = 0
        self.statCreepsEscaped = 0
        self.statCreepsKilled = 0
        self.statTowersBuilt = 0
        self.statTowersSold = 0

        self.time = 0
        self.towers = {}
        self.wave = 0
        self.waveTimer = 0

        self.loop()

    # ----------------------------------------

    def spawnCreep(self, ai):
        """
        add creep to game
        :param ai: creep type
        :return: none
        """
        self._idCreep = self._idCreep + 1

        creep = Creep(self._idCreep)
        creep.ai = ai

        if ai == 1:
            creep.rank = self.wave
            creep.energy = (creep.rank // 5) + 1
            creep.mass = (5 * creep.rank) + 20
            creep.speed = 48
        elif ai == 2:
            pass
        elif ai == 3:
            pass
        elif ai == 4:
            pass
        elif ai == 5:
            pass
        elif ai == 6:
            pass
        elif ai == 7:
            pass
        elif ai == 8:
            pass
        elif ai == 9:
            pass
        elif ai == 10:
            pass
        elif ai == 11:
            pass
        elif ai == 12:
            pass
        elif ai == 13:
            pass
        elif ai == 14:
            pass
        elif ai == 15:
            pass
        else:
            pass

        self.creeps.update({self._idCreep: creep})
        return creep

    # ----------------------------------------

    def spawnTower(self, ai, col, row):

        self._idTower = self._idTower + 1

        tower = Tower(self._idTower)
        tower.ai = ai
        tower.col = col
        tower.row = row

        self.towers.update({self._idTower: tower})
        self.statTowersBuilt = self.statTowersBuilt + 1

    # ----------------------------------------

    def spawnWave(self):
        """
        add next creep wave to game
        :return: none
        """
        if self.debug:
            self.wave = 0
        else:
            self.wave = self.wave + 1

        if self.wave in Game.WAVES:
            for creeps in Game.WAVES[self.wave]:
                ai, count = creeps
                for i in range(count):
                    creep = self.spawnCreep(ai)
                    if ai < 10:
                        col = random.randint(1, 20)
                        row = random.randint(Grid.baseNorth(), Grid.baseSouth())
                    else:
                        col = 3
                        row = random.randint(Grid.baseNorth() + 2, Grid.baseSouth() - 2)

                    creep.x = - ((col * Cell.DIM) + Cell.half() - 1)
                    creep.y = self.grid.north + (row * Cell.DIM) + Cell.half() - 1

            if self.wave != Game.WAVE_MAX:
                self.waveTimer = Game.WAVE_TIMER

            self.pause = False

    # ----------------------------------------

    def updateCreeps(self):
        """
        update path, target, and location for all creeps
        :return: none
        """
        pathIndexes = {}
        removeCreeps = []

        if bool(self.creeps):
            for _id, creep in self.creeps.items():

                move = max(1, creep.speed) * self.delta / 1000

                if creep.x > (self.grid.east + creep.half):
                    removeCreeps.append(_id)
                    if not self.debug:
                        self.mass = self.mass - creep.damage
                    self.statCreepsEscaped = self.statCreepsEscaped + 1
                    continue

                if (creep.x < 0) or (creep.x > self.grid[Grid.baseNE()].x):
                    creep.angle = 0.0
                    creep.x = creep.x + move
                    continue

                creep.index = self.grid.pointToIndex(creep.xy)
                if not bool(creep.path):
                    creep.path = self.grid.pathCreep(creep.index)
                    for n in creep.path:
                        if not (n in pathIndexes):
                            pathIndexes.update({n: None})
                    creep.target = creep.path[0]

                if not bool(creep.path):
                    continue    # NTS: remove after build logic completed for path blocking

                xTarget, yTarget = self.grid.indexToPoint(creep.target)
                a = xTarget - creep.x
                b = creep.y - yTarget
                creep.angle = math.atan2(b, a)
                targetDistance = math.hypot(a, b)

                if move < targetDistance:
                    x = move * math.cos(creep.angle)
                    y = move * math.sin(creep.angle)
                    creep.x = creep.x + x
                    creep.y = creep.y - y
                else:
                    creep.path = self.grid.pathCreep(creep.index)
                    creep.target = creep.path[0]

                    if creep.target[0] > Grid.baseEast():
                        creep.angle = 0.0
                        creep.x = creep.x + move
                    else:
                        xTarget, yTarget = self.grid.indexToPoint(creep.target)
                        a = xTarget - creep.x
                        b = creep.y - yTarget
                        creep.angle = math.atan2(b, a)
                        x = move * math.cos(creep.angle)
                        y = move * math.sin(creep.angle)
                        creep.x = creep.x + x
                        creep.y = creep.y - y

            for n in pathIndexes:
                self.grid[n].path = True

            for n in removeCreeps:
                del self.creeps[n]
