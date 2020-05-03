"""
Prototype 2:  Week scheduling range with several constraints
Authors: Dieter and Elias
"""

import numpy as np
import random
import pprint
import operator
from classes import Course, NINJA, Assignment, TODO
from classes import TIMEBLOCKS, DAYS_PER_WEEK, NUM_BLOCKS

# random number generator
rng = np.random.default_rng()

# tunable paramaters
CLASS_WEIGHT = 1
HWCNT_WEIGHT = 1
MUTATION_PROB = 0.3


def gen_rand_solution(hws):
    """
    Generate a random solution for the scheduling problem, which is just
    a list of n TODOs. The number of TODOs is always equal to the number
    of homework assignments.
    """
    soln = []

    # generate a random todo for each homework in the list
    for hw in hws:
        # the random todo occurs on a random day at a
        # random time, but the duration remains the same
        start = np.random.randint(TIMEBLOCKS - hw.duration)
        day = np.random.randint(DAYS_PER_WEEK)
        todo = TODO(start, day, hw)

        soln.append(todo)

    return soln


def fitness(soln):
    """ Evaluates the fitness of the given solution in the overall fitness
    landscape. A solution's fitness is calculated based on:
        - how many classes overlap with any of the TODOs
        - whether or not any of the TODOs come after the assigned due date,
        - whether or not any of the TODOs overlap
        - if any of the homework assignments are missing (multiple TODOs for an assignment)
        - if a TODO overlaps with NINJA hours
    """
    res = 0
    cnt = sum(soln) # the number of hw periods is the sum

    for i in range(len(soln)):
        # award non-collision between constraint set
        # and solution set
        if classes[i] == 1 and soln[i] == 0:
            res += CLASS_WEIGHT
        else:
            res -= CLASS_WEIGHT

    # score decreases more if further from num of hws
    # in either polarity. penalize if we don't do
    # enough work or if we're doing too much (mental
    # health is important)
    res -= HWCNT_WEIGHT*abs(n-cnt)

    # during work hours is better (9-5)
    res += sum(soln[8*NUM_BLOCKS:16*NUM_BLOCKS])

    return res


def crossover(p1, p2):
    """ Breed two parent solutions together via single-point crossover,
    randomly returning one of the two offspring. """
    # single point crossover
    # we only want one child, so we can either generate
    # both and select one or randomly swap the parents
    # so we don't know if we're choosing the first
    # or second child
    if random.random() < 0.5:
        p1, p2 = p2, p1

    idx = np.random.randint(len(p1))
    child = p1[:idx] + p2[idx:]

    # randomly mutate the solution with a given probability
    if random.random() < MUTATION_PROB:
        # pick two random tasks and mutate across their time ranges
        ridx = rng.choice(len(child), 2, replace=False)
        TODO.mutate_across(child[ridx[0]], child[ridx[1]])

    return child


def run_algorithm(n):
    """
    run the algorithm with given num of iterations
    n: number of iterations
    """
    classes = gen_rand_classes()

    # how many assignments do we have to do today
    hw_num = 4

    #how big to have the population be
    pop_size = 10

    split = pop_size // 2
    split_dec = split - 1
    # generate an initial population
    hw_pop = []
    for i in range(pop_size):
        # fill the populate at gen 0 with individuals
        soln = gen_rand_solution(hw_num)
        individual = {"indiv" : soln,
                      "fitness": fitness(soln, classes, hw_num)}

        hw_pop.append(individual)

    # sort by fitness, sorted by descending
    hw_pop.sort(key=operator.itemgetter('fitness'), reverse=True)

    # within iteration number
    for i in range(n):
        # trim the list of bad solutions (last 5)
        del hw_pop[-split:]

        # breed new individuals!
        for i in range(split):
            # select fitest individuals in ordered pairs
            choice_p1 = random.randint(0,split_dec)
            choice_p2 = random.randint(0,split_dec)

            while choice_p1 == choice_p2:
                choice_p2 = random.randint(0,split_dec)

            p1 = hw_pop[random.randint(0,split_dec)]
            p2 = hw_pop[random.randint(0,split_dec)]

            child = crossover(p1, p2)

            hw_pop.append(child)

        hw_pop.sort(key=operator.itemgetter('fitness'), reverse=True)
        # print(hw_pop[0]["fitness"])

    print(hw_pop[0])
    print("classes  ",classes)

    # highlight conflicts in solution
    output = hw_pop[0]["indiv"]
    for i in range(len(output)):
        if classes[i] == 1 and classes[i] == output[i]:
            output[i] = 1
        else:
            output[i] = 0

    print("bad      ",output)
    # print("o hw  schedule", hw, len(hw), "hrs")
    # print("class schedule", classes, len(classes), "hrs")

if __name__ == "__main__":
    run_algorithm(100)
