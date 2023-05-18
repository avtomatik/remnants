#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 10:38:12 2023

@author: green-machine
"""


import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot, bootstrap_plot, lag_plot

from remnants.src.lib.read import read_pull_for_autocorrelation

FUNCTIONS = (
    # =========================================================================
    # Correlogram, Pandas;
    # =========================================================================
    autocorrelation_plot,
    # =========================================================================
    # Bootstrap Plot, Pandas;
    # =========================================================================
    bootstrap_plot,
    # =========================================================================
    # Lag Plot, Pandas
    # =========================================================================
    lag_plot,
)


def plot_built_in(module: callable) -> None:
    FILE_NAME = 'datasetAutocorrelation.txt'
    SERIES_IDS = sorted(set(pd.read_csv(FILE_NAME).iloc[:, [1]]))
    for _, series_id in enumerate(SERIES_IDS, start=1):
        plt.figure(_)
        read_pull_for_autocorrelation(FILE_NAME, series_id).pipe(module)
        plt.grid()

    SERIES_IDS = sorted(set(pd.read_csv(FILE_NAME).iloc[:, [1]]))
    FILE_NAME = 'CHN_TUR_GDP.zip'
    for _, series_id in enumerate(SERIES_IDS, start=5):
        plt.figure(_)
        read_pull_for_autocorrelation(FILE_NAME, series_id).pipe(module)
        plt.grid()

    plt.show()


if __name__ == '__main__':
    for func in FUNCTIONS:
        plot_built_in(func)
