import time
import typing
import pyautogui as gui


class Controller:
    def __init__(self):
        self.actions: typing.List[str] = [
            'hold_left',
            'release_left',
            'hold_right',
            'release_right',
            'press_space',
            'hold_space',
            'release_space',
            'none'
        ]

    """
    Execute input from algorithm based on user actions.
    """

    def  execute_action(self, action: str):
        match action:
            case 'hold_right':
                gui.keyUp('left')
                gui.keyDown('right')
            case 'release_right':
                gui.keyUp('right')
            case 'hold_left':
                gui.keyUp('right')
                gui.keyDown('left')
            case 'release_left':
                gui.keyUp('left')
            case 'press_space':
                gui.press('space')
            case 'hold_space':
                gui.keyDown('space')
            case 'release_space':
                gui.keyUp('space')
            case _:
                pass

    def get_actions(self):
        return self.actions

    def quit(self):
        gui.keyUp('left')
        gui.keyUp('right')
        gui.keyUp('space')