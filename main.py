from reportlab.pdfgen import canvas

from src.barcode_storage import get_or_create_barcode
from src.bootstrap import parse_args
from src.bootstrap import register_fonts
from src.excel_reader import read_products
from src.excel_writer import write_products_with_barcodes
from src.label_layouts import LABEL_WIDTH
from src.label_layouts import LABEL_HEIGHT
from src.label_layouts import render_label_v02
from src.output_paths import build_pdf_path


def main():
    args = parse_args()

    input_filepath = args.input
    output_filepath = args.output

    register_fonts()

    products = read_products(input_filepath)
    pdf_path = build_pdf_path(output_filepath)

    pdf = canvas.Canvas(str(pdf_path))
    pdf.setPageSize((LABEL_WIDTH, LABEL_HEIGHT))

    barcodes = {}

    for product in products:
        article = str(product["article"])
        name = str(product["name"])
        size = str(product["size"])
        price = str(product["price"])

        barcode_value = get_or_create_barcode(article, size)

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
        input_filepath,
        output_filepath,
        barcodes
    )

    print("Done")


if __name__ == "__main__":
    main()