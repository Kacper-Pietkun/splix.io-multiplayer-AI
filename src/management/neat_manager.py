import os
import neat
import pygame
import pickle
import src.gui.visualize as visualize
from math import inf
from src.constants import constant
from src.players.neat_bot import NeatBot
from src.players.heuristic_bot import HeuristicBot
from src.management.manager import Manager


class NeatManager(Manager):
    def __init__(self, max_fps, print_game, window):
        super().__init__(max_fps, window)
        self.gen = 0
        self.print_game = print_game
        self.config = None
        self.best_instance = None
        self.best_fitness = 0
        self.p = None

    def load_population(self):
        path = os.path.join(os.path.dirname(__file__), '../../resources/population.dat')
        try:
            with open(path, 'rb') as f:
                self.p = pickle.load(f)
        except IOError as e:
            raise

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

        bot_id = 1
        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, self.config)
            self.players.append(NeatBot(self.board, self, genome, net, bot_id))
            bot_id += 1

        # Add heuristic bots to the training process
        for i in range(0, constant.NUMBER_OF_HEURISTIC_BOTS_FOR_TRAINING):
            self.players.append(HeuristicBot(self.board, self, constant.HEURISTIC_BOT_SAFE_OFFSET, bot_id))
            bot_id += 1

        run = True
        while run:
            self.clock.tick(self.max_fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if self.are_there_any_neat_bots() is False:
                break
            self.players_action(None)
            self.remove_dead_players()
            if self.print_game:
                self.window.print_window(self.board, self.players)
            # print("NEAT BOTS LEFT: " + str(self.number_of_neat_bots()))

        if constant.SAVE_NEURAL_NETWORK_IMAGE_BEST_GENOME:
            self.draw_best_neural_network(genomes)

        self.kill_em_all()
        if self.gen % 10 == 0:
            local_dir = os.path.dirname(__file__)

            path = os.path.join(local_dir, '../../resources/population.dat')
            self.save_object(self.p, path)

            path = os.path.join(local_dir, '../../resources/best_genome.dat')
            self.save_object(self.get_best_genome(genomes), path)

            print("Exporting population and best genome")

    # When we use heuristic bots during the training, we need to make sure that neat bots were not eliminated
    # When neat bots are eliminated then end this generation
    def are_there_any_neat_bots(self):
        for player in self.players:
            if isinstance(player, NeatBot):
                return True
        return False

    def number_of_neat_bots(self):
        number = 0
        for player in self.players:
            if isinstance(player, NeatBot):
                number += 1
        return number

    # Used to kill all the heuristic bots at the end of the generation
    def kill_em_all(self):
        for player in self.players:
            player.die()
        self.remove_dead_players()

    def get_best_genome(self, genomes):
        best_genome = None
        best_fitness = -inf
        for genome_id, genome in genomes:
            if genome.fitness > best_fitness:
                best_fitness = genome.fitness
                best_genome = genome
        return best_genome

    def draw_best_neural_network(self, genomes):
        visualize.draw_net(self.config, self.get_best_genome(genomes))
