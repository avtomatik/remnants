#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:24:57 2022

@author: Alexander Mikhailov
"""


# =============================================================================
# Stores Unused or Test Codes
# =============================================================================

import itertools
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from pandas.plotting import autocorrelation_plot

from remnants.src.lib.read import read_usa_bea_excel
from remnants.src.lib.stockpile import stockpile_usa_bea_excel_zip
from remnants.src.lib.transform import transform_sub_special, transform_sub_sum
from thesis.src.lib.stockpile import stockpile_usa_bea


def test_data_capital_combined_archived():
    """Data Test"""
    kwargs = {
        # =====================================================================
        # ONE ARCHIVE NAME
        # =====================================================================
        'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        # =====================================================================
        # 'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        # =====================================================================
        'wb_name': 'Section1ALL_Hist.xls',
    }
    SH_NAME_CONTROL, SH_NAME_TEST = '10105 Ann', '10505 Ann'
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1
        # =====================================================================
        'A191RC1',
    )
    # =====================================================================
    # ONE SHEET NAME
    # =====================================================================
    kwargs['sh_name'] = SH_NAME_CONTROL
    # =========================================================================
    # TODO: Extract Method
    # =========================================================================
    df_control = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )
    # =========================================================================
    # OTHER SHEET NAME
    # =========================================================================
    kwargs['sh_name'] = SH_NAME_TEST
    df_test = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )

    if df_control.equals(df_test):
        print(
            f"""
            Series {' & '.join(map(lambda _: f"<{_}>", SERIES_IDS))} @ Worksheet {SH_NAME_CONTROL} Equals Series {' & '.join(map(lambda _: f"<{_}>", SERIES_IDS))} @ Worksheet {SH_NAME_TEST} for Period 1929--1969
            """
        )
    else:
        print(
            f"""
            Data Varies from Worksheet {SH_NAME_CONTROL} to Worksheet {SH_NAME_TEST}
            """
        )

    kwargs = {
        # =====================================================================
        # OTHER ARCHIVE NAME
        # =====================================================================
        'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        # =====================================================================
        # 'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
        # =====================================================================
        'wb_name': 'Section1all_xls.xls',
    }
    # =====================================================================
    # ONE SHEET NAME
    # =====================================================================
    kwargs['sh_name'] = SH_NAME_CONTROL
    df_control = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )
    # =========================================================================
    # OTHER SHEET NAME
    # =========================================================================
    kwargs['sh_name'] = SH_NAME_TEST
    df_test = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )

    if df_control.equals(df_test):
        print(
            f"""
            Series {' & '.join(map(lambda _: f"<{_}>", SERIES_IDS))} @ Worksheet {SH_NAME_CONTROL} Equals Series {' & '.join(map(lambda _: f"<{_}>", SERIES_IDS))} @ Worksheet {SH_NAME_TEST} for Period 1969--2012
            """
        )
    else:
        print(
            f"""
            Data Varies from Worksheet {SH_NAME_CONTROL} to Worksheet {SH_NAME_TEST}
            """
        )


def test_data_capital_combined_archived():
    """Data Test"""
    # =========================================================================
    # Nominal Investment Series: A006RC1, 1929--1969
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    # =========================================================================
    # ARCHIVE_NAMES = (
    #     'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
    #     'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    # )
    # =========================================================================
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAME_CONTROL, SH_NAME_TEST = '10105 Ann', '10505 Ann'
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1
        # =====================================================================
        'A191RC1',
    )
    df_control = pd.concat(
        map(
            lambda _: read_usa_bea_excel(
                *_, SH_NAME_CONTROL).loc[:, SERIES_IDS],
            zip(ARCHIVE_NAMES, WB_NAMES)
        )
    ).drop_duplicates()
    df_test = pd.concat(
        map(
            lambda _: read_usa_bea_excel(*_, SH_NAME_TEST).loc[:, SERIES_IDS],
            zip(ARCHIVE_NAMES, WB_NAMES)
        )
    ).drop_duplicates()
    if df_control.equals(df_test):
        print(
            f"""
            Series {' & '.join(map(lambda _: f"<{_}>", SERIES_IDS))} @ Worksheet {SH_NAME_CONTROL} Equals Series {' & '.join(map(lambda _: f"<{_}>", SERIES_IDS))} @ Worksheet {SH_NAME_TEST}
            """
        )
    else:
        print(
            f"""
            Data Varies from Worksheet {SH_NAME_CONTROL} to Worksheet {SH_NAME_TEST}
            """
        )


def test_data_consistency_d(
    archive_name: str = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
) -> None:
    """
    Project IV: USA Macroeconomic & Fixed Assets Data Tests

    Parameters
    ----------
    archive_name : str, optional
        DESCRIPTION. The default is 'dataset_usa_bea-release-2019-12-19-Survey.zip'.

    Returns
    -------
    None
        DESCRIPTION.

    """
    # =========================================================================
    # Macroeconomic Data Tests
    # =========================================================================
    def get_kwargs_list(
        archive_name: str,
        wb_name: str,
        sheet_names: tuple[str],
        fields: tuple[str] = ('archive_name', 'wb_name', 'sh_name')
    ) -> list[dict]:
        return list(
            map(
                lambda _: dict(zip(fields, _)),
                itertools.product([archive_name], [wb_name], sheet_names)
            )
        )

    # =========================================================================
    # Tested: "A051RC" != "A052RC" + "A262RC"
    # =========================================================================
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10705-A', 'T11200-A', 'T10705-A')
    SERIES_IDS = ('A051RC', 'A052RC', 'A262RC')
    stockpile_usa_bea_excel_zip(
        get_kwargs_list(archive_name, WB_NAME, SH_NAMES), SERIES_IDS
    ).pipe(transform_sub_sum).iloc[:, [-1]].dropna(axis=0).pipe(autocorrelation_plot)

    # =========================================================================
    # Tested: "Government" = "Federal" + "State and local"
    # =========================================================================
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A')
    SERIES_IDS = ('A822RC', 'A823RC', 'A829RC')
    stockpile_usa_bea_excel_zip(
        get_kwargs_list(archive_name, WB_NAME, SH_NAMES), SERIES_IDS
    ).pipe(transform_sub_sum).iloc[:, [-1]].dropna(axis=0).pipe(autocorrelation_plot)

    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30100-A', 'T30200-A', 'T30300-A')
    SERIES_IDS = ('A955RC', 'A957RC', 'A991RC')
    stockpile_usa_bea_excel_zip(
        get_kwargs_list(archive_name, WB_NAME, SH_NAMES), SERIES_IDS
    ).pipe(transform_sub_sum).iloc[:, [-1]].dropna(axis=0).pipe(autocorrelation_plot)

    # =========================================================================
    # Tested: "Federal" = "National defense" + "Nondefense"
    # =========================================================================
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A')
    SERIES_IDS = ('A823RC', 'A824RC', 'A825RC')
    stockpile_usa_bea_excel_zip(
        get_kwargs_list(archive_name, WB_NAME, SH_NAMES), SERIES_IDS
    ).pipe(transform_sub_sum).iloc[:, [-1]].dropna(axis=0).pipe(autocorrelation_plot)

    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30200-A', 'T30905-A', 'T30905-A')
    SERIES_IDS = ('A957RC', 'A997RC', 'A542RC')
    stockpile_usa_bea_excel_zip(
        get_kwargs_list(archive_name, WB_NAME, SH_NAMES), SERIES_IDS
    ).pipe(transform_sub_sum).iloc[:, [-1]].dropna(axis=0).pipe(autocorrelation_plot)


def test_usa_bea_fixed_assets():
    # =========================================================================
    # Fixed Assets Data Tests
    # =========================================================================
    # =========================================================================
    # Tested: "k3n31gd1es00" = "k3n31gd1eq00" + "k3n31gd1ip00" + "k3n31gd1st00"
    # =========================================================================

    SERIES_ID = {
        'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    }
    SERIES_IDS = {
        'k3n31gd1eq00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1ip00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1st00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    }

    stockpile_usa_bea(SERIES_ID | SERIES_IDS).pipe(
        transform_sub_sum
    ).iloc[:, [-1]].dropna(axis=0).pipe(autocorrelation_plot)

    # =========================================================================
    # Comparison of "k3n31gd1es00" out of df_control with "k3n31gd1es00" out of df_test
    # =========================================================================
    test_usa_bea_sfat_series_ids().pipe(
        transform_sub_special
    ).iloc[:, [-1]].dropna(axis=0).pipe(autocorrelation_plot)

    # =========================================================================
    # TODO: Future Project: Test Ratio of Manufacturing Fixed Assets to Overall Fixed Assets
    # =========================================================================


def test_usa_bea_sfat_series_ids(
    path_src: str = '/media/green-machine/KINGSTON',
    file_name: str = 'dataset_usa_bea-nipa-selected.zip',
    source_id: str = 'Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization',
    series_id: str = 'k3n31gd1es000'
) -> DataFrame:
    """
    Earlier Version of 'k3n31gd1es000'
    """
    # =========================================================================
    # Fixed Assets Series, 1925--2016
    # Test if Ratio of Manufacturing Fixed Assets to Overall Fixed Assets
    # =========================================================================

    SERIES_ID = {
        'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    }
    SERIES_IDS = {
        'k3n31gd1eq00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1ip00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1st00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    }

    df_test = stockpile_usa_bea(SERIES_ID | SERIES_IDS)

    kwargs = {
        'filepath_or_buffer': Path(path_src).joinpath(file_name),
        'header': 0,
        'names': ('source_id', 'series_id', 'period', 'value'),
        'index_col': 2,
        'usecols': (0, 8, 9, 10),
    }
    df = pd.read_csv(**kwargs)
    # =========================================================================
    # Option I
    # =========================================================================
    df = df[df.iloc[:, 1] == series_id]

    df_control = DataFrame()
    for source_id in sorted(set(df.iloc[:, 0])):
        chunk = df[df.iloc[:, 0] == source_id].iloc[:, [2]]
        chunk.columns = [
            ''.join((source_id.split()[1].replace('.', '_'), series_id))
        ]
        df_control = pd.concat([df_control, chunk], axis=1, sort=True)

    # =========================================================================
    # # =========================================================================
    # # Option II
    # # =========================================================================
    # df_control = df[
    #     (df.loc[:, 'source_id'] == source_id) &
    #     (df.loc[:, 'series_id'] == series_id)
    # ].iloc[:, [-1]].rename(columns={"value": series_id})
    # =========================================================================

    return pd.concat([df_test, df_control], axis=1, sort=True)
