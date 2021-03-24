from player import Player
import constant
from math import sqrt
import heapq
from random import randint


class HeuristicBot(Player):

    def __init__(self, board, game_manager, safe_offset):
        super().__init__(board, game_manager)
        self.safe_zone_positions = set()
        self.safe_offset = safe_offset  # used for determining whether player should move back to the safe zone
        self.go_back_to_safe_zone = False
        self.optimal_path = []
        for i in range(0, constant.BOARD_PLAYER_SPAWN_SIZE):
            for j in range(0, constant.BOARD_PLAYER_SPAWN_SIZE):
                self.safe_zone_positions.add((int(self.x) - 1 + i, int(self.y) - 1 + j))

    def action(self, pressed_key):
        self.determine_next_move()
        self.movement()

    def determine_next_move(self):
        # Possibility of changing direction is allowed only when player's coordinates are whole numbers
        if self.x.is_integer() and self.y.is_integer() and self.is_dead is False:
            if self.is_out_of_safe_zone is False:
                self.direction = self.get_direction_that_will_not_kill_me()
                self.go_back_to_safe_zone = False
            elif self.just_left_safe_zone is True:  # It prevents bot from doing an illegal move
                self.direction = self.get_direction_that_will_not_kill_me()
                self.just_left_safe_zone = False
            else:
                dist_to_enemy = self.get_distance_to_closest_enemy()
                dist_to_safe_tile, safe_tile_pos = self.get_distance_to_safe_zone()
                if dist_to_safe_tile + self.safe_offset >= dist_to_enemy or \
                        len(self.trail_positions) > constant.HEURISTIC_BOT_WANDER_LENGTH:
                    # move back to the safe zone
                    if self.go_back_to_safe_zone is False or len(self.optimal_path) == 0:
                        self.determine_path_to_the_tile(safe_tile_pos, dist_to_safe_tile)
                        self.go_back_to_safe_zone = True
                        self.follow_path()
                    else:
                        self.follow_path()
                else:
                    # wander around unsafe zone
                    self.direction = self.get_direction_that_will_not_kill_me()
                    self.go_back_to_safe_zone = False

    # follow path determined by A* algorithm
    def follow_path(self):
        next_pos = self.optimal_path.pop(0)
        self.set_direction_for_pos(next_pos)

    def set_direction_for_pos(self, pos):
        pos_x, pos_y = pos
        if pos_x == self.x + 1:
            self.direction = constant.DIRECTION_RIGHT
        elif pos_x == self.x - 1:
            self.direction = constant.DIRECTION_LEFT
        elif pos_y == self.y - 1:
            self.direction = constant.DIRECTION_UP
        elif pos_y == self.y + 1:
            self.direction = constant.DIRECTION_DOWN

    # A* algorithm for finding the shortest path to the safe zone
    def determine_path_to_the_tile(self, destination_position, smallest_distance):
        # list will contain tuples that have:
        # (heuristic distance + normal distance, normal distance from start, it's own position, parent's position)
        priority_queue = []
        done_elements = []
        heapq.heapify(priority_queue)
        heapq.heappush(priority_queue, (smallest_distance, 0, (int(self.x), int(self.y)), None))
        while True:
            if len(priority_queue) == 0:
                pass
            (whole_distance, norm_dist, own_pos, parent_pos) = heapq.heappop(priority_queue)
            if self.compare_positions(own_pos, destination_position) is True:
                heapq.heappush(priority_queue, (whole_distance, norm_dist, own_pos, parent_pos))
                break
            own_pos_x, own_pos_y = own_pos
            neighbours = [(own_pos_x + 1, own_pos_y), (own_pos_x, own_pos_y + 1),
                          (own_pos_x - 1, own_pos_y), (own_pos_x, own_pos_y - 1)]
            for n_x, n_y in neighbours:
                # bot cannot walk through its trail and go outside of the map
                if self.will_that_tile_kill_me((n_x, n_y)) is False:
                    # check if this positions is already in done_elements
                    was_it_before = next((x for x in done_elements if
                                          self.compare_positions(x[2], (n_x, n_y)) is True), None)
                    if was_it_before is not None:
                        continue
                    # check if this positions is already in priority queue
                    # if it is then choose option with smaller distance
                    org_from_list = next((x for x in priority_queue if
                                          self.compare_positions(x[2], (n_x, n_y)) is True), None)

                    dist = self.get_distance((n_x, n_y), destination_position) + norm_dist + 1
                    if org_from_list is not None and org_from_list[1] > norm_dist + 1:
                        # delete old value
                        priority_queue = list(filter(lambda x: self.compare_positions(x[2], (n_x, n_y) is False),
                                                     priority_queue))
                        # add updated value
                        heapq.heappush(priority_queue, (dist, norm_dist + 1, (n_x, n_y), own_pos))
                    elif org_from_list is None:
                        heapq.heappush(priority_queue, (dist, norm_dist + 1, (n_x, n_y), own_pos))
            done_elements.append((whole_distance, norm_dist, own_pos, parent_pos))
        # reconstruct the shortest path
        (_, _, own_pos, parent_pos) = heapq.heappop(priority_queue)
        self.optimal_path = [own_pos]
        while True:
            next_element = next((x for x in done_elements if
                                 self.compare_positions(x[2], parent_pos) is True), None)
            if next_element is None:
                pass
            (_, _, own_pos, parent_pos) = next_element
            self.optimal_path.insert(0, own_pos)
            if self.compare_positions(own_pos, (self.x, self.y)):
                self.optimal_path.remove(own_pos)
                break

    def compare_positions(self, pos_1, pos_2):
        x_1, y_1 = pos_1
        x_2, y_2 = pos_2
        if x_1 == x_2 and y_1 == y_2:
            return True
        return False

    def get_distance(self, pos_1, pos_2):
        x_1, y_1 = pos_1
        x_2, y_2 = pos_2
        return sqrt(pow(x_1 - x_2, 2) + pow(y_1 - y_2, 2))

    # There is a possibility that bot is in the dead lock, so every direction will get him killed
    # That is why we have created counter that allows only to draw new direction ten times
    # after ten times totally random direction will be chosen
    def get_direction_that_will_not_kill_me(self):
        counter = 0
        drawn_direction = randint(constant.DIRECTION_INDEX_START, constant.DIRECTION_INDEX_END)
        next_position = self.get_next_position(drawn_direction, 1)
        while (self.will_that_tile_kill_me(next_position) or
               (self.is_it_opposite_direction(drawn_direction) and self.is_out_of_safe_zone) or
               self.does_it_collide_with_my_trail((int(self.x), int(self.y)), next_position) or
               self.will_go_to_the_enemy(next_position)) and \
                counter < 20:
            drawn_direction = randint(constant.DIRECTION_INDEX_START, constant.DIRECTION_INDEX_END)
            next_position = self.get_next_position(drawn_direction, 1)
            counter += 1
        return drawn_direction

    def will_go_to_the_enemy(self, next_pos):
        if self.is_out_of_safe_zone is False and next_pos not in self.safe_zone_positions:
            if self.get_distance_to_closest_enemy_from_head() < constant.HEURISTIC_BOT_GO_OUT_OF_SAFE_ZONE_CONDITION:
                return True
        return False

    def will_that_tile_kill_me(self, position):
        x, y = position
        if x < 0 or x > constant.BOARD_WIDTH - 1 or y < 0 or y > constant.BOARD_HEIGHT - 1:
            return True
        tile = self.board.get_tile_information(x, y)
        if tile.is_trail is True and tile.owner_id == self.id:
            return True
        return False

    # in order to avoid dead lock we cannot let bot to move to the tiles that collide with the trail
    # one exception when bot can move like that can occur when A* algorithm assign such path
    def does_it_collide_with_my_trail(self, head_position, position):
        pos_x, pos_y = position
        head_x, head_y = head_position
        neighbours = [(pos_x + 1, pos_y), (pos_x, pos_y + 1), (pos_x - 1, pos_y), (pos_x, pos_y - 1)]
        neighbours.remove((head_x, head_y))
        for trail_x, trail_y in self.trail_positions:
            for neighbour_x, neighbour_y in neighbours:
                if trail_x == neighbour_x and trail_y == neighbour_y:
                    return True
        return False

    # opposite directions are UP and DOWN, LEFT and RIGHT
    def is_it_opposite_direction(self, drawn_direction):
        if self.direction == constant.DIRECTION_UP and drawn_direction == constant.DIRECTION_DOWN or \
                self.direction == constant.DIRECTION_DOWN and drawn_direction == constant.DIRECTION_UP or \
                self.direction == constant.DIRECTION_LEFT and drawn_direction == constant.DIRECTION_RIGHT or \
                self.direction == constant.DIRECTION_RIGHT and drawn_direction == constant.DIRECTION_LEFT:
            return True
        return False

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

    # the distance is from enemy only to bot's head
    def get_distance_to_closest_enemy_from_head(self):
        min_distance = constant.BOARD_WIDTH * constant.BOARD_HEIGHT
        for enemy in self.game_manager.players:
            if self.id != enemy.id:
                distance = sqrt(pow(enemy.x - self.x, 2) + pow(enemy.y - self.y, 2))
                if distance < min_distance:
                    min_distance = distance
        return min_distance

    # # returns length of the path in a straight line and also returns the position of the closest tile in the safe zone
    def get_distance_to_safe_zone(self):
        if self.is_out_of_safe_zone is False:
            return 0
        min_distance = constant.BOARD_WIDTH + constant.BOARD_HEIGHT
        closest_position = None
        for (x, y) in self.safe_zone_positions:
            distance = sqrt(pow(self.x - x, 2) + pow(self.y - y, 2))
            if distance < min_distance:
                min_distance = distance
                closest_position = (x, y)
        return min_distance, closest_position

    # trigger flood fill algorithm
    def extend_safe_zone(self):
        if self.is_dead is False:
            new_tiles_information, players_that_lost_zone = self.board.fill_zone(self)
            self.game_manager.update_players_safe_zone(players_that_lost_zone)
            self.is_out_of_safe_zone = False
            self.just_left_safe_zone = False
            # add positions of new tiles in the safe zone to the array
            for i in range(1, self.max_pos_x - self.min_pos_x + 2):
                for j in range(1, self.max_pos_y - self.min_pos_y + 2):
                    if new_tiles_information[i][j] != -1:
                        self.safe_zone_positions.add((self.min_pos_x + i - 1, self.min_pos_y + j - 1))
            # bot moved back to the safe zone so he has no trail
            self.trail_positions = []

    # Basing on the player's current position and given, as a parameter, direction, we get the position of next tile
    # that player will move to
    def get_next_position(self, assumed_direction, number_of_turns):
        next_x = int(self.x)
        next_y = int(self.y)
        if assumed_direction == constant.DIRECTION_UP:
            next_y -= number_of_turns
        elif assumed_direction == constant.DIRECTION_RIGHT:
            next_x += number_of_turns
        elif assumed_direction == constant.DIRECTION_DOWN:
            next_y += number_of_turns
        elif assumed_direction == constant.DIRECTION_LEFT:
            next_x -= number_of_turns
        return next_x, next_y

    def update_safe_zone(self):
        self.safe_zone_positions = set(filter(lambda el: (self.board.get_tile_information(el[0], el[1]).owner_id ==
                                                          self.id), self.safe_zone_positions))
        pass

    def change_direction(self, key):
        pass

