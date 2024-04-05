import subprocess

import pyautogui
import pyautogui as gui
import typing

import controller
from agents.base_agent import BaseAgent
from agents.randomized_agent import RandomizedAgent
from controller import Controller
import time

from environment import Environment
from trainer import Trainer

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
    agent = RandomizedAgent (environment.get_action_space())
    trainer = Trainer(environment, agent)

    trainer.train()


if __name__ == '__main__':
    main()
