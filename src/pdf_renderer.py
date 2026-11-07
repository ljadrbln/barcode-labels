from reportlab.pdfgen import canvas

from src.label_data_builder import build_label_data
from src.label_layouts import LABEL_WIDTH
from src.label_layouts import LABEL_HEIGHT
from src.label_layouts import render_label_58x40_vertical_price
from src.label_layouts import render_label_58x40_bags
from src.output_paths import build_pdf_path


def render_labels_pdf(
    profile_config,
    products,
    output_filepath,
    barcode_storage
):
    pdf_path = build_pdf_path(output_filepath)

    pdf = canvas.Canvas(str(pdf_path))
    pdf.setPageSize((LABEL_WIDTH, LABEL_HEIGHT))

    layouts = {
        "label_58x40_vertical_price": render_label_58x40_vertical_price,
        "label_58x40_bags": render_label_58x40_bags,
    }
    layout_name = profile_config.get("layout", "label_58x40_vertical_price")
    render_label = layouts[layout_name]

    barcodes_by_row = {}

    for product in products:
        barcode_value = barcode_storage.next_barcode()

        label_data = build_label_data(
            product,
            profile_config,
            barcode_value
        )

        row_index = product["_row_index"]
        barcode_value = label_data["barcode_value"]

        barcodes_by_row[row_index] = barcode_value

        render_label(
            pdf,
            label_data
        )

        pdf.showPage()

    pdf.save()

    return barcodes_by_row