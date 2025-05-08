#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 22:35:24 2023

@author: green-machine
"""

# =============================================================================
# usa_cobb_douglas0009.py
# =============================================================================


import matplotlib.pyplot as plt
import pandas as pd

from thesis.src.lib.transform import transform_cobb_douglas


def transform_plot(df: pd.DataFrame):
    """
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    ================== =================================
    """
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])

    df['lab_cap_int'].pipe(plot_filter_kol_zur)
    df['lab_cap_int'].pipe(plot_filter_rolling_mean)
    df['lab_cap_int'].pipe(plot_ewm)
    # =========================================================================
    # Figure 1
    # =========================================================================
    # Series 1
    # df['lab_cap_int'].pipe(plot_filter_kol_zur)
    # =========================================================================
    # Extra: 1
    # =========================================================================
    # Series 2
    # Header: Sheet1!$C$1
    # X Series: Period
    # Y Series: X @ WINDOW: 2 # <plot_filter_rolling_mean> CobbDouglas X [1:25]
    # =========================================================================
    # Extra: 2
    # =========================================================================
    # Series 3
    # Header: Sheet1!$F$1
    # X Series: Period
    # Y Series: X @ DELTA{1} # <plot_filter_kol_zur> CobbDouglas X [1:25]
    # =========================================================================
    # Extra: 3
    # =========================================================================
    # Series 4
    # Header: Sheet1!$I$1
    # X Series: Period
    # Y Series: X @ SMOOTHING (WINDOW: 5, ALPHA: 0.25) # <plot_ewm> CobbDouglas X [1:25]
    # =========================================================================
    # Extra: 4
    # =========================================================================
    # =========================================================================
    # Figure 2
    # =========================================================================
    # Series 1
    # Header: Y
    # X Series: Period
    # Y Series: Y
    # =========================================================================
    # Extra: 1
    # =========================================================================
    # Series 2
    # Header: Sheet2!$C$1
    # X Series: Period
    # Y Series: Y @ WINDOW: 2 # <plot_filter_rolling_mean> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 2
    # =========================================================================
    # Series 3
    # Header: Sheet2!$D$1
    # X Series: Period
    # Y Series: Y @ WINDOW: 3 # <plot_filter_rolling_mean> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 3
    # =========================================================================
    # Series 4
    # Header: Sheet2!$E$1
    # X Series: Period
    # Y Series: Y @ WINDOW: 4 # <plot_filter_rolling_mean> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 4
    # =========================================================================
    # Series 5
    # Header: Sheet2!$F$1
    # X Series: Period
    # Y Series: Y @ DELTA{1} # <plot_filter_kol_zur> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 5
    # =========================================================================
    # Series 6
    # Header: Sheet2!$G$1
    # X Series: Period
    # Y Series: Y @ DELTA{2} # <plot_filter_kol_zur> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 6
    # =========================================================================
    # Series 7
    # Header: Sheet2!$H$1
    # X Series: Period
    # Y Series: Y @ DELTA{3} # <plot_filter_kol_zur> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 7
    # =========================================================================
    # Series 8
    # Header: Sheet2!$I$1
    # X Series: Period
    # Y Series: Y @ SMOOTHING (WINDOW: 5, ALPHA: 0.25) # <plot_ewm> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 8
    # =========================================================================
    # Series 9
    # Header: Sheet2!$J$1
    # X Series: Period
    # Y Series: Y @ SMOOTHING (WINDOW: 5, ALPHA: 0.35) # <plot_ewm> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 9
    # =========================================================================
    # Series 10
    # Header: Sheet2!$K$1
    # X Series: Period
    # Y Series: Y @ SMOOTHING (WINDOW: 5, ALPHA: 0.45) # <plot_ewm> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 10
    # =========================================================================
    plt.figure(1)
    plt.plot(df['lab_cap_int'])
    plt.plot(df['lab_cap_int'].rolling(2, center=True).mean(), ':')
    plt.xlabel('Period')
    plt.ylabel('Labor Capital Intensity')
    plt.grid()
    plt.figure(2)
    plt.plot(df['lab_product'])
    plt.plot(df['lab_product'].rolling(2, center=True).mean(), ':')
    plt.plot(df['lab_product'].rolling(3, center=True).mean(), ':')
    plt.plot(df['lab_product'].rolling(4, center=True).mean(), ':')
    plt.xlabel('Period')
    plt.ylabel('Labor Productivity')
    plt.grid()
    plt.show()


YEAR_BASE = 1899
combine_cobb_douglas().pipe(
    transform_cobb_douglas, year_base=YEAR_BASE
)[0].pipe(transform_plot)
