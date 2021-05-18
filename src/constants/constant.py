# DO NOT CHANGE IF YOU DON't NEED TO
# **********************************************************************************************************************
# Game
GAME_MAX_FPS = 65
BOTS_NUMBER = 0
GAME_TIME = 5 * 60 * 1000  # 5 min in milliseconds
MULTIPLAYER_MAX_NO_OF_PLAYERS = 13
MINIMAL_NUMBER_OF_PLAYER_TO_START = 2
TITLE = 'Splix.io'

# Single player modes
MODE_HEURISTIC_BOTS_ONLY = 0
MODE_NEAT_BOTS_ONLY = 1
MODE_BOTH_BOTS_ONLY = 2

# Directions
DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_RIGHT = 2
DIRECTION_DOWN = 3
DIRECTION_LEFT = 4
DIRECTION_INDEX_START = 1
DIRECTION_INDEX_END = 4

# Board
BOARD_WIDTH = 65
BOARD_HEIGHT = 65
BOARD_PLAYER_SPAWN_SIZE = 3
BOARD_TILE_NEUTRAL_COLOR = (77, 77, 77)

# Window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Player
PLAYER_DELTA_MOVEMENT = 0.125  # It must be: "< 1","finite binary expansion", # "x * PLAYER_DELTA_MOVEMENT = 1 (x > 1)"
PLAYER_NEUTRAL_INDEX = 0

# Heuristic bot
HEURISTIC_BOT_KILL_RANGE = 6  # bot will not go further than this value specifies, in order to kill another bot
HEURISTIC_BOT_FIND_KILL_OFFSET = 2  # Bot will search for other bots that he can kill in his safe zone or 2 tile away
HEURISTIC_BOT_SAFE_OFFSET = 5  # variable that helps to decide whether bot is in danger and should go to the safe zone
HEURISTIC_BOT_WANDER_LENGTH = 5  # If bot's trail is longer than given value, he goes back to the safe zone
HEURISTIC_BOT_GO_OUT_OF_SAFE_ZONE_CONDITION = 5  # variable that helps decide whether bot is safe to leave the safe zone
# **********************************************************************************************************************


# CHANGE IF YOU WANT
# **********************************************************************************************************************
# Neat bot
NUMBER_OF_HEURISTIC_BOTS_FOR_TRAINING = 60  # Add some heuristic bots, that will compete with neat bots while training
TRAINING_MAX_FPS = 0  # zero means it will be as fast as it can
VISUALIZE_TRAINING = False  # You can visualize training, however it slows down the whole process
SAVE_NEURAL_NETWORK_IMAGE_BEST_GENOME = True
SAVE_STATISTICS = True
SAVE_GENERATION_RATE = 1  # This number specifies how many generations must take place in order to save the progress
# size of the population must be set in the neat.conf file
# **********************************************************************************************************************
