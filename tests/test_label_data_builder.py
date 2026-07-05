from src.label_data_builder import build_brand_line
from src.label_data_builder import build_item_line
from src.label_data_builder import build_product_key
from src.label_data_builder import build_label_data


def test_build_product_key_for_shoes():
    product = {
        "article": "2xx1-BR-37",
        "size": "37"
    }

    key_fields = [
        "article",
        "size"
    ]

    result = build_product_key(
        product,
        key_fields
    )

    assert result == "2xx1-BR-37:37"


def test_build_product_key_for_bags():
    product = {
        "article": "BG-001"
    }

    key_fields = [
        "article"
    ]

    result = build_product_key(
        product,
        key_fields
    )

    assert result == "BG-001"


def test_build_brand_line():
    product = {
        "brand": "Giovanna"
    }

    result = build_brand_line(product)

    assert result == "Giovanna"


def test_build_brand_line_returns_empty_string_when_brand_is_missing():
    product = {}

    result = build_brand_line(product)

    assert result == ""


def test_build_item_line_for_shoes():
    product = {
        "article": "2xx1-BR-37",
        "name": "Giovanna 2601",
        "size": "37"
    }

    item_fields = [
        "article",
        "name",
        "size"
    ]

    result = build_item_line(
        product,
        item_fields
    )

    assert result == "2xx1-BR-37 Giovanna 2601 37 р."


def test_build_item_line_for_bags():
    product = {
        "article": "BG-001",
        "name": "Leather Bag"
    }

    item_fields = [
        "article",
        "name"
    ]

    result = build_item_line(
        product,
        item_fields
    )

    assert result == "BG-001 Leather Bag"


def test_build_label_data_for_shoes():
    product = {
        "brand": "Giovanna",
        "article": "2xx1-BR-37",
        "name": "Giovanna 2601",
        "size": "37",
        "price": 199,
        "currency": "USD"
    }

    profile_config = {
        "store_name": "Roga i Kopyta",
        "product_key_fields": [
            "article",
            "size"
        ],
        "label_item_fields": [
            "article",
            "name",
            "size"
        ]
    }

    result = build_label_data(
        product,
        profile_config
    )

    assert result["store_line"] == "Roga i Kopyta"
    assert result["brand_line"] == "Giovanna"
    assert result["item_line"] == "2xx1-BR-37 Giovanna 2601 37 р."
    assert result["price_line"] == "199.00 $"
    assert len(result["barcode_value"]) == 13
    assert result["barcode_value"].isdigit()
