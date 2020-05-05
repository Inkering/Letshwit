"""
Prototype 3:  Week scheduling range with multiple flexible constraints

@authors: Dieter and Elias
"""

import numpy as np
from tunables import TIMEBLOCKS, DAYS_PER_WEEK, POP_SIZE, NUM_GENERATIONS
from models import TODO, Individual
from fitness import fitness
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


def run_algorithm(sched, n=NUM_GENERATIONS, m=POP_SIZE):
    """
    Runs the genetic algorithm over n generations with a population of size m
    using the provided schedule constraint and returns the found solution.
    """

    # generate an initial population of individuals
    population = []
    for i in range(m):
        soln = gen_rand_solution(sched.hws)
        population.append(Individual(soln, fitness(soln, sched)))

    # evolve over n generations!
    for i in range(n):
        new_gen = []

        for i in range(m):
            # select 2 parents via tournament selection and breed them to
            # create a child for the new generation
            parents = tournament(population)
            child_soln = crossover(parents[0].soln, parents[1].soln)
            child = Individual(child_soln, fitness(child_soln, sched))

            new_gen.append(child)

        population = new_gen

    # sort the final population by fitness and return the best one
    population.sort(key=lambda indiv: indiv.fitness, reverse=True)
    return population[0]
