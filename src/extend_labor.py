#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 22:20:06 2023

@author: green-machine
"""

# =============================================================================
# usa_cobb_douglas0011.py
# =============================================================================

import matplotlib.pyplot as plt
import pandas as pd
from core.classes import Dataset, SeriesID
from core.constants import SERIES_IDS_LAB
from core.funcs import get_pre_kwargs, stockpile, transform_mean

# =============================================================================
# Manufacturing Laborers' Series Comparison
# =============================================================================


def get_data_frame():

    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'

    SERIES_IDS = [
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        SeriesID('CDT3S1', Dataset.USA_COBB_DOUGLAS),
        # =====================================================================
        # Bureau of the Census 1949, D0069
        # =====================================================================
        SeriesID('D0069', Dataset.USCB),
        # =====================================================================
        # Bureau of the Census 1975, D0130
        # =====================================================================
        SeriesID('D0130', Dataset.USCB),
    ] or [
        # =====================================================================
        # Bureau of the Census 1949, J0004
        # =====================================================================
        SeriesID('J0004', Dataset.USCB),
        # =====================================================================
        # Bureau of the Census 1975, P0005
        # =====================================================================
        SeriesID('P0005', Dataset.USCB),
        # =====================================================================
        # Bureau of the Census 1975, P0062
        # =====================================================================
        SeriesID('P0062', Dataset.USCB),
    ]

    return pd.concat(
        [
            stockpile(SERIES_IDS),
            stockpile(SERIES_IDS_LAB).pipe(
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

    YEAR_BASE = 1929
    COL_NAME = 'historical'

    # =============================================================================
    # J.W. Kendrick, Productivity Trends in the United States, Table D-II, 'Persons Engaged' Column, pp. 465--466
    # =============================================================================
    SERIES_ID = [SeriesID('KTD02S02', Dataset.USA_KENDRICK)]

    df_hist = get_data_frame()

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

    df_left = stockpile(SERIES_ID).mul(
        df_right.at[YEAR_BASE, COL_NAME]
    ).div(100)

    plt.figure(2)
    plt.plot(df_right, label=COL_NAME, linewidth=4)
    plt.plot(df_left, label='J.W. Kendrick')
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
