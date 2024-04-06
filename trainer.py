from agents.base_agent import BaseAgent
from environment import Environment


class Trainer:
    def __init__(self, environment: Environment, agent: BaseAgent):
        self.environment = environment
        self.agent = agent

    """
    Trains the agent on the environment.
    Follows the pattern:
        Agent gets information from environment.
        Agent makes decision based on information from environment.
        Agent sends action to environment.
        Environment updates state based on action.
        Repeat until game is over (or for a specified number of steps)
    """

    def train(self):
        run = True
        iteration = 0
        try:
            while True:
                while run:
                    state = self.environment.get_state()
                    if state[2]:  # game over
                        break
                    action = self.agent.get_action(state)
                    self.environment.take_action(action)
                iteration += 1
                run = True

        except KeyboardInterrupt:
            print('Training is stopped')
            print('Shutting down')
            self.environment.quit()
