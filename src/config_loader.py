import json


def load_column_mapping():
    with open("config/columns.json", "r") as file:
        result = json.load(file)

    return result

def load_app_config():
    with open("config/app.json", "r") as file:
        result = json.load(file)

    return result