"""
All the data models our genetic algorithm.

@author: Elias and Dieter
"""
import numpy as np


NUM_BLOCKS = 2 # how many blocks per hour
TIMEBLOCKS = 24 * NUM_BLOCKS
DAYS_PER_WEEK = 7

DAY_MAP = ['S', 'U', 'M', 'T', 'W', 'R', 'F']


class Course:
    """ Holds all the information about the class. """

    def __init__(self, name, start, end, days):
        self.uuid = name
        self.start = start
        self.end = end
        self.days = [DAY_MAP.index(d) for d in days]
        #ov = self.occupancy_vector = numpy.zeros(TIMEBLOCKS * DAYS_PER_WEEK)
        # self.occupancy_vector[(ov >= start and ov <= end) and ov >= (days*TIMEBLOCKS)]


class NINJA(Course):
    """ Holds all the information pertaining to NINJA hours. """

    def __init__(self, nname, **ckwargs):
        self.ninja = nname
        super().__init__(**ckwargs)


class Assignment:
    """ The data model containing the information for homework assignments. """

    def __init__(self, cname, cuuid, duration, desc, duedate):
        self.cname = cname
        self.cuuid = cuuid
        self.duration = duration * NUM_BLOCKS
        self.desc = desc
        self.duedate = DAY_MAP.index(duedate)


class TODO(Assignment):
    """ The model for when to complete what homework assignment. """

    def __init__(self, start, day, hw):
        self.start = start
        self.end = start + hw.duration
        self.day = day
        super().__init__(cname=hw.cname, duration=hw.duration, desc=hw.desc, duedate=hw.duedate)

    def mutate_across(t1, t2):
        """ Mutates the two given instances by swapping their assigned completion ranges. """
        # swap the assigned days
        t1.day, t2.day = t2.day, t1.day

        # swap and recalculate the respective time ranges
        t1.start, t2.start = t2.start, t1.start
        t1.end = t1.start + t1.duration
        t2.end = t2.end + t2.duration
