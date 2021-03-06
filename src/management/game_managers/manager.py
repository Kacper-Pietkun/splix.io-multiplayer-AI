import pygame
from src.management.game_board.board import Board
from src.constants import constant


class Manager:
    def __init__(self, max_fps, window):
        pygame.init()
        self.max_fps = max_fps
        self.clock = pygame.time.Clock()
        self.window = window
        self.board = Board(self, constant.BOARD_WIDTH, constant.BOARD_HEIGHT, constant.BOARD_PLAYER_SPAWN_SIZE)
        self.players = []

    # abstract method
    def run(self):
        pass

    def players_action(self, pressed_key):
        for i in range(0, len(self.players)):
            self.players[i].action(pressed_key)

    def remove_dead_players(self):
        self.players = list(filter(lambda x: x.is_dead is False, self.players))

    def kill_player(self, player_id):
        for player in self.players:
            if player.id == player_id:
                player.die()

    # if indices list is empty then update safe zones of each player
    def update_players_safe_zone(self, indices):
        if not indices:
            for player in self.players:
                player.update_safe_zone()
        else:
            for player in self.players:
                for index in indices:
                    if player.id == index:
                        player.update_safe_zone()

    @staticmethod
    def map_direction_to_key(direction):
        if direction == constant.DIRECTION_UP:
            return pygame.K_UP
        elif direction == constant.DIRECTION_DOWN:
            return pygame.K_DOWN
        elif direction == constant.DIRECTION_LEFT:
            return pygame.K_LEFT
        elif direction == constant.DIRECTION_RIGHT:
            return pygame.K_RIGHT
