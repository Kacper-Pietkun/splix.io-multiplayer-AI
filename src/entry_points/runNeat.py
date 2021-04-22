import os
import sys
from src.management.neat_manager import NeatManager
from src.constants import constant
import pickle

import_population = constant.LOAD_POPULATION
# Make it True to import trained population
# Needs "../trained/population.dat" as a program parameter


def load_object(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


if __name__ == '__main__':
    pop = None
    if len(sys.argv) > 1 and import_population:
        local_dir = os.path.dirname(__file__)
        path = os.path.join(local_dir, sys.argv[1])
        pop = load_object(path)
        print("Reading population from: " + sys.argv[1])

    neat_manager = NeatManager(pop, constant.TRAINING_MAX_FPS, constant.VISUALIZE_TRAINING)
    neat_manager.run()
