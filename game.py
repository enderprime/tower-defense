"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense game class
[E] ender.prime@gmail.com
[F] game.py
[V] 01.23.17
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

    FPS = 30

    HEADER =  60
    FOOTER =  60
    SIDEBAR = 300

    WIDTH =  Grid.WIDTH + SIDEBAR
    HEIGHT = Grid.HEIGHT + HEADER + FOOTER
    DIMS =   (WIDTH, HEIGHT)

    ICON = 32

    # IMAGES = \
    #     {
    #         IMG_0: pygame.image.load(IMG_0),
    #         IMG_1: pygame.image.load(IMG_1),
    #         IMG_2: pygame.image.load(IMG_2),
    #         IMG_3: pygame.image.load(IMG_3),
    #         IMG_4: pygame.image.load(IMG_4),
    #         IMG_5: pygame.image.load(IMG_5),
    #         IMG_6: pygame.image.load(IMG_6),
    #         IMG_7: pygame.image.load(IMG_7),
    #         IMG_8: pygame.image.load(IMG_8)
    #     }

    # ----------------------------------------

    def __init__(self):

        self.grid = Grid(0, Game.HEADER)

        self.energy = 0
        self.mass = 0
        self.mouse = (0, 0)
        self.time = 0

        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(Game.DIMS)

        pygame.display.set_caption('TOWER DEFENSE')
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    # ----------------------------------------

    @classmethod
    def pointIsValid(cls, point):

        x, y = point

        xValid = bool(-1 < x < Game.WIDTH)
        yValid = bool(-1 < y < Game.HEIGHT)

        return bool(xValid and yValid)

    # ----------------------------------------

    def click(self, point, button):

        pass
        ####

    # ----------------------------------------

    def draw(self):

        font = pygame.font.SysFont(None, 32)
        cols, rows = Grid.CELLS

        self.window.fill(h_000000)

        # header

        rect = pygame.Rect(0, 0, Game.WIDTH, Game.HEADER)
        self.window.fill(h_333333, rect)

        # img = Game.IMAGES[IMG_CLOCK]
        # x, y = pad + 1, pad + 1
        # rect = pygame.Rect(x, y, Game.ICON, Game.ICON)
        # self.window.blit(img, rect)
        #
        # img = Game.IMAGES[IMG_MINES]
        # x = width - pad - Game.ICON
        # rect = pygame.Rect(x, y, Game.ICON, Game.ICON)
        # self.window.blit(img, rect)
        #
        # x = Game.ICON + (pad * 2)
        # y = pad + 6
        # p = (x, y)
        # text = font.render(str(self.time), True, h_000000)
        # self.window.blit(text, p)
        #
        # x = width - (Game.ICON * 2) - (pad * 2)
        # p = (x, y)
        # text = font.render(str(self.grid.flags), True, h_000000)
        # self.window.blit(text, p)

        # grid

        i1, i2, i3, i4 = Grid.CORNERS
        c1 = self.grid[i1]
        c2 = self.grid[i2]
        c3 = self.grid[i3]
        c4 = self.grid[i4]

        x1 = c1.x - 2
        y1 = c1.y - 2
        x2 = c2.x - 2
        y2 = c2.y + Cell.DIM
        x3 = c3.x + Cell.DIM
        y3 = c3.y - 2
        x4 = c4.x + Cell.DIM
        y4 = c4.y + Cell.DIM
        line = 10

        pygame.draw.line(self.window, h_FFFFFF, (x1, y1), (x3, y3), 2)
        pygame.draw.line(self.window, h_FFFFFF, (x2, y2), (x4, y4), 2)
        pygame.draw.line(self.window, h_FFFFFF, (x1, y1), (x1, y1 + line), 2)
        pygame.draw.line(self.window, h_FFFFFF, (x2, y2), (x2, y2 - line), 2)
        pygame.draw.line(self.window, h_FFFFFF, (x3, y3), (x3, y3 + line), 2)
        pygame.draw.line(self.window, h_FFFFFF, (x4, y4), (x4, y4 - line), 2)

        index = self.grid.pointToIndex(self.mouse)
        if self.grid.indexIsValid(index):
            cell = self.grid[index]
            if cell.base:
                if cell.empty:
                    color = h_006633
                else:
                    color = h_003366
                pygame.draw.rect(self.window, color, cell.rect)

        for col in range(cols):
            for row in range(rows):
                index = (col, row)
                cell = self.grid[index]

                ####

        # footer

        rect = pygame.Rect(0, Game.HEADER + Grid.HEIGHT, Game.WIDTH, Game.FOOTER)
        self.window.fill(h_333333, rect)

        # sidebar

        rect = pygame.Rect(Grid.WIDTH, 0, Game.SIDEBAR, Game.HEIGHT)
        self.window.fill(h_333333, rect)

        pygame.display.update()

    # ----------------------------------------

    def end(self):

        font = pygame.font.SysFont(None, 32)
        cols, rows = Grid.CELLS

        for col in range(cols):
            for row in range(rows):
                i = (col, row)
                cell = self.grid[i]

        self.draw()

        # rect = pygame.Rect(0, 0, width, Game.HEADER)
        # self.window.fill(color, rect)
        #
        # x = (width // 2) - 40
        # y = (Game.HEADER // 2) - 10
        # p = (x, y)
        # text = font.render(result, True, h_FFFFFF)
        # self.window.blit(text, p)

        pygame.display.update()

        new = False
        quit = False

        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit = True
                    wait = False

        if quit:
            pygame.quit()
            sys.exit()
        elif new:
            self.new()

    # ----------------------------------------

    def loop(self):

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
                        if event.key == K_ESCAPE:
                            self.pause()
                    elif event.type == MOUSEBUTTONUP:
                        self.click(event.pos, event.button)
                    elif event.type == MOUSEMOTION:
                        self.mouse = event.pos
                    elif event.type == USEREVENT + 1:
                        self.time = self.time + 1

            self.draw()
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

        self.grid.reset()

        self.energy = 100
        self.mass = 100
        self.time = 0

        self.loop()

    # ----------------------------------------

    def pause(self):

        font = pygame.font.SysFont(None, 32)
        xCenter, yCenter = self.grid.center

        rect = pygame.Rect(xCenter - 55, yCenter + 10, 110, 40)
        self.window.fill(h_000000, rect)

        x = xCenter - 45
        y = yCenter + 20
        p = (x, y)
        text = font.render('PAUSED', True, h_FFFFFF)
        self.window.blit(text, p)

        pygame.display.update()

        quit = False
        pause = True
        while pause:

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit = True
                    pause = False
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pause = False

        if quit:
            pygame.quit()
            sys.exit()
