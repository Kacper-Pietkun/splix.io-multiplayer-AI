from src.players.player import Player
from src.constants import constant
from math import sqrt


class Bot(Player):

    def __init__(self, board, game_manager, player_id):
        super().__init__(board, game_manager, player_id)

    # abstract method
    def action(self, pressed_key):
        pass

    # my_x and my_y must be equal to self.x and sel.y or one of them might be differ by one
    # when specifying my_x and my_y different from self.x and self.y this function is used to determine distance for
    # the next move of the bot i.e. what would be the distance if bot went for instance to the left
    def get_distance_to_safe_zone(self, my_x, my_y):
        if self.x == my_x and self.y == my_y and self.is_out_of_safe_zone is False:
            return 0, (self.x, self.y)

        min_distance = constant.BOARD_WIDTH + constant.BOARD_HEIGHT
        closest_position = None
        for (x, y) in self.safe_zone_positions:
            distance = sqrt(pow(my_x - x, 2) + pow(my_y - y, 2))
            if distance < min_distance:
                min_distance = distance
                closest_position = (x, y)
            if min_distance == 0:
                break
        return min_distance, closest_position

    # the distance is from enemy to any part of this bot's body (it may be head or trail)
    # my_x and my_y must be equal to self.x and sel.y or one of them might be differ by one
    # when specifying my_x and my_y different from self.x and self.y this function is used to determine distance for
    # the next move of the bot i.e. what would be the distance if bot went for instance to the left
    def get_distance_to_closest_enemy(self, my_x, my_y):
        min_distance = constant.BOARD_WIDTH * constant.BOARD_HEIGHT
        for enemy in self.game_manager.players:
            if self.id != enemy.id:
                distance = sqrt(pow(enemy.x - my_x, 2) + pow(enemy.y - my_y, 2))
                if distance < min_distance:
                    min_distance = distance
                distance = sqrt(pow(enemy.x - self.x, 2) + pow(enemy.y - self.y, 2))
                if distance < min_distance:
                    min_distance = distance
                for (pos_x, pos_y) in self.trail_positions:
                    distance = sqrt(pow(enemy.x - pos_x, 2) + pow(enemy.y - pos_y, 2))
                    if distance < min_distance:
                        min_distance = distance
        return min_distance

    def will_that_tile_kill_me(self, position):
        x, y = position
        if x < 0 or x > constant.BOARD_WIDTH - 1 or y < 0 or y > constant.BOARD_HEIGHT - 1:
            return True
        tile = self.board.get_tile_information(x, y)
        if tile.is_trail is True and tile.owner_id == self.id:
            return True
        return False
