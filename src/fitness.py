"""
A helper file containing all the functions related to fitness calculation.

@authors: Elias and Dieter
"""
from classes import TODO, Schedulable


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


def todo_classes_overlap_fitness(soln):
    """
    Evaluate the fitness of the given solution based on:
    - how many classes overlap with any of the TODOs
    """
    delta = 0
    return delta


def todo_duedate_fitness(soln):
    """
    Evaluate the fitness of the given solution based on:
    - whether or not any of the TODOs come after the assigned due date
    """
    delta = 0
    return delta

def todo_hwcnt_fitness(soln):
    """
    Evaluate the fitness of the given solution based on:
    -  if any of the homework assignments are missing (multiple TODOs for an assignment)
    """
    delta = 0
    return delta


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
