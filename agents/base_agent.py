class BaseAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def get_action(self, state):
        raise NotImplementedError

    def learn(self, *args):
        raise NotImplementedError
