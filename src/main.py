"""
Prototype 2:  Week scheduling range with several constraints
Authors: Dieter and Elias
"""

import numpy as np
import random
import pprint
import operator

from tunables import TIMEBLOCKS, DAYS_PER_WEEK, MUTATION_PROB, POP_SIZE, DAY_MAP
from models import TODO
from fitness import fitness
from data_importer import load_classes, load_homework,load_ninja_hrs


# random number generator
rng = np.random.default_rng()


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
        # day = random.choice(d)
        todo = TODO(start, day, hw)

        soln.append(todo)

    return soln


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

    # randomly mutate the solution with a given probability
    if random.random() < MUTATION_PROB:
        # pick two random tasks and mutate across their time ranges
        ridx = rng.choice(len(child), 2, replace=False)
        TODO.mutate_across(child[ridx[0]], child[ridx[1]])

    return child


def run_algorithm(n):
    """
    run the genetic algorithm
    n: number of iterations
    """
    # our course data
    courses = load_classes("classes.csv")

    # our homework data
    homeworks = load_homework("homework.csv")

    # our ninja hours data
    ninja_hrs = load_ninja_hrs("ninja.csv")

    # generate an initial population of todo individuals
    individual = gen_rand_solution(homeworks)

    # print([homework.due for homework in homeworks])
    # print([todo.start for todo in individual])
    

if __name__ == "__main__":
    run_algorithm(100)


# def run_algorithm(n):
#     """
#     run the algorithm with given num of iterations
#     n: number of iterations
#     """
#     classes = gen_rand_classes()

#     # how many assignments do we have to do today
#     hw_num = 4

#     # how big to have the population be
#     split = POP_SIZE // 2
#     split_dec = split - 1

#     # generate an initial population
#     hw_pop = []
#     for i in range(POP_SIZE):
#         # fill the populate at gen 0 with individuals
#         soln = gen_rand_solution(hw_num)
#         individual = {"indiv": soln, "fitness": fitness(soln, classes, hw_num)}

#         hw_pop.append(individual)

#     # sort by fitness, sorted by descending
#     hw_pop.sort(key=operator.itemgetter("fitness"), reverse=True)

#     # run the GA
#     for i in range(n):
#         # trim the list of bad solutions (last 5)
#         del hw_pop[-split:]

#         # breed new individuals!
#         for i in range(split):
#             # select fitest individuals in ordered pairs
#             choice_p1 = random.randint(0, split_dec)
#             choice_p2 = random.randint(0, split_dec)

#             while choice_p1 == choice_p2:
#                 choice_p2 = random.randint(0, split_dec)

#             p1 = hw_pop[random.randint(0, split_dec)]
#             p2 = hw_pop[random.randint(0, split_dec)]

#             child = crossover(p1, p2)

#             hw_pop.append(child)

#         hw_pop.sort(key=operator.itemgetter("fitness"), reverse=True)
#         # print(hw_pop[0]["fitness"])

#     print(hw_pop[0])
#     print("classes  ", classes)

#     # highlight conflicts in solution
#     output = hw_pop[0]["indiv"]
#     for i in range(len(output)):
#         if classes[i] == 1 and classes[i] == output[i]:
#             output[i] = 1
#         else:
#             output[i] = 0

#     print("bad      ", output)
#     # print("o hw  schedule", hw, len(hw), "hrs")
#     # print("class schedule", classes, len(classes), "hrs")
