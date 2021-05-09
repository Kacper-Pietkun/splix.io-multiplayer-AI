from src.players.player import Player
from src.constants import constant
import pygame


class HumanPlayer(Player):

    def __init__(self, board, game_manager, player_id):
        super().__init__(board, game_manager, player_id)

    def action(self, pressed_key):
        self.change_direction(pressed_key)
        self.movement()

    def movement(self):
        if self.last_pressed_key is not None:
            if self.change_direction(self.last_pressed_key):
                self.last_pressed_key = None
        super().movement()

    # We want to change direction only if player's coordinates are whole numbers
    # because player can move only on a grid created from tiles
    def change_direction(self, key):
        if key == pygame.K_UP or key == pygame.K_DOWN:
            if not self.x.is_integer():
                self.last_pressed_key = key
                return False
            elif key == pygame.K_UP:
                self.direction = constant.DIRECTION_UP
            else:
                self.direction = constant.DIRECTION_DOWN
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            if not self.y.is_integer():
                self.last_pressed_key = key
                return False
            elif key == pygame.K_LEFT:
                self.direction = constant.DIRECTION_LEFT
            else:
                self.direction = constant.DIRECTION_RIGHT
        return True
