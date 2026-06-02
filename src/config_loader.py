import json
from pathlib import Path


CONFIG_DIR = Path("config")


def load_json_config(filepath):
    with open(filepath, "r") as file:
        result = json.load(file)

    return result


def load_profile_config(profile_name):
    filepath = CONFIG_DIR / "profiles" / f"{profile_name}.json"
    example_filepath = CONFIG_DIR / "profiles" / f"{profile_name}.example.json"

    if not filepath.exists():
        filepath = example_filepath

    if not filepath.exists():
        message = (
            f"Profile config not found: {filepath}\n"
            f"Create config/profiles/{profile_name}.json "
            f"or config/profiles/{profile_name}.example.json."
        )

        raise FileNotFoundError(message)

    result = load_json_config(filepath)

    return result