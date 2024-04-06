
import random

from agents.base_agent import BaseAgent


class RandomizedAgent(BaseAgent):
    def get_action(self):
        return random.choice(self.action_space)
