from flatland import Flatland
from operator import itemgetter
import random
import math


class Direction():
    """Represents North, East, South and West in tuples for coordinates"""
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)


class Agent():
    """Superclass for different agents implemented

    This superclass provides all the common functions that the agents need when
    moving around the environment. Every other agent should inherit this class
    and add the decision-making logic or other perception skills.

    Public Attributes:
    environment -- Flatland in which the agent will move
    position -- current position of the agent in the environment
    reward -- current reward of the agent in the environment
    steps -- lists of positions that agent has traveled in the environment
    facing -- current Direction that the agent is facing

    """

    def __init__(self):
        self.environment = None
        self.position = None
        self.reward = 0
        self.steps = []
        self.facing = Direction.N

    def new_environment(self, new_env):
        """Sets a new Flatland environment for the agent"""
        # Change the environment
        self.environment = new_env
        # Update the position to the new initial one
        self.position = (new_env.agent_x, new_env.agent_y)
        # Clear the previous solution trace
        self.steps = []
        # Clear the rewards from the previous solution
        self.reward = 0

    def move_to(self, direction):
        """Moves the agent to the cell (x,y) in its actual environment

        The method updates the agent's environment according to the movement,
        updates the rewards obtained by the agent and returns if the simulation
        is over because of the agent running into a wall.
        """
        # Update the position of the agent in the environment
        x = self.position[0] + direction[0]
        y = self.position[1] + direction[1]
        mov_reward = self.environment.move_agent(x, y)
        # Update the rewards, position and direction value
        self.reward += mov_reward
        self.position = (x, y)
        self.facing = direction
        # Check if the agent just ran into a wall
        end = mov_reward == -100
        return (x, y), end

    def look_at(self, direction):
        """Return the value of the cell in a given direction"""
        return self.environment.get_cell(self.position[0] + direction[0],
                                         self.position[1] + direction[1])

    def look_around(self):
        """Returns the values of the left, front and right cells

        This method implements the basic perception of an agent. Returns a
        triple with the values of each cell (left, front and right in that
        order) and the direction associated to each of the cells.
        """

        front = self.facing
        if (front == Direction.N):
            left = Direction.W
            right = Direction.E
        elif (front == Direction.E):
            left = Direction.N
            right = Direction.S
        elif (front == Direction.S):
            left = Direction.E
            right = Direction.W
        elif (front == Direction.W):
            left = Direction.S
            right = Direction.N

        surroundings = ((front, self.look_at(front)),
                        (left, self.look_at(left)),
                        (right, self.look_at(right)))

        # print('I see {} in front, {} left, and {} right.'.format(
        #     surroundings[0][1], surroundings[1][1], surroundings[2][1]))

        return surroundings

    def policy_movement(self):
        """Follow the greedy policy to choose next step"""
        # See the options
        front, left, right = self.look_around()
        choices = [front[0], left[0], right[0]]
        options = [front[1], left[1], right[1]]

        # If there is any food, go for it:
        if 'F' in options:
            return choices[options.index('F')]
        # If there is no food, just go for an empty cell
        elif '.' in options:
            return choices[options.index('.')]
        # If there is no other way...
        #
        # Drain the pressure from the swelling,
        # The sensation's overwhelming,
        # Give me a long kiss goodnight
        # and everything will be alright
        # Tell me that I won't feel a thing
        # So give me Novacaine.
        elif 'P' in options:
            return choices[options.index('P')]

        # And well, this should never happen, but for the sake of completeness
        else:
            return choices[options.index('W')]


class GreedyAgent(Agent):
    """Agent that follows greedily a policy based on classic rules"""

    def __init__(self):
        Agent.__init__(self)

    def run(self, iterations, output):
        """Run a complete simulation of a given number of steps

        Arguments:
        iterations -- number of iterations to perform
        output -- True if output is desired, false if not
        """
        # Define a dictionary of directions to strings
        dirs = {Direction.N: 'North',
                Direction.E: 'East',
                Direction.S: 'South',
                Direction.W: 'West'}

        # Greedy policy is deterministic so there is no point in running more
        # than once.
        if self.steps != []:
            print('Solution already exists in this agent')
            return self.reward
        else:
            self.steps.append(self.position)

        # Display initial board
        if output:
            print('The initial board is:\n')
            print(self.environment.to_string())
            print()

        # Execution loop
        for i in range(iterations):
            direction = self.policy_movement()
            pos, end = self.move_to(direction)
            self.position = pos
            self.steps.append(pos)
            if output:
                print('Iteration {}: {}, {}'.format(i, dirs[direction],
                                                    self.reward))
            if end:
                return self.reward

        if output:
            print('End of solution, final reward: {}\n'.format(self.reward))
            print(self.environment.to_string())
        return self.reward


class SupervisedAgent(Agent):

    def __init__(self, learning_rate):
        Agent.__init__(self)
        self.learning_rate = learning_rate
        self.neurons = [0 for _ in range(12)]
        self.weights = [random.uniform(0, 0.001) for _ in range(36)]

    def train(self):
        """Updates the neurons taking into account the surroundings

        The neuron array consists of 12 neurons, 4 neurons per cell (front,
        left, right) that can represent the 4 different values of that given
        cell. This method updates the neuron array according to the agent's
        board at a given point.
        """
        # Find all combinations of directions and possible values
        surroundings = self.look_around()
        pairs = [(x[1], y) for x in surroundings for y in ['.', 'W', 'F', 'P']]
        directions = [x[0] for x in surroundings]
        print(pairs)

        # Fill the neuron array by comparing each of the values generated
        for i in range(len(pairs)):
            direction, value = pairs[i]
            self.neurons[i] = 1 if (direction == value) else 0

        print(self.neurons)

        # Compute weights and choose the next movement
        self.outputs = [(0, direction) for direction in directions]
        for i in range(3):
            inputs = [w * n for (w, n) in zip(self.weights[i:(i+11)],
                                              self.neurons)]
            self.outputs[i][0] = sum(inputs)

        # Make a choice based on the input obtained
        getvalue = itemgetter(0)
        choice = max(self.outputs, key=getvalue)[1]

        # Learn from the last step taken
        policy = self.policy_movement()
        correct = 1 if (policy == choice) else 0
        # Compute exponential part of delta_i
        output_values = list(map(getvalue, self.outputs))
        sum_exp = sum([math.exp(n) for n in output_values])
        # Update each of the weights
        for weight in self.weights:
            # Compute input and output values of the weight
            input_n = self.neurons[self.weights.index(weight) % 12]
            output_n = self.outputs[self.weights.index(weight) // 12]
            # Update the value using delta formula
            delta = - (math.exp(output_n) / sum_exp) + correct
            weight += self.learning_rate * input_n * delta

        # Return the final action
        return choice


def test():
    agent = SupervisedAgent()
    env = Flatland(10, 10)
    agent.new_environment(env)
    agent.think()
    # print(agent.environment.to_string())
    # agent.visualize_steps()
    # agent.visualize_board()


if __name__ == "__main__":
    test()
