#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:24:57 2022

@author: Alexander Mikhailov
"""


# =============================================================================
# Stores Unused or Test Codes
# =============================================================================

import pandas as pd

from thesis.src.lib.read import read_usa_bea_excel
from thesis.src.lib.test import (test_subtract_a, test_subtract_b,
                                 test_usa_bea_sfat_series_ids,
                                 test_usa_bea_subtract)


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
        # =====================================================================
        # ONE SHEET NAME
        # =====================================================================
        'sh_name': '10105 Ann'
    }
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
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )
    # =========================================================================
    # OTHER SHEET NAME
    # =========================================================================
    kwargs['sh_name'] = '10505 Ann'
    df_test = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )

    if df_control.equals(df_test):
        print("Series 'A006RC1' & 'A191RC1' @ Worksheet '10105 Ann' Equals Series 'A006RC1' & 'A191RC1' @ Worksheet '10505 Ann' for Period 1929--1969")
    else:
        print("Data Varies from Worksheet '10105 Ann' to Worksheet '10505 Ann'")

    kwargs = {
        # =====================================================================
        # OTHER ARCHIVE NAME
        # =====================================================================
        'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        # =====================================================================
        # 'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
        # =====================================================================
        'wb_name': 'Section1all_xls.xls',
        # =====================================================================
        # ONE SHEET NAME
        # =====================================================================
        'sh_name': '10105 Ann'
    }
    df_control = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )
    # =========================================================================
    # OTHER SHEET NAME
    # =========================================================================
    kwargs['sh_name'] = '10505 Ann'
    df_test = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )

    if df_control.equals(df_test):
        print("Series 'A006RC1' & 'A191RC1' @ Worksheet '10105 Ann' Equals Series 'A006RC1' & 'A191RC1' @ Worksheet '10505 Ann' for Period 1969--2012")
    else:
        print("Data Varies from Worksheet '10105 Ann' to Worksheet '10505 Ann'")


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
        'A191RC1'
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
            """
            Series "A006RC1" & "A191RC1" @ Worksheet "10105 Ann" Equals Series "A006RC1" & "A191RC1" @ Worksheet "10505 Ann"
            """
        )
    else:
        print(
            """
            Data Varies from Worksheet "10105 Ann" to Worksheet "10505 Ann"
            """
        )


def test_data_consistency_d():
    """Project IV: USA Macroeconomic & Fixed Assets Data Tests"""
    # =========================================================================
    # Macroeconomic Data Tests
    # =========================================================================
    def _generate_kwargs_list(
            archive_name: str,
            wb_name: str,
            sheet_names: tuple[str],
            series_ids: tuple[str]
    ) -> list[dict]:
        return [
            {
                'archive_name': archive_name,
                'wb_name': wb_name,
                'sh_name': _sh,
                'series_id': series_id,
            } for _sh, series_id in zip(sheet_names, series_ids)
        ]

    # =========================================================================
    # Tested: "A051RC" != "A052RC" + "A262RC"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10705-A', 'T11200-A', 'T10705-A')
    SERIES_IDS = ('A051RC', 'A052RC', 'A262RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Tested: "Government" = "Federal" + "State and local"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A')
    SERIES_IDS = ('A822RC', 'A823RC', 'A829RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30100-A', 'T30200-A', 'T30300-A')
    SERIES_IDS = ('A955RC', 'A957RC', 'A991RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Tested: "Federal" = "National defense" + "Nondefense"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A')
    SERIES_IDS = ('A823RC', 'A824RC', 'A825RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30200-A', 'T30905-A', 'T30905-A')
    SERIES_IDS = ('A957RC', 'A997RC', 'A542RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Fixed Assets Data Tests
    # =========================================================================
    df = test_usa_bea_sfat_series_ids()

    test_subtract_a()
    # =========================================================================
    # Comparison of "k3n31gd1es00" out of df_control with "k3n31gd1es00" out of df_test
    # =========================================================================
    test_subtract_b(df)
    # =========================================================================
    # Future Project: Test Ratio of Manufacturing Fixed Assets to Overall Fixed Assets
    # =========================================================================
    # =========================================================================
    # TODO:
    # =========================================================================
    return
