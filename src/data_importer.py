import numpy as np
import pandas as pd
import random


def load_classes(file_name):
    """
    load classes from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = '../data/' + file_name
    data = pd.read_csv(path)


def load_ninja_hrs(file_name):
    """
    load ninja hours from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = '../data/' + file_name
    data = pd.read_csv(path)


def load_homework(file_name):
    """
    load homework from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = '../data/' + file_name
    data = pd.read_csv(path)
