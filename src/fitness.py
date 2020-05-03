"""
A helper file containing all the functions related to fitness calculation.

@authors: Elias and Dieter
"""
from generics import Schedule, Schedulable
from tunables import OVERLAP_WEIGHT, NINJA_WEIGHT, CLASS_WEIGHT, OVERDUE_WEIGHT, TIMEBLOCKS, HWCNT_WEIGHT


def overlap_fitness_comp(soln, sched):
    """
    Calculates the numerical component of the fitness function related to assigned time overlap.
    Solutions that contain TODOs scheduled with overlapping times are punished.
    """
    delta = 0

    # look at each possible pairing of times
    for i in soln:
        for j in soln:
            delta -= OVERLAP_WEIGHT*Schedulable.calculate_overlap(i, j)

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
            if j.cname == i.cname:
                delta += NINJA_WEIGHT*Schedulable.calculate_overlap(i, j)

    return delta


def class_overlap_fitness_comp(soln, sched):
    """
    Finds the the duration of time any of the solutions are overlapping with
    any of the classes and returns the negative sum.
    """
    delta = 0

    for c in sched.classes:
        for i in soln:
            delta -= CLASS_WEIGHT*Schedulable.calculate_overlap(c, i)

    return delta


def overdue_fitness_comp(soln, sched):
    """
    Returns the negative number of timeblocks every assignment would be if overdue.
    """
    delta = 0

    for s in soln:
        if s.day >= s.due:
            # to make this continuous it returns the number of timeblocks overdue an
            # assignment would be
            # TODO: does this need to be different? i dont really know
            delta -= OVERDUE_WEIGHT*TIMEBLOCKS*(s.day - s.due)

    return delta


def hwcnt_fitness_comp(soln, sched):
    """
    Returns the difference between the number of homeworks that are expected
    and the number of unique homeworks that are actually scheduled to be completed.
    """
    # get the difference in the number of homeworks we're supposed to have and the
    # number of UNIQUE homeworks we actually schedule time for, and negatively weight
    # the outcome
    return -HWCNT_WEIGHT*(len(sched.hws) - len({c.cname for c in soln}))


# find all the previously-defined fitness functions based on function name
# this is hackish, but kinda cool. it also has to come after all the function
# declarations/definitions
FIT_FUNCS = [fn for name, fn in locals().items() if name.endswith("_fitness_comp")]
def fitness(soln, sched):
    """
    Evaluates the fitness of the given solution in the overall fitness landscape.
    A solution's fitness is calculated based on the sum of all the fitness functions
    defined in this file (collected dynamically).
    """
    return sum([fn(soln, sched) for fn in FIT_FUNCS])
