from cell import Cell
import random

class World(object):

    @classmethod
    def from_file(cls, filename, worldType):
        """
        Given a properly formatted text file, return a new World object.
        :param filename: path and filename to the text file.
        :return: a new World object made from the text file.
        """
        with open(filename, 'r') as myFile:
            text = myFile.readlines()

        rows = len(text)
        columns = len(text[0])


        newWorld = worldType(rows, columns)
        for rowNumber, row in enumerate(text):
            for columnNumber, cellText in enumerate(row):
                if cellText == Cell.liveChar:
                    newWorld.set_cell(rowNumber, columnNumber, True)
        return newWorld


    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._grid = self.create_grid()
        self._livingCellCount = 0
        self._generation = 0
        self.create_neighbors()

    def __str__(self):
        """Return a string that represents the current generation. For example,
        a completely dead world (4x5) would look like this, assuming that
        Cell.deadChar is a period:
        .....
        .....
        .....
        .....
        A world (4x5) with one living cell would look like this, assuming
        that Cell.liveChar is an 'X' at position self.__grid[1][3]:
        .....
        ...X.
        .....
        .....
        Of course, you would not check on Cell.deadChar or Cell.liveChar. You
        would rely on the cell to know how it should be printed.
        """
        string = ''
        for row in self._grid:
            for cell in row:
                string += cell.__str__()
            string += '\n'
        return string

    def create_grid(self):
        """Return the grid as a list of lists. There should be one list
        to contain the entire grid and in that list there should be one
        list to contain each row in the generation. Each of the "row lists"
        should contain one object of class Cell for each column in the world."""

        grid = []
        for rowNumber in range(self._rows):
            row = []
            for columnNumber in range(self._columns):
                row.append(Cell(rowNumber, columnNumber))
            grid.append(row)
        return grid

    def create_neighbors(self):
        """Loop through the grid and assign the neighbors to each cell."""
        # print('---creating neighbors---')
        for row in self._grid:
            for cell in row:
                #
                # There are some nine situations that we have to account for:
                #
                # 1. upper left corner (3 neighbors)
                # 2. rest of the top row (5 neighbors)
                # 3. upper right corner (3 neighbors)
                # 4. far left side (5 neighbors)
                # 5. normal cells (8 neighbors)
                # 6. far right side (5 neighbors)
                # 7. lower left corner (3 neighbors)
                # 8. rest of bottom row (5 neighbors)
                # 9. lower right corner (3 neighbors)
                #
                row = cell.get_row()
                column = cell.get_column()
                # print(f'({row},{column})')
                # top row
                if row == 0:
                    # 1. upper left corner (3 neighbors)
                    if column == 0:
                        # print('upper left')
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column + 1])
                    # 2. rest of the top row (5 neighbors)
                    elif column < (self._columns - 1):
                        # print('upper row')
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row + 1][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column + 1])
                    # 3. upper right corner (3 neighbors)
                    else:
                        # print('upper right')
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                # middle row
                elif row < (self._rows - 1):
                    # 4. far left side (5 neighbors)
                    if column == 0:
                        # print('left side')
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column + 1])
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column + 1])
                    # 5. normal cells (8 neighbors)
                    elif column < (self._columns - 1):
                        # print('middle')
                        cell.add_neighbor(self._grid[row - 1][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column + 1])
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row + 1][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column + 1])
                    # 6. far right side (5 neighbors)
                    else:
                        # print('right side')
                        cell.add_neighbor(self._grid[row - 1][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                # bottom row
                else:
                    # 7. lower left corner (3 neighbors)
                    if column == 0:
                        # print('lower left')
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column + 1])
                        cell.add_neighbor(self._grid[row][column + 1])
                    # 8. rest of the bottom row (5 neighbors)
                    elif column < (self._columns - 1):
                        # print('lower row')
                        cell.add_neighbor(self._grid[row - 1][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column + 1])
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row][column + 1])
                    # 9. lower right corner (3 neighbors)
                    else:
                        # print('lower right')
                        cell.add_neighbor(self._grid[row - 1][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row][column - 1])

    def set_cell(self, row, column, living):
        """Change the state of the cell at self.__grid[row][column] to the
         value of living."""
        self._grid[row][column].set_living(living)

    def next_generation(self):
        """Changes the grid to the next generation after following the
        propagation rules. """
        self._livingCellCount = 0
        newGrid = self.create_grid()
        for row in self._grid:
            for cell in row:
                if cell.get_living() == True:
                    if cell.living_neighbors() in [2, 3]:
                        newGrid[cell.get_row()][cell.get_column()].set_living(True)
                        self._livingCellCount += 1
                else:
                    if cell.living_neighbors() == 3:
                        newGrid[cell.get_row()][cell.get_column()].set_living(True)
                        self._livingCellCount += 1
        self._grid = newGrid
        self.create_neighbors()
        self._generation += 1

    def randomize(self, percent):
        """Randomly make each cell in the world alive based on the percent given."""
        self._livingCellCount = 0
        for row in self._grid:
            for cell in row:
                if random.randint(0,100) <= percent:
                    cell.set_living(True)
                    self._livingCellCount += 1
                else:
                    cell.set_living(False)

    def save(self, filename):
        """
        Save the world as a text file.
        :param filename: path and filename with '.life' at the end.
        :return: None
        """
        currentDisplaySet = Cell.currentDisplaySet
        Cell.set_display('basic')
        text = self.__str__()
        Cell.set_display(currentDisplaySet)
        with open(filename, 'w') as myFile:
            myFile.write(text)

    def get_living_cell_count(self):
        return self._livingCellCount

    def get_rows(self):
        return self._rows

    def get_columns(self):
        return self._columns

    def get_generation(self):
        return self._generation