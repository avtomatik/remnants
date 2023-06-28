import os
from pathlib import Path, PosixPath
from zipfile import ZipFile

import pandas as pd


def convert_can_archive_csv(path_ctrl: PosixPath) -> str:
    return f"{Path(path_ctrl).stem.split('/')[-1].replace('-eng', '')}.csv"


def unlink_file_if_same(path_ctrl: PosixPath, path_test: PosixPath) -> None:

    filepath_or_buffer_c = path_ctrl
    filepath_or_buffer_t = path_test
    if pd.read_csv(filepath_or_buffer_c).equals(
        pd.read_csv(filepath_or_buffer_t)
    ):
        os.unlink(path_test)


def unlink_archive_if_same(path_ctrl: PosixPath, path_test: PosixPath) -> None:

    filepath_or_buffer_c = ZipFile(path_ctrl).open(
        convert_can_archive_csv(path_ctrl))
    filepath_or_buffer_t = ZipFile(path_test).open(
        convert_can_archive_csv(path_test))
    if pd.read_csv(filepath_or_buffer_c).equals(
        pd.read_csv(filepath_or_buffer_t)
    ):
        os.unlink(path_test)


if __name__ == '__main__':
    PATH_CTRL = '/home/green-machine/data_science/data/external'
    PATH_TEST = '/media/green-machine/904F-3DB1/data/external'

    for _ in range(10100008, 37100144):
        try:
            unlink_archive_if_same(
                Path(PATH_CTRL).joinpath(f'{_}-eng.zip'),
                Path(PATH_TEST).joinpath(f'{_}-eng.zip')
            )
        except FileNotFoundError:
            pass
