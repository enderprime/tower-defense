"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense game class
[E] ender.prime@gmail.com
[F] game.py
[V] 01.26.17
"""

from bool import *
from cell import *
from const import *
from grid import *

import pygame
from pygame.locals import *
import sys

# --------------------------------------------------------------------------------------------------------------------

class Game(object):
    """
    game logic and pygame display
    """

    FPS = 30

    HEADER = 60
    FOOTER = 60
    SIDEBAR = 300

    # ----------------------------------------

    def __init__(self):

        self.clock = pygame.time.Clock()
        self.grid = Grid(0, Game.HEADER)
        self.energy = 0
        self.mass = 0
        self.mouse = (0, 0)
        self.pause = True
        self.showCreepPath = True
        self.showGridLines = True
        self.time = 0
        self.window = pygame.display.set_mode((Game.width(), Game.height()))

        self.window.fill(h_000000)
        pygame.display.set_caption('TOWER DEFENSE')
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

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
    def colors(self):
        """
        :return: dictionary with display colors
        """
        return \
            {
                'CELL_BLOCK': h_990033,
                'CELL_OPEN':  h_006633,
                'CELL_HOVER': h_003366,
                'FOOT_BG':    h_000000,
                'FOOT_BODY':  h_FFFFFF,
                'FOOT_HEAD':  h_FFFFFF,
                'GRID_BASE':  h_FFFFFF,
                'GRID_BG':    h_000000,
                'GRID_BODY':  h_FFFFFF,
                'GRID_GRID':  h_333333,
                'GRID_HEAD':  h_FFFFFF,
                'GRID_PATH':  h_CC6600,
                'HEAD_BG':    h_000000,
                'HEAD_BODY':  h_FFFFFF,
                'HEAD_HEAD':  h_FFFFFF,
                'MAIN_BLUE':  h_003366,
                'MAIN_GREEN': h_006633,
                'MAIN_RED':   h_990033,
                'SIDE_BG':    h_000000,
                'SIDE_BODY':  h_FFFFFF,
                'SIDE_HEAD':  h_FFFFFF
            }

    # ----------------------------------------

    @property
    def fonts(self):
        """
        :return: dictionary with display fonts
        """
        return \
            {
                'FOOT_BODY': pygame.font.SysFont(None, 24),
                'FOOT_HEAD': pygame.font.SysFont(None, 32),
                'GRID_BODY': pygame.font.SysFont(None, 24),
                'GRID_HEAD': pygame.font.SysFont(None, 32),
                'HEAD_BODY': pygame.font.SysFont(None, 24),
                'HEAD_HEAD': pygame.font.SysFont(None, 32),
                'SIDE_BODY': pygame.font.SysFont(None, 24),
                'SIDE_HEAD': pygame.font.SysFont(None, 32)
            }

    # ----------------------------------------

    def eventClick(self, point, button):
        """
        event handling for mouse clicks
        :param point: mouse (x, y) passed from pygame event loop
        :param button: mouse button passed from pygame event loop
        :return: none
        """
        pass

        ####

    # ----------------------------------------

    def eventKey(self, key):
        """
        event handling for keyboard
        :param key: keyboard input passed from pygame event loop
        :return: None
        """
        if key == K_ESCAPE:
            self.pause = not self.pause
            ####
        elif key == K_SPACE:
            self.pause = not self.pause
        elif key == K_g:
            self.showGridLines = not self.showGridLines
        elif key == K_p:
            self.showCreepPath = not self.showCreepPath

    # ----------------------------------------

    def drawHeader(self):
        """
        draw interface header on screen
        :return: none
        """
        color = self.colors['HEAD_BG']
        rect = pygame.Rect(0, 0, Game.width(), Game.HEADER)
        self.window.fill(color, rect)

    # ----------------------------------------

    def drawGrid(self):
        """
        draw main game area on screen
        :return: none
        """

        # background
        color = self.colors['GRID_BG']
        rect = pygame.Rect(self.grid.x, self.grid.y, Grid.width(), Grid.height())
        self.window.fill(color, rect)

        # base grid
        color = self.colors['GRID_GRID']
        if self.showGridLines:
            for lst in self.grid.base:
                for cell in lst:
                    pygame.draw.rect(self.window, color, (cell.west, cell.north, Cell.DIM, Cell.DIM), 1)

        # base border
        c1, c2 = Grid.baseBounds()
        west, north = self.grid[c1].NW
        east, south = self.grid[c2].SE
        east = east + 1
        north = north - 2
        south = south + 1
        west = west - 2

        color = self.colors['GRID_BASE']
        pygame.draw.line(self.window, color, (west, north), (east, north), 2)
        pygame.draw.line(self.window, color, (west, south), (east, south), 2)
        pygame.draw.line(self.window, color, (west, north), (west, north + 10), 2)
        pygame.draw.line(self.window, color, (east, north), (east, north + 10), 2)
        pygame.draw.line(self.window, color, (west, south), (west, south - 10), 2)
        pygame.draw.line(self.window, color, (east, south), (east, south - 10), 2)

        # cell highlighting
        index = self.grid.pointToIndex(self.mouse)
        if self.grid.indexIsValid(index):
            cell = self.grid[index]
            if cell.base:
                if cell.build:
                    color = self.colors['CELL_HOVER']
                else:
                    if cell.open:
                        color = self.colors['CELL_OPEN']
                    else:
                        color = self.colors['CELL_BLOCK']
                self.window.fill(color, (cell.west, cell.north, Cell.DIM, Cell.DIM))

        # towers

        # creeps

    # ----------------------------------------

    def drawFooter(self):
        """
        draw interface footer on screen
        :return: none
        """
        color = self.colors['FOOT_BG']
        rect = pygame.Rect(0, Game.HEADER + Grid.height(), Game.width(), Game.FOOTER)
        self.window.fill(color, rect)

    # ----------------------------------------

    def drawSidebar(self):
        """
        draw interface sidebar on screen
        :return: none
        """
        color = self.colors['SIDE_BG']
        rect = pygame.Rect(Grid.width(), 0, Game.SIDEBAR, Game.height())
        self.window.fill(color, rect)

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

            if self.pause:
                font = self.fonts['GRID_HEAD']
                x, y = self.grid.center
                rect = pygame.Rect(x - 55, y - 20, 110, 40)
                self.window.fill(h_000000, rect)
                text = font.render('PAUSED', True, h_FFFFFF)
                self.window.blit(text, (x - 45, y - 10))
            else:
                self.drawHeader()
                self.drawGrid()
                self.drawFooter()
                self.drawSidebar()

            self.clock.tick(Game.FPS)
            pygame.display.update()

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
        self.grid.reset()

        self.energy = 100
        self.mass = 100
        self.pause = True
        self.time = 0

        self.drawHeader()
        self.drawGrid()
        self.drawFooter()
        self.drawSidebar()

        self.loop()

    # ----------------------------------------

    def pause(self):
        """
        pause logic
        :return: none
        """
        font = self.fonts['GRID_HEAD']
        x, y = self.grid.center

        rect = pygame.Rect(x - 55, y - 20, 110, 40)
        self.window.fill(h_000000, rect)

        text = font.render('PAUSED', True, h_FFFFFF)
        self.window.blit(text, (x - 45, y - 10))

        pygame.display.update()

        pause = True
        while pause:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP:
                    key = event.key
                    if (key == K_ESCAPE) or (key == K_SPACE):
                        pause = False
