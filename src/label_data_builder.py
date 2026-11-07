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


def remove_brand_prefix(name, brand):
    name = str(name or "").strip()
    brand = str(brand or "").strip()

    if not brand or not name.casefold().startswith(brand.casefold()):
        return name

    remainder = name[len(brand):]

    if remainder and remainder[0] not in " -–—:|,":
        return name

    return remainder.lstrip(" -–—:|,") or name


def format_size(size):
    if not size:
        return ""

    return f"р. {size}"


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
    profile_config,
    barcode_value
):
    store_name = profile_config["store_name"]
    item_fields = profile_config["label_item_fields"]

    price_line = build_price_line(product)
    brand_line = build_brand_line(product)

    item_product = product

    if profile_config.get("layout") == "label_58x40_bags":
        item_product = product.copy()
        item_product["name"] = remove_brand_prefix(
            product.get("name"),
            brand_line
        )

    item_line = build_item_line(
        item_product,
        item_fields
    )

    result = {
        "store_line": store_name,
        "logo_path": profile_config.get("logo_path"),
        "brand_line": brand_line,
        "item_line": item_line,
        "price_line": price_line,
        "barcode_value": barcode_value,
    }

    return result
