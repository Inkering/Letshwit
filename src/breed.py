"""
Defines the algorithms for selecting, breeding, and mutating individual solutions.

@authors: Elias and Dieter
"""
import numpy as np
import random
from tunables import (
    TIMEBLOCKS,
    RNG,
    TOURNAMENT_PROB,
    MUT_DAY_PROB,
    MUT_ALTER_PROB,
    MUT_SWAP_PROB,
    K_SIZE,
)


def mutate_across(t1, t2):
    """
    Mutates several properties across the two given TODOs with tunable probabilities.
    """
    # swap days
    if random.random() < MUT_DAY_PROB:
        t1.day, t2.day = t2.day, t1.day

    # change t1 timerange
    if random.random() < MUT_ALTER_PROB:
        t1.start = np.random.randint(TIMEBLOCKS - t1.hw.duration)
        t1.end = t1.start + t1.hw.duration

    # change t2 timerange
    if random.random() < MUT_ALTER_PROB:
        t2.start = np.random.randint(TIMEBLOCKS - t2.hw.duration)
        t2.end = t2.start + t2.hw.duration

    # swap t1 and t2 timeranges
    if random.random() < MUT_SWAP_PROB:
        # we have to swap timeranges based on endtimes. if we swapped
        # based on start we might go beyond TIMEBLOCKS if the durations
        # are different
        t1.end, t2.end = t2.end, t1.end
        t1.start = t1.end - t1.hw.duration
        t2.start = t2.end - t2.hw.duration


def crossover(p1, p2):
    """
    Breed two parent solutions together via single-point crossover,
    randomly returning one of the two offspring.
    """
    # single point crossover
    # we only want one child, so we can either generate
    # both and select one or randomly swap the parents
    # so we don't know if we're choosing the first
    # or second child
    if random.random() < 0.5:
        p1, p2 = p2, p1

    idx = np.random.randint(len(p1))
    child = p1[:idx] + p2[idx:]
    t1 = t2 = None

    # select two tasks to mutate across. we have to ensure that we pick two
    # TODOs that reference different assignments since the assignment object
    # is shared in memory. if we didn't check, funky stuff might happen
    while t1 is t2:
        # pick two random distinct tasks
        ridx = RNG.choice(len(child), 2, replace=False)
        t1 = child[ridx[0]]
        t2 = child[ridx[1]]

    # mutate across the two tasks
    mutate_across(t1, t2)

    return child


def tournament(population):
    """
    Runs a probabilistic tournament selection with the given population and returns
    two parents for crossbreeding. The probability that an individual is selected
    decreases with its fitness value based on the following geometric series:
    
        I(s) = ranking when sorted by fitness from high to low
        P(s) = p(1 - p)^I(s)
    
    By default, p=1. Individuals cannot breed with themselves, buy may breed more
    than once.
    """
    parents = []

    while len(parents) < 2:
        # pull a random sample of size K and sort by fitness in DESC order
        participants = random.sample(population, K_SIZE)
        participants.sort(key=lambda i: i.fitness, reverse=True)

        # cycle through the participants and select them with decreasing likelihood
        # note that this doesn't guarantee that an individual will be chosen when p < 1
        for i, indiv in enumerate(participants):
            if random.random() < TOURNAMENT_PROB * ((1 - TOURNAMENT_PROB) ** i):
                parents.append(indiv)
                break

    return parents
