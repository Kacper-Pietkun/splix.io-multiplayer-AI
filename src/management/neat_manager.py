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
from random import randint


class NeatManager(Manager):
    def __init__(self, max_fps, visualize_training, window):
        super().__init__(max_fps, window)
        self.generation = 0
        self.visualize_training = visualize_training
        self.config = None
        self.best_instance = None
        self.best_fitness = 0
        self.population = None
        self.statistics = None

    def load_population(self):
        path = os.path.join(os.path.dirname(__file__), '../../resources/population.dat')
        try:
            with open(path, 'rb') as f:
                self.population = pickle.load(f)
        except IOError as e:
            raise

    def run(self):
        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, '../../resources/neat.conf')

        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                         config_file)

        # if user didn't want to load existing population then create a new one
        if self.population is None:
            # Create the population, which is the top-level object for a NEAT run.
            self.population = neat.Population(self.config)
            # Add a stdout reporter to show progress in the terminal.
            self.population.add_reporter(neat.StdOutReporter(True))
            self.statistics = neat.StatisticsReporter()
            self.population.add_reporter(self.statistics)

        winner = self.population.run(self.eval_genomes, 1000000)
        self.save_files(None)

        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))

    def save_object(self, obj, filename):
        with open(filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    def eval_genomes(self, genomes, _):
        self.generation += 1

        bot_id = [1]
        self.spawn_neat_bots(genomes, bot_id)
        self.spawn_heuristic_bots(bot_id)

        self.train_one_generation()

        # clear map from all heuristic bots that are left
        self.kill_em_all()
        self.save_files(genomes)

    def train_one_generation(self):
        run = True
        iteration = 0
        while run:
            if iteration > 100000:
                break
            self.clock.tick(self.max_fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.are_there_any_neat_bots() is False:
                break
            self.players_action(None)
            self.remove_dead_players()
            if self.visualize_training:
                self.window.print_window(self.board, self.players)
            # print("NEAT BOTS LEFT: " + str(self.number_of_neat_bots()))
            iteration += 1
        print(iteration)

    def spawn_neat_bots(self, genomes, bot_id):
        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, self.config)
            self.players.append(NeatBot(self.board, self, genome, net, bot_id[0]))
            bot_id[0] += 1

    # Add heuristic bots to the training process (only if it was specified in constant.py)
    def spawn_heuristic_bots(self, bot_id):
        for i in range(0, constant.NUMBER_OF_HEURISTIC_BOTS_FOR_TRAINING):
            self.players.append(HeuristicBot(self.board, self, constant.HEURISTIC_BOT_SAFE_OFFSET, bot_id[0]))
            # change color of heuristic bots to distinguish them from neat bots
            white_shade = randint(200, 230)
            self.players[-1].change_color_set(player_color=(white_shade - 25, white_shade - 25, white_shade - 25),
                                              tile_color=(white_shade, white_shade, white_shade),
                                              trail_color=(white_shade + 25, white_shade + 25, white_shade + 25))
            bot_id[0] += 1

    def save_files(self, genomes):
        if self.generation % constant.SAVE_GENERATION_RATE == 0 and genomes is not None:
            self.save_current_progress(genomes)

        if self.generation % constant.SAVE_GENERATION_RATE == 0 and \
                constant.SAVE_NEURAL_NETWORK_IMAGE_BEST_GENOME and genomes is not None:
            self.save_best_neural_network_image(genomes)

        if self.generation % constant.SAVE_GENERATION_RATE == 0 and \
                constant.SAVE_STATISTICS:
            self.save_statistics()

    def save_current_progress(self, genomes):
        local_dir = os.path.dirname(__file__)

        path = os.path.join(local_dir, '../../resources/population.dat')
        self.save_object(self.population, path)

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

    def save_best_neural_network_image(self, genomes):
        path = os.path.join(os.path.dirname(__file__), '../../resources/net')
        visualize.draw_net(self.config, self.get_best_genome(genomes), filename=path)

    def save_statistics(self):
        path = os.path.join(os.path.dirname(__file__), '../../resources/avg_fitness.svg')
        visualize.plot_stats(statistics=self.statistics, filename=path)
