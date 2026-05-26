from src.barcode_generator import calculate_ean13_checksum


def test_calculate_ean13_checksum():
    first_12_digits = "296615006173"

    result = calculate_ean13_checksum(first_12_digits)

    assert result == "6"