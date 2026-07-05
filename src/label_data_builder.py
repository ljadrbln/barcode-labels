from src.barcode_generator import generate_ean13_barcode


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
        value = product[field]

        if field == "size":
            value = format_size(value)

        values.append(str(value))

    result = " ".join(values)

    return result


def format_size(size):
    if not size:
        return ""

    return f"{size} р."


def build_brand_line(product):
    result = product.get("brand") or ""

    return result


def build_price_line(product):
    price = product["price"]
    currency = product.get("currency") or ""

    result = format_price(
        price,
        currency
    )

    return result


def format_price(
    price,
    currency
):
    amount = float(price)

    formatted_amount = f"{amount:,.2f}"
    formatted_amount = formatted_amount.replace(",", " ")

    formatted_currency = format_currency(
        currency
    )

    result = (
        f"{formatted_amount} "
        f"{formatted_currency}"
    ).strip()

    return result


def format_currency(currency):
    currency_map = {
        "USD": "$",
        "EUR": "€",
        "RUB": "₽",
        "UAH": "грн",
    }

    result = currency_map.get(
        currency,
        currency
    )

    return result


def build_label_data(
    product,
    profile_config
):
    store_name = profile_config["store_name"]
    key_fields = profile_config["product_key_fields"]
    item_fields = profile_config["label_item_fields"]

    price_line = build_price_line(product)
    brand_line = build_brand_line(product)

    item_line = build_item_line(
        product,
        item_fields
    )

    product_key = build_product_key(
        product,
        key_fields
    )

    barcode_value = generate_ean13_barcode(
        product_key
    )

    result = {
        "store_line": store_name,
        "brand_line": brand_line,
        "item_line": item_line,
        "price_line": price_line,
        "barcode_value": barcode_value,
    }

    return result