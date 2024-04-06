import subprocess
from time import sleep

import cv2
import mss.tools
import numpy as np
from mss import mss as mss_class

from constants import game_state_constants
from environment.controller import Controller
from utilties import image_utilities, general_utilities


class Environment:
    def __init__(self, window_id: str):
        self.counter = 0
        self.window_id = window_id
        self.capture_path = 'images/capture.png'
        self.controller = Controller()
        self.focus_window()
        self.screenshot()


        # State Representation includes the below
        self.current_frame = None
        self.previous_frame = None
        self.current_gems = 0
        self.previous_gems = 0
        self.delta_gems = 0
        self.game_over = False
        self.current_run_frames_captured = 1

    """
    Utility function to put game window into focus.
    """

    def focus_window(self):
        subprocess.run(["xdotool", "windowactivate", self.window_id])

    """
    Take screenshot of the game window. Grayscale the screenshot, used in determining game state.
    """

    def screenshot(self, monitor_index=2):
        sct = mss_class()
        monitor = sct.monitors[monitor_index]
        monitor_region = {
            "top": monitor["top"] + 38,
            "left": monitor["left"],
            "width": 380,
            "height": 284,
        }
        screenshot = sct.grab(monitor_region)
        # Convert to an OpenCV image (BGR)
        img = np.array(screenshot)

        # Convert to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        grayscale_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=self.capture_path)
        self.counter += 1
        sct.close()
        return grayscale_img

    def process_screenshot(self, screenshot_path: str):
        game_over = image_utilities.parse_image(screenshot_path, game_state_constants.GAME_OVER_LOCATION)
        gems = image_utilities.parse_image(screenshot_path, game_state_constants.GEMS_LOCATION)

        return gems, game_over

    def get_action_space(self):
        return self.controller.get_actions()

    def take_action(self, action):
        self.controller.execute_action(action)
        sleep(0.10)  # Give a delay to understand the rewards and change in environment

    def update_state(self):
        self.previous_frame = self.current_frame
        self.previous_gems = self.current_gems

        self.current_frame = self.screenshot()
        current_gems_str, game_over_str = self.process_screenshot(self.capture_path)
        self.current_gems = general_utilities.convert_string_to_int(current_gems_str)
        if game_over_str.lower() == "game over":
            self.game_over = True
        else:
            self.game_over = False
        self.delta_gems = self.current_gems - self.previous_gems
        self.current_run_frames_captured += 1

    def get_state(self):
        return {
            "current_frame": self.current_frame,
            "current_gems": self.current_gems,
            "game_over": self.game_over,
        }

    """
    Simple reward function, just use raw gems value and game over status scaled by a high number.
    
    Idea is to promote gem collection, and incentivize not getting game over.
    """
    def get_reward(self):
        r = self.delta_gems * 5 - self.current_run_frames_captured
        if self.game_over:
            r -= 1000
        return r

    def quit(self):
        print("Screenshots processed: " + str(self.counter))
        self.controller.quit()

    def reset(self):
        self.current_frame = None
        self.previous_frame = None
        self.current_gems = 0
        self.previous_gems = 0
        self.delta_gems = 0
        self.game_over = False
        self.current_run_frames_captured = 1