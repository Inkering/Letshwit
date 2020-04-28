"""
Prototype 1: One day scheduling range with one constraint: class times
Authors: Dieter and Elias
"""

import numpy as np
import random
import pprint
import operator
pp = pprint.PrettyPrinter(indent=4)

# time blocks where there are classes
def gen_classes():
    classes = []
    for i in range(24):
        p = random.random()
        if p > 0.3:
            classes.append(0)
        else:
            classes.append(1)
    return classes

def generate_rand_soln():
    # possible set of times to do hw in 24 1hr blocks
    given_solution = []
    for i in range(24):
        p = random.random()
        if p > 0.3:
            given_solution.append(0)
        else:
            given_solution.append(1)
    return given_solution


def fitness(soln, classes, n):
    """
    Evaluate the fitness of a solution
    """
    res = 0
    cnt = 0

    class_weight = 1
    cnt_weight = 1

    for i in range(len(soln)):
        # award non-collision between constraint set
        # and solution set
        if classes[i] != soln[i]:
            res += class_weight
        i
        if soln[i] == 1:
            cnt += 1

    # score decreases more if further from num of hws
    # in either polarity
    if cnt < n:
        res -= cnt_weight*(n - cnt)
    elif cnt >= n:
        res -= cnt_weight*(cnt - n)

    return res


def run_algorithm(n):
    classes = gen_classes()

    # how many assignments do we  have to do today
    hw_num = 4

    # generate an initial population
    hw_pop = []
    for i in range(hw_num):
        # fill the populate at gen 0 with individuals
        soln = generate_rand_soln()
        individual = {"indiv" : soln,
                      "fitness": fitness(soln, classes, hw_num)}

        hw_pop.append(individual)

    # sort by fitness, sorted by descending
    hw_pop.sort(key=operator.itemgetter('fitness'), reverse=True)

    pp.pprint(hw_pop)
    # print("o hw  schedule", hw, len(hw), "hrs")
    # print("class schedule", classes, len(classes), "hrs")

if __name__ == "__main__":
    run_algorithm(40)


