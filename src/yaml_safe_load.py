from pathlib import Path

import yaml
from core.config import DATA_DIR


def load_map(file_path: Path) -> dict:
    with file_path.open() as stream:
        return yaml.safe_load(stream)


def main():
    FILE_NAME = 'read_can.yaml'

    print(load_map(DATA_DIR.joinpath(FILE_NAME)))


if __name__ == '__main__':
    main()
