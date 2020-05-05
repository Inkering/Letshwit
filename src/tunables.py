"""
All the model constants, parameters, and weights for tuning the fitness and crossover functions in the genetic algorithm.

@authors: Elias and Dieter
"""
import numpy as np


NUM_BLOCKS = 2  # how many blocks per hour
TIMEBLOCKS = 24 * NUM_BLOCKS  # how many blocks per day
DAYS = ["S", "U", "M", "T", "W", "R", "F"]
DAY_MAP = {d: i for i, d in enumerate(DAYS)}
DAYS_PER_WEEK = len(DAYS)


NUM_GENERATIONS = 100
POP_SIZE = 50


TOURNAMENT_SIZE = 3
TOURNAMENT_PROB = 1


CLASS_WEIGHT = 50
HWCNT_WEIGHT = 30
OVERLAP_WEIGHT = 30
OVERDUE_WEIGHT = 1
NINJA_WEIGHT = 5


MUT_DAY_PROB = 0.3
MUT_ALTER_PROB = 0.3
MUT_SWAP_PROB = 0.3


# random number generator
RNG = np.random.default_rng()
