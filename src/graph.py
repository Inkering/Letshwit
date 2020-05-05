"""
Wraps and runs the core GA for timing and runtime evaulation.

@authors: Elias and Dieter
"""
from generics import Schedule
from data_importer import load_classes, load_homework, load_ninja_hrs
from matplotlib import pyplot as plt
import timeit


def execute():
    """
    Runs the main program and evaulates its runtime over varying size parameters.
    """
    # load the courses, homework assignments, and ninja hours
    courses, craw = load_classes("classes.csv")
    homeworks, hraw = load_homework("homework.csv")
    ninja_hrs, nraw = load_ninja_hrs("ninja.csv")

    # store the imported data into a dummy object
    sched = Schedule(courses, ninja_hrs, homeworks)
    xs = range(1, 201, 20)
    ys = []

    # for n in xs:
    #    ys.append(
    #        timeit.timeit(
    #            "run_algorithm(sched, n=n)",
    #            setup="from ga import run_algorithm",
    #            globals=locals(),
    #            number=100,
    #        )
    #    )

    # plt.title("GA Runtime vs Number of Generations")
    # plt.xlabel("number of generations")
    # plt.ylabel("time (s)")
    # plt.plot(xs, ys)
    # plt.savefig("gen_time.png")

    for m in xs:
        ys.append(
            timeit.timeit(
                "run_algorithm(sched, m=m+5)",
                setup="from ga import run_algorithm",
                globals=locals(),
                number=100,
            )
        )

    plt.title("GA Runtime vs Population Size")
    plt.xlabel("population size")
    plt.ylabel("time (s)")
    plt.plot(xs, ys)
    plt.savefig("pop_time.png")


if __name__ == "__main__":
    execute()
