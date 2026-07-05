from src.barcode_generator import calculate_ean13_checksum
from src.barcode_generator import generate_ean13_barcode

import pytest


def test_calculate_ean13_checksum():
    first_12_digits = "296615006173"

    result = calculate_ean13_checksum(first_12_digits)

    assert result == "6"


def test_generate_ean13_barcode_returns_13_digits():
    barcode = generate_ean13_barcode("2601-BR:38")

    assert len(barcode) == 13
    assert barcode.isdigit()


def test_generate_ean13_barcode_returns_same_barcode_for_same_product_key():
    first_barcode = generate_ean13_barcode("2601-BR:38")
    second_barcode = generate_ean13_barcode("2601-BR:38")

    assert first_barcode == second_barcode


def test_generate_ean13_barcode_returns_different_barcode_for_different_product_key():
    first_barcode = generate_ean13_barcode("2601-BR:38")
    second_barcode = generate_ean13_barcode("2601-BR:39")

    assert first_barcode != second_barcode


def test_generate_ean13_barcode_uses_prefix():
    barcode = generate_ean13_barcode(
        "2601-BR:38",
        "29"
    )

    assert barcode.startswith("29")


def test_generate_ean13_barcode_rejects_long_prefix():
    with pytest.raises(ValueError):
        generate_ean13_barcode(
            "2601-BR:38",
            "123456789012"
        )


def test_generate_ean13_barcode_rejects_non_digit_prefix():
    with pytest.raises(ValueError):
        generate_ean13_barcode(
            "2601-BR:38",
            "ABC"
        )