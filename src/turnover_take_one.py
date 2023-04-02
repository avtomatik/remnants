#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:05:32 2023

@author: green-machine
"""

# =============================================================================
# usa_cobb_douglas0005.py
# =============================================================================


import matplotlib.pyplot as plt
from pandas import DataFrame

from thesis.src.lib.collect import stockpile_cobb_douglas


def plot_turnover_take_one(df: DataFrame) -> None:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Product
        ================== =================================
    """
    df['c_turnover'] = df.iloc[:, 1].div(df.iloc[:, 0])
    plt.figure(1)
    plt.plot(df.iloc[:, 2], df.iloc[:, 0])
    plt.title(
        'Fixed Assets Volume to Fixed Assets Turnover, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Fixed Assets Turnover')
    plt.ylabel('Fixed Assets Volume')
    plt.grid()
    plt.figure(2)
    plt.plot(df.iloc[:, 2], label='Fixed Assets Turnover')
    plt.title('Fixed Assets Turnover, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Fixed Assets Turnover')
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == '__main__':
    stockpile_cobb_douglas().iloc[:, [0, 2]].pipe(plot_turnover_take_one)
