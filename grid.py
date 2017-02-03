"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense grid class
[E] ender.prime@gmail.com
[F] grid.py
[V] 02.03.17
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
    BASE = (19, 13)
    SPACE = (2, 1)

    # ----------------------------------------

    def __init__(self, x = 0, y = 0):

        # (x, y) == top left point
        self.x = x
        self.y = y

        self.base = {}
        self.cells = []
        self.space = {}

        cols, rows = Grid.indexes()
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
                    self.base.update({cell.index: None})
                else:
                    self.space.update({cell.index: None})
                lst.append(cell)
            self.cells.append(lst)

        self.fuzz = 1 + (1 / (cols * rows))
        self.start = self.pathStart()
        self.goal = self.pathGoal()
        self.path = [self.start] + self.pathfinder(self.start, self.goal)

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
    def adjacent(cls, index, diag = False, path = False):
        """
        :param index: (col, row)
        :param diag: true if diagonals allowed
        :param path: true if pathfinding restrictions
        :return: list of valid adjacent indexes
        """
        colBase, rowBase = index
        lst = []

        for n in ((1, 0), (0, 1), (0, -1), (-1, 0)):
            colStep, rowStep = n
            col = colBase + colStep
            row = rowBase + rowStep
            adj = (col, row)
            if Grid.indexIsValid(adj):
                lst.append(adj)

        if diag:
            for n in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                colStep, rowStep = n
                colAdj = colBase + colStep
                rowAdj = rowBase + rowStep
                adj = (colAdj, rowAdj)
                if Grid.indexIsValid(adj):
                    if path:
                        c1, r1 = (colAdj, rowBase)
                        c2, r2 = (colBase, rowAdj)
                        if grid.cells[c1][r1].open and grid.cells[c2][r2].open:
                            lst.append(adj)
                    else:
                        lst.append(adj)

        return lst

    # ----------------------------------------

    @classmethod
    def baseBounds(cls):
        """
        :return: base area index bounds: ((west, north), (east, south))
        """
        return Grid.baseNW(), Grid.baseSE()

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
        col, row = index
        cols, rows = Grid.indexes()

        return bool((-1 < col < cols) and (-1 < row < rows))

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
        :return: bounding box points: ((west, north), (east, south))
        """
        return self.NW, self.SE

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

    def hx(self, start, goal, diag = False):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :param diag: true if diagonals allowed
        :return: heuristic: distance to goal
        """
        xStart, yStart = start
        xGoal, yGoal = goal
        a = xStart - xGoal
        b = yStart - yGoal

        if diag:
            distance = math.hypot(a, b)
        else:
            distance = abs(a) + abs(b)

        return distance * self.fuzz

    # ----------------------------------------

    def indexToPoint(self, index):
        """
        :param index: (column, row)
        :return: base point: (x, y) of cell at index, or (-1, -1) if index is outside bounds
        """
        if Grid.indexIsValid(index):
            col, row = index
            return self.cells[col][row].xy
        else:
            return -1, -1

    # ----------------------------------------

    def pathfinder(self, start, goal, diag = False):
        """
        :param start: (x, y)
        :param goal: (x, y)
        :param diag: true if diagonals allowed
        :return: list of indexes on path to goal
        """
        lst = []
        openSet = {}
        closedSet = {}

        if not (start == goal):
            grid = copy.deepcopy(self.cells)
            xStart, yStart = start
            xGoal, yGoal = goal

            node = grid[xStart][yStart]
            node.gx = 0
            node.hx = self.hx(start, goal, diag)
            node.parent = None
            openSet.update({start: node.fx})

            while bool(openSet) and (not (goal in openSet)):
                current = min(openSet, key = openSet.get)
                x, y = current
                del openSet[current]
                closedSet.update({current: None})

                for index in Grid.adjacent(current, diag, True):
                        xAdj, yAdj = index
                        node = grid[xAdj][yAdj]
                        if node.base and node.open:
                            gx = grid[x][y].gx + 1
                            if gx < node.gx:
                                if index in openSet: del openSet[index]
                                if index in closedSet: del closedSet[index]
                            if (not (index in openSet)) and (not (index in closedSet)):
                                node.gx = gx
                                node.hx = self.hx(index, goal, diag)
                                node.parent = current
                                openSet.update({index: node.fx})

            node = grid[xGoal][yGoal]
            if bool(node.parent):
                lst.append(goal)
                while bool(node.parent):
                    if not (node.parent == start):
                        lst.append(node.parent)
                    x, y = node.parent
                    node = grid[x][y]
                lst.reverse()

        return lst

    # ----------------------------------------

    def pathGoal(self):
        """
        :return: path goal index: (column, row)
        """
        cols, rows = Grid.BASE
        col = Grid.baseEast()
        row = Grid.baseCenter()[1]

        if not self.cells[col][row].open:
            for i in range(rows // 2):
                row = row + i
                if self.cells[col][row].open:
                    break
                row = row - i
                if self.cells[col][row].open:
                    break

        return col, row

    # ----------------------------------------

    def pathStart(self):
        """
        :return: path starting index: (column, row)
        """
        cols, rows = Grid.BASE
        col = Grid.baseWest()
        row = Grid.baseCenter()[1]

        if not self.cells[col][row].open:
            for i in range(rows // 2):
                row = row + i
                if self.cells[col][row].open:
                    break
                row = row - i
                if self.cells[col][row].open:
                    break

        return col, row

    # ----------------------------------------

    def pointIsValid(self, point):
        """
        :param point: (x, y)
        :return: true if point is within grid bounds
        """
        x, y = point

        xValid = bool(self.west <= x <= self.east)
        yValid = bool(self.north <= y <= self.south)

        return bool(xValid and yValid)

    # ----------------------------------------

    def pointToIndex(self, point):
        """
        :param point: (x, y)
        :return: cell index: (column, row) at point, or (-1, -1) if point is outside bounds
        """
        if self.pointIsValid(point):
            x, y = point
            x = x - self.west
            y = y - self.north
            col = x // Cell.DIM
            row = y // Cell.DIM
            return col, row
        else:
            return -1, -1

    # ----------------------------------------

    def reset(self):
        """
        :return: reset grid to new game conditions
        """
        for lst in self.cells:
            for cell in lst:
                cell.reset()

        self.start = self.pathStart()
        self.goal = self.pathGoal()
        self.path = [self.start] + self.pathfinder(self.start, self.goal)
