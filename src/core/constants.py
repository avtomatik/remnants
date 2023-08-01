
DATED_DATED_ARCHIVE_FILE_NAMES_UTILISED = (
    'dataset USA BEA 2013-12-02.csv',
    'dataset_usa_bea-nipa-2015-05-01.zip',
    'dataset USA BEA NipaDataA.txt',
    'dataset_usa_bea-nipa-2017-08-23-sfat.zip',
    'dataset USA BEA.csv',
    'dataset USA Census HSUS 1949 Series D062-D076 & J001-J012.csv',
    'dataset USA Census HSUS 1949 Series J149-J151.txt',
    'dataset USA Census HSUS 1949 Series L.csv',
    'dataset USA Census HSUS 1975 Series D127-D141 & P058-P067.csv',
    'dataset USA Census HSUS 1975 Series E.csv',
    'dataset USA Census HSUS 1975 Series K5.csv',
    'dataset USA Census HSUS 1975 Series P107-P176 & P231-P317 Refined.csv',
    'dataset USA Census HSUS 1975 Series P107-P176 & P231-P317.csv',
    'dataset USA Reference RU Brown M. 0597_088.csv',
)


DATED_ARCHIVE_FILE_NAMES_UTILISED = (
    'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
    'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
    'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip',
    'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    'dataset_usa_0025_p_r.txt',
    'dataset_usa_bea-GDPDEF.xls',
    'dataset_usa_davis-j-h-ip-total.xls',
    'dataset_usa_frb_g17_all_annual_2013_06_23.csv',
    'dataset_usa_frb_us3_ip_2018_09_02.csv',
    'dataset_usa_reference_ru_kurenkov_yu_v.csv',
)


# =============================================================================
# <plot_lab_prod_polynomial.py>
# =============================================================================
PARAMS = [
    [1.015657368157, 0.248747690395, 0., 0., 0.],
    [0.861832058762, 0.170010139109, 0., 0., 0.],
    [0.756806427251, 0.296618544244, -0.03675576822, 0., 0.],
    [0.488648702675, 0.795394788941, -0.324632165354, 0.052482721778, 0.],
    [
        -6.345929988031, 17.654255478448, -15.269178198223, 5.700049477943, -0.768094123014
    ]
]


URL_FIXED_ASSETS = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
SERIES_IDS_EA = {
    # =========================================================================
    # Not Used: Fixed Assets: Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
    # =========================================================================
    'k3n31gd1es00': URL_FIXED_ASSETS,
    # =========================================================================
    # Not Used: Fixed Assets: Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
    # =========================================================================
    'k3ntotl1si00': URL_FIXED_ASSETS,
    # =========================================================================
    # Not Used: Table 4.5. Chain-Type Quantity Indexes for Depreciation of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
    # =========================================================================
    'mcn31gd1es00': URL_FIXED_ASSETS,
    # =========================================================================
    # Not Used: Table 2.5. Chain-Type Quantity Indexes for Depreciation of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
    # =========================================================================
    'mcntotl1si00': URL_FIXED_ASSETS
} | {
    # =========================================================================
    # Fixed Assets: Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
    # =========================================================================
    'k1n31gd1es00': URL_FIXED_ASSETS,
    # =========================================================================
    # Fixed Assets: Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
    # =========================================================================
    'kcn31gd1es00': URL_FIXED_ASSETS
}


SERIES_IDS_CD = {
    # =========================================================================
    # Annual Increase in Terms of Cost Price (1)
    # =========================================================================
    'CDT2S1': 'dataset_usa_cobb-douglas.zip',
    # =========================================================================
    # Annual Increase in Terms of 1880 dollars (3)
    # =========================================================================
    'CDT2S3': 'dataset_usa_cobb-douglas.zip'
}


SERIES_IDS_PRCH = {
    'P0107': 'dataset_uscb.zip',
    'P0110': 'dataset_uscb.zip',
}


ARCHIVE_NAME = 'dataset_uscb.zip'

SERIES_IDS = [
    'E0007',
    'E0023',
    'E0040',
    'E0068',
    # =========================================================================
    # Warren & Pearson
    # =========================================================================
    'L0002' or 'E0052',
    'L0015',
] + [
    # =========================================================================
    # Less Preferrable
    # =========================================================================
    'E0008',
    # =========================================================================
    # Snyder-Tucker
    # =========================================================================
    'L0001',
] + [
    # =========================================================================
    # Least Preferrable
    # =========================================================================
    'E0009',
    'L0037',
]

SERIES_IDS_CB = dict.fromkeys(SERIES_IDS, ARCHIVE_NAME)


URL_NIPA_DATA_A = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
SERIES_IDS_LAB = {
    # =========================================================================
    # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
    # =========================================================================
    # =========================================================================
    # 1929--1948
    # =========================================================================
    'H4313C': URL_NIPA_DATA_A,
    # =========================================================================
    # 1948--1987
    # =========================================================================
    'J4313C': URL_NIPA_DATA_A,
    # =========================================================================
    # 1987--2000
    # =========================================================================
    'A4313C': URL_NIPA_DATA_A,
    # =========================================================================
    # 1998--2020
    # =========================================================================
    'N4313C': URL_NIPA_DATA_A,
}


SERIES_IDS_COL = [
    # =========================================================================
    # Cost-of-Living Indexes
    # =========================================================================
    # =========================================================================
    # Federal Reserve Bank, 1913=100
    # =========================================================================
    'E0183' or 'L0036',
    # =========================================================================
    # Burgess, 1913=100
    # =========================================================================
    'E0184' or 'L0038',
    # =========================================================================
    # Douglas, 1890-99=100
    # =========================================================================
    'E0185' or 'L0039',
    # =========================================================================
    # Rees, 1914=100
    # =========================================================================
    'E0186'
]  # No


MAP_KENDRICK = {
    'KTD02S01': 'Output',
    'KTD02S02': 'Persons Engaged',
    'KTD02S03': 'Output Per Person',
    'KTD02S04': 'Manhours',
    'KTD02S05': 'Output Per Manhour',
    'KTD02S06': 'Labor Input',
    'KTD02S07': 'Output per Unit of Labor Input',
}
