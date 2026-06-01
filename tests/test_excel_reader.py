from openpyxl import Workbook

from src.excel_reader import read_products


def test_read_products(tmp_path):
    filepath = tmp_path / "products.xlsx"

    workbook = Workbook()

    sheet = workbook.active

    sheet.append([
        "Article_1",
        "Title_1",
        "Size_1",
        "Price_1",
        "Currency_1"
    ])

    sheet.append([
        "2x7x01",
        "ICEBERG white",
        "40 (x)",
        290,
        "usd"
    ])

    workbook.save(filepath)

    column_mapping = {
        "article": "Article_1",
        "name": "Title_1",
        "size": "Size_1",
        "price": "Price_1",
        "currency": "Currency_1"
    }

    result = read_products(
        filepath,
        column_mapping
    )

    assert result == [
        {
            "_row_index": 2,
            "article": "2x7x01",
            "name": "ICEBERG white",
            "size": "40 (x)",
            "price": 290,
            "currency": "usd"
        }
    ]