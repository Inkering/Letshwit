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
    run_algorithm(100)