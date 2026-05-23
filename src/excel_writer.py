from pathlib import Path

from openpyxl import load_workbook


def write_products_with_barcodes(
    input_filepath,
    output_filepath,
    barcodes
):
    workbook = load_workbook(input_filepath)

    sheet = workbook.active

    headers = []

    for cell in sheet[1]:
        headers.append(cell.value)

    barcode_column_index = len(headers) + 1

    if "barcode" in headers:
        barcode_column_index = headers.index("barcode") + 1
    else:
        sheet.cell(
            row=1,
            column=barcode_column_index,
            value="barcode"
        )

    for row_index in range(2, sheet.max_row + 1):
        article = sheet.cell(
            row=row_index,
            column=headers.index("article") + 1
        ).value

        size = sheet.cell(
            row=row_index,
            column=headers.index("size") + 1
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