from typing import Any

import pandas as pd
from core.classes import URL, SeriesID
from core.config import DATA_DIR
from core.constants import SERIES_IDS_LAB
from core.funcs import get_pre_kwargs

from thesis.src.lib.combine import combine_usa_money
from thesis.src.lib.pull import pull_by_series_id
from thesis.src.lib.read import read_source, read_usa_frb_g17, read_usa_fred
from thesis.src.lib.stockpile import stockpile
from thesis.src.lib.transform import transform_mean


def combine_usa_xlsm() -> pd.DataFrame:
    FILE_NAME = 'dataset_usa_0025_p_r.txt'

    SERIES_IDS = [
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =====================================================================
        'A191RX',
        # =====================================================================
        # Nominal National income Series: A032RC, 1929--2021
        # =====================================================================
        'A032RC',
    ]
    return pd.concat(
        [
            stockpile(enlist_series_ids(SERIES_IDS, URL.NIPA)),
            pd.read_csv(**get_pre_kwargs(FILE_NAME)),
        ],
        axis=1
    )


def combine_usa_general() -> pd.DataFrame:
    """
    Returns
    -------
    pd.DataFrame
        DESCRIPTION.
    """
    FILE_NAME = 'dataset_usa_0025_p_r.txt'

    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        SeriesID('A006RC', URL.NIPA),
        # =====================================================================
        # Implicit Price Deflator Series: A006RD
        # =====================================================================
        SeriesID('A006RD', URL.NIPA),
        # =====================================================================
        # Gross private domestic investment -- Nonresidential: A008RC
        # =====================================================================
        SeriesID('A008RC', URL.NIPA),
        # =====================================================================
        # Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD
        # =====================================================================
        SeriesID('A008RD', URL.NIPA),
        # =====================================================================
        # Nominal National income Series: A032RC
        # =====================================================================
        SeriesID('A032RC', URL.NIPA),
        # =====================================================================
        # Gross Domestic Product, 2012=100: A191RA
        # =====================================================================
        SeriesID('A191RA', URL.NIPA),
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        SeriesID('A191RC', URL.NIPA),
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        SeriesID('A191RX', URL.NIPA),
        # =====================================================================
        # Gross Domestic Investment, W170RC
        # =====================================================================
        SeriesID('W170RC', URL.NIPA),
        # =====================================================================
        # Gross Domestic Investment, W170RX
        # =====================================================================
        SeriesID('W170RX', URL.NIPA),
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00
        # =====================================================================
        SeriesID('k1n31gd1es00', URL.FIAS),
        # =====================================================================
        # Investment in Fixed Assets and Consumer Durable Goods, Private
        # =====================================================================
        SeriesID('i3ptotl1es00', URL.FIAS),
        # =====================================================================
        # Chain-Type Quantity Indexes for Investment in Fixed Assets and Consumer Durable Goods, Private
        # =====================================================================
        SeriesID('icptotl1es00', URL.FIAS),
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es00
        # =====================================================================
        SeriesID('k3ptotl1es00', URL.FIAS),
    }
    return pd.concat(
        [
            pd.concat(
                [
                    pd.concat(
                        [
                            read_source(SERIES_IDS[series_id]).pipe(
                                pull_by_series_id, series_id)
                            for series_id in tuple(SERIES_IDS)[:8]
                        ],
                        axis=1
                    ),
                    stockpile(SERIES_IDS_LAB).pipe(
                        transform_mean, name='bea_labor_mfg'
                    ),
                    pd.concat(
                        [
                            read_source(SERIES_IDS[series_id]).pipe(
                                pull_by_series_id, series_id)
                            for series_id in tuple(SERIES_IDS)[8:]
                        ],
                        axis=1
                    ),
                ],
                axis=1,
                sort=True
            ),
            combine_usa_money(),
            pd.read_csv(**get_pre_kwargs(FILE_NAME)),
        ],
        axis=1
    )


