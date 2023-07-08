import os
import shutil
import datetime
import time
from config_reader import read_config

CONFIG = read_config("config.json")
SOURCE = CONFIG["source_path"]
BASE = CONFIG["base"]


def can_move_file(file_name: str, destination: str) -> bool:
    is_dir = os.path.isdir(destination)
    has_file = os.path.isfile(os.path.join(destination, file_name))

    return is_dir and not has_file


def add_date(destination: str) -> str:
    date = datetime.datetime.now().strftime("%Y-%m")
    return os.path.join(destination, date)


def create_dirs(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def move_files(extension, destination) -> None:
    destination_path = os.path.join(BASE, destination)
    destination_with_date = add_date(destination_path)

    files_in_source = [
        os.path.join(SOURCE, f)
        for f in os.listdir(SOURCE)
        if f.endswith(f".{extension}")
    ]

    print("Files to move: ", files_in_source)

    if not files_in_source:
        return
    create_dirs(destination_with_date)

    files_to_move = [
        f
        for f in files_in_source
        if can_move_file(os.path.basename(f), destination_with_date)
    ]
    for file in files_to_move:
        try:
            shutil.move(file, destination_with_date)
        except PermissionError:
            pass


def move_to_destination(destination: str, extensions: list[str]) -> None:
    for extension in extensions:
        move_files(extension, destination)


def main() -> None:
    print("Source: ", SOURCE)
    print("Base: ", BASE)
    while True:
        for destination, extensions in CONFIG["paths"].items():
            move_to_destination(destination, extensions)

        time.sleep(1)


if __name__ == "__main__":
    main()
