"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense grid class
[E] ender.prime@gmail.com
[F] grid.py
[V] 02.10.17
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
    BASE = (21, 13)
    SPACE = (3, 0)

    # ----------------------------------------

    def __init__(self, x = 0, y = 0):

        # (x, y) == top left point
        self.x = x
        self.y = y

        cols, rows = Grid.indexes()
        self.fuzz = 1 + (1 / (cols * rows))

        self.cells = []
        for col in range(cols):
            lst = []
            for row in range(rows):
                x = self.west + (col * Cell.DIM) + Cell.half() - 1
                y = self.north + (row * Cell.DIM) + Cell.half() - 1

                cell = Cell()
                cell.col = col
                cell.row = row
                cell.x = x
                cell.y = y

                colBase = bool(Grid.baseWest() <= col <= Grid.baseEast())
                rowBase = bool(Grid.baseNorth() <= row <= Grid.baseSouth())
                if bool(colBase and rowBase):
                    cell.base = True
                if not rowBase:
                    cell.open = False

                lst.append(cell)
            self.cells.append(lst)

        center = Grid.baseCenter()
        self.start = (Grid.baseWest() - 1, center[1])
        self.goal = (Grid.baseEast() + 1, center[1])
        self.path = []
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

        for n in ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)):
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
    def baseBounds(cls):
        """
        :return: base area index bounds: (west, north, east, south)
        """
        return Grid.baseNW() + Grid.baseSE()

    # ----------------------------------------

    @classmethod
    def baseCenter(cls):
        """
        :return: base area center index: (column, row)
        """
        cols, rows = Grid.indexes()
        return (cols // 2), (rows // 2)

    # ----------------------------------------

    @classmethod
    def baseEast(cls):
        """
        :return: base area east column value
        """
        return Grid.BASE[0] + Grid.SPACE[0] - 1

     # ----------------------------------------

    @classmethod
    def baseNorth(cls):
        """
        :return: base area north row value
        """
        return Grid.SPACE[1]

    # ----------------------------------------

    @classmethod
    def baseNE(cls):
        """
        :return: base area northeast index: (column, row)
        """
        return Grid.baseEast(), Grid.baseNorth()

    # ----------------------------------------

    @classmethod
    def baseNW(cls):
        """
        :return: base area northwest index: (column, row)
        """
        return Grid.baseWest(), Grid.baseNorth()

    # ----------------------------------------

    @classmethod
    def baseSouth(cls):
        """
        :return: base area south row value
        """
        return Grid.BASE[1] + Grid.SPACE[1] - 1

    # ----------------------------------------

    @classmethod
    def baseSE(cls):
        """
        :return: base area southeast index: (column, row)
        """
        return Grid.baseEast(), Grid.baseSouth()

    # ----------------------------------------

    @classmethod
    def baseSW(cls):
        """
        :return: base area southwest index: (column, row)
        """
        return Grid.baseWest(), Grid.baseSouth()

    # ----------------------------------------

    @classmethod
    def baseWest(cls):
        """
        :return: base area west column value
        """
        return Grid.SPACE[0]

    # ----------------------------------------

    @classmethod
    def height(cls):
        """
        :return: height in pixels
        """
        cols, rows = Grid.indexes()
        return rows * Cell.DIM

    # ----------------------------------------

    @classmethod
    def indexes(cls):
        """
        :return: cell array dimensions: (columns, rows)
        """
        baseCols, baseRows = Grid.BASE
        spaceCols, spaceRows = Grid.SPACE

        cols = (2 * spaceCols) + baseCols
        rows = (2 * spaceRows) + baseRows

        return cols, rows

    # ----------------------------------------

    @classmethod
    def indexIsValid(cls, index):
        """
        :param index: (column, row)
        :return: true if index is within grid bounds
        """
        if bool(index):
            col, row = index
            cols, rows = Grid.indexes()
            return bool((-1 < col < cols) and (-1 < row < rows))
        else:
            return False

    # ----------------------------------------

    @classmethod
    def width(cls):
        """
        :return: width in pixels
        """
        cols, rows = Grid.indexes()
        return cols * Cell.DIM

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
        x = self.west + (Grid.width() // 2)
        y = self.north + (Grid.height() // 2)

        return x, y

    # ----------------------------------------

    @property
    def east(self):
        """
        :return: east x value
        """
        return self.x + Grid.width() - 1

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
        return self.y + Grid.height() - 1

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

        for n in ((1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)):
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

        for n in ((1, 0), (0, 1), (0, -1), (-1, 0)):
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

    def hxEuclid(self, start, goal):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :return: heuristic: euclidean distance to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = xStart - xGoal
        b = yStart - yGoal

        return math.hypot(a, b) * self.fuzz

    # ----------------------------------------

    def hxManhattan(self, start, goal):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :return: heuristic: manhattan distance to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = xStart - xGoal
        b = yStart - yGoal

        return (abs(a) + abs(b)) * self.fuzz

    # ----------------------------------------

    def hxUniform(self, start, goal):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :return: heuristic: uniform cost distance to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = xStart - xGoal
        b = yStart - yGoal

        return max(abs(a), abs(b)) * self.fuzz

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

    def pathCreep(self, start):
        """
        :param start: (column, row)
        :return: list of indexes on path that connects start to main path
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

            if xStart < self.start[0]:
                goal = self.start
            else:
                row = 0
                index = (xStart, row)
                while not (index in self.path):
                    row = row + 1
                    index = (xStart, row)
                goal = index

            node = grid[xStart][yStart]
            node.parent = None
            openSet.update({start: 0})

            while bool(openSet):
                current = min(openSet, key = openSet.get)
                del openSet[current]
                closedSet.update({current: None})

                if current in self.path:
                    break

                x, y = current
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
                        node.hx = 10 * self.hxEuclid(index, goal)
                        node.parent = current
                        openSet.update({index: node.fx})

            x, y = current
            node = grid[x][y]
            if bool(node.parent):
                lst.append(current)
                while bool(node.parent):
                    if node.parent != start:
                        lst.append(node.parent)
                    x, y = node.parent
                    node = grid[x][y]
                lst.reverse()

                if current != self.goal:
                    n = self.path.index(current) + 1
                    lst = lst + self.path[n:]

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
        xGoal, yGoal = self.goal

        node = grid[xStart][yStart]
        node.parent = None
        openSet.update({self.start: 0})

        while bool(openSet):
            current = min(openSet, key = openSet.get)
            del openSet[current]
            closedSet.update({current: None})

            x, y = current
            yGoal = y
            goal = (xGoal, yGoal)

            if x == Grid.baseWest():
                yStart = y
                node = grid[x][y]
                node.parent = (xStart, yStart)
                node = grid[xStart][yStart]
                node.parent = None

            if x == Grid.baseEast() + 1:
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
                    node.hx = 10 * self.hxEuclid(index, goal)
                    node.parent = current
                    openSet.update({index: node.fx})

        node = grid[xGoal][yGoal]
        if bool(node.parent):
            lst.append(goal)
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
        self.path = self.pathGrid()
        self.start = self.path[0]
        self.goal = self.path[-1]

        cols, rows = Grid.indexes()
        for col in range(cols):
            for row in range(rows):
                self.cells[col][row].path = False

        for n in self.path:
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
