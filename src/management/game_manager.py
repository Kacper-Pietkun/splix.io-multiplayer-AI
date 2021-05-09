import os

import neat
import pygame
import pickle
from src.players.human_player import HumanPlayer
from src.players.heuristic_bot import HeuristicBot
from src.players.neat_bot import NeatBot
from src.constants import constant
from src.management.manager import Manager


class GameManager(Manager):
    def __init__(self, bots_mode, max_fps, no_of_all_bots, window):
        super().__init__(max_fps, window)
        player_id = 1
        self.players.append(HumanPlayer(self.board, self, player_id))
        player_id += 1

        if bots_mode == constant.MODE_HEURISTIC_BOTS_ONLY or bots_mode == constant.MODE_BOTH_BOTS_ONLY:
            for i in range(0, int(no_of_all_bots / 2)):
                self.players.append(HeuristicBot(self.board, self, constant.HEURISTIC_BOT_SAFE_OFFSET, player_id))
                player_id += 1

        if bots_mode == constant.MODE_NEAT_BOTS_ONLY or bots_mode == constant.MODE_BOTH_BOTS_ONLY:
            try:
                config = self.load_config()
                best_genome = self.load_best_genome()
                best_genome.fitness = 0
            except IOError as e:
                raise
            for i in range(0, int(no_of_all_bots / 2)):
                net = neat.nn.FeedForwardNetwork.create(best_genome, config)
                self.players.append(NeatBot(self.board, self, best_genome, net, player_id))
                player_id += 1

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

    def load_config(self):
        config_file = os.path.join(os.path.dirname(__file__), '../../resources/neat.conf')
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)
        return config

    def load_best_genome(self):
        path = os.path.join(os.path.dirname(__file__), '../../resources/best_genome.dat')
        try:
            with open(path, 'rb') as f:
                genome = pickle.load(f)
        except IOError as e:
            raise
        return genome

