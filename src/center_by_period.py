#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 11:23:21 2023

@author: green-machine
"""


from core.classes import Dataset
from core.constants import MAP_MC_CONNEL
from core.funcs import stockpile
from core.tools import transform_center_by_period


def main() -> None:
    # =============================================================================
    # Nominal National income Series: A032RC
    # =============================================================================

    SERIES_ID = SeriesID(
        'Национальный доход, млрд долл. США',
        Dataset.USA_MC_CONNELL
    )
    stockpile(SERIES_ID).truncate(before=1980).rename(
        columns=MAP_MC_CONNEL
    ).pipe(transform_center_by_period)

    SERIES_ID = [SeriesID('A032RC', URL.NIPA)]
    stockpile(SERIES_ID).pipe(transform_center_by_period)


if __name__ == '__main__':
    main()
