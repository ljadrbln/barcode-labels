import random


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


def generate_ean13_barcode(prefix="29"):
    if len(prefix) >= 12:
        raise ValueError("Prefix must be shorter than 12 digits.")

    if not prefix.isdigit():
        raise ValueError("Prefix must contain only digits.")

    random_length = 12 - len(prefix)

    random_part = ""

    for _ in range(random_length):
        random_part += str(random.randint(0, 9))

    first_12_digits = prefix + random_part
    checksum = calculate_ean13_checksum(first_12_digits)

    barcode = first_12_digits + checksum

    return barcode
