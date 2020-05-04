"""
Objects for holding all separate and distinct data models.

@authors: Elias and Dieter
"""
from generics import Schedulable
from tunables import NUM_BLOCKS, DAY_MAP, INV_DAY_MAP


class Course(Schedulable):
    """ Holds all the information about the class. """

    def __init__(self, name, **kwargs):
        self.cname = name
        super().__init__(**kwargs)


class NINJAHours(Course):
    """ Holds all the information pertaining to NINJA hours. """

    def __init__(self, ninja, **ckwargs):
        self.ninja = ninja
        super().__init__(**ckwargs)


class Assignment:
    """ The data model containing the information for homework assignments. """

    def __init__(self, cname, duration, desc, duedate):
        self.cname = cname
        self.duration = duration * NUM_BLOCKS
        self.desc = desc
        self.due = DAY_MAP[duedate]


class TODO(Schedulable):
    """ The model for when to complete what homework assignment. """

    def __init__(self, start, day, hw):
        self.hw = hw
        end = start + hw.duration
        super().__init__(start=start, end=end, days=[INV_DAY_MAP[day]])

    @property
    def day(self):
        """ Provides a shortcut for getting the assigned day. """
        return self.days[0]

    @day.setter
    def day(self, val):
        """ Enables setting the internal day value via a property setter. """
        self.days[0] = val

    def mutate_across(t1, t2):
        """ Mutates the two given instances by swapping their assigned completion ranges. """
        # swap the assigned days
        t1.day, t2.day = t2.day, t1.day

        # swap and recalculate the respective time ranges
        # t1.start, t2.start = t2.start, t1.start
        # t1.end = t1.start + t1.hw.duration
        # t2.end = t2.end + t2.hw.duration

        # print(t1.start, t1.end, t1.hw.duration, t1.end - t1.start == t1.hw.duration)


class Individual:
    """ Representation of an individual in our genetic model"""

    def __init__(self, soln, fitness):
        self.soln = soln
        self.fitness = fitness
