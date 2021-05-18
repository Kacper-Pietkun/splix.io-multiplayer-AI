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
            if self.genome.fitness >= 0:
                self.genome.fitness = sqrt(self.genome.fitness)  # player is punished for dying because of stagnation
            self.game_manager.kill_player(self.id)

        self.determine_next_move()
        self.movement()

    def determine_next_move(self):
        # Possibility of changing direction is allowed only when player's coordinates are whole numbers
        if self.x.is_integer() and self.y.is_integer() and self.is_dead is False:
            inputs = self.get_inputs()
            outputs = self.net.activate(inputs)

            relative_left = self.get_relative_direction(constant.DIRECTION_LEFT)
            relative_right = self.get_relative_direction(constant.DIRECTION_RIGHT)
            output = outputs[0]

            if output > 0.7:
                self.direction = relative_left
            elif output < -0.7:
                self.direction = relative_right

    def get_inputs(self):
        dist_straight_map_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_UP)
        dist_left_map_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_LEFT)
        dist_right_map_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_RIGHT)

        dist_safe_zone_border_straight = \
            self.get_distance_to_safe_zone_border_from_inside_in_relative_direction(constant.DIRECTION_UP)
        dist_safe_zone_border_left = \
            self.get_distance_to_safe_zone_border_from_inside_in_relative_direction(constant.DIRECTION_LEFT)
        dist_safe_zone_border_right = \
            self.get_distance_to_safe_zone_border_from_inside_in_relative_direction(constant.DIRECTION_RIGHT)

        dist_straight_map_border = 0 if (dist_straight_map_border != 1) else dist_straight_map_border
        dist_left_map_border = 0 if (dist_left_map_border != 1) else dist_left_map_border
        dist_right_map_border = 0 if (dist_right_map_border != 1) else dist_right_map_border

        distance_to_enemy = self.get_distance_to_closest_enemy(self.x, self.y)
        # current_x = self.x
        # current_y = self.y
        # current_direction = self.direction
        # relative_directions = [self.get_relative_direction(constant.DIRECTION_UP),
        #                        self.get_relative_direction(constant.DIRECTION_LEFT),
        #                        self.get_relative_direction(constant.DIRECTION_RIGHT)]
        # distances_to_enemies = []
        # distances_to_safe_zone = []
        # for direction in relative_directions:
        #     self.direction = direction
        #     self.simulate_movement()  # simulate movement in relative direction
        #     # distances_to_enemies.append(self.get_distance_to_closest_enemy(self.x, self.y))
        #     (distance, _) = self.get_distance_to_safe_zone(self.x, self.y)
        #     distances_to_safe_zone.append(distance)
        #     self.x = current_x  # reset bot's position and direction
        #     self.y = current_y
        #     self.direction = current_direction

        # input_list = [int(dist_left_border), int(dist_straight_border), int(dist_right_border)]
        # input_list.extend(distances_to_enemies)
        # input_list.extend(distances_to_safe_zone)

        input_list = [int(dist_straight_map_border), int(dist_left_map_border), int(dist_right_map_border),
                      int(dist_safe_zone_border_straight), int(dist_safe_zone_border_left),
                      int(dist_safe_zone_border_right), int(distance_to_enemy)]

        return input_list

    # When player is inside the safe zone, it returns distance in straight line
    # to the border of the safe zone in given direction
    def get_distance_to_safe_zone_border_from_inside_in_relative_direction(self, direction):
        if self.is_out_of_safe_zone:
            return 0

        relative_direction = self.get_relative_direction(direction)
        current_x = self.x
        current_y = self.y
        current_direction = self.direction
        self.direction = relative_direction
        distance = 0
        while (self.board.get_tile_information(int(self.x), int(self.y))).owner_id == self.id:
            self.simulate_movement()
            distance += 1
            # there is only map border
            if self.x < 0 or self.x > constant.BOARD_WIDTH - 1 or self.y < 0 or self.y > constant.BOARD_HEIGHT - 1:
                self.x = current_x
                self.y = current_y
                self.direction = current_direction
                return 0

        self.x = current_x
        self.y = current_y
        self.direction = current_direction
        return distance

    # just simulate it, change only x and y position of player, leave other variables unchanged
    # after simulating movement you have to remember to restore player's original position and direction
    def simulate_movement(self):
        if self.direction == constant.DIRECTION_UP:
            self.y = self.y - constant.PLAYER_DELTA_MOVEMENT
        elif self.direction == constant.DIRECTION_RIGHT:
            self.x = self.x + constant.PLAYER_DELTA_MOVEMENT
        elif self.direction == constant.DIRECTION_DOWN:
            self.y = self.y + constant.PLAYER_DELTA_MOVEMENT
        elif self.direction == constant.DIRECTION_LEFT:
            self.x = self.x - constant.PLAYER_DELTA_MOVEMENT

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
            return self.y + 1
        elif r_direction == constant.DIRECTION_LEFT:
            return self.x + 1
        elif r_direction == constant.DIRECTION_RIGHT:
            return self.board.width - self.x
        else:
            return self.board.height - self.y

    def extend_safe_zone(self):
        old_tiles_number = len(self.safe_zone_positions)
        super().extend_safe_zone()
        if self.is_dead is False:
            new_tiles_number = len(self.safe_zone_positions)
            delta_tiles_number = new_tiles_number - old_tiles_number
            self.genome.fitness += delta_tiles_number

    def die(self):
        if self.is_dead is False:
            self.genome.fitness -= 10  # punishment for bot
        super().die()




