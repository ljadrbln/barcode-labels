from pathlib import Path

from openpyxl import load_workbook


def write_products_with_barcodes(
    input_filepath,
    output_filepath,
    barcodes,
    column_mapping
):
    workbook = load_workbook(input_filepath)

    sheet = workbook.active

    headers = []

    for cell in sheet[1]:
        headers.append(cell.value)

    article_column_name = column_mapping["article"]
    size_column_name = column_mapping["size"]

    article_column_index = headers.index(article_column_name) + 1
    size_column_index = headers.index(size_column_name) + 1

    barcode_column_name = "barcode"
    barcode_column_index = len(headers) + 1

    if barcode_column_name in headers:
        barcode_column_index = headers.index(barcode_column_name) + 1
    else:
        sheet.cell(
            row=1,
            column=barcode_column_index,
            value=barcode_column_name
        )

    for row_index in range(2, sheet.max_row + 1):
        article = sheet.cell(
            row=row_index,
            column=article_column_index
        ).value

        size = sheet.cell(
            row=row_index,
            column=size_column_index
        ).value

        product_key = f"{article}:{size}"

        barcode = barcodes.get(product_key)

        sheet.cell(
            row=row_index,
            column=barcode_column_index,
            value=barcode
        )

    output_path = Path(output_filepath)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    workbook.save(output_filepath)