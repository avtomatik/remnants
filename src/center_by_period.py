#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 11:23:21 2023

@author: green-machine
"""


from lib.tools import transform_center_by_period

from thesis.src.lib.collect import stockpile_usa_bea, stockpile_usa_mcconnel


def main() -> None:
    # =============================================================================
    # Nominal National income Series: A032RC
    # =============================================================================

    SERIES_ID = {
        'Национальный доход, млрд долл. США': 'dataset_usa_mc_connell_brue.zip'
    }
    stockpile_usa_mcconnel(SERIES_ID).pipe(transform_center_by_period)

    SERIES_ID = {
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    stockpile_usa_bea(SERIES_ID).pipe(transform_center_by_period)


if __name__ == '__main__':
    main()
