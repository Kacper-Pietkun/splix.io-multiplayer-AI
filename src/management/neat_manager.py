import os
import neat
import pygame
from src.gui.window import Window
from src.board import Board
from src.constants import constant
from src.players.neat_bot import NeatBot
from src.management.manager import Manager
import pickle


class NeatManager(Manager):
    def __init__(self, pop, max_fps, print_game):
        super().__init__(max_fps)
        self.gen = 0
        self.print_game = print_game
        self.config = None
        self.best_instance = None
        self.best_fitness = 0
        self.p = pop

    def run(self):
        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, '../../resources/neat.conf')

        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                         config_file)
        if self.p is None:
            # Create the population, which is the top-level object for a NEAT run.
            self.p = neat.Population(self.config)
            # Add a stdout reporter to show progress in the terminal.
            self.p.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            self.p.add_reporter(stats)
            # self.p.add_reporter(neat.Checkpointer(5))
        winner = self.p.run(self.eval_genomes, 10000)
        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))

    def save_object(self, obj, filename):
        with open(filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    def save_best_generation_instance(self, filename='../../resources/best_generation_instances.pickle'):
        instances = []
        if os.path.isfile(filename):
            instances = self.load_object(filename)
        instances.append(self.best_instance)
        self.save_object(instances, filename)

    def eval_genomes(self, genomes, _):
        self.gen += 1
        nets = []

        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, self.config)
            self.players.append(NeatBot(self.board, self, genome, net))  # tutaj poprawić, ale tworzymy neat bota

        run = True
        while run:
            self.clock.tick(self.max_fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.players_action(None)
            self.remove_dead_players()
            if self.print_game:
                self.window.print_window(self.board, self.players)
            if len(self.players) == 0:
                break

        if self.gen % 10 == 0:
            local_dir = os.path.dirname(__file__)
            path = os.path.join(local_dir, '../../resources/population.dat')
            self.save_object(self.p, path)
            print("Exporting population")
