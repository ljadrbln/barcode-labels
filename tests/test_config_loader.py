import json

import src.config_loader as config_loader
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


def test_load_profile_config(tmp_path, monkeypatch):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    monkeypatch.setattr(config_loader, "CONFIG_DIR", tmp_path)

    example_config = {
        "product_key_fields": ["article", "size"],
        "label_item_fields": ["article", "color", "size"],
    }
    (profiles_dir / "shoes.example.json").write_text(
        json.dumps(example_config), encoding="utf-8"
    )

    assert load_profile_config("shoes") == example_config

    private_config = {
        "product_key_fields": ["article", "size"],
        "label_item_fields": ["article", "name", "size"],
    }
    (profiles_dir / "shoes.json").write_text(
        json.dumps(private_config), encoding="utf-8"
    )

    assert load_profile_config("shoes") == private_config
