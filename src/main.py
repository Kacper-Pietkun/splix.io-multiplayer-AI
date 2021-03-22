from game_manager import GameManager
import constant

if __name__ == '__main__':
    game_manager = GameManager(constant.GAME_MAX_FPS, constant.HEURISTIC_BOTS_NUMBER)
    game_manager.start_game()
