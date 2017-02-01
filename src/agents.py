from flatland import Flatland
from operator import itemgetter
from copy import copy
import random
import math


class Direction():
    """Represents North, East, South and West in tuples for coordinates"""
    N = (0, -1)
    NN = (0, -2)
    NNN = (0, -3)
    E = (1, 0)
    EE = (2, 0)
    EEE = (3, 0)
    S = (0, 1)
    SS = (0, 2)
    SSS = (0, 3)
    W = (-1, 0)
    WW = (-2, 0)
    WWW = (-3, 0)


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
        # Clear the stories
        self.output_story = []
        self.neuron_story = []

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
        self._r = mov_reward
        self.reward += mov_reward
        self.position = (x, y)
        self.facing = direction
        # Check if the agent just ran into a wall
        end = mov_reward == -100
        return (x, y), end

    def move_back(self, direction):
        """Moves the agent back from a certain cell, resetting the board.

        This movements is not valid and should only be used when evaluating the
        reinforced agent in order to obtain Q(s',a')
        """
        # Update the position of the agent in the environment
        x = self.position[0] - direction[0]
        y = self.position[1] - direction[1]
        mov_reward = self.environment.move_agent(x, y)
        # Update the rewards, position and direction value
        self._r = mov_reward
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

        front = copy(self.facing)
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
        else:
            print('Error: Invalid direction used = ', front)

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
    """Agent that implements a supervised ANN

    The neuron array consists of 12 neurons, 4 neurons per cell (front, left,
    right) that can represent the 4 different values of that given cell. There
    is also a weights dictionary, in that stores the weight associated to each
    of the pairs (i, j), where i is an output neuron and j is an input
    neuron. These weights are updated in order for the agent to learn.

    Public Attributes:
    learning_rate -- The rate at which the agent's weight are modified
    neurons -- Array of binary neurons that represent the surroundings
    weights -- Dictionary containing each of the (i,j) connections
    outputs -- Triple containing the sum of input neurons and direction
    """

    # Dictionaries with the neuron input and output meanings
    _input_strings = {0: 'E front',
                      1: 'W front',
                      2: 'F front',
                      3: 'P front',
                      4: 'E left',
                      5: 'W left',
                      6: 'F left',
                      7: 'P left',
                      8: 'E right',
                      9: 'W right',
                      10: 'F right',
                      11: 'P right',
                      12: 'E front (2)',
                      13: 'W front (2)',
                      14: 'F front (2)',
                      15: 'P front (2)',
                      16: 'E front (3)',
                      17: 'W front (3)',
                      18: 'F front (3)',
                      19: 'P front (3)',
                      20: 'E left (2)',
                      21: 'W left (2)',
                      22: 'F left (2)',
                      23: 'P left (2)',
                      24: 'E left (3)',
                      25: 'W left (3)',
                      26: 'F left (3)',
                      27: 'P left (3)',
                      28: 'E right (2)',
                      29: 'W right (2)',
                      30: 'F right (2)',
                      31: 'P right (2)',
                      32: 'E right (3)',
                      33: 'W right (3)',
                      34: 'F right (3)',
                      35: 'P right (3)'}

    _output_strings = {0: 'Move forwards',
                       1: 'Move left',
                       2: 'Move right'}

    def __init__(self, learning_rate):
        Agent.__init__(self)
        self.learning_rate = learning_rate
        self.neurons = [0 for _ in range(12)]
        pairs = [(i, j) for i in range(3) for j in range(12)]
        self.weights = {(i, j): random.uniform(0, 0.001) for (i, j) in pairs}
        self.output_story = []
        self.neuron_story = []

    def print_weights(self):
        """Print the weights values in a readable way"""
        print('Agent weights:')
        for i in range(len(self.outputs)):
            for j in range(len(self.neurons)):
                print('{} - {}: {}'.format(self._input_strings[j],
                                           self._output_strings[i],
                                           self.weights[i, j]))
        print('---')

    def _update_neurons(self):
        """Fill the neuron array with new information of the environment"""
        # Find all combinations of directions and possible values
        surroundings = self.look_around()
        pairs = [(x[1], y) for x in surroundings for y in ['.', 'W', 'F', 'P']]
        directions = [x[0] for x in surroundings[:3]]

        # Fill the neuron array by comparing each of the values generated
        for i in range(len(pairs)):
            direction, value = pairs[i]
            self.neurons[i] = 1 if (direction == value) else 0

        # Compute inputs
        self.outputs = [[0, direction] for direction in directions]
        for i in range(len(self.outputs)):
            for j in range(len(self.neurons)):
                self.outputs[i][0] += self.weights[(i, j)] * self.neurons[j]

    def _update_weights(self, max_out, choice):
        """Use the policy to update the agent weights

        Arguments:
        max_out -- maximum value of the output array (for normlization)
        choice -- choice taken by the neural network
        """
        # Learn from the last step taken
        policy = self.policy_movement()
        correct = 1 if (policy == choice) else 0
        # Compute exponential part of delta_i
        getvalue = itemgetter(0)
        output_values = list(map(getvalue, self.outputs))
        sum_exp = sum([math.exp(n - max_out) for n in output_values])

        # Update each of the weights
        idx = output_values.index(max_out)
        for j in range(len(self.neurons)):
            input_n = self.neurons[j]
            output_n = self.outputs[idx][0]
            delta = correct - (math.exp(output_n - max_out / sum_exp))
            self.weights[(idx, j)] += self.learning_rate * input_n * delta

        self.output_story.append(idx)

    def _learn_step(self):
        """Chooses a new movement and learns from it

        This method updates the neuron array to the new surroundings of the
        agent, computes the outputs of each decision and then chooses the best
        one. After that, uses the Widrow-Hoff rule to update the weights of the
        neurons in order to learn.

        """
        self._update_neurons()

        # Make a choice based on the input obtained
        getvalue = itemgetter(0)
        max_out, choice = max(self.outputs, key=getvalue)

        self._update_weights(max_out, choice)

        # Return the final action
        return choice

    def learn(self, iterations, output):
        """Run an iteration learning in each step

        Arguments:
        iterations -- number of iterations to perform
        output -- True if output is desired, false if not
        """
        # Define a dictionary of directions to strings
        dirs = {Direction.N: 'North',
                Direction.E: 'East',
                Direction.S: 'South',
                Direction.W: 'West'}

        self.steps.append(self.position)

        # Display initial board
        if output:
            print('The initial board is:\n')
            print(self.environment.to_string())
            print()

        # Execution loop
        for i in range(iterations):
            direction = self._learn_step()
            pos, end = self.move_to(direction)
            self.position = pos
            self.steps.append(pos)
            if output:
                print('Iteration {}: {}, {}'.format(i, dirs[direction],
                                                    self.reward))
            if end:
                self._into_wall()
                return self.reward

        if output:
            print('End of solution, final reward: {}\n'.format(self.reward))
            print(self.environment.to_string())
        return self.reward

    def _into_wall(self):
        # Only for inheritance in the QAgents
        pass

    def train(self, episodes, output):
        """Perform several executions in different environments to train the net

        Arguments:
        episodes -- number of episodes (100 executions) to perform
        output -- True if output is desired, false if not
        """
        rewards = []
        for i in range(episodes):
            episode_rewards = []
            for _ in range(100):
                env = Flatland(10, 10)
                self.new_environment(env)
                result = self.learn(50, output)
                episode_rewards.append(result)
            avg = sum(episode_rewards)/100
            print('Episode {}: {}'.format(i, avg))
            rewards.append(avg)
        return rewards


