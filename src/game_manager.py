import pygame
from window import Window
from board import Board
from player import Player
import constant


class GameManager:
    def __init__(self, max_fps):
        pygame.init()
        self.max_fps = max_fps
        self.clock = pygame.time.Clock()
        self.window = Window(constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT)
        self.board = Board(constant.BOARD_WIDTH, constant.BOARD_HEIGHT, constant.BOARD_PLAYER_SPAWN_SIZE)
        self.players = [Player(self.board)]

    def start_game(self):
        self.game_loop()
        pygame.quit()

    def game_loop(self):
        run = True
        while run:
            self.clock.tick(self.max_fps)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.players[0].change_direction(event.key)
                if event.type == pygame.QUIT:
                    run = False
            for i in range(0, len(self.players)):
                self.players[i].movement()
            self.window.print_window(self.board, self.players)
