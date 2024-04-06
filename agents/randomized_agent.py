import random

from agents.base_agent import BaseAgent


class RandomizedAgent(BaseAgent):
    def get_action(self):
        return random.randint(0, len(self.action_space))

    def observe_state(self, state):
        pass

    def learn(self):
        pass

    def store_experience(self, state, action, reward, new_state, done):
        pass

    def quit(self):
        pass