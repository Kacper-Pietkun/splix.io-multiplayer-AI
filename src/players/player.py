from random import randint
from operator import add
from src.constants import constant


class Player:

    def __init__(self, board, game_manager, player_id):
        self.id = player_id  # First player starts with id = 1, because id = 0 is reserved for neutral state
        self.board = board
        self.game_manager = game_manager
        self.tile_color = (randint(50, 205), randint(50, 205), randint(50, 205))
        self.player_color = tuple(map(add, self.tile_color, (randint(-50, -30), randint(-50, -30), randint(-50, -30))))
        self.trail_color = tuple(map(add, self.tile_color, (randint(30, 50), randint(30, 50), randint(30, 50))))
        self.x, self.y = self.spawn_on_random_position()
        self.direction = constant.DIRECTION_NONE
        self.last_pressed_key = None
        self.is_out_of_safe_zone = False
        self.just_left_safe_zone = False
        # We need max positions to determine the smallest possible area for a flood fill algorithm
        self.min_pos_y = int(self.y - int(self.board.player_spawn_size / 2))
        self.max_pos_y = int(self.y + int(self.board.player_spawn_size / 2))
        self.min_pos_x = int(self.x - int(self.board.player_spawn_size / 2))
        self.max_pos_x = int(self.x + int(self.board.player_spawn_size / 2))
        self.is_dead = False
        self.trail_positions = []
        self.safe_zone_positions = set()
        for i in range(0, constant.BOARD_PLAYER_SPAWN_SIZE):
            for j in range(0, constant.BOARD_PLAYER_SPAWN_SIZE):
                self.safe_zone_positions.add((int(self.x) - 1 + i, int(self.y) - 1 + j))

    # Drawing position for the player until it finds available area
    def spawn_on_random_position(self):
        self.x = randint(0, self.board.width)
        self.y = randint(0, self.board.height)
        i = 0
        while not self.board.can_create_player_spawn(self.x, self.y) and i < 25:
            self.x = randint(1, self.board.width - 1)
            self.y = randint(1, self.board.height - 1)
            i += 1
        self.board.create_player_spawn(self.id, self.tile_color, self.x, self.y)
        self.game_manager.update_players_safe_zone([])
        # player's initial position is in the center of his safe zone
        self.x += int(self.board.player_spawn_size / 2)
        self.y += int(self.board.player_spawn_size / 2)
        return float(self.x), float(self.y)

    # abstract method
    def action(self, pressed_key):
        pass

    # Change player's position
    def movement(self):
        if self.direction == constant.DIRECTION_UP:
            self.y = self.y - constant.PLAYER_DELTA_MOVEMENT
        elif self.direction == constant.DIRECTION_RIGHT:
            self.x = self.x + constant.PLAYER_DELTA_MOVEMENT
        elif self.direction == constant.DIRECTION_DOWN:
            self.y = self.y + constant.PLAYER_DELTA_MOVEMENT
        elif self.direction == constant.DIRECTION_LEFT:
            self.x = self.x - constant.PLAYER_DELTA_MOVEMENT
        self.update_max_positions()
        self.check_boundaries()
        self.check_current_tile()
        self.leave_trail()

    def update_max_positions(self):
        if self.x.is_integer():
            if self.x > self.max_pos_x:
                self.max_pos_x = int(self.x)
            elif self.x < self.min_pos_x:
                self.min_pos_x = int(self.x)
        if self.y.is_integer():
            if self.y > self.max_pos_y:
                self.max_pos_y = int(self.y)
            elif self.y < self.min_pos_y:
                self.min_pos_y = int(self.y)

    # Checking if player did not go outside of the map
    def check_boundaries(self):
        if self.x < 0 or self.x > self.board.width - 1 or\
                self.y < 0 or self.y > self.board.height - 1:
            self.die()

    # if player moves to the next tile, it may mean a lot of things
    # player could kill other player by crossing theirs trail
    # player could kill himself by crossing his own trail
    # player could come back to the safe zone after leaving a trail
    # player could leave his safe zone
    def check_current_tile(self):
        if self.x.is_integer() and self.y.is_integer():
            tile = self.board.get_tile_information(int(self.x), int(self.y))
            if tile.owner_id == self.id and tile.is_trail is True:
                self.die()  # Player kills himself
            if tile.owner_id != self.id and tile.is_trail is True:
                self.kill_other_player(tile.owner_id)  # Player kills someone
            if tile.owner_id == self.id and tile.is_trail is False and self.is_out_of_safe_zone is True:
                self.extend_safe_zone()  # player returned to the safe zone
            if tile.owner_id != self.id and self.is_out_of_safe_zone is False:
                self.is_out_of_safe_zone = True  # player left safe zone
                self.just_left_safe_zone = True

    def die(self):
        if self.is_dead is False:
            self.board.clear_player_tiles(self)
            self.is_dead = True

    def kill_other_player(self, killed_player_id):
        if self.is_dead is False:
            self.game_manager.kill_player(killed_player_id)

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

    # If player has moved to the next tile, he should leave a trial (paint adequate tile)
    def leave_trail(self):
        if self.x.is_integer() and self.y.is_integer() and self.is_out_of_safe_zone is True and self.is_dead is False:
            pos_x = int(self.x)
            pos_y = int(self.y)
            tile = self.board.get_tile_information(pos_x, pos_y)
            player_index = set()
            player_index.add(tile.owner_id)
            self.board.change_tile_information(self, pos_x, pos_y, is_trail=True)
            self.trail_positions.append((pos_x, pos_y))
            if tile.owner_id != constant.PLAYER_NEUTRAL_INDEX:
                self.game_manager.update_players_safe_zone(player_index)

    def update_safe_zone(self):
        self.safe_zone_positions = set(filter(lambda el: (self.board.get_tile_information(el[0], el[1]).owner_id ==
                                                          self.id), self.safe_zone_positions))

    def change_color_set(self, player_color, tile_color, trail_color):
        self.player_color = player_color
        self.tile_color = tile_color
        self.trail_color = trail_color
        for tile_x, tile_y in self.safe_zone_positions:
            self.board.change_tile_information(self, tile_x, tile_y, is_trail=False)
        for tile_x, tile_y in self.trail_positions:
            self.board.change_tile_information(self, tile_x, tile_y, is_trail=True)

