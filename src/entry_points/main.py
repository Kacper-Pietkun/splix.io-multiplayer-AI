from src.management.game_manager import GameManager
from src.constants import constant

if __name__ == '__main__':
    game_manager = GameManager(constant.GAME_MAX_FPS, constant.HEURISTIC_BOTS_NUMBER)
    game_manager.run()
