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

def test_read_products_without_size_column(tmp_path):
    filepath = tmp_path / "bags.xlsx"

    workbook = Workbook()

    sheet = workbook.active

    sheet.append([
        "Article",
        "Name",
        "Price"
    ])

    sheet.append([
        "BG-001",
        "Leather Bag",
        149
    ])

    workbook.save(filepath)

    column_mapping = {
        "article": "Article",
        "name": "Name",
        "price": "Price"
    }

    result = read_products(
        filepath,
        column_mapping
    )

    assert result == [
        {
            "_row_index": 2,
            "article": "BG-001",
            "name": "Leather Bag",
            "price": 149
        }
    ]

def test_read_products_ignores_extra_columns(tmp_path):
    filepath = tmp_path / "products.xlsx"

    workbook = Workbook()

    sheet = workbook.active

    sheet.append([
        "Article",
        "Name",
        "Price",
        "Color",
        "Country"
    ])

    sheet.append([
        "BG-001",
        "Leather Bag",
        149,
        "Black",
        "Italy"
    ])

    workbook.save(filepath)

    column_mapping = {
        "article": "Article",
        "name": "Name",
        "price": "Price"
    }

    result = read_products(
        filepath,
        column_mapping
    )

    assert result == [
        {
            "_row_index": 2,
            "article": "BG-001",
            "name": "Leather Bag",
            "price": 149
        }
    ]    