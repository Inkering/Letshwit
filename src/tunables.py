"""
All the model constants, parameters, and weights for tuning the fitness and crossover functions in the genetic algorithm.

@authors: Elias and Dieter
"""
## schedule properties
NUM_BLOCKS = 2  # how many blocks per hour
TIMEBLOCKS = 24 * NUM_BLOCKS  # how many blocks per day
DAYS_PER_WEEK = 7

# mapping of day abbreviation to index (dict for constant-time access)
DAY_MAP = {"S": 0, "U": 1, "M": 2, "T": 3, "W": 4, "R": 5, "F": 6}

# population details
POP_SIZE = 10

## fitness weights
CLASS_WEIGHT = 1
HWCNT_WEIGHT = 1
OVERLAP_WEIGHT = 1
OVERDUE_WEIGHT = 1
NINJA_WEIGHT = 1


## propbabilities
MUTATION_PROB = 0.3
