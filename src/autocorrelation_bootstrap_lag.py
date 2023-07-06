#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 21:27:14 2023

@author: green-machine
"""


from pathlib import Path, PosixPath
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
from core.funcs import pull_by_series_id, read_worldbank
from pandas.plotting import autocorrelation_plot, lag_plot


def get_kwargs(file_name: str) -> dict[str, Union[int, str, PosixPath]]:
    PATH = '/home/green-machine/data_science/remnants/data'
    return {
        'filepath_or_buffer': Path(PATH).joinpath(file_name),
        'header': 0,
        'names': ['period', 'series_ids', 'value'],
        'index_col': 0,
    }


FUNCTIONS = (
    # =========================================================================
    # Correlogram, Pandas;
    # =========================================================================
    autocorrelation_plot,
    # =========================================================================
    # Bootstrap Plot, Pandas;
    # =========================================================================
    # bootstrap_plot,
    # =========================================================================
    # Lag Plot, Pandas
    # =========================================================================
    lag_plot,
)

if __name__ == '__main__':

    # =============================================================================
    #     # =========================================================================
    #     # Early Attempt
    #     # =========================================================================
    #     FILE_NAMES = ['datasetAutocorrelation.txt', 'CHN_TUR_GDP.zip']
    #
    #     df = pd.concat(map(lambda _: pd.read_csv(**get_kwargs(_)), FILE_NAMES))
    #
    #     SERIES_IDS = df.loc[:, 'series_ids'].unique()
    #
    #     for func in FUNCTIONS:
    #         for _, series_id in enumerate(SERIES_IDS, start=1):
    #             plt.figure(_)
    #             df.pipe(pull_by_series_id, series_id).pipe(func)
    #             if func == lag_plot:
    #                 plt.grid()
    #             plt.show()
    # =============================================================================

    # =========================================================================
    # Revised
    # =========================================================================
    SOURCE_ID = 'NY.GDP.MKTP.CD'

    df = read_worldbank(SOURCE_ID)

    for func in FUNCTIONS:
        for _, country in enumerate(df.columns, start=1):
            chunk = df.loc[:, [country]].dropna(axis=0)
            if not chunk.empty:
                plt.figure(_)
                chunk.pipe(func)
                plt.title(country)
                if func == lag_plot:
                    plt.grid()
                plt.show()
