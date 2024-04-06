import queue
import subprocess

import cv2
import numpy as np

from constants import game_state_constants
from controller import Controller
from utilties import image_utilities, general_utilities
from mss import mss as mss_class
import mss.tools


class Environment:
    def __init__(self, window_id: str):
        self.state = None
        self.window_id = window_id
        self.controller = Controller()
        self.focus_window()
        self.counter = 0
        self.recent_frame = None
        self.gems = None,
        self.game_over = False

    def focus_window(self):
        subprocess.run(["xdotool", "windowactivate", self.window_id])

    def screenshot(self, monitor_index=2, output_filename="capture.png"):
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
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_filename)
        self.counter += 1
        sct.close()
        return grayscale_img

    # def take_screenshot(self):
    #     try:
    #         subprocess.run(["import", "-window", self.window_id, "current_frame.png"])
    #     except subprocess.CalledProcessError:
    #         print("Error while taking screenshot.")

    def get_action_space(self):
        return self.controller.get_actions()

    def take_action(self, action):
        self.controller.execute_action(action)

    def process_screenshot(self, screenshot_path: str):
        gems = image_utilities.parse_image(screenshot_path, game_state_constants.GAME_OVER_LOCATION)
        game_over = image_utilities.parse_image(screenshot_path, game_state_constants.GEMS_LOCATION)

        return gems, game_over

    def get_state(self):
        frame = self.screenshot()
        self.recent_frame = frame
        gems_str, game_over_str = self.process_screenshot('capture.png')
        gems_count = general_utilities.convert_string_to_int(gems_str)
        self.gems = gems_count
        if game_over_str.lower() == 'game over':
            self.game_over = True

        return self.recent_frame, self.gems, self.game_over

    def quit(self):
        print("Screenshots processed: " + str(self.counter))
        self.controller.quit()
