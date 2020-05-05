"""
Wraps and runs the core GA with some pretty CLI outputs.

@authors: Dieter and Elias
"""
import pandas as pd
from tabulate import tabulate
from tunables import TIMEBLOCKS, INV_DAY_MAP
from generics import Schedule
from data_importer import load_classes, load_homework, load_ninja_hrs, tprint
from fitness import (
    overlap_fitness_comp,
    ninja_fitness_comp,
    class_overlap_fitness_comp,
    overdue_fitness_comp,
    hwcnt_fitness_comp,
)
from ga import run_algorithm


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_soln(best, craw, hraw, nraw):
    """ pretty print the solution """
    calendar = pd.DataFrame(index=range(TIMEBLOCKS), columns=range(7))
    calendar.columns = pd.Series(["S", "U", "M", "T", "W", "R", "F"])

    count_overlap = 0
    count_due = 0

    # fill in classes
    for course in craw.iterrows():
        name = course[1][0]
        start = course[1][1]
        end = course[1][2]
        # select date range
        for idx, val in course[1].iloc[3:].items():
            if val == 1:
                calendar[str(idx)].iloc[start:end] = (
                    bcolors.OKGREEN + name + bcolors.ENDC
                )

    # fill in ninja hours
    for ninja in nraw.iterrows():
        name = ninja[1][0]
        start = ninja[1][1]
        end = ninja[1][2]
        # select date range
        for idx, val in ninja[1].iloc[3:-1].items():
            if val == 1:
                calendar[str(idx)].iloc[start:end] = (
                    bcolors.OKBLUE + name + bcolors.ENDC
                )

    # fill in homework
    for i in best.soln:
        start = i.start
        end = i.end
        name = i.hw.desc
        day = INV_DAY_MAP[i.day]
        # TODO: add seperate color for NINJA hours
        if calendar[day].iloc[start:end].count() > 0:
            count_overlap += 1
            color = bcolors.FAIL
        else:
            color = bcolors.HEADER

        if i.day >= i.hw.due:
            count_due += 1
            color = bcolors.UNDERLINE

        calendar[str(day)].iloc[start:end] = color + name + bcolors.ENDC

    calendar.fillna(" ", inplace=True)

    print(
        "Key: ",
        bcolors.OKGREEN + "course" + bcolors.ENDC,
        bcolors.OKBLUE + "ninja hours" + bcolors.ENDC,
        bcolors.FAIL + "conflict" + bcolors.ENDC,
        bcolors.UNDERLINE + "due date wrong" + bcolors.ENDC,
        bcolors.HEADER + "homework correct" + bcolors.ENDC,
        "\n",
    )
    tprint("Calendar", calendar)
    print(
        "course overlap conflicts:",
        count_overlap,
        "after due date conflict:",
        count_due,
    )


def execute():
    """
    Runs the main program with useful and pretty terminal outputs.
    """
    print("\n====")
    print("==== IMPORTED DATA ====")
    print("====\n")

    # load the courses, homework assignments, and ninja hours
    courses, craw = load_classes("classes.csv")
    homeworks, hraw = load_homework("homework.csv")
    ninja_hrs, nraw = load_ninja_hrs("ninja.csv")

    # store the imported data into a dummy object
    sched = Schedule(courses, ninja_hrs, homeworks)

    print("\n====")
    print("==== EVOLUTION ====")
    print("====\n")

    best = run_algorithm(sched)

    print_soln(best, craw, hraw, nraw)
    print("solution:", [(i.start, i.end) for i in best.soln])
    print("fitness:", best.fitness)
    print("  - overlap:", overlap_fitness_comp(best.soln, sched))
    print("  - ninja:", ninja_fitness_comp(best.soln, sched))
    print("  - class:", class_overlap_fitness_comp(best.soln, sched))
    print("  - overdue:", overdue_fitness_comp(best.soln, sched))
    print("  - hwcnt:", hwcnt_fitness_comp(best.soln, sched))


if __name__ == "__main__":
    execute()
