import random


class Flatland():
    """A random representation of the Flatland environment

    As stated in the assignment, the Flatland is a board generated randomly
    where 'each of the 10x10 squares, there is a 50% chance that it could spawn
    with food in it. If a particular square doesn’t receive any food, there is
    a 50% chance that it could spawn with poison in it. Otherwise, the square
    remains empty. The agent starts in a random square.'

    Each cell of the board can have different values:
    - '.': an empty cell. Moving to it is an action with 0 reward.
    - 'F': a cell containing food. Moving to it has a reward of 4.
    - 'P': a cell containing poison. Moving to it has a reward of -1.
    - 'W': a wall. Running into a wall has a reward of -100 and stops the
    simulation.
    - 'A': the agent's position in each certain moment.

    Since walls are by default only out of bounds cells, the board should
    always be accessed through the method provided.

    Public variables:
    rows -- number of rows in the board
    cols -- number of columns in the board
    board -- board itself, as a 2D list of chars
    agent_x -- x coordinate of the agent in that moment
    agent_y -- y coordinate of the agent in that moment
    food -- list of food coordinates
    poison -- list of poison coordinates
    eaten_food -- list of already eaten food positions
    eaten_poison -- list of already poison food positions
    """

    # Dictionary storing the reinforcements of each cell. Should not be edited.
    _reinforcements = {
        '.': 0,
        'F': 1,
        'P': -4,
        'W': -100,
        'A': 0
    }

    def __init__(self, rows, cols):
        """Creates a new random Flatland representation of a given size."""
        self.rows = rows
        self.cols = cols
        self.board = [[] for i in range(rows)]
        self.food = []
        self.poison = []
        self.eaten_food = []
        self.eaten_poison = []

        agent_placed = False

        # Possible value of the cells: empty (.), food (F), poison (P)
        for row in self.board:
            for _ in range(cols):
                # Rules for distribution as stated in the assignment
                if (random.randint(0, 1)):
                    # Add food to the board
                    cell = 'F'
                    self.food.append((len(row), self.board.index(row)))
                elif (random.randint(0, 1)):
                    # Add poison to the board
                    cell = 'P'
                    self.poison.append((len(row), self.board.index(row)))
                else:
                    if not agent_placed and random.randint(0, 5) == 0:
                        # Add the agent to the board
                        self.agent_x = len(row)
                        self.agent_y = self.board.index(row)
                        agent_placed = True
                        cell = 'A'
                    else:
                        # Add an empty cell
                        cell = '.'
                row.append(cell)

    def to_string(self):
        """Returns a string representation of the Flatland environment."""
        return '\n'.join([' '.join(row) for row in self.board])

    def get_cell(self, x, y):
        """Returns the value of the cell (x,y)

        The return value is a char ('.', 'W', 'F', 'P') representing each of
        the possible values of a cell. Since walls are not part of the board
        list when out of bounds, it is always recommended to use this method.
        """
        if (0 <= x < self.cols and 0 <= y < self.rows):
            return self.board[x][y]
        else:
            return 'W'

    def move_agent(self, x, y):
        """Moves the agent to the cell (x,y)

        The method ensures to maintain the coherence among all attributes in
        the Flatland object when moving the agent, by updating not only the
        board but the new position of the agent too. It returns the
        reinforcement of the action just taken.
        """
        value = self._reinforcements[self.get_cell(x, y)]
        # if value == 1:
        #     self.food.remove((x, y))
        #     self.eaten_food.append((x, y))
        # elif value == -4:
        #     self.poison.remove((x, y))
        #     self.eaten_food.append((x, y))
        self.board[self.agent_x][self.agent_y] = '.'
        self.agent_x = x
        self.agent_y = y
        self.board[self.agent_x][self.agent_y] = 'A'
        return value
