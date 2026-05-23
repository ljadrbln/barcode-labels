import json
from pathlib import Path

from src.barcode_generator import generate_ean13_barcode


DATA_FILE = Path("data/barcodes.json")


def load_storage():
    if not DATA_FILE.exists():
        return {}

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    return data


def save_storage(data):
    DATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(DATA_FILE, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )


def build_product_key(
    article,
    size
):
    result = f"{article}:{size}"

    return result


def get_or_create_barcode(
    article,
    size
):
    storage = load_storage()

    product_key = build_product_key(
        article,
        size
    )

    if product_key in storage:
        result = storage[product_key]

        return result

    barcode = generate_ean13_barcode()

    storage[product_key] = barcode

    save_storage(storage)

    return barcode