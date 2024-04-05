import subprocess

from controller import Controller


class Environment:
    def __init__(self, window_id: str):
        self.state = None
        self.window_id = window_id
        self.controller = Controller()
        self.focus_window()

    def focus_window(self):
        subprocess.run(["xdotool", "windowactivate", self.window_id])

    def take_screenshot(self):
        try:
            subprocess.run(["import", "-window", self.window_id, "screenshot.png"])
        except subprocess.CalledProcessError:
            print("Error while taking screenshot.")

    def get_state(self):
        return self.state

    def get_action_space(self):
        return self.controller.get_actions()

    def take_action(self, action):
        self.controller.execute_action(action)

    def update_state(self):
        self.state = None