"""
Generic schedulable interface and schedule object for holding all imported data. This
makes it easier than passing around a a dict or multiple variables to all of the fitness functions.

@author: Elias and Dieter
"""
from abc import ABC  # Easy as 1-2-3!


class Schedulable(ABC):
    """ A generic interface for data models that have a temporal component. """

    def __init__(self, start, end, days):
        self.start = start
        self.end = end
        self.days = [DAY_MAP[d] for d in days]

    def calculate_overlap(s1, s2):
        """ Calculates the overlap between the date ranges of the two given schedulables. """
        delta = 0

        # loop through all the possible days and add up all the overlap
        for d1 in s1.days:
            for d2 in s2.days:
                if d1 == d2:
                    # add the time overlap from the either side of the first event
                    if s1.start <= s2.end:
                        delta += s2.end - s1.start
                    if s2.start <= s1.end:
                        delta += s1.end - s2.start

        return delta


class Schedule:
    """ Dummy structure for holding imported data. """

    def __init__(self, classes, hours, assignments):
        self.classes = classes
        self.ninja_hours = hours
        self.hws = assignments