import pygame
from src.players.human_player import HumanPlayer
from src.players.heuristic_bot import HeuristicBot
from src.constants import constant
from src.management.manager import Manager


class GameManager(Manager):
    def __init__(self, max_fps, no_of_heuristic_bots):
        super().__init__(max_fps)
        self.players.append(HumanPlayer(self.board, self))
        for i in range(0, no_of_heuristic_bots):
            self.players.append(HeuristicBot(self.board, self, constant.HEURISTIC_BOT_SAFE_OFFSET))

    def run(self):
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
