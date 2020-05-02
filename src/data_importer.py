import numpy as np
import pandas as pd
import random
from classes import *


def load_classes(file_name):
    """
    load classes from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = '../data/' + file_name
    data = pd.read_csv(path)

    class_list = []

    return class_list


def load_ninja_hrs(file_name):
    """
    load ninja hours from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = '../data/' + file_name
    data = pd.read_csv(path)

    ninja_list = []
    return ninja_list


def load_homework(file_name):
    """
    load homework from a unique csv file in the data folder
    file_name: the name of the csv file
    """
    path = '../data/' + file_name
    data = pd.read_csv(path)

    homework_list = []
    return homework_list
