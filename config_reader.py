import json


def read_config(config_file: str):
    with open(config_file, "r", encoding="utf8") as json_data_file:
        config = json.load(json_data_file)
    return config
