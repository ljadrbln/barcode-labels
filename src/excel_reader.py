from openpyxl import load_workbook

def read_products(filepath):
    workbook = load_workbook(filepath)

    sheet = workbook.active

    rows = list(
        sheet.iter_rows(values_only=True)
    )

    headers = rows[0]

    result = []

    for row in rows[1:]:
        item = {}

        for index, value in enumerate(row):
            key = headers[index]

            item[key] = value

        result.append(item)

    return result