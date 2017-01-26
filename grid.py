"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense grid class
[E] ender.prime@gmail.com
[F] grid.py
[V] 01.25.17
"""

from bool import *
from cell import *
from const import *

# --------------------------------------------------------------------------------------------------------------------

class Grid(object):

    BASE = (21, 15)
    SPACE = (3, 2)

    # ----------------------------------------

    def __init__(self, x, y):

        cols, rows = Grid.indexes()

        self.x = x
        self.y = y

        self.base = []
        self.cells = []
        self.space = []

        for col in range(cols):

            listBase = []
            listCells = []
            listSpace = []

            for row in range(rows):

                x = self.west + (col * Cell.DIM) + Cell.HALF
                y = self.north + (row * Cell.DIM) + Cell.HALF

                cell = Cell(x, y)
                cell.col = col
                cell.row = row

                if Grid.indexIsBase(cell.index):
                    cell.base = True
                    listBase.append(cell)
                else:
                    listSpace.append(cell)

                listCells.append(cell)

            if bool(listBase):
                self.base.append(listBase)

            self.cells.append(listCells)
            self.space.append(listSpace)

        self.path = []

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
        :param index: (column, row)
        :return: list of valid adjacent indexes
        """
        baseCol, baseRow = index
        lst = []

        for n in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            colStep, rowStep = n
            adjCol = baseCol + colStep
            adjRow = baseRow + rowStep
            adjIndex = (adjCol, adjRow)
            if Grid.indexIsValid(adjIndex):
                lst.append(adjIndex)

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
    def indexIsBase(cls, index):
        """
        :param index: (column, row)
        :return: true if index is within base area bounds
        """
        col, row = index

        colBase = bool(Grid.baseWest() <= col <= Grid.baseEast())
        rowBase = bool(Grid.baseNorth() <= row <= Grid.baseSouth())

        return bool(colBase and rowBase)

    # ----------------------------------------

    @classmethod
    def indexIsValid(cls, index):
        """
        :param index: (column, row)
        :return: true if index is within grid bounds
        """
        col, row = index
        cols, rows = Grid.indexes()

        colValid = bool(-1 < col < cols)
        rowValid = bool(-1 < row < rows)

        return bool(colValid and rowValid)

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

    def pointIsValid(self, point):
        """
        :param point: (x, y)
        :return: true if point is within grid bounds
        """
        x, y = point

        xValid = bool(self.west <= x < self.east)
        yValid = bool(self.north <= y < self.south)

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
