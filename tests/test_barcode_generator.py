from src.barcode_generator import calculate_ean13_checksum
from src.barcode_generator import generate_ean13_barcode

import pytest


def test_calculate_ean13_checksum():
    first_12_digits = "296615006173"

    result = calculate_ean13_checksum(first_12_digits)

    assert result == "6"


def test_generate_ean13_barcode_returns_13_digits():
    barcode = generate_ean13_barcode(1)

    assert len(barcode) == 13
    assert barcode.isdigit()


def test_generate_ean13_barcode_returns_different_barcode_for_each_sequence():
    first_barcode = generate_ean13_barcode(1)
    second_barcode = generate_ean13_barcode(2)

    assert first_barcode != second_barcode


def test_generate_ean13_barcode_uses_prefix():
    barcode = generate_ean13_barcode(
        1,
        "29"
    )

    assert barcode.startswith("29")


def test_generate_ean13_barcode_rejects_long_prefix():
    with pytest.raises(ValueError):
        generate_ean13_barcode(
            1,
            "123456789012"
        )


def test_generate_ean13_barcode_rejects_non_digit_prefix():
    with pytest.raises(ValueError):
        generate_ean13_barcode(
            1,
            "ABC"
        )


def test_generate_ean13_barcode_rejects_non_positive_sequence():
    with pytest.raises(ValueError):
        generate_ean13_barcode(0)


def test_generate_ean13_barcode_rejects_exhausted_sequence():
    with pytest.raises(ValueError):
        generate_ean13_barcode(
            10_000_000_000,
            "29"
        )
