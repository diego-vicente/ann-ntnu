from flatland import Flatland
from agents import GreedyAgent, SupervisedAgent, ReinforcementAgent, EnhancedAgent
from window import Simulation
import matplotlib.pyplot as plt


def main():
    # compare_agents(50)
    run_simulation()


def compare_agents(rounds):
    """Run each of the agents, train them and compare them in a plot"""
    # Greedy agent measure
    agent_g = GreedyAgent()
    sum_reward = 0
    trials = 1000
    print('Starting: GreedyAgent in {} trials:'.format(trials))
    for _ in range(trials):
        board = Flatland(10, 10)
        agent_g.new_environment(board)
        agent_g.run(50, False)
        sum_reward += agent_g.reward
    greedy_avg = sum_reward/trials
    print('Average score obtained: ', greedy_avg)
    greedy_score = [greedy_avg for _ in range(rounds)]

    # Supervised agent measure
    agent_s = SupervisedAgent(0.01)
    supervised_score = agent_s.train(rounds, False)

    # Reinforcement agent measure
    agent_r = ReinforcementAgent(0.005, 0.99, 1)
    reinforced_score = agent_r.train(rounds, False)

    # Enhanced agent measure
    agent_e = EnhancedAgent(0.005, 0.99, 1)
    enhanced_score = agent_e.train(rounds, False)

    plt.figure()
    plt.plot(greedy_score, label='Greedy Agent', ls='dashed')
    plt.plot(supervised_score, label='Supervised Agent')
    plt.plot(reinforced_score, label='Reinforced Agent')
    plt.plot(enhanced_score, label='Enhanced Agent')
    plt.legend(loc='lower right')
    plt.show()


def run_simulation():
    """Run the graphical simulation after training the agent"""
    agent = ReinforcementAgent(0.005, 0.99, 1)
    agent.train(50, False)
    simulation = Simulation(agent)
    simulation.start()


if __name__ == '__main__':
    main()
