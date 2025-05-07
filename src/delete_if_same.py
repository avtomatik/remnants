import zipfile
from pathlib import Path

import pandas as pd
from core.config import DATA_DIR


def convert_can_archive_csv(path_ctrl: Path) -> str:
    return f"{Path(path_ctrl).stem.split('/')[-1].replace('-eng', '')}.csv"


def unlink_file_if_same(path_ctrl: Path, path_test: Path) -> None:

    filepath_or_buffer_c = path_ctrl
    filepath_or_buffer_t = path_test
    if pd.read_csv(filepath_or_buffer_c).equals(
        pd.read_csv(filepath_or_buffer_t)
    ):
        path_test.unlink()


def unlink_archive_if_same(path_ctrl: Path, path_test: Path) -> None:

    filepath_or_buffer_c = zipfile.ZipFile(path_ctrl).open(
        convert_can_archive_csv(path_ctrl))
    filepath_or_buffer_t = zipfile.ZipFile(path_test).open(
        convert_can_archive_csv(path_test))
    if pd.read_csv(filepath_or_buffer_c).equals(
        pd.read_csv(filepath_or_buffer_t)
    ):
        path_test.unlink()


if __name__ == '__main__':
    for _ in range(10100008, 37100144):
        try:
            unlink_archive_if_same(
                DATA_DIR.joinpath(f'{_}-eng.zip'),
                DATA_DIR.joinpath(f'{_}-eng.zip')
            )
        except FileNotFoundError:
            pass
