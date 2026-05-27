import json
from pathlib import Path

from src.barcode_generator import generate_ean13_barcode


DATA_FILE = Path("data/barcodes.json")


def load_storage(data_file=DATA_FILE):
    if not data_file.exists():
        return {}

    with open(data_file, "r") as file:
        data = json.load(file)

    return data


def save_storage(data, data_file=DATA_FILE):
    data_file.parent.mkdir(parents=True, exist_ok=True)

    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)


def build_product_key(
    article,
    size
):
    result = f"{article}:{size}"

    return result


def get_or_create_barcode(article, size, data_file=DATA_FILE):
    storage = load_storage(data_file)
    product_key = build_product_key(article, size)

    if product_key in storage:
        return storage[product_key]

    barcode = generate_ean13_barcode()
    storage[product_key] = barcode
    save_storage(storage, data_file)

    return barcode