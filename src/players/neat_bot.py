from src.players.bot import Bot
from src.constants import constant
from random import randint
from math import sqrt


class NeatBot(Bot):
    def __init__(self, board, game_manager, genome, net):
        super().__init__(board, game_manager)
        self.genome = genome
        self.net = net
        self.time_alive = 0
        self.zone_time = 0
        self.out_of_zone_time = 0

    def action(self, pressed_key):
        if not self.is_dead:
            self.time_alive += 1
        if not self.is_out_of_safe_zone:
            self.zone_time += 1
        else:
            self.zone_time = 0

        # kill the player who doesn't move out of the safe zone
        if (self.zone_time > 200 and self.genome.fitness == 0) or self.zone_time > 1000:
            self.game_manager.kill_player(self.id)

        # encourage bot to move out of the safe zone
        if self.just_left_safe_zone is True:
            self.genome.fitness += 0.05
            self.just_left_safe_zone = False

        self.determine_next_move()
        self.movement()

    def determine_next_move(self):
        # Possibility of changing direction is allowed only when player's coordinates are whole numbers
        if self.x.is_integer() and self.y.is_integer() and self.is_dead is False:
            inputs = self.get_inputs()
            outputs = self.net.activate(inputs)

            max_index = 0
            max_value = -2
            for i in range(0, len(outputs)):
                if max_value <= outputs[i]:
                    max_value = outputs[i]
                    max_index = i

            if max_index == 0:  # turn left
                self.direction = self.get_relative_direction(constant.DIRECTION_LEFT)
            elif max_index == 1:  # turn right
                self.direction = self.get_relative_direction(constant.DIRECTION_RIGHT)
            else:  # max_index == 2:  # don't turn
                self.direction = self.get_relative_direction(constant.DIRECTION_UP)

    def get_inputs(self):
        (distance_to_safe_zone, _) = self.get_distance_to_safe_zone()
        distance_to_closest_wall = self.get_distance_to_closest_wall()
        dist_to_closest_enemy = self.get_distance_to_closest_enemy()

        return [distance_to_safe_zone, distance_to_closest_wall, dist_to_closest_enemy]

    def get_relative_direction(self, direction):
        # constant.DIRECTION_UP - go straight
        # constant.DIRECTION_LEFT - go left
        # constant.DIRECTION_RIGHT - go right
        if self.direction == constant.DIRECTION_NONE:
            self.direction = randint(1, 4)
        if direction == constant.DIRECTION_UP:
            return self.direction
        if direction == constant.DIRECTION_LEFT:
            return (self.direction - 1 + constant.DIRECTION_LEFT - 1) % 4 + 1
        if direction == constant.DIRECTION_RIGHT:
            return self.direction % 4 + 1

    def get_distance_to_closest_wall(self):
        return min(self.x + 1, constant.BOARD_WIDTH - self.x, self.y + 1, constant.BOARD_HEIGHT - self.y)

    def extend_safe_zone(self):
        old_tiles_number = len(self.safe_zone_positions)
        super().extend_safe_zone()
        if self.is_dead is False:
            new_tiles_number = len(self.safe_zone_positions)
            delta_tiles_number = new_tiles_number - old_tiles_number
            self.genome.fitness += delta_tiles_number

    def kill_other_player(self, killed_player_id):
        super().kill_other_player(killed_player_id)
        if self.is_dead is False:
            # self.genome.fitness += 0.05
            pass

    def die(self):
        if self.is_dead is False:
            self.genome.fitness = sqrt(self.genome.fitness)
            self.genome.fitness -= 10  # punishment for bot
        super().die()




