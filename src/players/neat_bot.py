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

            # directions are constants from 1 to 4
            self.direction = max_index + 1

    def get_inputs(self):
        all_next_positions = [(int(self.x), int(self.y - 1)),
                              (int(self.x), int(self.y + 1)),
                              (int(self.x + 1), int(self.y)),
                              (int(self.x - 1), int(self.y))]
        all_inputs = []

        for next_x, next_y in all_next_positions:
            will_it_kill_me = self.will_that_tile_kill_me((next_x, next_y))
            dist_to_enemy = 0 if will_it_kill_me else self.get_distance_to_closest_enemy(next_x, next_y)
            dist_to_wall = 0 if will_it_kill_me else self.get_distance_to_closest_wall(next_x, next_y)
            dist_to_safe_zone, _ = inf, inf if will_it_kill_me else self.get_distance_to_safe_zone(next_x, next_y)
            all_inputs.extend([will_it_kill_me, dist_to_safe_zone])
        return all_inputs

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




