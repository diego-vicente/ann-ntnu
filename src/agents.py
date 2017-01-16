from flatland import Flatland
import matplotlib.pyplot as plt


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

    def visualize_steps(self):
        """Save a graphic representation of the steps taken by the agent.

        Save a file with the visualization of the steps taken by the agent to
        the visualization of steps taken by the agent. All the images are saved
        to the snapshots folder.
        """
        plt.figure()
        plt.scatter(*zip(*self.environment.food), color='green', s=10)
        plt.scatter(*zip(*self.environment.poison), color='red', s=10)
        plt.scatter(*zip(*[self.position]), color='yellow', s=10)
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal', adjustable='datalim')
        plt.axis('off')
        plt.savefig('test.png')
        plt.clf


def test():
    agent = Agent()
    env = Flatland(10, 10)
    agent.new_environment(env)
    print(agent.environment.to_string())
    agent.visualize_steps()


if __name__ == "__main__":
    test()
