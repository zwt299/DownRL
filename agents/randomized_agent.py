
import random

from agents.base_agent import BaseAgent


class RandomizedAgent(BaseAgent):
    def select_action(self, state=None):
        return random.choice(self.action_space)
