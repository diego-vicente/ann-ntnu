from flatland import Flatland
from agents import GreedyAgent, SupervisedAgent
import pygame
import time


class Simulation():
    """A visual representation of the path taken by an Agent in a Flatland

    A Simulation generates a pygame screen in which the Flatland environment is
    rendered, along with the solution of an agent in it.
    """
    # Colors defined for convinience
    _black = (0, 0, 0)
    _white = (255, 255, 255)
    _food = (0, 127, 0)
    _eaten_food = (180, 220, 180)
    _poison = (255, 0, 0)
    _eaten_poison = (255, 100, 100)
    _agent = (230, 230, 0)
    _wall = (200, 200, 200)

    # Coordinates and other parameters of size
    _grid_o = (20, 20)
    _cell_size = 40

    def __init__(self, agent):
        """Creates a new Simulation given an agent and a environment"""
        self.agent = agent
        self.env = agent.environment
        # Compute window size
        self.height = (self.env.rows + 2) * self._cell_size + 2*self._grid_o[1]
        self.width = (self.env.cols + 2) * self._cell_size + 2*self._grid_o[0]
        # Populate grid centers dictionary
        self._grid = {}
        for i in range(-1, self.env.rows + 1):
            for j in range(-1, self.env.cols + 1):
                # Compute the corner of the cell
                self._grid[i, j] = (self._grid_o[0] + (i+1.5)*self._cell_size,
                                    self._grid_o[1] + (j+1.5)*self._cell_size)
                # Round to int
                self._grid[i, j] = (int(self._grid[i, j][0]),
                                    int(self._grid[i, j][1]))
        self._step = 1

    def start(self):
        """Starts the simulation loop"""
        # Create the screen
        self.screen = pygame.display.set_mode((self.height, self.width))
        # Call the draw function to start
        self._draw_window()
        # Intiate the GUI loop
        end = False
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.previous_step()
                    elif event.key == pygame.K_RIGHT:
                        self.next_step()
                    elif event.key == pygame.K_SPACE:
                        self.run()

    def _points_to_coordinates(self, points):
        """Translate a list of points to coordinates in Simulation canvas"""
        return [self._grid[point] for point in points]

    def _draw_window(self):
        """Draws all the components in the window at a given time"""
        # Draw a white background
        self.screen.fill(self._white)

        # Draw vertical lines of the grid
        for i in range(self.env.cols + 3):
            start = (self._grid_o[0] + i * self._cell_size,
                     self._grid_o[1])
            end = (self._grid_o[0] + i * self._cell_size,
                   self._grid_o[1] + (self.env.rows + 2) * self._cell_size)
            pygame.draw.lines(self.screen, self._black, False, [start, end], 1)

        # Draw horizontal lines of the grid
        for i in range(self.env.rows + 3):
            start = (self._grid_o[0],
                     self._grid_o[1] + i * self._cell_size)
            end = (self._grid_o[0] + (self.env.cols + 2) * self._cell_size,
                   self._grid_o[1] + i * self._cell_size)
            pygame.draw.lines(self.screen, self._black, False, [start, end], 1)

        steps = self.agent.steps[:self._step]

        # Draw each element in the grid
        for i in range(-1, self.env.rows + 1):
            for j in range(-1, self.env.cols + 1):
                cell = self.env.get_original_cell(i, j)
                if (cell == 'W'):
                    pygame.draw.circle(self.screen, self._wall,
                                       self._grid[i, j], 10, 0)
                elif (cell == 'F'):
                    if (i, j) in steps:
                        pygame.draw.circle(self.screen, self._eaten_food,
                                           self._grid[i, j], 10, 0)
                    else:
                        pygame.draw.circle(self.screen, self._food,
                                           self._grid[i, j], 10, 0)
                elif (cell == 'P'):
                    if (i, j) in steps:
                        pygame.draw.circle(self.screen, self._eaten_poison,
                                           self._grid[i, j], 10, 0)
                    else:
                        pygame.draw.circle(self.screen, self._poison,
                                           self._grid[i, j], 10, 0)

        agent = self._grid[steps[-1]]
        pygame.draw.circle(self.screen, self._agent, agent, 10, 0)

        trace = self._points_to_coordinates(steps)
        if (len(trace) > 1):
            pygame.draw.lines(self.screen, self._agent, False, trace, 5)

        # Refresh the window once all the changes are done
        pygame.display.update()

    def next_step(self):
        """Displays next step in the simulation (if any)"""
        if (self._step < len(self.agent.steps)):
            self._step += 1
            self._draw_window()

    def previous_step(self):
        """Displays previous step in the simulation (if any)"""
        if (self._step > 1):
            self._step -= 1
            self._draw_window()

    def run(self):
        for step in (self.agent.steps):
            pygame.time.wait(200)
            self.next_step()


def main():
    agent = SupervisedAgent(0.4)
    env = Flatland(10, 10)
    agent.train(20, False)
    agent.new_environment(env)
    agent.learn(50, True)
    simulation = Simulation(agent)
    simulation.start()


if __name__ == "__main__":
    main()
