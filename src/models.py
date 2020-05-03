"""
Objects for holding all separate and distinct data models.

@authors: Elias and Dieter
"""


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
        self.due = DAY_MAP[duedate]


class TODO(Assignment, Schedulable):
    """ The model for when to complete what homework assignment. """

    def __init__(self, start, day, hw):
        end = start + hw.duration
        super().__init__(
            start=start,
            end=end,
            days=[day],
            cname=hw.cname,
            duration=hw.duration,
            desc=hw.desc,
            duedate=hw.due,
        )

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
