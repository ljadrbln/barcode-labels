from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.graphics.barcode import createBarcodeDrawing


LABEL_WIDTH = 58 * mm
LABEL_HEIGHT = 40 * mm

FONT_FAMILY = "DejaVu"
BOLD_FONT_FAMILY = "DejaVu-Bold"

STORE_FONT_SIZE = 10
ITEM_FONT_SIZE = 10
PRICE_FONT_SIZE = 12

ITEM_LINE_HEIGHT = 5 * mm

BARCODE_WIDTH = 32 * mm
BARCODE_HEIGHT = 8 * mm

LAYOUT_MARGIN = 2 * mm
LEFT_COLUMN_WIDTH = 10 * mm


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


def render_label_58x40_bags(
    pdf,
    label_data
):
    layout = build_layout()

    draw_vertical_separator(pdf, layout)
    draw_vertical_price(pdf, layout, label_data["price_line"])
    draw_bags_logo(pdf, layout, label_data)
    draw_bags_brand(pdf, layout, label_data["brand_line"])
    draw_bags_article(pdf, layout, label_data["article_line"])
    draw_bags_color(pdf, layout, label_data["item_line"])
    draw_barcode(pdf, layout, label_data["barcode_value"])


def draw_bags_logo(pdf, layout, label_data):
    logo_path = label_data.get("logo_path")

    if not logo_path:
        draw_store_line(pdf, layout, label_data["store_line"])
        return

    logo = ImageReader(str(logo_path))
    image_width, image_height = logo.getSize()
    max_width = layout["right_width"] - (4 * mm)
    max_height = 7 * mm
    scale = min(max_width / image_width, max_height / image_height)
    width = image_width * scale
    height = image_height * scale

    x = layout["right_x"] + (layout["right_width"] - width) / 2
    y = layout["inner_y"] + layout["inner_height"] - height - (1 * mm)

    pdf.drawImage(
        logo,
        x,
        y,
        width=width,
        height=height,
        mask="auto"
    )


def draw_bags_brand(pdf, layout, brand_line):
    if not brand_line:
        return

    pdf.setFont(BOLD_FONT_FAMILY, STORE_FONT_SIZE)

    x = layout["right_x"] + layout["right_width"] / 2
    y = layout["inner_y"] + layout["inner_height"] - (12 * mm)

    pdf.drawCentredString(x, y, str(brand_line))


def draw_bags_article(pdf, layout, article_line):
    pdf.setFont(FONT_FAMILY, ITEM_FONT_SIZE)
    x = layout["right_x"] + layout["right_width"] / 2
    y = layout["inner_y"] + 18 * mm
    pdf.drawCentredString(x, y, str(article_line))


def draw_bags_color(pdf, layout, color_line):
    pdf.setFont(FONT_FAMILY, ITEM_FONT_SIZE)
    x = layout["right_x"] + layout["right_width"] / 2
    y = layout["inner_y"] + 13 * mm
    pdf.drawCentredString(x, y, str(color_line))


def build_layout():
    inner_x = LAYOUT_MARGIN
    inner_y = LAYOUT_MARGIN

    inner_width = LABEL_WIDTH - (LAYOUT_MARGIN * 2)
    inner_height = LABEL_HEIGHT - (LAYOUT_MARGIN * 2)

    right_x = inner_x + LEFT_COLUMN_WIDTH
    right_width = inner_width - LEFT_COLUMN_WIDTH

    result = {
        "inner_x": inner_x,
        "inner_y": inner_y,
        "inner_width": inner_width,
        "inner_height": inner_height,
        "right_x": right_x,
        "right_width": right_width,
    }

    return result


def draw_vertical_separator(
    pdf,
    layout
):
    x = layout["inner_x"] + LEFT_COLUMN_WIDTH

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

    pdf.setFont(
        BOLD_FONT_FAMILY,
        PRICE_FONT_SIZE
    )

    price_x = layout["inner_x"] + (LEFT_COLUMN_WIDTH / 2)
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
    pdf.setFont(
        BOLD_FONT_FAMILY,
        STORE_FONT_SIZE
    )

    x = layout["right_x"] + (layout["right_width"] / 2)

    y = (
        layout["inner_y"]
        + layout["inner_height"]
        - (5 * mm)
    )

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
    pdf.setFont(
        FONT_FAMILY,
        ITEM_FONT_SIZE
    )

    max_text_width = layout["right_width"] - (4 * mm)

    lines = simpleSplit(
        item_line,
        FONT_FAMILY,
        ITEM_FONT_SIZE,
        max_text_width
    )

    block_height = len(lines) * ITEM_LINE_HEIGHT

    start_y = (
        layout["inner_y"]
        + (layout["inner_height"] / 2)
        + (block_height / 2)
        - (3 * mm)
    )

    x = layout["right_x"] + (layout["right_width"] / 2)

    for index, line in enumerate(lines):
        y = start_y - (index * ITEM_LINE_HEIGHT)

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
        barHeight=BARCODE_HEIGHT,
        humanReadable=True
    )

    barcode_x = (
        layout["right_x"]
        + (
            (
                layout["right_width"]
                - BARCODE_WIDTH
            ) / 2
        )
    )

    barcode_y = layout["inner_y"] + (2 * mm)

    barcode.drawOn(
        pdf,
        barcode_x,
        barcode_y
    )