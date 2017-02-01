from flatland import Flatland
from agents import GreedyAgent, SupervisedAgent, ReinforcementAgent, \
    EnhancedAgent
from window import Simulation
import matplotlib.pyplot as plt


def main():

    print("""
    Demo for IT3708 - Project 1:

    1. Launch the visual simulation with a GreedyAgent
    2. Train and launch the visual simulation with a SupervisedAgent
    3. Train and launch the visual simulation with a ReinforcedAgent
    4. Train and launch the visual simulation with an EnhancedAgent

    5. Launch a visual training with a SupervisedAgent
    6. Launch a visual training with a ReinforcedAgent
    7. Launch a visual training with a EnhancedAgent

    8. Run all the agents in text training and plot results

    """)

    choice = input('Enter the option: ')

    if choice == '1':
        run_simulation('g', False)
    elif choice == '2':
        run_simulation('s', True)
    elif choice == '3':
        run_simulation('r', True)
    elif choice == '4':
        run_simulation('e', True)
    elif choice == '5':
        run_simulation('s', False)
    elif choice == '6':
        run_simulation('r', False)
    elif choice == '7':
        run_simulation('e', False)
    elif choice == '8':
        compare_agents(50)
    else:
        print("The option entered was not valid.")


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


def run_simulation(agent, training):
    """Run the graphical simulation after training the agent"""
    if agent == 'g':
        agent = GreedyAgent()
    elif agent == 's':
        agent = SupervisedAgent(0.01)
    elif agent == 'r':
        agent = ReinforcementAgent(0.005, 0.99, 1)
    elif agent == 'e':
        agent = EnhancedAgent(0.005, 0.99, 1)

    if training:
        env = Flatland(10, 10)
        agent.train(20, False)
        agent.new_environment(env)
        agent.learn(50, False)
    else:
        env = Flatland(10, 10)
        agent.new_environment(env)
        if isinstance(agent, GreedyAgent):
            agent.run(50, False)
        else:
            agent.learn(50, False)
    simulation = Simulation(agent)
    simulation.start()


if __name__ == '__main__':
    main()
