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

        # Possible value of the cells: empty (.), food (F), or poison (P)
        values = ['.', 'F', 'P']

        for row in self.board:
            for _ in range(columns):
                row.append(random.choice(values))

    def toString(self):
        '''
        Returns a String representation of the Flatland environment
        :return: String with the Flatland matrix
        '''
        return '\n'.join([' '.join(row) for row in self.board])


def main():
    test = Flatland(10, 10)
    print(test.toString())


if __name__ == "__main__":
    main()
