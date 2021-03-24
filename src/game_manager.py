import pygame
from window import Window
from board import Board
from player import Player
from heuristic_bot import HeuristicBot
import constant


class GameManager:
    def __init__(self, max_fps, no_of_heuristic_bots):
        pygame.init()
        self.max_fps = max_fps
        self.clock = pygame.time.Clock()
        self.window = Window(constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT)
        self.board = Board(self, constant.BOARD_WIDTH, constant.BOARD_HEIGHT, constant.BOARD_PLAYER_SPAWN_SIZE)
        self.players = [Player(self.board, self)]
        for i in range(0, no_of_heuristic_bots):
            self.players.append(HeuristicBot(self.board, self, constant.HEURISTIC_BOT_SAFE_OFFSET))

    def start_game(self):
        self.game_loop()
        pygame.quit()

    def game_loop(self):
        run = True
        while run:
            self.clock.tick(self.max_fps)
            pressed_key = None
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pressed_key = event.key
                if event.type == pygame.QUIT:
                    run = False
            self.players_action(pressed_key)
            self.remove_dead_players()
            self.window.print_window(self.board, self.players)
            print(len(self.players))

    def players_action(self, pressed_key):
        for i in range(0, len(self.players)):
            self.players[i].action(pressed_key)

    def remove_dead_players(self):
        self.players = list(filter(lambda x: x.is_dead is False, self.players))

    def kill_player(self, player_id):
        for player in self.players:
            if player.id == player_id:
                player.die()

    def update_players_safe_zone(self, indices):
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
