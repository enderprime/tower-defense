"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense game class
[E] ender.prime@gmail.com
[F] game.py
[V] 02.19.17
"""

from boolean import *
from constant import *
from creep import *
from display import *
from grid import *
from tower import *

import math
import pygame
from pygame.locals import *
import sys

# --------------------------------------------------------------------------------------------------------------------

class Game(object):
    """
    core game logic
    """

    DEBUG = True           # debug mode for testing
    FPS = 20                # frames per second
    TICK = 1000 // FPS      # time in ms per game loop

    WAVE_MAX = 100
    WAVE_TIMER = 42         # seconds

    # creep waves: key = wave number, value = list of creep groups: (creep ai, creep count)
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

        self.clock = pygame.time.Clock()
        self.creepsByIndex = {Grid.PATH_START: []}
        self.display = Display()
        self.grid = Grid()

        self.showGrid = False
        self.showHealth = True
        self.showPath = False

        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

        self._idCreep = 0           # creep id int
        self._idTower = 0           # tower id int

        self.building = None        # if player is in build mode, holds tower type (0-9)
        self.creeps = {}            # active creeps in game
        self.delta = 0              # time in ms of last game loop
        self.energy = 100           # main player resource used to buy towers and upgrades
        self.mass = 20              # player health, game over if this reaches zero
        self.pause = True
        self.select = None          # index of selected cell
        self.tick = 0               # time in ms of last clock tick

        self.statCreepsEscaped = 0
        self.statCreepsKilled = 0
        self.statCreepsSpawned = 0
        self.statTowersBuilt = 0
        self.statTowersSold = 0

        self.time = 0               # running time in seconds from start of new game
        self.towers = {}            # active towers in game
        self.wave = 0               # current creep wave
        self.waveTimer = 0          # countdown to next creep wave

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

    def buildIsAllowed(self, index):
        """
        :param index: (column, row) where building will occur
        :return: true if building at index would not block all paths
        """
        cell = self.grid[index]

        if bool(cell.build) and (cell.build.ai == 0):
            return True
        elif index in self.creepsByIndex:
            return False
        else:
            grid = copy.deepcopy(self.grid)
            grid[index].open = False
            grid.pathfinder()
            for index in self.creepsByIndex.keys():
                path = grid.path(index)
                if (not bool(path)) or path[-1] != Grid.PATH_GOAL:
                    return False
            return True

    # ----------------------------------------

    def drawHeader(self):
        """
        draw interface header on screen
        :return: none
        """

        rect = pygame.Rect(0, 0, Display.WIDTH, Display.HEADER)
        self.display.window.fill(Display.COLOR_BLACK, rect)

        color = Display.COLOR_WHITE
        font = self.display._fonts['LUCID_20']

        # mass
        x = 160
        y = (Display.HEADER // 2) - 14
        self.display.window.blit(self.display._text['MASS'], (x, y))

        if self.mass < 10:
            img = PATH_IMG + 'mass-0' + str(self.mass) + '.png'
        else:
            img = PATH_IMG + 'mass-' + str(self.mass) + '.png'

        x = x + 65
        y = (Display.HEADER // 2) - 18
        rect = pygame.Rect(x, y, 282, 28)
        self.display.window.blit(Display.IMAGES[img], rect)

        # energy
        x = x + 330
        y = (Display.HEADER // 2) - 14
        self.display.window.blit(self.display._text['ENERGY'], (x, y))

        x = x + 90
        text = font.render(str(self.energy), True, color)
        self.display.window.blit(text, (x, y))

        # wave number
        x = x + 100
        self.display.window.blit(self.display._text['WAVE'], (x, y))

        x = x + 70
        if self.wave == 0:
            text = font.render('--', True, color)
        else:
            text = font.render(str(self.wave), True, color)
        self.display.window.blit(text, (x, y))

        # wave timer
        x = x + 90
        self.display.window.blit(self.display._text['NEXT'], (x, y))

        x = x + 70
        if self.waveTimer < 1:
            text = font.render('--', True, color)
        else:
            text = font.render(str(int(self.waveTimer)), True, color)
        self.display.window.blit(text, (x, y))

        # play button
        if self.pause:
            img = Display.IMAGES[IMG_PLAY]
        else:
            img = Display.IMAGES[IMG_PAUSE]

        x1, y1, x2, y2 = Display.BTN_PLAY
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.display.window.blit(img, rect)

        # next button
        if self.wave < Game.WAVE_MAX:
            img = Display.IMAGES[IMG_NEXT_ACTIVE]
        else:
            img = Display.IMAGES[IMG_NEXT_INACTIVE]
        x1, y1, x2, y2 = Display.BTN_NEXT
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.display.window.blit(img, rect)

    # ----------------------------------------

    def drawFooter(self):
        """
        draw interface footer on screen
        :return: none
        """
        rect = pygame.Rect(0, Display.HEADER + Grid.HEIGHT, Display.WIDTH, Display.FOOTER)
        self.display.window.fill(Display.COLOR_BLACK, rect)

        ####

    # ----------------------------------------

    def drawGrid(self):
        """
        draw main game area on screen
        :return: none
        """

        # background
        rect = pygame.Rect(Grid.X, Grid.Y, Grid.WIDTH, Grid.HEIGHT)
        self.display.window.fill(Display.COLOR_BLACK, rect)

        # grid lines
        if self.showGrid:
            for lst in self.grid.cells:
                for cell in lst:
                    if cell.base and cell.open:
                        rect = (cell.west, cell.north, Cell.DIM, Cell.DIM)
                        pygame.draw.rect(self.display.window, Display.COLOR_GREY_1, rect, 1)

        # hover
        index = Grid.pointToIndex(self.display.mouse)
        if bool(index):
            cell = self.grid[index]
            if cell.base and notNull(self.building):
                if self.buildIsAllowed(index):
                    color = Display.COLOR_GREEN
                else:
                    color = Display.COLOR_RED
                rect = pygame.Rect(cell.west, cell.north, Cell.DIM, Cell.DIM)
                self.display.window.fill(color, rect)

        # selected
        if notNull(self.select):
            cell = self.grid[self.select]
            rect = pygame.Rect(cell.west, cell.north, Cell.DIM, Cell.DIM)
            self.display.window.fill(Display.COLOR_BLUE, rect)

        # base border
        color = Display.COLOR_WHITE
        west, north, east, south = Grid.XY_BASE_BOUNDS
        east = east + 3
        north = north - 4
        south = south + 3
        west = west - 4
        pygame.draw.line(self.display.window, color, (west, north), (east, north), 2)
        pygame.draw.line(self.display.window, color, (west, south), (east, south), 2)
        pygame.draw.line(self.display.window, color, (west, north), (west, north + 11), 2)
        pygame.draw.line(self.display.window, color, (east, north), (east, north + 11), 2)
        pygame.draw.line(self.display.window, color, (west, south), (west, south - 11), 2)
        pygame.draw.line(self.display.window, color, (east, south), (east, south - 11), 2)

        # path
        if self.showPath:
            if self.DEBUG:
                for cell in self.grid:
                    col, row = cell.index
                    x, y = cell.NW
                    rect = pygame.Rect(x, y, Cell.DIM, Cell.DIM)
                    img = Display.IMAGES[IMG_PATH]

                    if bool(cell.path):
                        colTarget, rowTarget = cell.path
                        a = colTarget - col
                        b = row - rowTarget
                        angle = math.atan2(b, a)
                    else:
                        angle = 0

                    if angle != 0:
                        img = pygame.transform.rotate(img, math.degrees(angle))
                    self.display.window.blit(img, rect)
            else:
                for index in self.grid.path():
                    cell = self.grid[index]
                    pygame.draw.circle(self.display.window, Display.COLOR_ORANGE, cell.xy, 3)

        # towers
        if bool(self.towers):
            for _id, tower in self.towers.items():
                x, y = self.grid[tower.index].NW
                rect = pygame.Rect(x, y, Cell.DIM, Cell.DIM)
                img = Display.IMAGES[IMG_TOWER_BASE]
                self.display.window.blit(img, rect)

                if tower.ai != 0:
                    img = Display.IMAGES[tower.imgTower]
                    if tower.angle != 0:
                        img = pygame.transform.rotate(img, math.degrees(tower.angle))
                    self.display.window.blit(img, rect)

        # creeps
        if bool(self.creeps):
            for _id, creep in self.creeps.items():
                x, y = creep.NW
                rect = pygame.Rect(x, y, creep._size, creep._size)
                img = Display.IMAGES[creep.image]
                if creep.angle != 0:
                    img = pygame.transform.rotate(img, math.degrees(creep.angle))
                self.display.window.blit(img, rect)

    # ----------------------------------------

    def drawSidebar(self):
        """
        draw interface sidebar on screen
        :return: none
        """
        rect = pygame.Rect(Grid.WIDTH, 0, Display.SIDEBAR, Display.HEIGHT)
        self.display.window.fill(Display.COLOR_BLACK, rect)

        font = self.display._fonts['LUCID_20']

        # new game button
        img = Display.IMAGES[IMG_NEW]
        x1, y1, x2, y2 = Display.BTN_NEW
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.display.window.blit(img, rect)

        # debug info
        if Game.DEBUG:

            x = Display.WIDTH - 140
            y = Display.HEIGHT - 30
            self.display.window.blit(self.display._text['TICK'], (x, y))

            x = x + 70
            if self.tick < Game.TICK:
                color = Display.COLOR_GREEN
            else:
                color = Display.COLOR_RED
            text = font.render(str(self.tick), True, color)
            self.display.window.blit(text, (x, y))

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
            index = Grid.pointToIndex(point)
            if bool(index):
                cell = self.grid[index]
                col, row = index
                if cell.base:
                    if notNull(self.building) and self.buildIsAllowed(index):
                        cell.build = self.spawnTower(self.building, col, row)
                        self.grid.pathfinder()
                    elif notNull(cell.build):
                        self.select = index
            else:
                west, north, east, south = Display.BTN_PLAY
                if (west <= x <= east) and (north <= y <= south):
                    self.pause = not self.pause

                west, north, east, south = Display.BTN_NEXT
                if (west <= x <= east) and (north <= y <= south):
                    self.spawnWave()

                west, north, east, south = Display.BTN_NEW
                if (west <= x <= east) and (north <= y <= south):
                    self.new()

        elif button == 3:
            self.building = None
            self.select = None

    # ----------------------------------------

    def eventKey(self, key):
        """
        event handling for keyboard
        :param key: keyboard input from pygame event loop
        :return: none
        """
        if key == K_ESCAPE:
            self.building = None
            self.select = None
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

        if notNull(self.building):
            self.select = None

    # ----------------------------------------

    def end(self):
        """
        game over logic
        :return: none
        """

        ####

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    west, north, east, south = Display.BTN_NEW
                    if (west <= x <= east) and (north <= y <= south):
                        self.new()

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
                for n in self.grid:
                    if n.build:
                        n.open = False
                    else:
                        n.open = True
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
                    self.display.mouse = event.pos
                elif event.type == USEREVENT + 1:
                    self.time = self.time + 1
                    if not self.pause:
                        if self.wave != Game.WAVE_MAX:
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
        self.grid.reset()

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
        :return: creep object reference
        """
        self._idCreep = self._idCreep + 1

        if ai == 0:
            creep = CreepScout(self._idCreep)
        else:
            creep = CreepScout(self._idCreep)

        creep.spawn(self.wave)
        self.creeps.update({self._idCreep: creep})
        self.statCreepsSpawned = self.statCreepsSpawned + 1

        return creep

    # ----------------------------------------

    def spawnTower(self, ai, col, row):
        """
        add tower to game
        :param ai: tower type
        :param col: column value
        :param row: row value
        :return: tower object reference
        """
        self._idTower = self._idTower + 1

        if ai == 0:     tower = TowerBase(self._idTower)
        elif ai == 1:   tower = TowerGun(self._idTower)
        elif ai == 2:   tower = TowerCannon(self._idTower)
        elif ai == 3:   tower = TowerMissle(self._idTower)
        elif ai == 4:   tower = TowerSlow(self._idTower)
        elif ai == 5:   tower = TowerLaser(self._idTower)
        elif ai == 6:   tower = TowerRail(self._idTower)
        elif ai == 7:   tower = TowerBash(self._idTower)
        elif ai == 8:   tower = TowerSupport(self._idTower)
        else:           tower = TowerBase(self._idTower)

        tower.spawn(col, row)

        cell = self.grid.cells[col][row]
        cell.build = tower
        cell.open = False
        cell.path = None

        self.towers.update({self._idTower: tower})
        self.statTowersBuilt = self.statTowersBuilt + 1

        return tower

    # ----------------------------------------

    def spawnWave(self):
        """
        add next creep wave to game
        :return: none
        """
        if (self.wave + 1) <= Game.WAVE_MAX:
            if Game.DEBUG:
                self.wave = 0
            else:
                self.wave = self.wave + 1
            for creeps in Game.WAVES[self.wave]:
                ai, count = creeps
                for i in range(count):
                    self.spawnCreep(ai)

            if self.wave != Game.WAVE_MAX:
                self.waveTimer = Game.WAVE_TIMER
            self.pause = False

    # ----------------------------------------

    def updateCreeps(self):
        """
        update location and target for all creeps
        :return: none
        """
        self.creepsByIndex = {Grid.PATH_START: []}
        removeCreeps = []

        if bool(self.creeps):
            for _id, creep in self.creeps.items():

                if creep.x > (Grid.XY_EAST + creep._half):
                    removeCreeps.append(_id)
                    if not Game.DEBUG:
                        self.mass = self.mass - creep.damage
                    self.statCreepsEscaped = self.statCreepsEscaped + 1
                else:
                    creep.move(self.grid, self.delta)
                    if bool(creep.index):
                        if creep.index in self.creepsByIndex:
                            self.creepsByIndex[creep.index].append(creep._id)
                        else:
                            self.creepsByIndex.update({creep.index: [creep._id]})

            for n in removeCreeps:
                del self.creeps[n]
