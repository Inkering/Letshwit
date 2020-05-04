"""
A helper file containing all the functions related to fitness calculation.

@authors: Elias and Dieter
"""
from generics import Schedule, Schedulable
from tunables import (
    OVERLAP_WEIGHT,
    NINJA_WEIGHT,
    CLASS_WEIGHT,
    OVERDUE_WEIGHT,
    TIMEBLOCKS,
    HWCNT_WEIGHT,
)


def overlap_fitness_comp(soln, sched):
    """
    Calculates the numerical component of the fitness function related to assigned time overlap.
    Solutions that contain TODOs scheduled with overlapping times are punished.
    """
    delta = 0

    # look at each possible pairing of times
    for i in soln:
        for j in soln:
            if i is not j:
                delta -= OVERLAP_WEIGHT * Schedulable.calculate_overlap(i, j)

    return delta


def ninja_fitness_comp(soln, sched):
    """
    Calculates the numerical componet of the fitness function based on whether or not TODOs in
    the solution overlap with NINJA hours for its specific class.
    """
    delta = 0

    # check if any todos overlap with NINJA hours
    for i in soln:
        for j in sched.ninja_hours:
            # if the NINJA is right for the class
            if j.cname == i.hw.cname:
                delta += NINJA_WEIGHT * Schedulable.calculate_overlap(i, j)

    return delta


def class_overlap_fitness_comp(soln, sched):
    """
    Finds the the duration of time any of the solutions are overlapping with
    any of the classes and returns the negative sum.
    """
    delta = 0

    for i in soln:
        for c in sched.classes:
            delta -= CLASS_WEIGHT * Schedulable.calculate_overlap(i, c)

    return delta


def overdue_fitness_comp(soln, sched):
    """
    Returns the negative number of timeblocks every assignment would be if overdue.
    """
    delta = 0

    for s in soln:
        if s.day >= s.hw.due:
            delta -= OVERDUE_WEIGHT * TIMEBLOCKS * (s.day - s.hw.due + 1)

    return delta


def hwcnt_fitness_comp(soln, sched):
    """
    Returns the difference between the number of homeworks that are expected
    and the number of unique homeworks that are actually scheduled to be completed.
    """
    # get the difference in the number of homeworks we're supposed to have and the
    # number of UNIQUE homeworks we actually schedule time for, and negatively weight
    # the outcome
    return -HWCNT_WEIGHT * (len(sched.hws) - len({c.hw.cname for c in soln}))


def fitness(soln, sched):
    """
    Evaluates the fitness of the given solution in the overall fitness landscape.
    A solution's fitness is calculated based on the sum of all the fitness functions
    defined in this file.
    """
    return (
        overlap_fitness_comp(soln, sched)
        + ninja_fitness_comp(soln, sched)
        + class_overlap_fitness_comp(soln, sched)
        + overdue_fitness_comp(soln, sched)
        + hwcnt_fitness_comp(soln, sched)
    )
