# from flatland import Flatland
import matplotlib as plt

class Agent():

    def __init__(self):
        self.environment = None
        self.position = None
        self.reward = 0
        self.steps = []

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

    def move_to(self, x, y):
        """Moves the agent to the cell (x,y) in its actual environment

        The method updates the agent's environment according to the movement,
        updates the rewards obtained by the agent and returns if the simulation
        is over because of the agent running into a wall.
        """
        # Update the position of the agent in the environment
        mov_reward = self.environment.move_agent(x, y)
        # Update the rewards value
        self.reward += mov_reward
        # Check if the agent just ran into a wall
        end = mov_reward == -100
        return end
