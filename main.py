from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.barcode_storage import get_or_create_barcode
from src.excel_reader import read_products
from src.excel_writer import write_products_with_barcodes
from src.label_layouts import LABEL_WIDTH
from src.label_layouts import LABEL_HEIGHT
from src.label_layouts import render_label_v02


def register_fonts():
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            font_path
        )
    )


def main():
    register_fonts()

    products = read_products(
        "input/demo_products.xlsx"
    )

    pdf = canvas.Canvas("label.pdf")

    pdf.setPageSize(
        (
            LABEL_WIDTH,
            LABEL_HEIGHT
        )
    )

    barcodes = {}

    for product in products:
        article = str(product["article"])
        name = str(product["name"])
        size = str(product["size"])
        price = str(product["price"])

        barcode_value = get_or_create_barcode(
            article,
            size
        )

        product_key = f"{article}:{size}"
        barcodes[product_key] = barcode_value

        render_label_v02(
            pdf,
            article,
            name,
            size,
            price,
            barcode_value
        )

        pdf.showPage()

    pdf.save()

    write_products_with_barcodes(
        "input/demo_products.xlsx",
        "output/products_with_barcodes.xlsx",
        barcodes
    )    

    print("Done")


if __name__ == "__main__":
    main()