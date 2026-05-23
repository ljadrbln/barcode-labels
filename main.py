from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


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


def main():
    article = "227701"
    name = "ICEBERG білий"
    size = "40(p)"
    price = "9790"
    barcode_value = "2966150061736"

    pdf = canvas.Canvas("label.pdf")

    pdf.setPageSize(
        (
            LABEL_WIDTH,
            LABEL_HEIGHT
        )
    )

    # Register font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            font_path
        )
    )

    render_label_v01(
        pdf,
        article,
        name,
        size,
        price,
        barcode_value
    )

    pdf.save()

    print("Done")


if __name__ == "__main__":
    main()