class ReinforcementAgent(SupervisedAgent):
    """Agent based on reinforcement learning"""

    def __init__(self, learning_rate, discount, decay):
        SupervisedAgent.__init__(self, learning_rate)
        self.discount = discount
        self.decay = decay

    def _update_weights(self, max_q, choice):

        if self._prev_neurons is not None:
            i = self._prev_out
            for j in range(len(self.neurons)):
                input_n = self._prev_neurons[j]
                delta = self._r + self.discount * max_q - self._prev_q
                self.weights[(i, j)] += self.learning_rate * input_n * delta

        getvalue = itemgetter(0)
        output_values = list(map(getvalue, self.outputs))
        self._prev_out = output_values.index(max_q)
        self._prev_r = self._r
        self._prev_neurons = copy(self.neurons)
        self._prev_q = max_q

        self.neuron_story.append(copy(self.neurons))
        self.output_story.append(copy(self._prev_out))

        if self._r == -100:
            print("Does this ever happen?")

    def _into_wall(self):
        i = self._prev_out
        for j in range(len(self.neurons)):
            input_n = self._prev_neurons[j]
            delta = -100 + self.discount * (-100) - self._prev_q
            self.weights[(i, j)] += self.learning_rate * input_n * delta

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
        # Clear the state/action variables to maintain integrity
        self._prev_q = None
        self._prev_r = None
        self._prev_out = None
        self._prev_neurons = None
        self._r = 0
        # Decay the learning rate
        self.learning_rate *= self.decay
        # Clear the stories
        self.output_story = []
        self.neuron_story = []


