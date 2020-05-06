# Let's HW It

One of the most challenging tasks about college is scheduling. Between classes, extra-curriculars, sleep, and time with friends, figuring out how and when you need to complete your assignments becomes an enourmous task. To help mitigate some of that stress, we designed and implemented an intelligent homework scheduling application. Accepting students' weekly schedules and a list of their assignments, Let's HW It makes use of a homebrew genetic algorithm to find and suggest an agenda that works for a user.

If you want to read more about the design process and implementation details, feel free to skim through (or read) our more comprehensive report [here](./docs/report.md).

## Features / Design Principles

* Robust to a wide variety of schedules and inputs
* Simple to understand and use
  * Data is imported via CSV
* Modular to allow seamless integration into existing applications via a stable API
* Nice to look at in a terminal
* Tunable to fit individual needs
  * Runtime parameters (like time intervals, fitness weights, and mutation probabilities) can be tweaked

## Installation

### Prerequisite

By design, Let's HW It is cross-platform and environment independent. There are only two prerequisites before you can get it up and running on your local machine:
- Python 3.8+
- [Poetry](https://python-poetry.org/docs/) (or a compatible Python environment manager)

### Downloading and Running

Once you've installed the prerequisites, simply clone this repository, install the dependencies, and run the program. You can do all of that via:

```sh
  $ git clone https://github.com/lemoment/letshwit.git
  $ cd letshwit/src
  $ poetry install
  $ poetry run python cli.py
```

## Tweaking

You can adjust the schedule and assignment inputs by adjusting the CSVs in the `data` directory. In the future, inputting your own data will be as simple as syncing with Google Calendar or Outlook Calendar.

If you're finding that your proposed solutions could be better, feel free to tweak the algorithmic paramters in `src/tunables.py`. **Make sure you know what you're doing though! Changing things like `TOURAMENT_SIZE` can have unintended (and often negative) consequences.**
