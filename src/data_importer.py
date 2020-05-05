"""
Imports and parses data from the supplied CSVs.

@authors: Dieter and Elias
"""
import pandas as pd
from tabulate import tabulate
from models import Course, NINJAHours, Assignment


# TODO: refactor this
def day_parse(row):
    days = []

    if row["S"] == 1:
        days.append("S")
    if row["U"] == 1:
        days.append("U")
    if row["M"] == 1:
        days.append("M")
    if row["T"] == 1:
        days.append("T")
    if row["W"] == 1:
        days.append("W")
    if row["R"] == 1:
        days.append("R")
    if row["F"] == 1:
        days.append("F")

    return days


def tprint(header, data):
    """
    prints the data using tabulate
    """
    print("  ", header, ":")
    print(tabulate(data, headers="keys", tablefmt="fancy_grid"), "\n")


def load_classes(file_name):
    """
    load classes from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = "../data/" + file_name
    data = pd.read_csv(path)

    tprint("Classes", data)

    class_list = []

    for index, row in data.iterrows():
        days = day_parse(row)
        course = Course(
            name=row["class"], start=row["start-block"], end=row["end-block"], days=days
        )

        class_list.append(course)

    return class_list, data


def load_ninja_hrs(file_name):
    """
    load ninja hours from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = "../data/" + file_name
    data = pd.read_csv(path)

    tprint("NINJA Hours", data)

    ninja_list = []

    for index, row in data.iterrows():
        days = day_parse(row)

        a_ninja = NINJAHours(
            ninja=row["name"],
            name=row["class"],
            start=row["start-block"],
            end=row["end-block"],
            days=days,
        )

        ninja_list.append(a_ninja)

    return ninja_list, data


def load_homework(file_name):
    """
    load homework from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = "../data/" + file_name
    data = pd.read_csv(path)

    tprint("Homeworks", data)

    homework_list = []

    for index, row in data.iterrows():
        a_assignment = Assignment(
            cname=row["class"],
            desc=row["description"],
            duration=row["duration"],
            due=row["due"],
        )

        homework_list.append(a_assignment)

    return homework_list, data
