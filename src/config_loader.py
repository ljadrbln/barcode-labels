import json
from pathlib import Path


CONFIG_DIR = Path("config")


def load_json_config(filepath):
    with open(filepath, "r") as file:
        result = json.load(file)

    return result


def load_column_mapping():
    filepath = CONFIG_DIR / "columns.json"

    result = load_json_config(filepath)

    return result


def load_app_config():
    filepath = CONFIG_DIR / "app.json"

    result = load_json_config(filepath)

    return result

def load_profile_config(profile_name):
    filepath = CONFIG_DIR / "profiles" / f"{profile_name}.json"

    result = load_json_config(filepath)

    return result