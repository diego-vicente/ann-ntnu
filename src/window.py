from flatland import Flatland
from agents import Agent
import pygame
import sys


class Window():
    # Colors defined for convinience
    black = (0, 0, 0)
    white = (255, 255, 255)

    def __init__(self, agent, environment):
        self.agent = agent
        self.environment = environment
        self.screen = pygame.display.set_mode((640, 480))

    def start_simulation(self):
        self._draw_window()
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def _draw_window(self):
        grid_zero_x = 20
        grid_zero_y = 20
        cell_size = 30
        # Draw a white background
        self.screen.fill(self.white)

        # Draw vertical lines of the grid
        for i in range(self.environment.columns + 3):
            start = (grid_zero_x + i*cell_size, grid_zero_y)
            end = (grid_zero_x + i*cell_size,
                   grid_zero_y + (self.environment.rows + 2)*cell_size)
            pygame.draw.lines(self.screen, self.black, False, [start, end], 2)

        # Draw horizontal lines of the grid
        for i in range(self.environment.rows + 3):
            start = (grid_zero_x, grid_zero_y + i*cell_size)
            end = (grid_zero_x + (self.environment.columns + 2)*cell_size,
                   grid_zero_y + i*cell_size)
            pygame.draw.lines(self.screen, self.black, False, [start, end], 2)

        pygame.display.update()


def main():
    agent = Agent()
    environment = Flatland(10, 10)
    window = Window(agent, environment)
    window.start_simulation()


if __name__ == "__main__":
    main()
