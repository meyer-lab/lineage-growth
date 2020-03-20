"""
File: figure4.py
Purpose: Generates figure 4.
Figure 4 analyzes heterogeneous (2 state), censored (by both time and fate),
populations of lineages (more than one lineage per populations)
with at least 16 cells per lineage
over increasing number of lineages per population.
"""
import numpy as np

from .figureCommon import getSetup, subplotLabel, commonAnalyze, figureMaker, pi, T, E, min_desired_num_cells, min_experiment_time, min_num_lineages, max_num_lineages, num_data_points
from ..LineageTree import LineageTree


def makeFigure():
    """
    Makes figure 4.
    """

    # Get list of axis objects
    ax, f = getSetup((7, 6), (2, 3))

    figureMaker(ax, *accuracy())

    subplotLabel(ax)

    return f


def accuracy():
    """
    Calculates accuracy and parameter estimation
    over an increasing number of lineages in a population for
    a censored two-state model.
    We increase the desired number of cells in a lineage by
    the experiment time.
    """

    # Creating a list of populations to analyze over
    num_lineages = np.linspace(min_num_lineages, max_num_lineages, num_data_points, dtype=int)
    list_of_populations = []
    for num in num_lineages:
        population = []

        for _ in range(num):
            population.append(LineageTree(pi, T, E, min_desired_num_cells, censor_condition=3, desired_experiment_time=min_experiment_time))

        # Adding populations into a holder for analysing
        list_of_populations.append(population)

    return commonAnalyze(list_of_populations)
