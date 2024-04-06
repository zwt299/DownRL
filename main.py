import subprocess
from datetime import time
from time import sleep

from agents.dqn_agent import DQNAgent
from environment.environment import Environment
from performance.performance_logger import PerformanceLogger
from trainer.trainer import Trainer
import tensorflow as tf

DOWNWELL = 'Downwell'


def get_game_window_id() -> str:
    try:
        window_ids = subprocess.check_output(["xdotool", "search", "--name", DOWNWELL]).decode("utf-8").strip().split('\n')
        for window in window_ids:
            name = subprocess.check_output(["xdotool", "getwindowname", window]).decode("utf-8").strip()
            if name == DOWNWELL:
                return window
    except subprocess.CalledProcessError:
        print("Downwell not found.")


def main():
    game_window_id = get_game_window_id()
    environment = Environment(game_window_id)
    # agent = RandomizedAgent(environment.get_action_space())

    agent = DQNAgent(environment.get_action_space())
    trainer = Trainer(environment, agent, PerformanceLogger())

    trainer.train()


if __name__ == '__main__':
    main()
