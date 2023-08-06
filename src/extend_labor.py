#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 22:20:06 2023

@author: green-machine
"""

# =============================================================================
# usa_cobb_douglas0011.py
# =============================================================================
import os

import matplotlib.pyplot as plt
import pandas as pd
from core.constants import SERIES_IDS_LAB
from core.funcs import (get_pre_kwargs, stockpile_usa_bea, stockpile_usa_hist,
                        transform_mean)

# =============================================================================
# Manufacturing Laborers' Series Comparison
# =============================================================================


def combine_data():

    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'

    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': 'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # Bureau of the Census 1949, D0069
        # =====================================================================
        'D0069': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, D0130
        # =====================================================================
        'D0130': 'dataset_uscb.zip',
    } or {
        # =====================================================================
        # Bureau of the Census 1949, J0004
        # =====================================================================
        'J0004': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, P0005
        # =====================================================================
        'P0005': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, P0062
        # =====================================================================
        'P0062': 'dataset_uscb.zip',
    }

    return pd.concat(
        [
            stockpile_usa_hist(SERIES_IDS),
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            pd.read_csv(**get_pre_kwargs(FILE_NAME)).iloc[:, [1]]
        ],
        axis=1
    )


if __name__ == '__main__':
    # =============================================================================
    # TODO: Bureau of Labor Statistics
    # =============================================================================
    # =============================================================================
    # TODO: Federal Reserve Board
    # =============================================================================

    PATH = '/media/green-machine/KINGSTON'

    YEAR_BASE = 1929
    COL_NAME = 'historical'

    # =============================================================================
    # Kendrick J.W., Productivity Trends in the United States, Table D-II, 'Persons Engaged' Column, pp. 465--466
    # =============================================================================
    SERIES_ID = {'KTD02S02': 'dataset_usa_kendrick.zip'}

    os.chdir(PATH)

    df_hist = combine_data()

    LABEL = [
        'C.W. Cobb, P.H. Douglas Labor Series',
        'Census 1949, D0069',
        'Census 1975, D0130',
        'bea_labor_mfg',
        'Kurenkov Yu.V.'
    ]

    plt.figure(1)
    plt.plot(df_hist.iloc[:, 0], label=LABEL[0], linewidth=4)
    plt.plot(df_hist.iloc[:, 1:], label=LABEL[1:])
    plt.title('Manufacturing Workers Number')
    plt.xlabel('Period')
    plt.ylabel('Thousands People')
    plt.legend()
    plt.grid()

    df_right = df_hist.pipe(transform_mean, name=COL_NAME)

    df_left = stockpile_usa_hist(SERIES_ID).mul(
        df_right.at[YEAR_BASE, COL_NAME]
    ).div(100)

    plt.figure(2)
    plt.plot(df_right, label=COL_NAME, linewidth=4)
    plt.plot(df_left, label='Kendrick J.W.')
    plt.title('Manufacturing Workers Number')
    plt.xlabel('Period')
    plt.ylabel('Thousands People')
    plt.legend()
    plt.grid()

    df = pd.concat([df_left, df_right], axis=1).pipe(
        transform_mean, name='labor_combined'
    )

    LABEL = [
        'C.W. Cobb, P.H. Douglas Labor Series',
        'labor_combined'
    ]

    plt.figure(3)
    plt.plot(df_hist.iloc[:, 0], linewidth=4)
    plt.plot(df)
    plt.title('Manufacturing Workers Number Data Fusion')
    plt.xlabel('Period')
    plt.ylabel('Thousands People')
    plt.legend(LABEL)
    plt.grid()
    plt.show()
