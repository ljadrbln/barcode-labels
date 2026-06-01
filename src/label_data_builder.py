from reportlab.pdfgen import canvas

from src.bootstrap import parse_args
from src.bootstrap import register_fonts
from src.config_loader import load_profile_config
from src.excel_reader import read_products
from src.excel_writer import write_products_with_barcodes
from src.label_data_builder import build_label_data
from src.label_layouts import LABEL_WIDTH
from src.label_layouts import LABEL_HEIGHT
from src.label_layouts import render_label_58x40_vertical_price
from src.output_paths import build_pdf_path


def render_labels_pdf(
    profile_config,
    products,
    output_filepath
):
    pdf_path = build_pdf_path(output_filepath)

    pdf = canvas.Canvas(str(pdf_path))
    pdf.setPageSize((LABEL_WIDTH, LABEL_HEIGHT))

    barcodes_by_row = {}

    for product in products:
        label_data = build_label_data(
            product,
            profile_config
        )

        row_index = product["_row_index"]
        barcode_value = label_data["barcode_value"]

        barcodes_by_row[row_index] = barcode_value

        render_label_58x40_vertical_price(
            pdf,
            label_data
        )

        pdf.showPage()

    pdf.save()

    return barcodes_by_row


def main():
    args = parse_args()

    input_filepath = args.input
    output_filepath = args.output

    register_fonts()

    profile_config = load_profile_config(
        args.profile
    )

    column_mapping = profile_config["columns"]

    products = read_products(
        input_filepath,
        column_mapping
    )

    barcodes_by_row = render_labels_pdf(
        profile_config,
        products,
        output_filepath
    )

    write_products_with_barcodes(
        input_filepath,
        output_filepath,
        barcodes_by_row,
        column_mapping
    )

    print("Done")


if __name__ == "__main__":
    main()