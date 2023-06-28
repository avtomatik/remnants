import os

import pandas as pd

# =============================================================================
# Separate Procedure
# =============================================================================


def some_incoherent_action(file_name, sheet_name):
    MAP = {
        'Unnamed0': 'Period',
        'СельскоеХозяйство': 'Agriculture',
        'Производство': 'Manufacturing',
        'СфераУслуг': 'Services',
    }

    df = pd.read_excel(file_name, sheet_name).transpose()
    FILE_NAME = 'temporary.xlsx'
    kwargs = {
        'excel_writer': FILE_NAME,
        'index': False
    }
    df.to_excel(**kwargs)
    FILE_NAME = 'temporary.xlsx'
    df = pd.read_excel(FILE_NAME, skiprows=1)
    df.columns = df.columns.str.title()
    df.columns = df.columns.to_series().replace(
        {'[ .:;@_]': ''},
        regex=True
    )
    df.rename(columns=MAP, inplace=True)
    df = df.set_index('Period')
    df = df.div(100)
    df.plot(grid=True)
    FILE_NAME = 'employment.csv'
    df.to_csv(FILE_NAME)
    FILE_NAME = 'temporary.xlsx'
    os.unlink(FILE_NAME)


# =============================================================================
# Separate Procedure
# =============================================================================
MAP = {
    'KTD02S01': 'Output',
    'KTD02S02': 'Persons Engaged',
    'KTD02S03': 'Output Per Person',
    'KTD02S04': 'Manhours',
    'KTD02S05': 'Output Per Manhour',
    'KTD02S06': 'Labor Input',
    'KTD02S07': 'Output per Unit of Labor Input',
}

COL_NUM = 0
df = pd.DataFrame()
df['VECTOR'] = df.iloc[:, COL_NUM].map(MAP)


# =============================================================================
# Separate Procedure
# =============================================================================

FILE_NAME = 'Graduate Project Figures.xlsx'
FILE_NAME = 'Graduate Project Financial Plan Revised.xlsx'
SHEET_NAME = 'Лист1'
PATH = 'C:\\Projects\\graduate_project'

os.chdir(PATH)

some_incoherent_action(FILE_NAME, SHEET_NAME)
