# DO NOT CHANGE
# **********************************************************************************************************************
# Game
GAME_MAX_FPS = 60
HEURISTIC_BOTS_NUMBER = 60

# Directions
DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_RIGHT = 2
DIRECTION_DOWN = 3
DIRECTION_LEFT = 4
DIRECTION_INDEX_START = 1
DIRECTION_INDEX_END = 4

# Board
BOARD_WIDTH = 50
BOARD_HEIGHT = 50
BOARD_PLAYER_SPAWN_SIZE = 3
BOARD_TILE_NEUTRAL_COLOR = (77, 77, 77)

# Window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Player
PLAYER_DELTA_MOVEMENT = 0.125  # It must be: "< 1","finite binary expansion", # "x * PLAYER_DELTA_MOVEMENT = 1 (x > 1)"
PLAYER_NEUTRAL_INDEX = 0

# Heuristic bot
HEURISTIC_BOT_SAFE_OFFSET = 5
HEURISTIC_BOT_WANDER_LENGTH = 5
HEURISTIC_BOT_GO_OUT_OF_SAFE_ZONE_CONDITION = 5
# **********************************************************************************************************************


# CHANGE IF YOU WANT
# **********************************************************************************************************************
# Neat bot
TRAINING_MAX_FPS = 0  # zero means it will be as fast as it can
VISUALIZE_TRAINING = True  # You can visualize training, however it slows down the whole process
LOAD_POPULATION = True  # False - start learning from zero, True - load saved population from file
# size of the population must be set in the neat.conf file
# **********************************************************************************************************************
