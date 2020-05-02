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


class NINJA(Class):
    """ Holds all the information pertaining to NINJA hours. """
    def __init__(self, nname, **ckwargs):
        self.ninja = nname
        super().__init__(**ckwargs)


class Assignment:
    """ The data model containing the information for homework assignments. """
    def __init__(self, cname, duration, desc, duedate):
        self.cname = cname
        self.duration = duration * NUM_BLOCKS
        self.desc = desc
        self.duedate = DAY_MAP.index(duedate)
