from random import randint
from operator import add
import constant
import pygame


class Player:
    players_number = 0  # static counter

    def __init__(self, board):
        self.players_number = self.players_number + 1
        self.id = self.players_number  # First player starts with id = 1, because id = 0 is reserved for neutral state
        self.board = board
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
        self.leave_trail()
        self.update_max_positions()

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

    # If player has moved to the next tile, he should leave a trial (paint adequate tile)
    def leave_trail(self):
        if self.x.is_integer() and self.y.is_integer():
            left_trail = self.board.leave_a_trail(self.id, self.trail_color, self.x, self.y)
            # Condition check whether player came back to the safe zone
            # If he did then we should activate flood fill algorithm to color tiles that are marked by a player's trail
            if not left_trail and self.is_out_of_safe_zone:
                self.board.fill_zone(self.id, self.tile_color, self.min_pos_y, self.max_pos_y,
                                     self.min_pos_x, self.max_pos_x)
            self.is_out_of_safe_zone = left_trail
