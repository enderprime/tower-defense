"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense grid class
[E] ender.prime@gmail.com
[F] grid.py
[V] 03.05.17
"""

from boolean import *
from cell import *
from constant import *

import copy
import math

# --------------------------------------------------------------------------------------------------------------------

class Grid(object):
    """
    represents game board using 2d array of cells
    """

    # relative indexes for adjacent cells
    ADJACENT_ALL = ((-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1))
    ADJACENT_DIAG = ((-1, 1), (-1, -1), (1, 1), (1, -1))
    ADJACENT_ORTHO = ((-1, 0), (0, 1), (0, -1), (1, 0))

    # index dimensions
    BASE = (21, 13)
    SPACE = (3, 0)

    COLS = BASE[0] + (2 * SPACE[0])
    ROWS = BASE[1] + (2 * SPACE[1])
    INDEXES = (COLS, ROWS)

    # base index boundaries
    BASE_EAST = BASE[0] + SPACE[0] - 1
    BASE_NORTH = SPACE[1]
    BASE_SOUTH = BASE[1] + SPACE[1] - 1
    BASE_WEST = SPACE[0]

    BASE_CENTER = (COLS // 2, ROWS // 2)
    BASE_NE = (BASE_EAST, BASE_NORTH)
    BASE_NW = (BASE_WEST, BASE_NORTH)
    BASE_SE = (BASE_EAST, BASE_SOUTH)
    BASE_SW = (BASE_WEST, BASE_SOUTH)
    BASE_BOUNDS = BASE_NW + BASE_SE

    # main path
    PATH_FUZZ = 1 - (1 / (COLS * ROWS))
    PATH_START = (0, BASE_CENTER[1])
    PATH_GOAL = (BASE_EAST + SPACE[0] - 1, BASE_CENTER[1])

    # pixel dimensions
    WIDTH = COLS * Cell.DIM
    HEIGHT = ROWS * Cell.DIM

    # top left corner
    X = 0
    Y = 84
    XY = (X, Y)

    # grid coordinate boundaries
    XY_EAST = X + WIDTH - 1
    XY_NORTH = Y
    XY_SOUTH = Y + HEIGHT - 1
    XY_WEST = X

    XY_CENTER = (XY_WEST + (WIDTH // 2), XY_NORTH + (HEIGHT // 2))
    XY_NE = (XY_EAST, XY_NORTH)
    XY_NW = (XY_WEST, XY_NORTH)
    XY_SE = (XY_EAST, XY_SOUTH)
    XY_SW = (XY_WEST, XY_SOUTH)
    XY_BOUNDS = XY_NW + XY_SE

    # base coordinate boundaries
    XY_BASE_EAST = X + ((BASE[0] + SPACE[0]) * Cell.DIM) - 1
    XY_BASE_NORTH = Y + (SPACE[1] * Cell.DIM) - 1
    XY_BASE_SOUTH = Y + ((BASE[1] + SPACE[1]) * Cell.DIM) - 1
    XY_BASE_WEST = X + (SPACE[0] * Cell.DIM) - 1

    XY_BASE_NE = (XY_BASE_EAST, XY_BASE_NORTH)
    XY_BASE_NW = (XY_BASE_WEST, XY_BASE_NORTH)
    XY_BASE_SE = (XY_BASE_EAST, XY_BASE_SOUTH)
    XY_BASE_SW = (XY_BASE_WEST, XY_BASE_SOUTH)
    XY_BASE_BOUNDS = XY_BASE_NW + XY_BASE_SE

    # ----------------------------------------

    def __init__(self):

        self.cells = []     # 2d array of cell objects

        for col in range(Grid.COLS):
            lst = []
            for row in range(Grid.ROWS):

                cell = Cell()
                cell.col = col
                cell.row = row
                cell.x = Grid.XY_WEST + (col * Cell.DIM) + Cell.HALF - 1
                cell.y = Grid.XY_NORTH + (row * Cell.DIM) + Cell.HALF - 1

                colBase = bool(Grid.BASE_WEST <= col <= Grid.BASE_EAST)
                rowBase = bool(Grid.BASE_NORTH <= row <= Grid.BASE_SOUTH)
                if bool(colBase and rowBase):
                    cell.base = True
                if not rowBase:
                    cell.pathable = False

                lst.append(cell)
            self.cells.append(lst)

        self.pathfinder()

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

        cols, rows = Grid.INDEXES
        return cols * rows

    # ----------------------------------------

    def __repr__(self):

        return 'Grid()'

    # ----------------------------------------

    def __str__(self):

        cols, rows = Grid.INDEXES

        s = ''
        for row in range(rows):
            s = s + '['
            for col in range(cols):
                s = s + str(self.cells[col][row])
                if col < cols - 1:
                    s = s + ', '
            s = s + ']\n'

        return s

    # ----------------------------------------

    @classmethod
    def adjacent(cls, index):
        """
        :param index: (col, row)
        :return: list of adjacent indexes
        """
        colBase, rowBase = index
        lst = []

        for n in Grid.ADJACENT_ALL:
            colStep, rowStep = n
            col = colBase + colStep
            row = rowBase + rowStep
            adj = (col, row)
            if Grid.indexIsValid(adj):
                lst.append(adj)

        return lst

    # ----------------------------------------

    @classmethod
    def angle(cls, start, goal):
        """
        :param start: (column, row)
        :param goal: (column, row)
        :return: angle in radians from start to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal

        xStep = xGoal - xStart
        yStep = yStart - yGoal
        step = (xStep, yStep)

        if step == (1, 0):      angle = 0.0
        elif step == (1, 1):    angle = math.pi / 4
        elif step == (0, 1):    angle = math.pi / 2
        elif step == (-1, 1):   angle = 3 * math.pi / 4
        elif step == (-1, 0):   angle = math.pi
        elif step == (-1, -1):  angle = 5 * math.pi / 4
        elif step == (0, -1):   angle = 3 * math.pi / 2
        elif step == (1, -1):   angle = 7 * math.pi / 4
        else:                   angle = math.atan2(yStep, xStep)

        return angle

    # ----------------------------------------

    @classmethod
    def gx(cls, start, goal):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :return: movement cost from start to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = abs(xStart - xGoal)
        b = abs(yStart - yGoal)

        if (a - b) == 0:
            return Cell.MOVE_DIAG
        else:
            return Cell.MOVE_COST

    # ----------------------------------------

    @classmethod
    def hxDiagonal(cls, start, goal):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :return: heuristic: diagonal distance to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = abs(xStart - xGoal)
        b = abs(yStart - yGoal)
        hx = ((a + b) - (6 * min(a, b)))

        return Cell.MOVE_COST * hx * Grid.PATH_FUZZ

    # ----------------------------------------

    @classmethod
    def hxEuclid(cls, start, goal):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :return: heuristic: euclidean distance to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = xStart - xGoal
        b = yStart - yGoal
        hx = math.hypot(a, b)

        return Cell.MOVE_COST * hx * Grid.PATH_FUZZ

    # ----------------------------------------

    @classmethod
    def hxManhattan(cls, start, goal):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :return: heuristic: manhattan distance to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = abs(xStart - xGoal)
        b = abs(yStart - yGoal)
        hx = (a + b)

        return Cell.MOVE_COST * hx * Grid.PATH_FUZZ

    # ----------------------------------------

    @classmethod
    def hxUniform(cls, start, goal):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :return: heuristic: uniform cost distance to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = abs(xStart - xGoal)
        b = abs(yStart - yGoal)
        hx = max(a, b)

        return Cell.MOVE_COST * hx * Grid.PATH_FUZZ

    # ----------------------------------------

    @classmethod
    def indexIsValid(cls, index):
        """
        :param index: (column, row)
        :return: true if index is within grid bounds
        """
        if bool(index):
            col, row = index
            return bool((-1 < col < Grid.COLS) and (-1 < row < Grid.ROWS))
        else:
            return False

    # ----------------------------------------

    @classmethod
    def pointIsValid(cls, point):
        """
        :param point: (x, y)
        :return: true if point is within grid bounds
        """
        if bool(point):
            x, y = point
            xValid = bool(Grid.XY_WEST <= x <= Grid.XY_EAST)
            yValid = bool(Grid.XY_NORTH <= y <= Grid.XY_SOUTH)
            return bool(xValid and yValid)
        else:
            return False

    # ----------------------------------------

    @classmethod
    def pointToIndex(cls, point):
        """
        :param point: (x, y)
        :return: cell index: (column, row) at point, or None if point is outside bounds
        """
        x, y = point

        if Grid.pointIsValid((x, y)):
            x = x - Grid.XY_WEST
            y = y - Grid.XY_NORTH
            col = int(round(x // Cell.DIM, 0))
            row = int(round(y // Cell.DIM, 0))
            return col, row
        else:
            return None

    # ----------------------------------------

    def adjOpenDiag(self, index):
        """
        :param index: (col, row)
        :return: list of adjacent open indexes, with diagonals
        """
        colBase, rowBase = index
        lst = []

        for n in Grid.ADJACENT_ALL:
            colStep, rowStep = n
            col = colBase + colStep
            row = rowBase + rowStep
            adj = (col, row)
            if Grid.indexIsValid(adj):
                if self.cells[col][row].pathable:
                    lst.append(adj)

        return lst

    # ----------------------------------------

    def adjOpenOrtho(self, index):
        """
        :param index: (column, row)
        :return: list of adjacent open indexes, without diagonals
        """
        colBase, rowBase = index
        lst = []

        for n in Grid.ADJACENT_ORTHO:
            colStep, rowStep = n
            col = colBase + colStep
            row = rowBase + rowStep
            adj = (col, row)
            if Grid.indexIsValid(adj):
                if self.cells[col][row].pathable:
                    lst.append(adj)

        return lst

    # ----------------------------------------

    def adjOpenPath(self, index):
        """
        :param index: (column, row)
        :return: list of adjacent open indexes, with pathfinder diagonals
        pathfinder diagonal ex: northwest is open only if north and west are also open
        """
        colBase, rowBase = index
        lst = []

        for n in Grid.ADJACENT_ALL:
            colStep, rowStep = n
            col = colBase + colStep
            row = rowBase + rowStep
            adj = (col, row)
            if Grid.indexIsValid(adj):
                if self.cells[col][row].pathable:
                    if n in Grid.ADJACENT_DIAG:
                        c1, r1 = (col, rowBase)
                        c2, r2 = (colBase, row)
                        if self.cells[c1][r1].pathable and self.cells[c2][r2].pathable:
                            lst.append(adj)
                    else:
                        lst.append(adj)

        return lst

    # ----------------------------------------

    def indexToPoint(self, index):
        """
        :param index: (column, row)
        :return: base point: (x, y) of cell at index, or None if index is outside bounds
        """
        if Grid.indexIsValid(index):
            col, row = index
            return self.cells[col][row].xy
        else:
            return None

    # ----------------------------------------

    def path(self, start = None):
        """
        :param start: (column, row)
        :return: list of indexes from start to Grid.PATH_GOAL
        """
        path = []

        if not bool(start):
            start = Grid.PATH_START

        xStart, yStart = start
        cell = self.cells[xStart][yStart]

        while (cell.index != Grid.PATH_GOAL) and bool(cell.path):
            path.append(cell.path)
            x, y = cell.path
            cell = self.cells[x][y]

        return path

    # ----------------------------------------

    def pathfinder(self):
        """
        update path destination indexes for all cells
        :return: none
        """
        for lst in self.cells:
            for cell in lst:
                cell.path = None

        grid = copy.deepcopy(self.cells)
        openSet = {}
        closedSet = {}

        xGoal, yGoal = Grid.PATH_GOAL
        node = grid[xGoal][yGoal]
        node.parent = None
        openSet.update({Grid.PATH_GOAL: 0})

        while bool(openSet):

            current = x, y = min(openSet, key = openSet.get)
            del openSet[current]
            closedSet.update({current: None})

            for index in self.adjOpenPath(current):
                xAdj, yAdj = index
                node = grid[xAdj][yAdj]
                gx = grid[x][y].gx + Grid.gx(current, index)
                if gx < node.gx:
                    if index in openSet: del openSet[index]
                    if index in closedSet: del closedSet[index]
                if (not (index in openSet)) and (not (index in closedSet)):
                    node.gx = gx
                    node.hx = Grid.hxDiagonal(index, Grid.PATH_GOAL)
                    node.parent = current
                    openSet.update({index: node.fx})

        for lst in self.cells:
            for cell in lst:
                x, y = cell.index
                cell.path = grid[x][y].parent

    # ----------------------------------------

    def reset(self):
        """
        :return: reset grid to new game conditions
        """
        for lst in self.cells:
            for cell in lst:
                cell.reset()

        self.pathfinder()
