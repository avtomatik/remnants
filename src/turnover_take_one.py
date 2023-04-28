#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:05:32 2023

@author: green-machine
"""

# =============================================================================
# usa_cobb_douglas0005.py
# =============================================================================


from remnants.src.lib.plot import plot_turnover_take_one
from thesis.src.lib.stockpile import stockpile_cobb_douglas

if __name__ == '__main__':
    stockpile_cobb_douglas().iloc[:, [0, 2]].pipe(plot_turnover_take_one)

