"""
Prototype 1: One day scheduling range with one constraint: class times
Authors: Dieter and Elias
"""

import numpy as np
import random
import pprint
import operator

# for assorted terminal print outs,
# makess dictionaries print nicer
pp = pprint.PrettyPrinter(indent=4)

def gen_classes():
    """
    randomly generate a set of classes with times
    """
    classes = []
    for i in range(24):
        p = random.random()
        if p > 0.3:
            classes.append(0)
        else:
            classes.append(1)
    return classes


def generate_rand_soln(hw_num):
    """
    randomly generate an individual set of hw schedulings
    """
    # possible set of times to do hw in 24 1hr blocks
    given_solution = []
    cnt = 0
    for i in range(24):
        p = random.random()
        if p > 0.6 and cnt != hw_num:
            given_solution.append(1)
            cnt += 1
        else:
            given_solution.append(0)
    return given_solution


def fitness(soln, classes, n):
    """
    Evaluate the fitness of a solution
    soln: an solution set of size 24
    classes: when classes are
    n: number of homeworks
    """
    res = 0
    cnt = 0

    class_weight = 1
    cnt_weight = 1

    for i in range(len(soln)):
        # award non-collision between constraint set
        # and solution set
        if classes[i] == 1 and classes[i] != soln[i]:
            res += class_weight
        else:
            res -= 1
        if soln[i] == 1:
            cnt += 1

    # score decreases more if further from num of hws
    # in either polarity
    if cnt < n:
        res -= cnt_weight*(n - cnt)
    elif cnt >= n:
        res -= cnt_weight*(cnt - n)

    # during work hours is better (9-5)
    res += sum(soln[8:16])

    return res


def crossover(p1, p2, classes, hw_num):
    """
    breed two individuals together
    p1: individual 1
    p2: individual 2
    classes: set of classes for fitness function
    hw_num: num of classes for fitness function
    return: dictionary with valid individual structure
    """
    p1_cross = p1["indiv"][:12]
    p2_cross = p2["indiv"][12:]
    child_soln = p2_cross + p1_cross
    # print("p1", p1_cross,"p2",p2_cross, "child", child_soln)


    # chance of mutation (swapping)
    m_p = random.random()
    if m_p > 0.3:
        # random swap
        idx1 = random.randint(0,23)
        idx2 = random.randint(0,23)

        child_soln[idx1], child_soln[idx2] = child_soln[idx2], child_soln[idx1]

    child = {"indiv" : child_soln,
             "fitness" : fitness(child_soln, classes, hw_num)}
    return child


def run_algorithm(n):
    """
    run the algorithm with given num of iterations
    n: number of iterations
    """
    classes = gen_classes()

    # how many assignments do we  have to do today
    hw_num = 4

    #how big to have the population be
    pop_size = 100

    split = pop_size // 2
    split_dec = split - 1
    # generate an initial population
    hw_pop = []
    for i in range(pop_size):
        # fill the populate at gen 0 with individuals
        soln = generate_rand_soln(hw_num)
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

            child = crossover(p1, p2, classes, hw_num)

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


