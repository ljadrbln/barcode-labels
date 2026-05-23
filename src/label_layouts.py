from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.graphics.barcode import createBarcodeDrawing

LABEL_WIDTH = 58 * mm
LABEL_HEIGHT = 40 * mm

def render_label_v01(
    pdf,
    article,
    name,
    size,
    price,
    barcode_value
):
    margin = 2 * mm

    # Outer border
    pdf.roundRect(
        margin,
        margin,
        LABEL_WIDTH - (margin * 2),
        LABEL_HEIGHT - (margin * 2),
        2 * mm
    )

    # Brand
    pdf.setFont("DejaVu", 8)

    pdf.drawCentredString(
        LABEL_WIDTH / 2,
        35 * mm,
        "COSMO"
    )

    # Product name
    pdf.setFont("DejaVu", 16)

    pdf.drawCentredString(
        LABEL_WIDTH / 2,
        28 * mm,
        name
    )

    # Size
    pdf.setFont("DejaVu", 14)

    pdf.drawCentredString(
        LABEL_WIDTH / 2,
        22 * mm,
        size
    )

    # Price
    pdf.setFont("DejaVu", 22)

    pdf.drawCentredString(
        LABEL_WIDTH / 2,
        15 * mm,
        f"{price} грн"
    )

    # Barcode
    barcode = createBarcodeDrawing(
        'EAN13',
        value=barcode_value,
        barHeight=10 * mm,
        humanReadable=True
    )

    barcode.drawOn(
        pdf,
        7 * mm,
        2 * mm
    )

def render_label_v02(
    pdf,
    article,
    name,
    size,
    price,
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
    # Vertical price
    pdf.saveState()

    pdf.setFont("DejaVu", 16)

    price_x = inner_x + (left_column_width / 2)
    price_y = inner_y + (inner_height / 2)

    pdf.translate(
        price_x,
        price_y
    )

    pdf.rotate(90)

    pdf.drawCentredString(
        0,
        -5,
        f"{price} грн"
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
        "COSMO"
    )

    # Product text
    product_text = f"{article} {name} {size}"

    pdf.setFont("DejaVu", 10)

    max_text_width = right_width - (4 * mm)

    lines = simpleSplit(
        product_text,
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
        
    # product_text = f"{article} {name} {size}"

    # pdf.setFont("DejaVu", 12)

    # pdf.drawCentredString(
    #     right_x + (right_width / 2),
    #     inner_y + (inner_height / 2),
    #     product_text
    # )

    # Barcode
    barcode = createBarcodeDrawing(
        'EAN13',
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