from pathlib import Path

import pandas as pd
from pandas import DataFrame


def read_employment() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    PATH = '/home/green-machine/Downloads'

    FILE_NAME = 'graduate_project_figures.xlsx'

    SHEET_NAME = 'Лист1'

    kwargs = {
        'io': Path(PATH).joinpath(FILE_NAME),
        'sheet_name': SHEET_NAME,
        'index_col': 0
    }
    return pd.read_excel(**kwargs)


if __name__ == '__main__':

    MAP_COLUMNS = dict(
        zip(
            ['Сельское хозяйство', 'Производство', 'Сфера услуг'],
            'Agriculture Manufacturing Services'.split()
        )
    )

    # =============================================================================
    # TODO: Read This File
    # =============================================================================
    # FILE_NAME = 'graduate_project_financial_plan_revised.xlsx'

    read_employment().transpose().rename(
        columns=MAP_COLUMNS
    ).rename_axis('period').plot(grid=True)
