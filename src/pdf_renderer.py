from reportlab.pdfgen import canvas

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