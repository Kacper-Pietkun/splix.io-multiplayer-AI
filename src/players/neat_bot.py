from src.players.bot import Bot
from src.constants import constant
from random import randint


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
        if self.zone_time > 300 and self.zone_time % 20 == 0:
            self.genome.fitness -= 0.05
        if self.zone_time > 480 or self.genome.fitness < -100:  # kill the player who doesn't move out of the safe zone
            self.game_manager.kill_player(self.id)

        self.determine_next_move()
        self.movement()

    def determine_next_move(self):
        # Possibility of changing direction is allowed only when player's coordinates are whole numbers
        if self.x.is_integer() and self.y.is_integer() and self.is_dead is False:
            inputs = self.get_inputs()

            if inputs[4] > 10:             # distance_to_safe_zone
                self.genome.fitness -= 0.025
            elif 2 <= inputs[4] <= 10:     # distance_to_safe_zone
                self.genome.fitness += 0.01
            if inputs[1] <= 1:              # there is a border at the bot's path
                self.genome.fitness -= 0.5

            outputs = self.net.activate(inputs)
            direction = outputs[0]
            if direction <= -0.2:  # turn left
                self.direction = self.get_relative_direction(constant.DIRECTION_LEFT)
            elif direction >= 0.2:  # turn right
                self.direction = self.get_relative_direction(constant.DIRECTION_RIGHT)
            else:  # don't turn
                self.direction = self.get_relative_direction(constant.DIRECTION_UP)

    def get_inputs(self):
        dist_straight_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_UP)
        dist_left_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_LEFT)
        dist_right_border = self.get_distance_to_wall_in_relative_direction(constant.DIRECTION_RIGHT)

        dist_to_closest_enemy = self.get_distance_to_closest_enemy()
        (distance_to_safe_zone, _) = self.get_distance_to_safe_zone()

        return [int(dist_left_border), int(dist_straight_border), int(dist_right_border),
                int(dist_to_closest_enemy), int(distance_to_safe_zone)]

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
            return self.board.width-self.x
        else:
            return self.board.height-self.y

    def extend_safe_zone(self):
        old_tiles_number = len(self.safe_zone_positions)
        super().extend_safe_zone()
        if self.is_dead is False:
            new_tiles_number = len(self.safe_zone_positions)
            delta_tiles_number = new_tiles_number - old_tiles_number

            if delta_tiles_number == 2:
                self.genome.fitness += 0.025  # increase the fitness
            if delta_tiles_number > 2:
                self.genome.fitness += delta_tiles_number * 0.05  # increase the fitness

    def kill_other_player(self, killed_player_id):
        super().kill_other_player(killed_player_id)
        if self.is_dead is False:
            # self.genome.fitness += 0.05
            pass

    def die(self):
        if self.is_dead is False:
            self.genome.fitness -= 1  # punishment for bot
        super().die()







