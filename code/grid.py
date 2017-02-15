"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense grid class
[E] ender.prime@gmail.com
[F] grid.py
[V] 02.14.17
"""

from bool import *
from cell import *
from const import *

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

    BASE = (21, 13)                             # base area dimensions
    SPACE = (3, 0)                              # space around base area

    COLS = (2 * SPACE[0]) + BASE[0]             # total columns
    ROWS = (2 * SPACE[1]) + BASE[1]             # total rows

    INDEXES = (COLS, ROWS)                      # total dimensions
    CENTER = (COLS // 2, ROWS // 2)             # center index
    FUZZ = 1 - (1 / (COLS * ROWS))              # used in pathfinding

    WIDTH = COLS * Cell.DIM                     # width in pixels
    HEIGHT = ROWS * Cell.DIM                    # height in pixels

    BASE_EAST = BASE[0] + SPACE[0] - 1          # base area east column value
    BASE_NORTH = SPACE[1]                       # base area north row value
    BASE_SOUTH = BASE[1] + SPACE[1] - 1         # base area south row value
    BASE_WEST = SPACE[0]                        # base area west column value

    BASE_NE = BASE_EAST, BASE_NORTH             # base area northeast index
    BASE_NW = BASE_WEST, BASE_NORTH             # base area northwest index
    BASE_SE = BASE_EAST, BASE_SOUTH             # base area southeast index
    BASE_SW = BASE_WEST, BASE_SOUTH             # base area southwest index

    BASE_BOUNDS = BASE_NW + BASE_SE             # base area index bounds
    
    PATH_START = (BASE_WEST - 1, CENTER[1])     # first index on main path
    PATH_GOAL = (BASE_EAST + 1, CENTER[1])      # last index on main path

    # ----------------------------------------

    def __init__(self, x = 0, y = 0):

        # (x, y) == top left point
        self.x = x
        self.y = y

        self.cells = []     # 2d array of cell objects

        for col in range(Grid.COLS):
            lst = []
            for row in range(Grid.ROWS):
                x = self.west + (col * Cell.DIM) + Cell.HALF - 1
                y = self.north + (row * Cell.DIM) + Cell.HALF - 1

                cell = Cell()
                cell.col = col
                cell.row = row
                cell.x = x
                cell.y = y

                colBase = bool(Grid.BASE_WEST <= col <= Grid.BASE_EAST)
                rowBase = bool(Grid.BASE_NORTH <= row <= Grid.BASE_SOUTH)
                if bool(colBase and rowBase):
                    cell.base = True
                if not rowBase:
                    cell.open = False

                if col >= Grid.BASE_EAST:
                    cell.gx = Cell.MOVE_COST

                lst.append(cell)
            self.cells.append(lst)

        self.path = self.pathfinder()       # main path index list

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

        cols, rows = Grid.indexes()
        return cols * rows

    # ----------------------------------------

    def __repr__(self):

        return 'Grid' + str(self.xy)

    # ----------------------------------------

    def __str__(self):

        cols, rows = Grid.indexes()

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

        return Cell.MOVE_COST * hx * Grid.FUZZ

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

        return Cell.MOVE_COST * hx * Grid.FUZZ

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

        return Cell.MOVE_COST * hx * Grid.FUZZ

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

        return Cell.MOVE_COST * hx * Grid.FUZZ

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

    @property
    def bounds(self):
        """
        :return: bounding box points: (west, north, east, south)
        """
        return self.NW + self.SE

    # ----------------------------------------

    @property
    def center(self):
        """
        :return: center point: (x, y)
        """
        x = self.west + (Grid.WIDTH // 2)
        y = self.north + (Grid.HEIGHT // 2)

        return x, y

    # ----------------------------------------

    @property
    def east(self):
        """
        :return: east x value
        """
        return self.x + Grid.WIDTH - 1

    # ----------------------------------------

    @property
    def north(self):
        """
        :return: north y value
        """
        return self.y

    # ----------------------------------------

    @property
    def NE(self):
        """
        :return: northeast point: (x, y)
        """
        return self.east, self.north

    # ----------------------------------------

    @property
    def NW(self):
        """
        :return: northwest point: (x, y)
        """
        return self.west, self.north

    # ----------------------------------------

    @property
    def south(self):
        """
        :return: south y value
        """
        return self.y + Grid.HEIGHT - 1

    # ----------------------------------------

    @property
    def SE(self):
        """
        :return: southeast point: (x, y)
        """
        return self.east, self.south

    # ----------------------------------------

    @property
    def SW(self):
        """
        :return: southwest point: (x, y)
        """
        return self.west, self.south

    # ----------------------------------------

    @property
    def west(self):
        """
        :return: west x value
        """
        return self.x

    # ----------------------------------------

    @property
    def xy(self):
        """
        :return: base point at top left: (x, y)
        """
        return self.x, self.y

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
                if self.cells[col][row].open:
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
                if self.cells[col][row].open:
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
                if self.cells[col][row].open:
                    if n in Grid.ADJACENT_DIAG:
                        c1, r1 = (col, rowBase)
                        c2, r2 = (colBase, row)
                        if self.cells[c1][r1].open and self.cells[c2][r2].open:
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

    def pathfinder(self):
        """
        update path destination indexes for all cells
        :return: main path index list from Grid.PATH_START to Grid.PATH_GOAL
        """
        for lst in self.cells:
            for cell in lst:
                cell.path = None

        grid = copy.deepcopy(self.cells)
        xStart, yStart = Grid.PATH_START
        xGoal, yGoal = Grid.PATH_GOAL

        openSet = {}
        closedSet = {}

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
                    node.hx = Grid.hxDiagonal(Grid.PATH_GOAL, index)
                    node.parent = current
                    openSet.update({index: node.fx})

        for lst in self.cells:
            for cell in lst:
                x, y = cell.index
                cell.path = grid[x][y].parent

        cell = grid[xStart][yStart]
        path = [cell.index]
        while (cell.index != Grid.PATH_GOAL) and bool(cell.parent):
            path.append(cell.parent)
            x, y = cell.parent
            cell = grid[x][y]

        return path

    # ----------------------------------------

    def pointIsValid(self, point):
        """
        :param point: (x, y)
        :return: true if point is within grid bounds
        """
        if bool(point):
            x, y = point
            xValid = bool(self.west <= x <= self.east)
            yValid = bool(self.north <= y <= self.south)
            return bool(xValid and yValid)
        else:
            return False

    # ----------------------------------------

    def pointToIndex(self, point):
        """
        :param point: (x, y)
        :return: cell index: (column, row) at point, or None if point is outside bounds
        """
        if self.pointIsValid(point):
            x = int(round(point[0], 0))
            y = int(round(point[1], 0))
            x = x - self.west
            y = y - self.north
            col = x // Cell.DIM
            row = y // Cell.DIM
            return col, row
        else:
            return None

    # ----------------------------------------

    def reset(self):
        """
        :return: reset grid to new game conditions
        """
        for lst in self.cells:
            for cell in lst:
                cell.reset()

        self.pathUpdate()
