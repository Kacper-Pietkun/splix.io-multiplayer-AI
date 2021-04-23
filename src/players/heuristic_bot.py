import heapq
from src.players.bot import Bot
from src.constants import constant
from math import sqrt
from random import randint


class HeuristicBot(Bot):

    def __init__(self, board, game_manager, safe_offset):
        super().__init__(board, game_manager)
        self.safe_offset = safe_offset  # used for determining whether player should move back to the safe zone
        self.is_following_a_path = False
        self.optimal_path = []

    def action(self, pressed_key):
        self.determine_next_move()
        self.movement()

    def determine_next_move(self):
        # Possibility of changing direction is allowed only when player's coordinates are whole numbers
        if self.x.is_integer() and self.y.is_integer() and self.is_dead is False:
            distance_to_kill, killing_position = self.get_distance_to_closest_enemy_trail()
            dist_to_safe_tile, safe_tile_pos = self.get_distance_to_safe_zone()
            dist_to_enemy = self.get_distance_to_closest_enemy()

            self.check_followed_path()
            if self.is_following_a_path:
                self.follow_path()
            elif distance_to_kill < dist_to_enemy and dist_to_safe_tile < constant.HEURISTIC_BOT_FIND_KILL_OFFSET and \
                    distance_to_kill < constant.HEURISTIC_BOT_KILL_RANGE:
                self.determine_path_to_the_tile(killing_position, distance_to_kill)
                self.follow_path()
                self.is_following_a_path = True
            elif self.is_out_of_safe_zone is False:
                self.direction = self.get_direction_that_will_not_kill_me()
            elif self.just_left_safe_zone is True:  # It prevents bot from doing an illegal move
                self.direction = self.get_direction_that_will_not_kill_me()
                self.just_left_safe_zone = False
            else:
                if dist_to_safe_tile + self.safe_offset >= dist_to_enemy or \
                        len(self.trail_positions) > constant.HEURISTIC_BOT_WANDER_LENGTH:
                    self.determine_path_to_the_tile(safe_tile_pos, dist_to_safe_tile)
                    self.follow_path()
                    self.is_following_a_path = True
                else:
                    # wander around unsafe zone
                    self.direction = self.get_direction_that_will_not_kill_me()

    # if bot follows path to kill other bot, check if the tile is still the trail of that bot's
    # if bot follows path to go back to the safe zone, check if the tile is still in his safe zone
    def check_followed_path(self):
        if len(self.optimal_path) > 0:
            dest_x, dest_y = self.optimal_path[-1]
            dest_tile = self.board.get_tile_information(dest_x, dest_y)
            if dest_tile.owner_id == self.id and dest_tile.is_trail:
                return
            if dest_tile.owner_id != self.id and dest_tile.is_trail:
                return

            # if the above conditions are not satisfied then stop following that path
            self.is_following_a_path = False
            self.optimal_path = []


    # follow path determined by A* algorithm
    def follow_path(self):
        if len(self.optimal_path) != 0:
            next_pos = self.optimal_path.pop(0)
            self.set_direction_for_pos(next_pos)
        else:
            self.direction = self.get_direction_that_will_not_kill_me()
            self.is_following_a_path = False

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
                return
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

    # compare whether positions are equal or not euqal
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

    # the distance is from enemy only to bot's head
    def get_distance_to_closest_enemy_from_head(self):
        min_distance = constant.BOARD_WIDTH * constant.BOARD_HEIGHT
        for enemy in self.game_manager.players:
            if self.id != enemy.id:
                distance = sqrt(pow(enemy.x - self.x, 2) + pow(enemy.y - self.y, 2))
                if distance < min_distance:
                    min_distance = distance
        return min_distance

    # Used for determining whether this bot should kill another one
    def get_distance_to_closest_enemy_trail(self):
        min_distance = constant.BOARD_WIDTH * constant.BOARD_HEIGHT
        closest_position = None
        for enemy in self.game_manager.players:
            if self.id != enemy.id:
                for (trail_x, trail_y) in enemy.trail_positions:
                    distance = sqrt(pow(trail_x - self.x, 2) + pow(trail_y - self.y, 2))
                    if distance < min_distance:
                        min_distance = distance
                        closest_position = (trail_x, trail_y)
        return min_distance, closest_position

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