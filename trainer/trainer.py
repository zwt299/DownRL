from datetime import datetime

from agents.base_agent import BaseAgent
from environment.environment import Environment
from performance.performance_logger import PerformanceLogger


class Trainer:
    def __init__(self, environment: Environment, agent: BaseAgent, logger: PerformanceLogger):
        self.environment = environment
        self.agent = agent
        self.logger = logger

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
                preload_frames = True
                episode_time = datetime.now()
                episode_results = None
                print('Starting episode {}'.format(episode_time))
                while run:
                    if preload_frames:
                        self.environment.update_state()
                        preload_frames = False

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
                    reward = self.environment.get_reward()

                    # Agent learns from updated state and reward.
                    self.agent.store_experience(state, action, reward, new_state, new_state.get('game_over'))

                    # Terminate if game hit terminal state.
                    if new_state.get('game_over'):
                        self.environment.reset()
                        self.agent.reset()
                        episode_results = new_state.get('gems')
                        run = False

                # Preference for training at the end of each game run using experiences stored in memory.
                episode_time = datetime.now() - episode_time
                print('Finished an episode run.')
                print('Elapsed time: {}'.format(episode_time))

                learn_time = datetime.now()
                print('Starting learning, time: {}'.format(learn_time))
                self.agent.learn()
                learn_time = datetime.now() - learn_time
                print('Learning finished, starting new episode.')
                print('Learning process elapsed time: {}'.format(learn_time))
                print('Logging results')
                self.logger.log_episode_results({'time': episode_time, 'gems': episode_results})

                # Start new run
                self.environment.controller.execute_action(
                    self.environment.controller.get_index_of_action('press_space'))
                iteration += 1
                run = True

        except KeyboardInterrupt:
            print('Training is stopped')
            print('Shutting down')
            self.environment.quit()
            self.agent.quit()
