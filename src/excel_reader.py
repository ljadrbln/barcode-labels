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

    for row_index, row in enumerate(rows[1:], start=2):
        is_empty = True

        for value in row:
            if value not in (None, ""):
                is_empty = False
                break

        if is_empty:
            continue

        item = {
            "_row_index": row_index
        }

        for internal_name, index in header_indexes.items():
            item[internal_name] = row[index]

        result.append(item)

    return result