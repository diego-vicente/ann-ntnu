from flatland import Flatland
from agents import GreedyAgent, EnhancedAgent
import pygame


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
    _neuron_on = (100, 100, 200)

    # Grid coordinates and other parameters of size
    _grid_o = (20, 20)
    _cell_size = 40

    # Brain coordinates and other parameters of size
    _input_spacing = 42
    _output_spacing = 170

    # Hardcoded meanings of each input neuron
    _input_meanings = {0: 'E front',
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

    # Hardcoded meanings of each output neuron
    _output_meanings = {0: 'Move forwards',
                        1: 'Move left',
                        2: 'Move right'}

    def __init__(self, agent):
        """Creates a new Simulation given an agent and a environment"""
        self.agent = agent
        self.env = agent.environment
        self._only_grid = isinstance(self.agent, GreedyAgent)
        # Compute window size
        self.height = (self.env.rows + 2) * self._cell_size + 2*self._grid_o[1]
        self.width = (self.env.cols + 2) * self._cell_size + 2*self._grid_o[0]
        if not self._only_grid:
            # Compute the brain size and update window
            self._brain_o = (self.height, 20)
            self.height *= 2
            self._input_o = self._brain_o
            self._input_n_o = (self._input_o[0] + 90, self._input_o[1] + 5)
            self._output_o = (self._input_o[0] + 350, 85)
            self._output_n_o = (self._output_o[0] - 20, 90)
            self._avg_o = (self._output_n_o[0], 480)
            # Fine tune the spacing:
            if isinstance(agent, EnhancedAgent):
                self._input_spacing = round(self._input_spacing / 3)
                self._input_o = (self._brain_o[0], 10)
                self._input_n_o = (self._input_o[0] + 90, self._input_o[1] + 5)
                self._output_o = (self._input_o[0] + 350, 85)
                self._output_n_o = (self._output_o[0] - 20, 90)

        # Init the font module
        pygame.init()
        self._font = pygame.font.SysFont("Consolas", 20)

        self._step = 1
        self._avg = None

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

        if self._only_grid:
            return

        # Populate the input & output neurons dictionaries
        self._inputs = {}
        for i in range(len(self.agent.neurons)):
            self._inputs[i] = (self._input_n_o[0],
                               self._input_n_o[1] + i * self._input_spacing)

        self._outputs = {}
        for i in range(3):
            self._outputs[i] = (self._output_n_o[0],
                                self._output_n_o[1] + i * self._output_spacing)

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
                    elif event.key == pygame.K_t and not self._only_grid:
                        self.visual_training()
                    elif event.key == pygame.K_w and not self._only_grid:
                        self.agent.print_weights()
                    elif event.key == pygame.K_n:
                        self._new_run()

    def _points_to_coordinates(self, points):
        """Translate a list of points to coordinates in Simulation canvas"""
        return [self._grid[point] for point in points]

    def _draw_window(self, training=False):
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

        if not training:
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

        # If we have a greedy agent, stop here
        if self._only_grid:
            pygame.display.update()
            return

        # Draw brain
        last = self._step >= len(self.agent.output_story)
        for i in range(len(self.agent.neurons)):
            # Render input neuron text
            neuron = self._font.render(self._input_meanings[i],
                                       True, self._black)
            origin = (self._input_o[0],
                      self._input_o[1] + i * self._input_spacing)
            self.screen.blit(neuron, origin)

            # Render the current neural perception
            triggered = False
            if not last:
                triggered = self.agent.neuron_story[self._step-1][i]
            if triggered and not training:
                origin = (self._input_n_o[0],
                          self._input_n_o[1] + i * self._input_spacing)
                pygame.draw.circle(self.screen, self._neuron_on,
                                   origin, 10, 0)

        output = -1
        if not last:
            output = self.agent.output_story[self._step-1]
        for i in range(len(self.agent.outputs)):
            # Render output neuron text
            neuron = self._font.render(self._output_meanings[i],
                                       True, self._black)
            origin = (self._output_o[0],
                      self._output_o[1] + i * self._output_spacing)
            self.screen.blit(neuron, origin)

            if i == output and not training and not last:
                origin = (self._output_n_o[0],
                          self._output_n_o[1] + i * self._output_spacing)
                pygame.draw.circle(self.screen, self._neuron_on,
                                   origin, 10, 0)

        # Normalize weights to print the lines accordingly
        max_v = max(self.agent.weights.values())
        min_v = min(self.agent.weights.values())
        bound = max_v if (max_v > abs(min_v)) else -min_v
        factor = 255.0 / bound
        normalized_weights = {k: round(v*factor) for k, v in
                              self.agent.weights.items()}

        for i in range(len(self.agent.outputs)):
            for j in range(len(self.agent.neurons)):
                weight = round(normalized_weights[i, j])
                if weight > 0:
                    color = (255 - weight, 255, 255 - weight)
                else:
                    color = (255, 255 + weight, 255 + weight)
                start = self._inputs[j]
                end = self._outputs[i]
                pygame.draw.lines(self.screen, color, False,
                                  [start, end], 4)

        # Display rewards if any
        if self._avg is not None:
            label = self._font.render('Average rewards: {}'.format(self._avg),
                                      True, self._black)
            self.screen.blit(label, self._avg_o)

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
        """Run the complete execution automatically"""
        self._step = 1
        for step in (self.agent.steps):
            pygame.time.wait(200)
            self.next_step()

    def visual_training(self):
        """Display the evolution of the ANN during a training"""
        self._draw_window()
        for i in range(50):
            episode_rewards = []
            for _ in range(100):
                env = Flatland(10, 10)
                self.agent.new_environment(env)
                result = self.agent.learn(50, False)
                episode_rewards.append(result)
            self._avg = sum(episode_rewards)/100
            self._draw_window(training=True)

    def _new_run(self):
        self.env = Flatland(10, 10)
        # agent.train(20, False)
        self.agent.new_environment(self.env)
        self.agent.learn(50, False)
        self._step = 1
        self._draw_window()


def main():
    # agent = EnhancedAgent(0.005, 0.99, 1)
    agent = GreedyAgent()
    env = Flatland(10, 10)
    agent.new_environment(env)
    agent.run(50, False)
    simulation = Simulation(agent)
    simulation.start()


if __name__ == "__main__":
    main()
