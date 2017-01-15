import random


class Flatland():
    reinforcements = {
        '.': 0,
        'F': 4,
        'P': -1,
        'W': -100
    }

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
                    cell = 'F'
                elif (random.randint(0, 1)):
                    cell = 'P'
                else:
                    if not agent_placed and random.randint(0, 15) == 0:
                        self.agent_x = len(row)
                        self.agent_y = self.board.index(row)
                        agent_placed = True
                        cell = 'A'
                    else:
                        cell = '.'
                row.append(cell)

    def to_string(self):
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

    def move_agent(self, x, y):
        '''
        Moves the agent to a new cell and returns the value of the destination
        cell chosen.
        :param x: coordinate x of the destination cell
        :param y: coordinate y of the destination cell
        :return: Value of the destination cell
        '''
        value = self.reinforcements[self.get_cell(x, y)]
        self.board[self.agent_x][self.agent_y] = '.'
        self.agent_x = x
        self.agent_y = y
        self.board[self.agent_x][self.agent_y] = 'A'
        return value


def main():
    test = Flatland(10, 10)
    print()
    print(test.to_string())
    print()
    print(test.agent_x, test.agent_y)
    print()
    value = test.move_agent(3, 3)
    print('When moving to a new cell we got ', value)
    print()
    print(test.to_string())


if __name__ == "__main__":
    main()
