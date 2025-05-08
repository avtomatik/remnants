#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 10:33:07 2023

@author: green-machine
"""


import pandas as pd
from core.combine import combine_bea_def_from_file, combine_usa_bea_def
from core.config import DATA_DIR

from thesis.src.lib.tools import price_direct, price_inverse_double

# =============================================================================
# TODO: Eliminate XLSM
# =============================================================================

def main() -> None:
    FILE_NAME = 'pricesDirect.xlsm' or 'archiveProjectPricesConverterDirect.xlsm'
    kwargs = {
        'io': DATA_DIR.joinpath(FILE_NAME),
        'index_col': 0
    }
    pd.read_excel(**kwargs).pipe(price_direct, year_base=2005)

    file_name = 'dataset USA.csv'
    pd.read_csv(file_name).pipe(price_inverse_double, 7, 8)

    FILE_NAME = 'pricesDatasetBeaGdp.xlsm' or 'archiveProjectPricesConverterGDP.xlsm'
    kwargs = {
        'io': DATA_DIR.joinpath(FILE_NAME),
        # =====================================================================
        # Where A191RC & A191RX
        # =====================================================================
        'index_col': 0
    }
    pd.read_excel(**kwargs).pipe(price_inverse_double, 0, 1)

    FILE_NAME = 'pricesInverse.xlsm' or 'archiveProjectPricesConverterReverse.xlsm'
    kwargs = {
        'io': DATA_DIR.joinpath(FILE_NAME),
        # =====================================================================
        # Where A191RX/A191RC
        # =====================================================================
        'index_col': 0
    }
    pd.read_excel(**kwargs).pct_change().dropna(axis=0)

    # =========================================================================
    # A006RD@'dataset USA CobbDouglas Modern Dataset.csv'
    # =========================================================================
    combine_usa_bea_def().pct_change().dropna(axis=0)
    # =========================================================================
    # A191RD3@'dataset USA CobbDouglas Modern Dataset.csv'
    # =========================================================================
    combine_bea_def_from_file().pct_change().dropna(axis=0)


if __name__ == '__main__':
    main()
