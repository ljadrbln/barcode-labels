import sqlite3

import pytest

from src.barcode_storage import BarcodeStorage


def test_storage_returns_unique_barcodes(tmp_path):
    filepath = tmp_path / "barcodes.sqlite3"
    storage = BarcodeStorage(filepath)

    first_barcode = storage.next_barcode()
    second_barcode = storage.next_barcode()

    assert first_barcode != second_barcode


def test_storage_does_not_reuse_barcode_after_restart(tmp_path):
    filepath = tmp_path / "barcodes.sqlite3"

    first_storage = BarcodeStorage(filepath)
    first_barcode = first_storage.next_barcode()

    second_storage = BarcodeStorage(filepath)
    second_barcode = second_storage.next_barcode()

    assert first_barcode != second_barcode


def test_storage_persists_generated_barcodes(tmp_path):
    filepath = tmp_path / "barcodes.sqlite3"
    storage = BarcodeStorage(filepath)

    first_barcode = storage.next_barcode()
    second_barcode = storage.next_barcode()

    connection = sqlite3.connect(str(filepath))

    try:
        rows = connection.execute(
            "SELECT barcode FROM barcodes ORDER BY id"
        ).fetchall()
    finally:
        connection.close()

    barcodes = [row[0] for row in rows]

    assert barcodes == [first_barcode, second_barcode]


@pytest.mark.skip(reason="Slow uniqueness stress test")
def test_storage_generates_many_unique_barcodes(tmp_path):
    filepath = tmp_path / "barcodes.sqlite3"
    storage = BarcodeStorage(filepath)

    barcodes = []

    for _ in range(10000):
        barcodes.append(storage.next_barcode())

    assert len(barcodes) == 10000
    assert len(set(barcodes)) == 10000
