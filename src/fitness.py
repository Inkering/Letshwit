"""
A helper file containing all the functions related to fitness calculation.

@authors: Elias and Dieter
"""
from classes import Schedulable


def overlap_fitness_comp(soln):
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


def ninja_fitness_comp(soln, ninja_hours):
    """
    Calculates the numerical componet of the fitness function based on whether or not TODOs in
    the solution overlap with NINJA hours for its specific class.
    """
    delta = 0

    # check if any todos overlap with NINJA hours
    for i in soln:
        for j in ninja_hours:
            # if the NINJA is right for the class
            if j.cname == i.cname:
                delta += NINJA_WEIGHT*Schedulable.calculate_overlap(i, j)

    return delta


def class_overlap_fitness_comp(soln, classes):
    """
    Finds the the duration of time any of the solutions are overlapping with
    any of the classes and returns the negative sum.
    """
    delta = 0

    for c in classes:
        for i in soln:
            delta -= CLASS_WEIGHT*Schedulable.calculate_overlap(c, i)

    return delta


def overdue_fitness_comp(soln):
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

def hwcnt_fitness_comp(soln, hws):
    """
    Returns the difference between the number of homeworks that are expected
    and the number of unique homeworks that are actually scheduled to be completed.
    """
    # get the difference in the number of homeworks we're supposed to have and the
    # number of UNIQUE homeworks we actually schedule time for, and negatively weight
    # the outcome
    return -HWCNT_WEIGHT*(len(hws) - len({c.cname for c in soln}))


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
