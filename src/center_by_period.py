#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 11:23:21 2023

@author: green-machine
"""


from core.classes import Token
from core.constants import MAP_MC_CONNEL
from core.funcs import stockpile_usa_bea, stockpile_usa_hist
from core.tools import transform_center_by_period


def main() -> None:
    # =============================================================================
    # Nominal National income Series: A032RC
    # =============================================================================

    SERIES_ID = {
        'Национальный доход, млрд долл. США': Token.USA_MC_CONNELL
    }
    stockpile_usa_hist(SERIES_ID).truncate(before=1980).rename(
        columns=MAP_MC_CONNEL
    ).pipe(transform_center_by_period)

    SERIES_ID = {
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    stockpile_usa_bea(SERIES_ID).pipe(transform_center_by_period)


if __name__ == '__main__':
    main()
