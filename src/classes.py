"""
The data models and generic schedulable interface for running the GA.

@author: Elias and Dieter
"""
import numpy as np
from abc import ABC

NUM_BLOCKS = 2 # how many blocks per hour
TIMEBLOCKS = 24 * NUM_BLOCKS
DAYS_PER_WEEK = 7

DAY_MAP = ['S', 'U', 'M', 'T', 'W', 'R', 'F']


class Schedulable(ABC):
    """ A generic interface for data models that have a temporal component. """

    def __init__(self, start, end, days):
        self.start = start
        self.end = end
        self.days = [DAY_MAP.index(d) for d in days]

    def calculate_overlap(s1, s2):
        """ Calculates the overlap between the date ranges of the two given schedulables. """
        delta = 0

        # loop through all the possible days and add up all the overlap
        for d1 in s1.days:
            for d2 in s2.days:
                if d1 == d2:
                    # add the time overlap from the either side of the first event
                    if s1.start <= s2.end: delta += s2.end - s1.start
                    if s2.start <= s1.end: delta += s1.end - s2.start

        return delta


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

    def __init__(self, cname, cuuid, duration, desc, duedate):
        self.cname = cname
        self.cuuid = cuuid
        self.duration = duration * NUM_BLOCKS
        self.desc = desc
        self.due = DAY_MAP.index(duedate)


class TODO(Assignment, Schedulable):
    """ The model for when to complete what homework assignment. """

    def __init__(self, day, **kwargs, hw):
        end = start + hw.duration
        super().__init__(days=[day],
                end=end, cname=hw.cname, duration=hw.duration, desc=hw.desc, duedate=hw.due)

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
        t1.start, t2.start = t2.start, t1.start
        t1.end = t1.start + t1.duration
        t2.end = t2.end + t2.duration
