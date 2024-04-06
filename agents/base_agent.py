class BaseAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def get_action(self):
        raise NotImplementedError

    def observe_state(self, state):
        raise NotImplementedError

    def learn(self):
        raise NotImplementedError

    def store_experience(self, state, action, reward, new_state, done):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def quit(self):
        raise NotImplementedError