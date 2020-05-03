import numpy as np
import pandas as pd
import random
from classes import Course, NINJA, Assignment, TODO


def day_parse(row):
    days = []
    # handler for if S//U column doesn't exist?
    if row["S"] == 1:
        days.append("S")
    elif row["U"] == 1:
        days.append("U")
    elif row["M"] == 1:
        days.append("M")
    elif row["T"] == 1:
        days.append("T")
    elif row["W"] == 1:
        days.append("W")
    elif row["TH"] == 1:
        days.append("TH")
    elif row["F"] == 1:
        days.append("F")

    return days


def load_classes(file_name):
    """
    load classes from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = "../data/" + file_name
    data = pd.read_csv(path)

    class_list = []

    for index, row in data.iterrows():
        days = day_parse(row)
        course = Course(
            uuid=row["CUUID"], start=row["start-block"], end=row["end-block"], days=days
        )

        class_list.append(course)

    return class_list


def load_ninja_hrs(file_name):
    """
    load ninja hours from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = "../data/" + file_name
    data = pd.read_csv(path)

    ninja_list = []

    for index, row in data.iterrows():
        days = day_parse(row)
        # todo: change column name to ninja-name or something
        a_ninja = NINJA(
            nname=row["Class"],
            uuid=row["CUUID"],
            start=row["start-block"],
            end=row["end-block"],
            days=days,
        )

        ninja_list.append(a_ninja)

    return ninja_list


def load_homework(file_name):
    """
    load homework from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = "../data/" + file_name
    data = pd.read_csv(path)

    homework_list = []

    for index, row in data.iterrows():
        days = day_parse(row)
        # todo: change column name to ninja-name or something
        a_assignment = NINJA(
            cname=row["class"],
            cuuid=row["CUUID"],
            desc=row["assignment"],
            duedate=row[due],
        )
        # TODO: add durations column

        home_list.append(a_assignment)

    return homework_list