class EnhancedAgent(ReinforcementAgent):

    def __init__(self, learning_rate, discount, decay):
        ReinforcementAgent.__init__(self, learning_rate, discount, decay)
        self.neurons = [0 for _ in range(36)]
        pairs = [(i, j) for i in range(3) for j in range(36)]
        self.weights = {(i, j): random.uniform(0, 0.001) for (i, j) in pairs}

    def look_around(self):
        """Returns the values of the left, front and right cells

        This method implements the basic perception of an agent. Returns a
        triple with the values of each cell (left, front and right in that
        order) and the direction associated to each of the cells.
        """

        front = copy(self.facing)
        if (front == Direction.N):
            front1 = Direction.NN
            front2 = Direction.NNN
            left = Direction.W
            left1 = Direction.WW
            left2 = Direction.WWW
            right = Direction.E
            right1 = Direction.EE
            right2 = Direction.EEE
        elif (front == Direction.E):
            front1 = Direction.EE
            front2 = Direction.EEE
            left = Direction.N
            left1 = Direction.NN
            left2 = Direction.NNN
            right = Direction.S
            right1 = Direction.SS
            right2 = Direction.SSS
        elif (front == Direction.S):
            front1 = Direction.SS
            front2 = Direction.SSS
            left = Direction.E
            left1 = Direction.EE
            left2 = Direction.EEE
            right = Direction.W
            right1 = Direction.WW
            right2 = Direction.WWW
        elif (front == Direction.W):
            front1 = Direction.WW
            front2 = Direction.WWW
            left = Direction.S
            left1 = Direction.SS
            left2 = Direction.SSS
            right = Direction.N
            right1 = Direction.NN
            right2 = Direction.NNN
        else:
            print('Error: Invalid direction used = ', front)

        surroundings = ((front, self.look_at(front)),
                        (left, self.look_at(left)),
                        (right, self.look_at(right)),
                        (front1, self.look_at(front1)),
                        (front2, self.look_at(front2)),
                        (left1, self.look_at(left1)),
                        (left2, self.look_at(left2)),
                        (right1, self.look_at(right1)),
                        (right2, self.look_at(right2)))

        # print('I see {} in front, {} left, and {} right.'.format(
        #     surroundings[0][1], surroundings[1][1], surroundings[2][1]))

        return surroundings


if __name__ == '__main__':
    agent = ReinforcementAgent(0.005, 0.99, 1)
    # agent = GreedyAgent()
    agent.train(50, False)
    agent.print_weights()
