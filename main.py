from reportlab.pdfgen import canvas

from src.barcode_storage import get_or_create_barcode
from src.bootstrap import parse_args
from src.bootstrap import register_fonts
from src.config_loader import load_column_mapping
from src.excel_reader import read_products
from src.excel_writer import write_products_with_barcodes
from src.label_layouts import LABEL_WIDTH
from src.label_layouts import LABEL_HEIGHT
from src.label_layouts import render_label_58x40_vertical_price
from src.output_paths import build_pdf_path

STORE_LINE = "COSMO"

def build_label_data(product):
    article = str(product["article"])
    name = str(product["name"])
    size = str(product["size"])
    price = str(product["price"])
    currency = product.get("currency") or ""

    price_line = f"{price} {currency}".strip()
    item_line = f"{article} {name} {size}"

    barcode_value = get_or_create_barcode(article, size)

    product_key = f"{article}:{size}"

    result = {
        "product_key": product_key,
        "barcode_value": barcode_value,
        "item_line": item_line,
        "price_line": price_line,
    }

    return result


def render_labels_pdf(
    products,
    output_filepath
):
    pdf_path = build_pdf_path(output_filepath)

    pdf = canvas.Canvas(str(pdf_path))
    pdf.setPageSize((LABEL_WIDTH, LABEL_HEIGHT))

    barcodes = {}

    for product in products:
        label_data = build_label_data(product)

        product_key = label_data["product_key"]
        barcode_value = label_data["barcode_value"]

        barcodes[product_key] = barcode_value

        render_label_58x40_vertical_price(
            pdf,
            STORE_LINE,
            label_data["item_line"],
            label_data["price_line"],
            barcode_value
        )

        pdf.showPage()

    pdf.save()

    return barcodes


def main():
    args = parse_args()

    input_filepath = args.input
    output_filepath = args.output

    register_fonts()

    column_mapping = load_column_mapping()
    products = read_products(input_filepath, column_mapping)

    barcodes = render_labels_pdf(
        products,
        output_filepath
    )

    write_products_with_barcodes(
        input_filepath,
        output_filepath,
        barcodes,
        column_mapping
    )

    print("Done")


if __name__ == "__main__":
    main()