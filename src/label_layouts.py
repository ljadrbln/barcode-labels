from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.graphics.barcode import createBarcodeDrawing


LABEL_WIDTH = 58 * mm
LABEL_HEIGHT = 40 * mm


def render_label_58x40_vertical_price(
    pdf,
    label_data
):
    layout = build_layout()

    draw_vertical_separator(pdf, layout)
    draw_vertical_price(pdf, layout, label_data["price_line"])
    draw_store_line(pdf, layout, label_data["store_line"])
    draw_item_line(pdf, layout, label_data["item_line"])
    draw_barcode(pdf, layout, label_data["barcode_value"])


def build_layout():
    margin = 2 * mm

    inner_x = margin
    inner_y = margin

    inner_width = LABEL_WIDTH - (margin * 2)
    inner_height = LABEL_HEIGHT - (margin * 2)

    left_column_width = 10 * mm

    right_x = inner_x + left_column_width
    right_width = inner_width - left_column_width

    result = {
        "inner_x": inner_x,
        "inner_y": inner_y,
        "inner_width": inner_width,
        "inner_height": inner_height,
        "left_column_width": left_column_width,
        "right_x": right_x,
        "right_width": right_width,
    }

    return result


def draw_vertical_separator(
    pdf,
    layout
):
    x = layout["inner_x"] + layout["left_column_width"]

    pdf.line(
        x,
        layout["inner_y"],
        x,
        layout["inner_y"] + layout["inner_height"]
    )


def draw_vertical_price(
    pdf,
    layout,
    price_line
):
    pdf.saveState()

    pdf.setFont("DejaVu", 16)

    price_x = layout["inner_x"] + (layout["left_column_width"] / 2)
    price_y = layout["inner_y"] + (layout["inner_height"] / 2)

    pdf.translate(price_x, price_y)
    pdf.rotate(90)

    pdf.drawCentredString(
        0,
        -5,
        price_line
    )

    pdf.restoreState()


def draw_store_line(
    pdf,
    layout,
    store_line
):
    pdf.setFont("DejaVu", 12)

    x = layout["right_x"] + (layout["right_width"] / 2)
    y = layout["inner_y"] + layout["inner_height"] - (5 * mm)

    pdf.drawCentredString(
        x,
        y,
        store_line
    )


def draw_item_line(
    pdf,
    layout,
    item_line
):
    pdf.setFont("DejaVu", 10)

    max_text_width = layout["right_width"] - (4 * mm)

    lines = simpleSplit(
        item_line,
        "DejaVu",
        10,
        max_text_width
    )

    line_height = 5 * mm
    block_height = len(lines) * line_height

    start_y = (
        layout["inner_y"]
        + (layout["inner_height"] / 2)
        + (block_height / 2)
        - (3 * mm)
    )

    x = layout["right_x"] + (layout["right_width"] / 2)

    for index, line in enumerate(lines):
        y = start_y - (index * line_height)

        pdf.drawCentredString(
            x,
            y,
            line
        )


def draw_barcode(
    pdf,
    layout,
    barcode_value
):
    barcode = createBarcodeDrawing(
        "EAN13",
        value=barcode_value,
        barHeight=8 * mm,
        humanReadable=True
    )

    barcode_width = 32 * mm

    barcode_x = layout["right_x"] + ((layout["right_width"] - barcode_width) / 2)
    barcode_y = layout["inner_y"] + (2 * mm)

    barcode.drawOn(
        pdf,
        barcode_x,
        barcode_y
    )