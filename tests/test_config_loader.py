import json

from src.config_loader import load_json_config
from src.config_loader import load_profile_config


def test_load_json_config(tmp_path):
    filepath = tmp_path / "config.json"

    data = {
        "store_name": "Roga i Kopyta"
    }

    with open(filepath, "w") as file:
        json.dump(data, file)

    result = load_json_config(filepath)

    assert result == data


def test_load_profile_config():
    result = load_profile_config("shoes")

    assert result["product_key_fields"] == [
        "article",
        "size"
    ]

    assert result["label_item_fields"] == [
        "article",
        "name",
        "size"
    ]