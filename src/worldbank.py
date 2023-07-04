#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 22:17:50 2023

@author: green-machine
"""


from functools import partial

import matplotlib.pyplot as plt
from core.funcs import read_worldbank
from pandas.plotting import autocorrelation_plot, lag_plot

if __name__ == '__main__':
    FUNCTIONS = (
        # =====================================================================
        # Correlogram, Pandas;
        # =====================================================================
        autocorrelation_plot,
        # =====================================================================
        # Bootstrap Plot, Pandas;
        # =====================================================================
        # bootstrap_plot,
        # =====================================================================
        # Lag Plot, Pandas
        # =====================================================================
        lag_plot,
    )

    SOURCE_ID = 'NY.GDP.MKTP.CD'

    df = read_worldbank(SOURCE_ID)

    for func in FUNCTIONS:
        for _, country in enumerate(df.columns, start=1):
            chunk = df.loc[:, [country]].dropna(axis=0)
            if not chunk.empty:
                plt.figure(_)
                partial(func, chunk)()
                plt.title(country)
                plt.grid()
        plt.show()
