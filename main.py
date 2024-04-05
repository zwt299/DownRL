import subprocess

import pyautogui
import pyautogui as gui
import typing

from agents.base_agent import BaseAgent
from agents.randomized_agent import RandomizedAgent
from controller import Controller
import time

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



def take_screenshot(id :str):
    try:
        subprocess.run(["import", "-window", id, "screenshot.png"])
    except subprocess.CalledProcessError:
        print("Error while taking screenshot.")

def main():
    game_window_id = get_game_window_id()
    subprocess.run(["xdotool", "windowactivate", game_window_id])

    controller = Controller()
    agent = RandomizedAgent(action_space=controller.actions)
    try:
        while True:
            # take_screenshot(game_window_id)
            action = agent.select_action()
            print(action)
            controller.execute_action(action)

            time.sleep(0.02)
    except:
        print("Terminating program.")





if __name__ == '__main__':
    main()
