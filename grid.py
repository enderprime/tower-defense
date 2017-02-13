"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense grid class
[E] ender.prime@gmail.com
[F] grid.py
[V] 02.13.17
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
    BASE = (21, 13)                         # base area dimensions: (columns, rows)
    SPACE = (3, 0)                          # space around base area: (columns, rows)

    COLS = (2 * SPACE[0]) + BASE[0]         # total columns
    ROWS = (2 * SPACE[1]) + BASE[1]         # total rows

    INDEXES = (COLS, ROWS)                  # total dimensions
    CENTER = (COLS // 2, ROWS // 2)         # center index
    FUZZ = 1 + (1 / (COLS * ROWS))          # used in pathfinding

    WIDTH = COLS * Cell.DIM                 # width in pixels
    HEIGHT = ROWS * Cell.DIM                # height in pixels

    # relative indexes for adjacent cells
    ADJACENT_DIAG = ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1))
    ADJACENT_ORTHO = ((1, 0), (0, 1), (0, -1), (-1, 0))

    BASE_EAST = BASE[0] + SPACE[0] - 1      # base area east column value
    BASE_NORTH = SPACE[1]                   # base area north row value
    BASE_SOUTH = BASE[1] + SPACE[1] - 1     # base area south row value
    BASE_WEST = SPACE[0]                    # base area west column value

    BASE_NE = BASE_EAST, BASE_NORTH         # base area northeast index: (column, row)
    BASE_NW = BASE_WEST, BASE_NORTH         # base area northwest index: (column, row)
    BASE_SE = BASE_EAST, BASE_SOUTH         # base area southeast index: (column, row)
    BASE_SW = BASE_WEST, BASE_SOUTH         # base area southwest index: (column, row)

    BASE_BOUNDS = BASE_NW + BASE_SE         # base area index bounds: (west, north, east, south)

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

                lst.append(cell)
            self.cells.append(lst)

        self.start = (Grid.BASE_WEST - 1, Grid.CENTER[1])   # first index on main path
        self.goal = (Grid.BASE_EAST + 1, Grid.CENTER[1])    # last index on main path
        self.path = []                                      # main path index list
        self.pathMain()

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

        for n in Grid.ADJACENT_DIAG:
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

        return math.hypot(a, b) * Grid.FUZZ

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
        a = xStart - xGoal
        b = yStart - yGoal

        return (abs(a) + abs(b)) * Grid.FUZZ

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
        a = xStart - xGoal
        b = yStart - yGoal

        return max(abs(a), abs(b)) * Grid.FUZZ

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

        for n in Grid.ADJACENT_DIAG:
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

        for n in ((1, 0), (0, 1), (0, -1), (-1, 0)):
            colStep, rowStep = n
            col = colBase + colStep
            row = rowBase + rowStep
            adj = (col, row)
            if Grid.indexIsValid(adj):
                if self.cells[col][row].open:
                    lst.append(adj)

        for n in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            colStep, rowStep = n
            col = colBase + colStep
            row = rowBase + rowStep
            adj = (col, row)
            if Grid.indexIsValid(adj):
                if self.cells[col][row].open:
                    c1, r1 = (col, rowBase)
                    c2, r2 = (colBase, row)
                    if self.cells[c1][r1].open and self.cells[c2][r2].open:
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

    def pathCreep(self, start, goal):
        """
        :param start: (column, row)
        :param goal: (column, row)
        :return: list of indexes on path to goal
        """
        lst = []
        openSet = {}
        closedSet = {}

        if start in self.path:
            n = self.path.index(start) + 1
            lst = self.path[n:]
        else:
            grid = copy.deepcopy(self.cells)

            xStart, yStart = start
            node = grid[xStart][yStart]
            node.parent = None
            openSet.update({start: 0})

            while bool(openSet):

                current = x, y = min(openSet, key = openSet.get)
                del openSet[current]
                closedSet.update({current: None})

                if (current == goal) or (x == (Grid.BASE_EAST + 1)) or (current in self.path):
                    break

                for index in self.adjOpenPath(current):
                    xAdj, yAdj = index
                    node = grid[xAdj][yAdj]
                    if (abs(x - xAdj) + abs(y - yAdj)) == 2:
                        gx = grid[x][y].gx + 14
                    else:
                        gx = grid[x][y].gx + 10
                    if gx < node.gx:
                        if index in openSet: del openSet[index]
                        if index in closedSet: del closedSet[index]
                    if (not (index in openSet)) and (not (index in closedSet)):
                        node.gx = gx
                        node.hx = 10 * Grid.hxUniform(start, goal)
                        node.parent = current
                        openSet.update({index: node.fx})

            x, y = current
            node = grid[x][y]
            if bool(node.parent):
                lst.append(current)
                while bool(node.parent):
                    if node.parent == start:
                        break
                    x, y = node.parent
                    node = grid[x][y]
                lst.reverse()

        return lst

    # ----------------------------------------

    def pathGrid(self):
        """
        :return: list of indexes on main path
        """
        lst = []
        openSet = {}
        closedSet = {}

        grid = copy.deepcopy(self.cells)
        xStart, yStart = self.start

        node = grid[xStart][yStart]
        node.parent = None
        openSet.update({self.start: 0})

        while bool(openSet):
            current = x, y = min(openSet, key = openSet.get)
            del openSet[current]
            closedSet.update({current: None})

            if x == (Grid.BASE_EAST + 1):
                break

            if x == Grid.BASE_WEST:
                yStart = y
                node = grid[x][y]
                node.parent = (xStart, yStart)
                node = grid[xStart][yStart]
                node.parent = None

            for index in self.adjOpenPath(current):
                xAdj, yAdj = index
                node = grid[xAdj][yAdj]
                if (abs(x - xAdj) + abs(y - yAdj)) == 2:
                    gx = grid[x][y].gx + 14
                else:
                    gx = grid[x][y].gx + 10
                if gx < node.gx:
                    if index in openSet: del openSet[index]
                    if index in closedSet: del closedSet[index]
                if (not (index in openSet)) and (not (index in closedSet)):
                    node.gx = gx
                    node.hx = 10 * Grid.hxUniform(self.start, self.goal)
                    node.parent = current
                    openSet.update({index: node.fx})

        x, y = current
        node = grid[x][y]
        if bool(node.parent):
            lst.append(current)
            while bool(node.parent):
                lst.append(node.parent)
                x, y = node.parent
                node = grid[x][y]
            lst.reverse()

        return lst

    # ----------------------------------------

    def pathMain(self):
        """
        update grid start, grid goal, and main path
        :return: none
        """
        path = self.pathGrid()

        if bool(path):
            self.path = path
            self.start = path[0]
            self.goal = path[-1]

            for col in range(Grid.COLS):
                for row in range(Grid.ROWS):
                    self.cells[col][row].path = False

            for n in path:
                col, row = n
                self.cells[col][row].path = True

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
            x, y = point
            x = x - self.west
            y = y - self.north
            col = int(x // Cell.DIM)
            row = int(y // Cell.DIM)
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
