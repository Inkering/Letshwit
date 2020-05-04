"""
Prototype 3:  Week scheduling range with multiple flexible constraints
Authors: Dieter and Elias
"""

import numpy as np
import pandas as pd
import random
from tabulate import tabulate
from tunables import (
    TIMEBLOCKS,
    NUM_BLOCKS,
    DAYS_PER_WEEK,
    POP_SIZE,
    DAY_MAP,
    K_SIZE,
    INV_DAY_MAP,
)
from models import TODO, Individual
from fitness import *
from generics import Schedule
from data_importer import load_classes, load_homework, load_ninja_hrs, tprint
from breed import tournament, crossover


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


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


def print_soln(best, craw, hraw, nraw):
    """ pretty print the solution """
    calendar = pd.DataFrame(index=range(TIMEBLOCKS), columns=range(7))
    calendar.columns = pd.Series(["S", "U", "M", "T", "W", "R", "F"])

    count_overlap = 0
    count_due = 0

    # fill in classes
    for course in craw.iterrows():
        name = course[1][0]
        start = course[1][1]
        end = course[1][2]
        # select date range
        for idx, val in course[1].iloc[3:].items():
            if val == 1:
                calendar[str(idx)].iloc[start:end] = bcolors.OKGREEN + name + bcolors.ENDC

    # fill in ninja hours
    for ninja in nraw.iterrows():
        name = ninja[1][0]
        start = ninja[1][1]
        end = ninja[1][2]
        # select date range
        for idx, val in ninja[1].iloc[3:-1].items():
            if val == 1:
                calendar[str(idx)].iloc[start:end] = (
                    bcolors.OKBLUE + name + bcolors.ENDC
                )

    # fill in homework
    for i in best.soln:
        start = i.start
        end = i.end
        name = i.hw.desc
        day = INV_DAY_MAP[i.day]
        # TODO: add seperate color for NINJA hours
        if calendar[day].iloc[start:end].count() > 0:
            count_overlap += 1
            color = bcolors.FAIL
        else:
            color = bcolors.HEADER

        if i.day >= i.hw.due:
            count_due += 1
            color = bcolors.UNDERLINE

        calendar[str(day)].iloc[start:end] = color + name + bcolors.ENDC

    calendar.fillna(" ", inplace=True)

    print(
        "Key: ",
        bcolors.OKGREEN + "course" + bcolors.ENDC,
        bcolors.OKBLUE + "ninja hours" + bcolors.ENDC,
        bcolors.FAIL + "conflict" + bcolors.ENDC,
        bcolors.UNDERLINE + "due date wrong" + bcolors.ENDC,
        bcolors.HEADER + "homework correct" + bcolors.ENDC,
        "\n",
    )
    tprint("Calendar", calendar)
    print(
        "course overlap conflicts:",
        count_overlap,
        "after due date conflict:",
        count_due,
    )


def run_algorithm(n):
    """
    run the genetic algorithm
    n: number of iterations
    """

    print("\n====")
    print("==== IMPORTED DATA ====")
    print("====\n")

    # load the courses, homework assignments, and ninja hours
    courses, craw = load_classes("classes.csv")
    homeworks, hraw = load_homework("homework.csv")
    ninja_hrs, nraw = load_ninja_hrs("ninja.csv")

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
    print([f.fitness for f in population])

    print_soln(best, craw, hraw, nraw)
    # print("solution:", [(i.start, i.end) for i in best.soln])
    # print("fitness:", best.fitness)
    # print("  - overlap:", overlap_fitness_comp(best.soln, sched))
    # print("  - ninja:", ninja_fitness_comp(best.soln, sched))
    # print("  - class:", class_overlap_fitness_comp(best.soln, sched))
    # print("  - overdue:", overdue_fitness_comp(best.soln, sched))
    # print("  - hwcnt:", hwcnt_fitness_comp(best.soln, sched))


if __name__ == "__main__":
    run_algorithm(100)
