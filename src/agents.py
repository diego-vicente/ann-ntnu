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
        # It's easier to hardcode the border walls since the env will always be
        # 10 x 10
        walls = [(-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4),
                 (-1, 5), (-1, 6), (-1, 7), (-1, 8), (-1, 9), (-1, 10),
                 (10, -1), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4),
                 (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10),
                 (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1),
                 (6, -1), (7, -1), (8, -1), (9, -1), (0, 10), (1, 10),
                 (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10),
                 (8, 10), (9, 10)]

        plt.figure(frameon=False, figsize=(8, 8), dpi=80)
        plt.scatter(*zip(*self.environment.food), color='green', s=20)
        plt.scatter(*zip(*walls), color='grey', s=20)
        plt.scatter(*zip(*self.environment.poison), color='red', s=20)
        plt.scatter(*zip(*[self.position]), color='yellow', edgecolor='black',
                    s=20)
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal', adjustable='datalim')
        plt.axis('off')
        plt.savefig('../snapshots/test.png', bbox_inches='tight')
        plt.clf


def test():
    agent = Agent()
    env = Flatland(10, 10)
    agent.new_environment(env)
    print(agent.environment.to_string())
    agent.visualize_steps()


if __name__ == "__main__":
    test()
