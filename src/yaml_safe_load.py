from pathlib import Path

import yaml


def load_map(path_src: str, file_name: str) -> dict:
    with open(Path(path_src).joinpath(file_name)) as stream:
        return yaml.safe_load(stream)


def main():
    PATH_SRC = '../cfg'
    FILE_NAME = 'read_can.yaml'

    print(load_map(PATH_SRC, FILE_NAME))


if __name__ == '__main__':
    main()
