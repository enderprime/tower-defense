"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense grid class
[E] ender.prime@gmail.com
[F] grid.py
[V] 01.23.17
"""

from bool import *
from cell import *
from const import *

import pygame

# --------------------------------------------------------------------------------------------------------------------

class Grid(object):

    ADJACENT = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    BASE =    (21, 15)
    SPACE =   (3, 2)
    CELLS =   (BASE[0] + (SPACE[0] * 2), BASE[1] + (SPACE[1] * 2))

    CORNERS = \
        (
            (SPACE[0], SPACE[1]),
            (SPACE[0], BASE[1] + SPACE[1] - 1),
            (BASE[0] + SPACE[0] - 1, SPACE[1]),
            (BASE[0] + SPACE[0] - 1, BASE[1] + SPACE[1] - 1)
        )

    WIDTH =   CELLS[0] * Cell.DIM
    HEIGHT =  CELLS[1] * Cell.DIM

    # ----------------------------------------

    def __init__(self, x, y):

        baseCols, baseRows = Grid.BASE
        gridCols, gridRows = Grid.CELLS
        spaceCols, spaceRows = Grid.SPACE

        self.x = x
        self.y = y

        self.base = []
        self.cells = []
        self.space = []

        for col in range(gridCols):

            listBase = []
            listCells = []
            listSpace = []

            for row in range(gridRows):

                x = self.x + (col * Cell.DIM)
                y = self.y + (row * Cell.DIM)

                cell = Cell(x, y)

                cell.col = col
                cell.row = row

                colBase = bool((spaceCols - 1) < col < (baseCols + spaceCols))
                rowBase = bool((spaceRows - 1) < row < (baseRows + spaceRows))

                if bool(colBase and rowBase):
                    cell.base = True
                    listBase.append(cell)
                else:
                    listSpace.append(cell)

                listCells.append(cell)

            if bool(listBase):
                self.base.append(listBase)

            self.cells.append(listCells)
            self.space.append(listSpace)

    # ----------------------------------------

    def __getitem__(self, index):

        col, row = index
        return self.cells[col][row]

    # ----------------------------------------

    def __iter__(self):

        for lst in self.cells:
            for cell in lst:
                yield cell

    # ----------------------------------------

    def __len__(self):

        cols, rows = Grid.CELLS
        return cols * rows

    # ----------------------------------------

    def __repr__(self):

        cols, rows = Grid.CELLS
        return 'Grid(' + str(cols) + ', ' + str(rows) + ')'

    # ----------------------------------------

    def __str__(self):

        cols, rows = Grid.CELLS

        s = '['
        for col in range(cols):
            s = s + '['
            for row in range(rows):
                s = s + str(self.cells[col][row])
                if row < rows - 1:
                    s = s + ', '
            s = s + ']'
        s = s + ']'

        return s

    # ----------------------------------------

    @property
    def center(self):

        x = self.x + (Grid.WIDTH // 2)
        y = self.y + (Grid.HEIGHT // 2)

        return x, y

    # ----------------------------------------

    @property
    def rect(self):

        return pygame.Rect(self.x, self.y, Grid.WIDTH, Grid.HEIGHT)

    # ----------------------------------------

    @property
    def xy(self):

        return self.x, self.y

    # ----------------------------------------

    @classmethod
    def indexIsValid(cls, index):

        col, row = index
        cols, rows = Grid.CELLS

        colValid = bool(-1 < col < cols)
        rowValid = bool(-1 < row < rows)

        return bool(colValid and rowValid)

    # ----------------------------------------

    def indexToPoint(self, index):

        col, row = index

        x = self.x + (col * Cell.DIM)
        y = self.y + (row * Cell.DIM)

        return x, y

    # ----------------------------------------

    def pointIsValid(self, point):

        x, y = point

        xValid = bool((self.x - 1) < x < (self.x + Grid.WIDTH))
        yValid = bool((self.y - 1) < y < (self.y + Grid.HEIGHT))

        return bool(xValid and yValid)

    # ----------------------------------------

    def pointToIndex(self, point):

        if self.pointIsValid(point):
            x, y = point
            x = x - self.x
            y = y - self.y
            col = x // Cell.DIM
            row = y // Cell.DIM
            return col, row
        else:
            return -1, -1

    # ----------------------------------------

    def reset(self):

        for lst in self.cells:
            for cell in lst:
                cell.reset()
