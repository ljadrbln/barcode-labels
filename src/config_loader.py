from pathlib import Path
import json


CONFIG_DIR = Path("config")


def load_json_config(filename):
    filepath = CONFIG_DIR / filename

    with open(filepath, "r") as file:
        result = json.load(file)

    return result


def load_column_mapping():
    result = load_json_config(
        "columns.json"
    )

    return result


def load_app_config():
    result = load_json_config(
        "app.json"
    )

    return result