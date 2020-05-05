"""
All the model constants, parameters, and weights for tuning the fitness and crossover functions in the genetic algorithm.

@authors: Elias and Dieter
"""
import numpy as np


## schedule properties
NUM_BLOCKS = 2  # how many blocks per hour
TIMEBLOCKS = 24 * NUM_BLOCKS  # how many blocks per day
DAYS_PER_WEEK = 7

# mapping of day abbreviation to index (dict for constant-time access)
DAY_MAP = {"S": 0, "U": 1, "M": 2, "T": 3, "W": 4, "R": 5, "F": 6}
INV_DAY_MAP = {v: k for k, v in DAY_MAP.items()}

# population details
NUM_GENERATIONS = 100
POP_SIZE = 12
K_SIZE = 6


## fitness weights
CLASS_WEIGHT = 50
HWCNT_WEIGHT = 30
OVERLAP_WEIGHT = 30
OVERDUE_WEIGHT = 1
NINJA_WEIGHT = 5


## propbabilities
MUT_DAY_PROB = 0.3
MUT_ALTER_PROB = 0.3
MUT_SWAP_PROB = 0.3

# random number generator
RNG = np.random.default_rng()

# when this is 1, the fittest individual in the tournament always wins
TOURNAMENT_PROB = 1
