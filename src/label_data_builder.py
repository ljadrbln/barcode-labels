from src.barcode_storage import get_or_create_barcode


def build_product_key(product, key_fields):
    values = []

    for field in key_fields:
        value = str(product[field])
        values.append(value)

    result = ":".join(values)

    return result


def build_item_line(product, item_fields):
    values = []

    for field in item_fields:
        value = str(product[field])
        values.append(value)

    result = " ".join(values)

    return result


def build_label_data(
    product,
    profile_config,
    data_file=None
):
    store_name = profile_config["store_name"]
    key_fields = profile_config["product_key_fields"]
    item_fields = profile_config["label_item_fields"]

    price = str(product["price"])
    currency = product.get("currency") or ""

    price_line = f"{price} {currency}".strip()

    item_line = build_item_line(
        product,
        item_fields
    )

    product_key = build_product_key(
        product,
        key_fields
    )

    if data_file is None:
        barcode_value = get_or_create_barcode(product_key)
    else:
        barcode_value = get_or_create_barcode(product_key, data_file)

    result = {
        "store_line": store_name,
        "item_line": item_line,
        "price_line": price_line,
        "barcode_value": barcode_value,
    }

    return result