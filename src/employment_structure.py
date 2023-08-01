from pathlib import Path
from typing import Any

import pandas as pd


def get_kwargs() -> dict[str, Any]:

    PATH = '/home/green-machine/Downloads'

    FILE_NAME = 'graduate_project_figures.xlsx'

    SHEET_NAME = 'Лист1'

    return {
        'io': Path(PATH).joinpath(FILE_NAME),
        'sheet_name': SHEET_NAME,
        'index_col': 0
    }


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

    pd.read_excel(**get_kwargs()).transpose().rename(
        columns=MAP_COLUMNS
    ).rename_axis('period').plot(grid=True)
