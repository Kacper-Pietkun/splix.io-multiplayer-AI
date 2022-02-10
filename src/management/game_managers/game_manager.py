import os
import sys
import neat
import pygame
import pickle
from src.players.human_player import HumanPlayer
from src.players.heuristic_bot import HeuristicBot
from src.players.neat_bot import NeatBot
from src.constants import constant
from src.management.game_managers.manager import Manager
from random import randint
from src.gui.gui_view.pop_up_view import PopUpView


# For single player games
class GameManager(Manager):
    def __init__(self, bots_mode, max_fps, no_of_all_bots, window, my_view, player_name):
        super().__init__(max_fps, window)
        player_id = 1
        self.players.append(HumanPlayer(self.board, self, player_id, player_name))
        self.human_score = 0
        self.my_view = my_view
        player_id += 1

        heuristic_bots_number = 0
        neat_bots_number = 0
        if bots_mode == constant.MODE_BOTH_BOTS_ONLY:
            heuristic_bots_number = int(no_of_all_bots / 2)
            neat_bots_number = int(no_of_all_bots / 2)
        elif bots_mode == constant.MODE_HEURISTIC_BOTS_ONLY:
            heuristic_bots_number = no_of_all_bots
        else:
            neat_bots_number = no_of_all_bots

        if bots_mode == constant.MODE_HEURISTIC_BOTS_ONLY or bots_mode == constant.MODE_BOTH_BOTS_ONLY:
            for i in range(0, heuristic_bots_number):
                self.players.append(HeuristicBot(self.board, self, constant.HEURISTIC_BOT_SAFE_OFFSET, player_id,
                                                 constant.HEURISTIC_BOT_PREFIX_NAME + str(player_id)))
                player_id += 1
                if bots_mode == constant.MODE_BOTH_BOTS_ONLY and constant.DISTINGUISH_HEURISTIC_AND_NEAT_BOTS:
                    white_shade = randint(200, 230)
                    self.players[-1].change_color_set_on_fly(player_color=(white_shade - 25, white_shade - 25,
                                                                           white_shade - 25),
                                                             tile_color=(white_shade, white_shade, white_shade),
                                                             trail_color=(white_shade + 25, white_shade + 25,
                                                                          white_shade + 25))

        if bots_mode == constant.MODE_NEAT_BOTS_ONLY or bots_mode == constant.MODE_BOTH_BOTS_ONLY:
            try:
                config = self.load_config()
                best_genome = self.load_best_genome()
                best_genome.fitness = 0
            except IOError as e:
                raise
            for i in range(0, neat_bots_number):
                net = neat.nn.FeedForwardNetwork.create(best_genome, config)
                self.players.append(NeatBot(self.board, self, best_genome, net, player_id,
                                            constant.NEAT_BOT_PREFIX_NAME + str(player_id)))
                player_id += 1

    def run(self):
        self.game_loop()

    def game_loop(self):
        run = True
        while run:
            self.clock.tick(self.max_fps)
            pressed_key = None
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pressed_key = event.key
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.players_action(pressed_key)
            self.remove_dead_players()
            self.window.print_window(self.board, self.players)
            self.update_human_score()
            if self.check_if_human_died():
                run = False
                pop_up_view = PopUpView(self.my_view, 'You lost', 'Your score: ' + str(self.human_score), 'ok', None)
                pop_up_view.display_menu()

    def update_human_score(self):
        for player in self.players:
            if player.id == 1:
                self.human_score = len(player.safe_zone_positions)
        return True

    def check_if_human_died(self):
        for player in self.players:
            if player.id == 1:
                return False
        return True

    def load_config(self):
        config_file = os.path.join(constant.ROOT_DIR, constant.PATH_NEAT_CONF)
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)
        return config

    def load_best_genome(self):
        path = os.path.join(constant.ROOT_DIR, constant.PATH_BEST_GENOME)
        try:
            with open(path, 'rb') as f:
                genome = pickle.load(f)
        except IOError as e:
            raise
        return genome

