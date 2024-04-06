"""
Game Screen Locations
When looking at a game screen there are certain states displayed on screen that display in a consistent position.
Parsing these values appropriately is important for determining state and rewards as well as tracking metrics for each
episode.

These values represent the absolute window positions of the game screen in the format:
(top-left x, top-left y, bottom-right x, bottom-right y).

This is for an image size of 380 x 284 pixels, which is a game display scale of 1x
(Downwell allows scale for the game to vary between 1x and 6x). Using minimal image size makes it easier to train
algorithms but makes image processing more difficult due to certain packages like pytesseract having difficulty
parsing strings from smaller images.
"""

GAME_OVER_LOCATION = (151, 61, 229, 72)  # This is critical for determining end of an episode

CURRENT_HEALTH_LOCATION = (15, 9, 47, 18)
MAX_HEALTH_LOCATION = (55, 9, 92, 18)
GEMS_LOCATION = (312, 11, 354, 21)

LEVEL_LOCATION_GAME_OVER_SCREEN = (133, 83, 199, 92)
KILLS_LOCATION_GAME_OVER_SCREEN = (132, 102, 197, 113)
MAX_COMBO_LOCATION_GAME_OVER_SCREEN = (133, 115, 212, 128)
TIME_LOCATION_GAME_OVER_SCREEN = (132, 131, 232, 141)
