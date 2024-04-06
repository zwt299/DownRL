from agents.base_agent import BaseAgent
from environment import Environment


class Trainer:
    def __init__(self, environment: Environment, agent: BaseAgent):
        self.environment = environment
        self.agent = agent

    """
    Trains the agent on the environment.
    Follows the pattern:
        Agent observes environment.
        Agent decides on action based on environment observation.
        Agent sends action to environment, which executes action.
        Environment updates state and reward.
        Agent learns from updated state and reward.
        Repeat until game is over (or for a specified number of steps)
    """

    def train(self):
        run = True
        iteration = 0
        try:
            while True:
                while run:
                    # Agent observes environment
                    state = self.environment.get_state()
                    self.agent.observe_state(state)

                    # Agent decides on action
                    action = self.agent.get_action()

                    # Agent sends action to environment
                    self.environment.take_action(action)

                    # Environment updates state
                    self.environment.update_state()
                    new_state = self.environment.get_state()

                    # Agent learns from updated state and reward.
                    self.agent.learn(new_state, action)

                    # Terminate if game hit terminal state.
                    if new_state.get('game_over'):
                        run = False

                iteration += 1
                run = True

        except KeyboardInterrupt:
            print('Training is stopped')
            print('Shutting down')
            self.environment.quit()
