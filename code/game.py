"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense game class
[E] ender.prime@gmail.com
[F] game.py
[V] 02.13.17
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
    FPS = 25                # frames per second
    TICK = 1000 // FPS      # time in ms per game loop

    HEADER = 84             # pixels
    FOOTER = 133            # pixels
    SIDEBAR = 250           # pixels

    WIDTH = Grid.WIDTH + SIDEBAR                # width in pixels
    HEIGHT = HEADER + Grid.HEIGHT + FOOTER      # height in pixels

    # next button bounds
    BTN_NEXT_X = 1100
    BTN_NEXT_Y = (HEADER // 2) - 18
    BTN_NEXT = (BTN_NEXT_X, BTN_NEXT_Y, BTN_NEXT_X + 27, BTN_NEXT_Y + 27)   # (west, north, east, south)

    # play button bounds
    BTN_PLAY_X = 1050
    BTN_PLAY_Y = (HEADER // 2) - 18
    BTN_PLAY = (BTN_PLAY_X, BTN_PLAY_Y, BTN_PLAY_X + 27, BTN_PLAY_Y + 27)   # (west, north, east, south)

    WAVE_MAX = 100
    WAVE_TIMER = 30     # seconds

    COLOR_BLACK = (0, 0, 0)
    COLOR_BLUE = (32, 64, 128)
    COLOR_GREEN = (51, 102, 51)
    COLOR_GREY_1 = (24, 24, 24)
    COLOR_GREY_2 = (36, 36, 36)
    COLOR_ORANGE = (204, 102, 0)
    COLOR_PURPLE = (102, 0, 102)
    COLOR_RED = (128, 28, 28)
    COLOR_WHITE = (255, 255, 255)

    COLORS = \
        {
            'CELL_BLOCK':  COLOR_RED,
            'CELL_BUILD':  COLOR_BLUE,
            'CELL_HOVER':  COLOR_WHITE,
            'CELL_OPEN':   COLOR_GREEN,

            'FOOT_BG':     COLOR_BLACK,
            'FOOT_BODY':   COLOR_WHITE,
            'FOOT_HEAD':   COLOR_WHITE,

            'GRID_BASE':   COLOR_WHITE,
            'GRID_BG':     COLOR_BLACK,
            'GRID_BODY':   COLOR_WHITE,
            'GRID_GRID':   COLOR_GREY_1,
            'GRID_HEAD':   COLOR_WHITE,
            'GRID_PATH':   COLOR_ORANGE,

            'HEAD_BG':     COLOR_BLACK,
            'HEAD_BODY':   COLOR_WHITE,
            'HEAD_HEAD':   COLOR_WHITE,

            'RANK_1':      COLOR_GREY_2,
            'RANK_2':      COLOR_GREEN,
            'RANK_3':      COLOR_BLUE,
            'RANK_4':      COLOR_PURPLE,
            'RANK_5':      COLOR_RED,

            'SIDE_BG':     COLOR_BLACK,
            'SIDE_BODY':   COLOR_WHITE,
            'SIDE_HEAD':   COLOR_WHITE,
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
            IMG_TOWER_8: pygame.image.load(IMG_TOWER_8)
        }

    # creep waves: key = wave number, value = list of creep groups: (creep ai, creep count)
    WAVES = \
        {
            0: [(1, 20)],
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
        self.window = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
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
        rect = pygame.Rect(0, 0, Game.WIDTH, Game.HEADER)
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

        x1, y1, x2, y2 = Game.BTN_PLAY
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.window.blit(img, rect)

        # next button
        img = Game.IMAGES[IMG_NEXT]
        x1, y1, x2, y2 = Game.BTN_NEXT
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.window.blit(img, rect)

    # ----------------------------------------

    def drawFooter(self):
        """
        draw interface footer on screen
        :return: none
        """
        color = Game.COLORS['FOOT_BG']
        rect = pygame.Rect(0, Game.HEADER + Grid.HEIGHT, Game.WIDTH, Game.FOOTER)
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
        rect = pygame.Rect(self.grid.x, self.grid.y, Grid.WIDTH, Grid.HEIGHT)
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
                        if cell.open or (cell.build == 0):      # NTS: update with path blocking logic
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
        west, north, east, south = Grid.BASE_BOUNDS
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
                if tower.angle != 0:
                    img = pygame.transform.rotate(img, math.degrees(tower.angle))
                self.window.blit(img, rect)

        # creeps
        if bool(self.creeps):
            for _id, creep in self.creeps.items():
                x, y = creep.NW
                rect = pygame.Rect(x, y, creep.size, creep.size)
                img = Game.IMAGES[creep.image]
                if creep.angle != 0:
                    img = pygame.transform.rotate(img, math.degrees(creep.angle))
                self.window.blit(img, rect)

    # ----------------------------------------

    def drawSidebar(self):
        """
        draw interface sidebar on screen
        :return: none
        """
        color = Game.COLORS['SIDE_BG']
        rect = pygame.Rect(Grid.WIDTH, 0, Game.SIDEBAR, Game.HEIGHT)
        self.window.fill(color, rect)

        ####

        # debug info
        if self.debug:
            color = self.COLORS['SIDE_BODY']
            font = self.fonts['SIDE_BODY']
            x = Game.WIDTH - 150
            y = Game.HEIGHT - 30
            p = (x, y)
            text = font.render('DEBUG', True, color)
            self.window.blit(text, p)

            x = x + 80
            y = y + 4
            if self.tick < Game.TICK:
                color = self.COLORS['RANK_2']
            else:
                color = self.COLORS['RANK_5']
            rect = pygame.Rect(x, y, 50, 12)
            self.window.fill(color, rect)

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
                col, row = index
                if cell.base:
                    # NTS: update with valid path logic
                    if notNull(self.building) and (cell.open or (cell.build == 0)):
                        cell.build = self.spawnTower(self.building, col, row)
                        self.grid.path = self.grid.pathfinder()
                    elif notNull(cell.build):
                        self.select = index
            else:
                west, north, east, south = Game.BTN_PLAY
                if (west <= x <= east) and (north <= y <= south):
                    self.pause = not self.pause

                west, north, east, south = Game.BTN_NEXT
                if (west <= x <= east) and (north <= y <= south):
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

        cell = self.grid.cells[col][row]
        cell.build = self._idTower
        cell.open = False
        cell.path = None

        self.towers.update({self._idTower: tower})
        self.statTowersBuilt = self.statTowersBuilt + 1

        return self._idTower

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
                        col = random.randint(1, count)
                        row = random.randint(Grid.BASE_NORTH, Grid.BASE_SOUTH)
                    else:
                        col = 3
                        row = random.randint(Grid.BASE_NORTH + 2, Grid.BASE_SOUTH - 2)

                    creep.x = - (col * Cell.DIM) - random.randint(1, Cell.DIM)
                    creep.y = self.grid.north + (row * Cell.DIM) + random.randint(1, Cell.DIM)

            if self.wave != Game.WAVE_MAX:
                self.waveTimer = Game.WAVE_TIMER

            self.pause = False

    # ----------------------------------------

    def updateCreeps(self):
        """
        update path, target, and location for all creeps
        :return: none
        """
        removeCreeps = []

        if bool(self.creeps):
            for _id, creep in self.creeps.items():

                move = max(1, creep.speed) * self.delta / 1000
                creep.index = self.grid.pointToIndex(creep.xy)

                if creep.x > (self.grid.east + creep.half):
                    removeCreeps.append(_id)
                    if not self.debug:
                        self.mass = self.mass - creep.damage
                    self.statCreepsEscaped = self.statCreepsEscaped + 1
                    continue

                if (not bool(creep.index)) or (creep.x >= self.grid.cells[Grid.BASE_EAST][0].NW[0]):
                    creep.angle = 0.0
                    creep.x = creep.x + move
                    continue

                if not bool(creep.target):
                    creep.target = self.grid[creep.index].path

                if not bool(creep.target):
                    creep.angle = 0.0
                    creep.x = creep.x + move
                    continue

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
                    creep.last = creep.index
                    creep.index = self.grid.pointToIndex(creep.xy)
                    creep.target = self.grid[creep.index].path

                    if not bool(creep.target):
                        creep.angle = 0.0
                        creep.x = creep.x + move
                        continue

                    xTarget, yTarget = self.grid.indexToPoint(creep.target)
                    a = xTarget - creep.x
                    b = creep.y - yTarget
                    creep.angle = math.atan2(b, a)
                    x = move * math.cos(creep.angle)
                    y = move * math.sin(creep.angle)
                    creep.x = creep.x + x
                    creep.y = creep.y - y

            for n in removeCreeps:
                del self.creeps[n]
