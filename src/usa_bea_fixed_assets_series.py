#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:30:16 2022

@author: Alexander Mikhailov
"""

# =============================================================================
# TODO: CHECK IT
# =============================================================================


SERIES_IDS = [
    # =============================================================================
    # Investment
    # =============================================================================
    'i3ptotl1es00',
    # =============================================================================
    # Investment
    # =============================================================================
    'icptotl1es00',
    # =============================================================================
    # Table 3.1ESI. Current-Cost Net Stock of Private Fixed Assets by Industry
    # =============================================================================
    'k1n31gd1es00',
    # =============================================================================
    # Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
    # =============================================================================
    'k1ntotl1si00',
    # =============================================================================
    # OK
    # =============================================================================
    'k3n31gd1es00',
    # =============================================================================
    # OK
    # =============================================================================
    'k3ntotl1si00',
    'k3ptotl1es00',
    'kcn31gd1es00',
    'mcn31gd1es00',
    'mcntotl1si00',
]


# =============================================================================
# US BEA Fixed Assets Series Tests
# =============================================================================
# =============================================================================
# Item 1.1
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 1.2
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 1.3
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 1.4: Don't Use
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 1.5
# =============================================================================
'kcptotl1es00'
# =============================================================================
# Item 2.1: Don't Use, Use Item 1.1 Instead
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 2.2: Don't Use, Use Item 1.2 Instead
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 2.3: Don't Use, Use Item 1.3 Instead
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 2.4
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 2.5: Don't Use, Use Item 1.5 Instead
# =============================================================================
'kcptotl1es00'
# =============================================================================
# Item 3.1: Don't Use, Use Item 1.1 Instead
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 3.2: Don't Use, Use Item 1.2 Instead
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 3.3: Don't Use, Use Item 1.3 Instead
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 3.4: Don't Use, Use Item 2.4 Instead
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 3.5: Don't Use, Use Item 1.5 Instead
# =============================================================================
'kcptotl1es00'
# =============================================================================
# Item 4.1: Don't Use
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 4.2: Don't Use
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 4.3: Don't Use
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 4.4: Don't Use
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 4.5: Don't Use
# =============================================================================
'kcptotl1es00'
# =============================================================================
# Item 5.1: Don't Use
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 5.2: Don't Use
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 5.3: Don't Use
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 5.4: Don't Use
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 5.5: Don't Use
# =============================================================================
'kcptotl1es00'
# =============================================================================
# Item 6.1: Don't Use, Use Item 1.1 Instead
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 6.2: Don't Use, Use Item 1.2 Instead
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 6.3: Don't Use, Use Item 1.3 Instead
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 6.4: Don't Use, Use Item 2.4 Instead
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 6.5: Don't Use, Use Item 1.5 Instead
# =============================================================================
'kcptotl1es00'
# =============================================================================
# Item 7.1: Don't Use
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 7.2: Don't Use
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 7.3: Don't Use
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 7.4: Don't Use
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 7.5: Don't Use
# =============================================================================
'kcptotl1es00'
# =============================================================================
# Item 8.1: Don't Use
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 8.2: Don't Use
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 8.3: Don't Use
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 8.4: Don't Use
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 8.5: Don't Use
# =============================================================================
'kcptotl1es00'
# =============================================================================
# Item 9.1: Don't Use
# =============================================================================
'i3ptotl1es00'
# =============================================================================
# Item 9.2: Don't Use
# =============================================================================
'icptotl1es00'
# =============================================================================
# Item 9.3: Don't Use
# =============================================================================
'k1ptotl1es00'
# =============================================================================
# Item 9.4: Don't Use
# =============================================================================
'k3ptotl1es00'
# =============================================================================
# Item 9.5: Don't Use
# =============================================================================
'kcptotl1es00'



collect_usa_general:
A = """
    # =========================================================================
    # Investment in Fixed Assets, Private, i3ptotl1es000, 1901--2016
    # =========================================================================
    # args = (
    #     'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section1ALL_xls.xls',
    #     '105 Ann',
    #     119,
    #     4,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section2ALL_xls.xls',
    #     '207 Ann',
    #     119,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section3ALL_xls.xls',
    #     '307ESI Ann',
    #     73,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section6ALL_xls.xls',
    #     '607 Ann',
    #     119,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Chain-Type Quantity Index for Investment in Fixed Assets, Private, icptotl1es000, 1901--2016
    # =========================================================================
    # args = (
    #     'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section1ALL_xls.xls',
    #     '106 Ann',
    #     119,
    #     4,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section2ALL_xls.xls',
    #     '208 Ann',
    #     119,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section3ALL_xls.xls',
    #     '308ESI Ann',
    #     73,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section6ALL_xls.xls',
    #     '608 Ann',
    #     119,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Current-Cost Net Stock of Fixed Assets, Private, k1ptotl1es000, 1925--2016
    # =========================================================================
    # args = (
    #     'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section1ALL_xls.xls',
    #     '101 Ann',
    #     95,
    #     4,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section2ALL_xls.xls',
    #     '201 Ann',
    #     95,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section3ALL_xls.xls',
    #     '301ESI Ann',
    #     73,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section6ALL_xls.xls',
    #     '601 Ann',
    #     95,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es000, 1925--2016
    # =========================================================================
    # args = (
    #     'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section2ALL_xls.xls',
    #     '203 Ann',
    #     95,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section3ALL_xls.xls',
    #     '303ESI Ann',
    #     73,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section6ALL_xls.xls',
    #     '603 Ann',
    #     95,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Chain-Type Quantity Indexes for Net Stock of Fixed Assets, Private, kcptotl1es000, 1925--2016
    # =========================================================================
    # args = (
    #     'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section1ALL_xls.xls',
    #     '102 Ann',
    #     95,
    #     4,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section2ALL_xls.xls',
    #     '202 Ann',
    #     95,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section3ALL_xls.xls',
    #     '302ESI Ann',
    #     73,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================
    # =========================================================================
    # Alternative:
    # =========================================================================
    # =========================================================================
    # args = (
    #     ''dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    #     'Section6ALL_xls.xls',
    #     '602 Ann',
    #     95,
    #     2,
    #     0
    # )
    # read_usa_bea_excel(*args)
    # =========================================================================

"""

