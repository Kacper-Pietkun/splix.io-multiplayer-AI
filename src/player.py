from random import randint
from operator import add
import constant
import pygame


class Player:
    players_number = 0  # static counter

    def __init__(self, board, game_manager):
        self.players_number = self.players_number + 1
        self.id = self.players_number  # First player starts with id = 1, because id = 0 is reserved for neutral state
        self.board = board
        self.game_manager = game_manager
        self.tile_color = (randint(50, 205), randint(50, 205), randint(50, 205))
        self.player_color = tuple(map(add, self.tile_color, (-50, -50, -50)))
        self.trail_color = tuple(map(add, self.tile_color, (50, 50, 50)))
        self.x, self.y = self.spawn_on_random_position()
        self.direction = constant.DIRECTION_NONE
        self.last_pressed_key = None
        self.is_out_of_safe_zone = False
        # We need max positions to determine the smallest possible area for a flood fill algorithm
        self.min_pos_y = int(self.y)
        self.max_pos_y = int(self.y + self.board.player_spawn_size - 1)
        self.min_pos_x = int(self.x)
        self.max_pos_x = int(self.x + self.board.player_spawn_size - 1)
        self.is_dead = False

    # Drawing position for the player until it finds available area
    def spawn_on_random_position(self):
        self.x = randint(0, self.board.width)
        self.y = randint(0, self.board.height)
        while not self.board.can_create_player_spawn(self.x, self.y):
            self.x = randint(0, self.board.width)
            self.y = randint(0, self.board.height)
        self.board.create_player_spawn(self.id, self.tile_color, self.x, self.y)
        return float(self.x), float(self.y)

    # We want to change direction only if player's coordinates are whole numbers
    # because player can move only on a grid created from tiles
    def change_direction(self, key):
        if key == pygame.K_UP or key == pygame.K_DOWN:
            if not self.x.is_integer():
                self.last_pressed_key = key
                return False
            elif key == pygame.K_UP:
                self.direction = constant.DIRECTION_UP
            else:
                self.direction = constant.DIRECTION_DOWN
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            if not self.y.is_integer():
                self.last_pressed_key = key
                return False
            elif key == pygame.K_LEFT:
                self.direction = constant.DIRECTION_LEFT
            else:
                self.direction = constant.DIRECTION_RIGHT
        return True

    # Change player's position
    def movement(self):
        if self.last_pressed_key is not None:
            if self.change_direction(self.last_pressed_key):
                self.last_pressed_key = None
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

    def die(self):
        if self.is_dead is False:
            self.board.clear_player_tiles(self)
            self.game_manager.players.remove(self)
            self.is_dead = True

    def kill_other_player(self, killed_player_id):
        if self.is_dead is False:
            self.board.clear_player_tiles(killed_player_id)
            self.game_manager.players.kill_player(killed_player_id)

    # trigger flood fill algorithm
    def extend_safe_zone(self):
        if self.is_dead is False:
            self.board.fill_zone(self)
            self.is_out_of_safe_zone = False

    # If player has moved to the next tile, he should leave a trial (paint adequate tile)
    def leave_trail(self):
        if self.x.is_integer() and self.y.is_integer() and self.is_out_of_safe_zone is True and self.is_dead is False:
            pos_x = int(self.x)
            pos_y = int(self.y)
            self.board.change_tile_information(self, pos_x, pos_y, is_trail=True)



