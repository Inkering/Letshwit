"""
Prototype 3:  Week scheduling range with multiple flexible constraints
Authors: Dieter and Elias
"""

import numpy as np
import random
from tunables import (
    TIMEBLOCKS,
    NUM_BLOCKS,
    DAYS_PER_WEEK,
    POP_SIZE,
    DAY_MAP,
    K_SIZE,
)
from models import TODO, Individual
from fitness import fitness
from generics import Schedule
from data_importer import load_classes, load_homework, load_ninja_hrs
from breed import tournament, crossover


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


def run_algorithm(n):
    """
    run the genetic algorithm
    n: number of iterations
    """

    print("\n====")
    print("==== IMPORTED DATA ====")
    print("====\n")

    # load the courses, homework assignments, and ninja hours
    courses = load_classes("classes.csv")
    homeworks = load_homework("homework.csv")
    ninja_hrs = load_ninja_hrs("ninja.csv")

    # store the imported data into a dummy object
    sched = Schedule(courses, ninja_hrs, homeworks)

    print("\n====")
    print("==== EVOLUTION ====")
    print("====\n")

    # generate an initial population of individuals
    population = []
    for i in range(POP_SIZE):
        soln = gen_rand_solution(homeworks)
        population.append(Individual(soln, fitness(soln, sched)))

    print("Ancestors:", [indiv.fitness for indiv in population])

    # evolve over n generations!
    for i in range(n):
        new_gen = []

        for i in range(POP_SIZE):
            parents = tournament(population)
            child_soln = crossover(parents[0].soln, parents[1].soln)
            child = Individual(child_soln, fitness(child_soln, sched))

            new_gen.append(child)

        population = new_gen

    population.sort(key=lambda indiv: indiv.fitness, reverse=True)
    best = population[0]

    print(
        "Best <",
        best.fitness,
        ">:",
        [
            (i.hw.cname, i.day, i.start // NUM_BLOCKS, i.end // NUM_BLOCKS)
            for i in best.soln
        ],
    )


if __name__ == "__main__":
    run_algorithm(10)


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
