"""
Generic schedulable interface and schedule object for holding all imported data. This
makes it easier than passing around a a dict or multiple variables to all of the fitness functions.

@author: Elias and Dieter
"""
from abc import ABC  # Easy as 1-2-3!
from tunables import DAY_MAP

class Schedulable(ABC):
    """ A generic interface for data models that have a temporal component. """

    def __init__(self, start, end, days):
        self.start = start
        self.end = end
        self.days = [DAY_MAP[d] for d in days]

    def calculate_overlap(s1, s2):
        """ Calculates the overlap between the date ranges of the two given schedulables. """
        delta = 0

        # if 'cname' in s2.__dict__:
        #     print(s2.cname, s2.days)

        # loop through all the possible days and add up all the overlap
        for d1 in s1.days:
            for d2 in s2.days:
                #if d1 == d2:
                 #   if s2.start <= s1.end:
                 #       print(s1.hw.desc, s1.start, s1.end, s2.start, s2.end, s2.end - s1.start)
                 #   else:
                 #       print(s1.hw.desc, s1.start, s1.end, s2.start, s2.end, s2.end - s1.start)
                # if they're on the same day and overlap
                if d1 == d2 and s2.start <= s1.end and s2.end > s1.start:
                    # calculate and add the overlapping range
                    delta += min(s1.end, s2.end) - max(s1.start, s2.start)

        return delta


class Schedule:
    """ Dummy structure for holding imported data. """

    def __init__(self, classes, hours, assignments):
        self.classes = classes
        self.ninja_hours = hours
        self.hws = assignments
