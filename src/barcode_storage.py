import sqlite3

from pathlib import Path

from src.barcode_generator import generate_ean13_barcode


class BarcodeStorage:
    def __init__(self, filepath="data/barcodes.sqlite3", prefix="29"):
        self.filepath = Path(filepath)
        self.prefix = prefix

    def next_barcode(self):
        self.filepath.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        connection = sqlite3.connect(
            str(self.filepath),
            timeout=30
        )

        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS barcodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode TEXT UNIQUE,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor = connection.execute(
                "INSERT INTO barcodes (barcode) VALUES (NULL)"
            )

            sequence = cursor.lastrowid
            barcode = generate_ean13_barcode(
                sequence,
                self.prefix
            )

            connection.execute(
                "UPDATE barcodes SET barcode = ? WHERE id = ?",
                (barcode, sequence)
            )

            connection.commit()

            return barcode
        finally:
            connection.close()
