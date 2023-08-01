from typing import Any

import pandas as pd


def get_kwargs(file_name) -> dict[str, Any]:
    return {
        'filepath_or_buffer': file_name,
        'sep': '\t'
    }


matchers = ['stat_can_file_']
file_names = sorted(get_file_names(matchers=matchers))


FILE_NAME = 'stat_can_file.csv'
kwargs = {
    'excel_writer': FILE_NAME,
    'index': False
}
pd.concat(
    map(lambda _: pd.read_csv(**get_kwargs(_)), file_names)
).to_csv(**kwargs)
