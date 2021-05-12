from src.players.bot import Bot
from src.constants import constant
from random import randint
from math import sqrt, inf


class NeatBot(Bot):
    def __init__(self, board, game_manager, genome, net, player_id):
        super().__init__(board, game_manager, player_id)
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
        # if self.just_left_safe_zone is True:
        #     self.genome.fitness += 0.05
        #     self.just_left_safe_zone = False

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

            if not self.is_it_opposite_direction(max_index + 1):
                # directions are constants from 1 to 4
                self.direction = max_index + 1

    def get_inputs(self):
        relative_straight = self.get_relative_direction(constant.DIRECTION_UP)
        relative_left = self.get_relative_direction(constant.DIRECTION_LEFT)
        relative_right = self.get_relative_direction(constant.DIRECTION_RIGHT)

        dist_straight_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_UP)
        dist_left_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_LEFT)
        dist_right_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_RIGHT)

        dist_straight_enemy_trail = self.get_distance_to_closest_enemy_in_direction(relative_straight)
        dist_left_enemy_trail = self.get_distance_to_closest_enemy_in_direction(relative_left)
        dist_right_enemy_trail = self.get_distance_to_closest_enemy_in_direction(relative_right)

        dist_straight_own_trail = self.get_distance_to_my_trail_in_direction(relative_straight)
        dist_left_own_trail = self.get_distance_to_my_trail_in_direction(relative_left)
        dist_right_own_trail = self.get_distance_to_my_trail_in_direction(relative_right)

        (distance_to_safe_zone, position_of_safe_zone) = self.get_distance_to_safe_zone(self.x, self.y)

        return [int(dist_left_border), int(dist_straight_border), int(dist_right_border),
                int(dist_left_enemy_trail), int(dist_straight_enemy_trail), int(dist_right_enemy_trail),
                int(dist_left_own_trail), int(dist_straight_own_trail), int(dist_right_own_trail),
                self.is_out_of_safe_zone, int(distance_to_safe_zone),
                ]

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

    def get_distance_to_wall_in_relative_direction(self, direction):
        r_direction = self.get_relative_direction(direction)
        if r_direction == constant.DIRECTION_UP:
            return self.y
        elif r_direction == constant.DIRECTION_LEFT:
            return self.x
        elif r_direction == constant.DIRECTION_RIGHT:
            return self.board.width - self.x
        else:
            return self.board.height - self.y


    def get_distance_to_closest_trail_in_direction(self, direction, who):
        min_distance = constant.BOARD_WIDTH * constant.BOARD_HEIGHT
        for enemy in self.game_manager.players:
            if (who == 'enemy' and self.id != enemy.id) or (who == "me" and self.id == enemy.id):
                if direction in (constant.DIRECTION_LEFT, constant.DIRECTION_RIGHT):
                    for (pos_x, pos_y) in enemy.trail_positions:
                        if pos_y == self.y and pos_x != self.x:
                            distance = pos_x - self.x
                            if direction == constant.DIRECTION_LEFT:
                                if distance < 0:
                                    distance *= -1
                                    if distance < min_distance:
                                        min_distance = distance
                            else:
                                if 0 <= distance < min_distance:
                                    min_distance = distance
                else:
                    for (pos_x, pos_y) in enemy.trail_positions:
                        if pos_x == self.x and pos_y != self.y:
                            distance = pos_y - self.y
                            if direction == constant.DIRECTION_UP:
                                if distance < 0:
                                    distance *= -1
                                    if distance < min_distance:
                                        min_distance = distance
                            else:
                                if 0 <= distance < min_distance:
                                    min_distance = distance
        return min_distance


    def get_distance_to_my_trail_in_direction(self, direction):
        return self.get_distance_to_closest_trail_in_direction(direction, 'me')

    def get_distance_to_closest_enemy_in_direction(self, direction):
        return self.get_distance_to_closest_trail_in_direction(direction, 'enemy')

    def get_distance_to_closest_wall(self, my_x, my_y):
        return min(my_x + 1, constant.BOARD_WIDTH - my_x, my_y + 1, constant.BOARD_HEIGHT - my_y)

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
            if self.genome.fitness >= 0:
                self.genome.fitness = sqrt(self.genome.fitness)
            self.genome.fitness -= 10  # punishment for bot
        super().die()




