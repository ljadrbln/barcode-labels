from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.graphics.barcode import createBarcodeDrawing

LABEL_WIDTH = 58 * mm
LABEL_HEIGHT = 40 * mm

def render_label_58x40_vertical_price(
    pdf,
    store_line,
    item_line,
    price_line,
    barcode_value
):
    margin = 2 * mm

    inner_x = margin
    inner_y = margin

    inner_width = LABEL_WIDTH - (margin * 2)
    inner_height = LABEL_HEIGHT - (margin * 2)

    left_column_width = 10 * mm

    # Vertical separator
    pdf.line(
        inner_x + left_column_width,
        inner_y,
        inner_x + left_column_width,
        inner_y + inner_height
    )

    # LEFT COLUMN
    pdf.saveState()

    pdf.setFont("DejaVu", 16)

    price_x = inner_x + (left_column_width / 2)
    price_y = inner_y + (inner_height / 2)

    pdf.translate(price_x, price_y)
    pdf.rotate(90)

    pdf.drawCentredString(
        0,
        -5,
        price_line
    )

    pdf.restoreState()

    # RIGHT COLUMN
    right_x = inner_x + left_column_width
    right_width = inner_width - left_column_width

    # Store name
    pdf.setFont("DejaVu", 12)

    pdf.drawCentredString(
        right_x + (right_width / 2),
        inner_y + inner_height - (5 * mm),
        store_line
    )

    # Item text
    pdf.setFont("DejaVu", 10)

    max_text_width = right_width - (4 * mm)

    lines = simpleSplit(
        item_line,
        "DejaVu",
        10,
        max_text_width
    )

    line_height = 5 * mm
    block_height = len(lines) * line_height

    start_y = (
        inner_y
        + (inner_height / 2)
        + (block_height / 2)
        - (3 * mm)
    )

    for index, line in enumerate(lines):
        y = start_y - (index * line_height)

        pdf.drawCentredString(
            right_x + (right_width / 2),
            y,
            line
        )

    # Barcode
    barcode = createBarcodeDrawing(
        "EAN13",
        value=barcode_value,
        barHeight=8 * mm,
        humanReadable=True
    )

    barcode_width = 32 * mm

    barcode_x = right_x + ((right_width - barcode_width) / 2)
    barcode_y = inner_y + (2 * mm)

    barcode.drawOn(
        pdf,
        barcode_x,
        barcode_y
    )