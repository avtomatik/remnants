#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:45:04 2023

@author: green-machine
"""

from thesis.src.lib.collect import stockpile_cobb_douglas
from thesis.src.lib.plot import plot_cobb_douglas, plot_cobb_douglas_alt

# =========================================================================
# Project I. Classified
# =========================================================================
# =========================================================================
# Project II. Scipy Signal Median Filter, Non-Linear Low-Pass Filter
# =========================================================================
# =========================================================================
# Project III. Scipy Signal Wiener Filter
# =========================================================================

df = stockpile_cobb_douglas(5)

df.iloc[:, range(3)].pipe(plot_cobb_douglas)
df.iloc[:, range(4)].pipe(plot_cobb_douglas_alt)
df.iloc[:, (0, 1, 2, 4)].pipe(plot_cobb_douglas_alt)
