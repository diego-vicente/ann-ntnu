import random


class Flatland():

    def __init__(self, rows, columns):
        '''
        Creates a new random Flatland representation of a given size.
        :param rows: number of rows
        :param columns: number of columns
        '''
        self.rows = rows
        self.columns = columns
        self.board = [[] for i in range(rows)]

        agent_placed = False

        # Possible value of the cells: empty (.), food (F), poison (P)
        for row in self.board:
            for _ in range(columns):
                # Rules for distribution are stated in the assignment
                if (random.randint(0, 1)):
                    value = 'F'
                elif (random.randint(0, 1)):
                    value = 'P'
                else:
                    if not agent_placed and random.randint(0, 15) == 0:
                        value = 'A'
                    else:
                        value = '.'
                row.append(value)

    def toString(self):
        '''
        Returns a String representation of the Flatland environment
        :return: String with the Flatland matrix
        '''
        return '\n'.join([' '.join(row) for row in self.board])

    def get_cell(self, x, y):
        '''
        Returns the value of a given cell, used to get the walls if out of
        bounds.
        :param x: coordinate x of the cell in the board
        :param y: coordinate y of the cell in the board
        :return: '.' (empty cell), 'F' (food), 'P' (poison), 'W' (wall),
        'A' (agent)
        '''
        if (0 <= x < self.columns and 0 <= y < self.rows):
            return self.board[x][y]
        else:
            return 'W'


def main():
    test = Flatland(10, 10)
    print(test.toString())


if __name__ == "__main__":
    main()
