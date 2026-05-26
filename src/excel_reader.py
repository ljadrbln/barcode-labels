from openpyxl import load_workbook


def read_products(
    filepath,
    column_mapping
):
    workbook = load_workbook(filepath)

    sheet = workbook.active

    rows = list(
        sheet.iter_rows(values_only=True)
    )

    headers = rows[0]

    header_indexes = {}

    for internal_name, excel_column_name in column_mapping.items():
        if excel_column_name not in headers:
            continue

        header_indexes[internal_name] = headers.index(
            excel_column_name
        )

    result = []

    for row in rows[1:]:
        item = {}

        for internal_name, index in header_indexes.items():
            item[internal_name] = row[index]

        result.append(item)

    return result