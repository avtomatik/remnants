#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 10:33:07 2023

@author: green-machine
"""


import pandas as pd

from remnants.src.lib.combine import combine_usa_bea_def
from thesis.src.lib.tools import (price_direct, price_inverse,
                                  price_inverse_double)


def main() -> None:
    kwargs = {
        'io': 'pricesDirect.xlsm',
        'index_col': 0
    }
    pd.read_excel(**kwargs).pipe(price_direct, year_base=2005)
    kwargs = {
        'io': 'pricesDatasetBeaGdp.xlsm',
        'index_col': 0
    }
    pd.read_excel(**kwargs).pipe(price_inverse_double)
    kwargs = {
        'io': 'pricesInverse.xlsm',
        'index_col': 0
    }
    pd.read_excel(**kwargs).pipe(price_inverse)
    # =========================================================================
    # A191RD3@dataset USA CobbDouglas Modern Dataset.csv
    # =========================================================================
    combine_usa_bea_def().pct_change()


if __name__ == '__main__':
    main()
