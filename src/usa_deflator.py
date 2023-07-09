#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:42:58 2023

@author: green-machine
"""


import matplotlib.pyplot as plt
import pandas as pd
from core.constants import SERIES_IDS_CD, SERIES_IDS_PRCH
from core.funcs import construct_usa_hist_deflator

# =============================================================================
# usa_cobb_douglas0008.py
# =============================================================================

LABEL = ['Cobb$-$Douglas Work', 'Census HSUS 1975']


df = pd.concat(
    map(construct_usa_hist_deflator, (SERIES_IDS_CD, SERIES_IDS_PRCH)),
    axis=1,
    sort=True
)
plt.figure()
plt.plot(df.iloc[:, 0], 'r', linewidth=3)
plt.plot(df.iloc[:, 1])
plt.title('Manufacturing Fixed Assets Deflator')
plt.xlabel('Period')
plt.ylabel('Index')
plt.grid()
plt.legend(LABEL)
plt.show()
