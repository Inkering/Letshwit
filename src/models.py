"""
Objects for holding all separate and distinct data models.

@authors: Elias and Dieter
"""
import copy
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
        days = [INV_DAY_MAP[day]]
        super().__init__(start=start, end=end, days=days)

    @property
    def day(self):
        """ Provides a shortcut for getting the assigned day. """
        return self.days[0]

    @day.setter
    def day(self, val):
        """ Enables setting the internal day value via a property setter. """
        self.days[0] = val
    
    def __deepcopy__(self, memo):
        """ Overrides __deepcopy__ to preserve the shared assignment attribute. """
        # cache hw
        hw = self.hw
        del self.__dict__['hw'] # remove attribute reference so we don't copy it

        # deepcopy and prevent infinite loops
        deepcopy_method = self.__deepcopy__
        self.__deepcopy__ = None
        cp = copy.deepcopy(self, memo)
        self.__deepcopy__ = deepcopy_method

        # restore cached hw
        self.hw = cp.hw = hw

        return cp


class Individual:
    """ Representation of an individual in our genetic model. """

    def __init__(self, soln, fitness):
        self.soln = soln
        self.fitness = fitness