def combine_usa_bea_gdp() -> pd.DataFrame:
    """
    USA BEA Gross Domestic Product
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================
    """

    SERIES_IDS = {
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        SeriesID('A191RC', URL.NIPA),
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        SeriesID('A191RX', URL.NIPA),
    }
    return stockpile(SERIES_IDS)


def transform_def(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cumulative Price Index

    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================.

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Product Deflator
        ================== =================================.

    """
    df['deflator_gdp'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    return df.iloc[:, [-1]]


def combine_bea_def_from_file() -> pd.DataFrame:
    """
    Returns Cumulative Price Index for Some Base Year from Certain Type BEA Deflator File
    -------
    pd.DataFrame
        DESCRIPTION.
    """

    df = pd.read_excel(**get_kwargs_usa_bea_def())
    return df.groupby(df.index.year).agg('prod').pow(1/4)


def get_kwargs_usa_bea_def() -> dict[str, Any]:
    FILE_NAME = 'dataset_usa_bea-GDPDEF.xls'
    return {
        "io": DATA_DIR.joinpath(FILE_NAME),
        "names": ('period', 'deflator_gdp'),
        "index_col": 0,
        "skiprows": 15,
        "parse_dates": True
    }


def combine_usa_investment_capital() -> pd.DataFrame:
    SERIES_ID = 'PPIACO'

    SERIES_IDS = [
        SeriesID('A006RC', URL.NIPA),
        SeriesID('A032RC', URL.NIPA),
    ] + [
        SeriesID('k1n31gd1es00', URL.FIAS)
    ]
    return pd.concat(
        [
            # =================================================================
            # Producer Price Index
            # =================================================================
            read_usa_fred(SERIES_ID),
            stockpile(SERIES_IDS)
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def combine_usa_macroeconomics() -> pd.DataFrame:
    """Data Fetch"""
    SERIES_ID = 'CAPUTL.B50001.A'

    SERIES_IDS = {
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        SeriesID('A191RC', URL.NIPA),
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX, 1929--2021, 2012=100
        # =====================================================================
        SeriesID('A191RX', URL.NIPA),
        # =====================================================================
        # Deflator Gross Domestic Product, A191RD, 1929--2021, 2012=100
        # =====================================================================
        SeriesID('A191RD', URL.NIPA),
        # =====================================================================
        # National Income: A032RC, 1929--2021
        # =====================================================================
        SeriesID('A032RC', URL.NIPA),
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1951--2021
        # =====================================================================
        SeriesID('k1n31gd1es00', URL.FIAS),
        # =====================================================================
        # Fixed Assets Series: k1ntotl1si00, 1925--2020
        # =====================================================================
        SeriesID('k1ntotl1si00', URL.FIAS),
        # =====================================================================
        # Fixed Assets Series: k3ntotl1si00, 1925--2020
        # =====================================================================
        SeriesID('k3ntotl1si00', URL.FIAS),
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1925--2020
        # =====================================================================
        SeriesID('k1n31gd1es00', URL.FIAS),
        # =====================================================================
        # Fixed Assets Series: k3n31gd1es00, 1925--2020
        # =====================================================================
        SeriesID('k3n31gd1es00', URL.FIAS),
    }
    return pd.concat(
        [
            stockpile(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0),
        ],
        axis=1,
        sort=True
    )


def combine_capital_combined_archived() -> pd.DataFrame:

    SERIES_IDS = [
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        SeriesID('A006RC', URL.NIPA),
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        SeriesID('A191RC', URL.NIPA),
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX1, 1929--2012
        # =====================================================================
        SeriesID('A191RX', URL.NIPA),
        # =====================================================================
        # Fixed Assets Series
        # =====================================================================
        SeriesID('k1n31gd1es00', URL.FIAS)
    ]
    return pd.concat(
        [
            stockpile(SERIES_IDS),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, ['CAPUTL.B50001.A']].dropna(axis=0),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Labor Series: A4601C
            # =================================================================
            stockpile([SeriesID('A4601C', URL.NIPA)])
        ],
        axis=1,
        sort=True
    )


def combine_usa_investment_turnover_bls() -> pd.DataFrame:
    SERIES_ID = 'PPIACO'

    SERIES_IDS = [
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        SeriesID('A006RC', URL.NIPA),
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        SeriesID('A191RX', URL.NIPA),
    ] + [
        SeriesID('k1n31gd1es00', URL.FIAS)
    ]
    df = pd.concat(
        [
            # =================================================================
            # Producer Price Index
            # =================================================================
            read_usa_fred(SERIES_ID),
            stockpile(SERIES_IDS),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    # =========================================================================
    # Deflator, 2012=100
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].add(1).cumprod()
    df.iloc[:, -1] = df.iloc[:, -1].rdiv(df.loc[2012, df.columns[-1]])
    # =========================================================================
    # Investment, 2012=100
    # =========================================================================
    df['investment'] = df.iloc[:, 1].mul(df.iloc[:, -1])
    # =========================================================================
    # Capital, 2012=100
    # =========================================================================
    df['capital'] = df.iloc[:, 3].mul(df.iloc[:, -1])
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    df['ratio_mu'] = df.iloc[:, -2].mul(1).sub(df.iloc[:, -1].shift(-1)).div(
        df.iloc[:, -1]).add(1)
    return (
        df.loc[:, ['investment', 'A191RX',
                   'capital', 'ratio_mu']].dropna(axis=0),
        df.loc[:, ['ratio_mu']].dropna(axis=0),
    )


def combine_combined_archived() -> pd.DataFrame:
    """Version: 02 December 2013"""

    SERIES_IDS = {
        SeriesID('A006RC', URL.NIPA),
        SeriesID('A006RD', URL.NIPA),
        SeriesID('A008RC', URL.NIPA),
        SeriesID('A008RD', URL.NIPA),
        SeriesID('A032RC', URL.NIPA),
        SeriesID('A191RA', URL.NIPA),
        SeriesID('A191RC', URL.NIPA),
        SeriesID('A191RX', URL.NIPA),
        SeriesID('W170RC', URL.NIPA),
        SeriesID('W170RX', URL.NIPA),
    }
    # =========================================================================
    # US BEA Fixed Assets Series Tests
    # =========================================================================

    SERIES_IDS_SFAT = [
        SeriesID('k1n31gd1es00', URL.FIAS)
    ] + [
        # =====================================================================
        # Investment in Fixed Assets, Private, i3ptotl1es00, 1901--2016
        # =====================================================================
        SeriesID('i3ptotl1es00', URL.FIAS),
        # =====================================================================
        # Chain-Type Quantity Index for Investment in Fixed Assets, Private, icptotl1es00, 1901--2016
        # =====================================================================
        SeriesID('icptotl1es00', URL.FIAS),
        # =====================================================================
        # Current-Cost Net Stock of Fixed Assets, Private, k1ptotl1es00, 1925--2016
        # =====================================================================
        SeriesID('k1ptotl1es00', URL.FIAS),
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es00, 1925--2016
        # =====================================================================
        SeriesID('k3ptotl1es00', URL.FIAS),
        # =====================================================================
        # Chain-Type Quantity Indexes for Net Stock of Fixed Assets, Private, kcptotl1es00, 1925--2016
        # =====================================================================
        SeriesID('kcptotl1es00', URL.FIAS),
    ]
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    return pd.concat(
        [
            stockpile(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            stockpile(SERIES_IDS_SFAT),
            combine_usa_money(),
            pd.read_csv(FILE_NAME, index_col=0),
        ],
        axis=1,
        sort=True
    )


def combine_local() -> pd.DataFrame:

    SERIES_IDS = [
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        SeriesID('A006RC', URL.NIPA),
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        SeriesID('A191RC', URL.NIPA),
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        SeriesID('A191RX', URL.NIPA),
    ] + [
        SeriesID('k1n31gd1es00', URL.FIAS)
    ]
    return pd.concat(
        [
            stockpile(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            read_usa_frb_g17().loc[:, ['CAPUTL.B50001.A']].dropna(axis=0),
        ],
        axis=1,
        sort=True
    )
