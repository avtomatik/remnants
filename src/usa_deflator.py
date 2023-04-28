#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:42:58 2023

@author: green-machine
"""


import matplotlib.pyplot as plt
import pandas as pd

from constants import SERIES_IDS_CD, SERIES_IDS_PRCH
from thesis.src.lib.tools import construct_usa_hist_deflator

# =============================================================================
# usa_cobb_douglas0008.py
# =============================================================================

LEGEND = ['Cobb$-$Douglas Work', 'Census HSUS 1975']
df = pd.concat(
    map(construct_usa_hist_deflator, (SERIES_IDS_CD, SERIES_IDS_PRCH)),
    axis=1,
    sort=True
)
plt.figure()
plt.plot(df.iloc[:, 0], 'r', linewidth=3)
plt.plot(df.iloc[:, 1])
plt.title(f'Manufacturing Fixed Assets Deflator, {df.iloc[55, 0]}=100')
plt.xlabel('Period')
plt.ylabel('Unity')
plt.grid()
plt.legend(LEGEND)
plt.show()
