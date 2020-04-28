import numpy as np
import random

# time blocks where there are classes
classes = []
for i in range(24):
    p = random.random()
    if p > 0.3:
        classes.append(0)
    else:
        classes.append(1)

# possible set of times to do hw in 24 1hr blocks
given_solution = []
for i in range(24):
    given_solution.append(0)

print("original hw schedule", given_solution, len(given_solution), "hrs")

print("class schedule", classes, len(classes), "hrs")

