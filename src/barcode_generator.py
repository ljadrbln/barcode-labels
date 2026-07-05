import hashlib


def calculate_ean13_checksum(first_12_digits):
    total = 0

    for index, digit in enumerate(first_12_digits):
        number = int(digit)

        if index % 2 == 0:
            total += number
        else:
            total += number * 3

    remainder = total % 10

    if remainder == 0:
        checksum = 0
    else:
        checksum = 10 - remainder

    return str(checksum)


def generate_ean13_barcode(
    product_key,
    prefix="29"
):
    if len(prefix) >= 12:
        raise ValueError("Prefix must be shorter than 12 digits.")

    if not prefix.isdigit():
        raise ValueError("Prefix must contain only digits.")

    payload_length = 12 - len(prefix)

    digest = hashlib.sha256(
        product_key.encode("utf-8")
    ).digest()

    number = int.from_bytes(
        digest,
        byteorder="big"
    )

    payload = str(
        number % (10 ** payload_length)
    ).zfill(payload_length)

    first_12_digits = prefix + payload
    checksum = calculate_ean13_checksum(first_12_digits)

    barcode = first_12_digits + checksum

    return barcode