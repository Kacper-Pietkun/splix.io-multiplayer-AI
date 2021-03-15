from random import randint
from operator import add
import constant
import pygame


class Player:
    players_number = 0

    def __init__(self, board):
        self.players_number = self.players_number + 1
        self.id = self.players_number
        self.board = board
        self.tile_color = (randint(50, 205), randint(50, 205), randint(50, 205))
        self.player_color = tuple(map(add, self.tile_color, (-50, -50, -50)))
        self.trail_color = tuple(map(add, self.tile_color, (50, 50, 50)))
        self.x = 0
        self.y = 0
        self.spawn_on_random_position()
        self.direction = constant.DIRECTION_NONE
        self.last_pressed_key = None
        self.is_out_of_zone = False
        self.y_top = self.y
        self.y_bottom = self.y + self.board.player_spawn_size - 1
        self.x_left = self.x
        self.x_right = self.x + self.board.player_spawn_size - 1

    def spawn_on_random_position(self):
        self.x = randint(0, self.board.width)
        self.y = randint(0, self.board.height)
        while not self.board.can_create_player_spawn(self.x, self.y):
            self.x = randint(0, self.board.width)
            self.y = randint(0, self.board.height)
        self.board.create_player_spawn(self.id, self.tile_color, self.x, self.y)
        self.x = float(self.x)
        self.y = float(self.y)

    def change_direction(self, key):
        # We want to change direction only if player's coordinates are whole numbers
        if key == pygame.K_UP or key == pygame.K_DOWN:
            if self.x.is_integer() == False:
                self.last_pressed_key = key
                return False
            elif key == pygame.K_UP:
                self.direction = constant.DIRECTION_UP
            else:
                self.direction = constant.DIRECTION_DOWN
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            if self.y.is_integer() == False:
                self.last_pressed_key = key
                return False
            elif key == pygame.K_LEFT:
                self.direction = constant.DIRECTION_LEFT
            else:
                self.direction = constant.DIRECTION_RIGHT
        return True

    def movement(self):
        if self.last_pressed_key != None:
            if self.change_direction(self.last_pressed_key) == True:
                self.last_pressed_key = None
        if self.direction == constant.DIRECTION_UP:
            self.y = self.y - 0.125
        elif self.direction == constant.DIRECTION_RIGHT:
            self.x = self.x + 0.125
        elif self.direction == constant.DIRECTION_DOWN:
            self.y = self.y + 0.125
        elif self.direction == constant.DIRECTION_LEFT:
            self.x = self.x - 0.125
        self.leave_trail()

    def leave_trail(self):
        if self.x.is_integer() and self.y.is_integer():
            left_trail = self.board.leave_a_trail(self.id, self.trail_color, self.x, self.y)
            if left_trail == False and self.is_out_of_zone == True:
                self.board.fill_zone(self.id, self.tile_color, 0, 49, 0, 49)
            self.is_out_of_zone = left_trail

