from src.players.player import Player
from src.constants import constant
from math import sqrt


class Bot(Player):

    def __init__(self, board, game_manager):
        super().__init__(board, game_manager)

    # abstract method
    def action(self, pressed_key):
        pass

    def get_distance_to_safe_zone(self):
        if self.is_out_of_safe_zone is False:
            return 0, (self.x, self.y)
        min_distance = constant.BOARD_WIDTH + constant.BOARD_HEIGHT
        closest_position = None
        for (x, y) in self.safe_zone_positions:
            distance = sqrt(pow(self.x - x, 2) + pow(self.y - y, 2))
            if distance < min_distance:
                min_distance = distance
                closest_position = (x, y)
        return min_distance, closest_position

    # the distance is from enemy to any part of this bot's body (it may be head or trail)
    def get_distance_to_closest_enemy(self):
        min_distance = constant.BOARD_WIDTH * constant.BOARD_HEIGHT
        for enemy in self.game_manager.players:
            if self.id != enemy.id:
                for (pos_x, pos_y) in self.trail_positions:
                    distance = sqrt(pow(enemy.x - pos_x, 2) + pow(enemy.y - pos_y, 2))
                    if distance < min_distance:
                        min_distance = distance
        return min_distance
