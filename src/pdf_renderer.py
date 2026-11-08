from decimal import Decimal, InvalidOperation

from reportlab.pdfgen import canvas

from src.label_data_builder import build_label_data
from src.barcode_generator import validate_ean13_barcode
from src.label_layouts import LABEL_WIDTH
from src.label_layouts import LABEL_HEIGHT
from src.label_layouts import render_label_58x40_vertical_price
from src.label_layouts import render_label_58x40_bags
from src.label_layouts import render_label_58x40_shoes
from src.output_paths import build_pdf_path


def get_label_quantity(product):
    raw = product.get("quantity")
    if raw is None or raw == "":
        return 1

    try:
        quantity = Decimal(str(raw).strip())
    except InvalidOperation:
        raise ValueError(f"Invalid quantity: {raw!r}")

    if not quantity.is_finite() or quantity < 0 or quantity != quantity.to_integral_value():
        raise ValueError(f"Invalid quantity: {raw!r}")

    return int(quantity)


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
        "label_58x40_shoes": render_label_58x40_shoes,
    }
    layout_name = profile_config.get("layout", "label_58x40_vertical_price")
    render_label = layouts[layout_name]

    barcodes_by_row = {}

    for product in products:
        quantity = get_label_quantity(product)
        existing_barcode = product.get("barcode")

        if existing_barcode is None or str(existing_barcode).strip() == "":
            barcode_value = barcode_storage.next_barcode()
        else:
            try:
                barcode_value = validate_ean13_barcode(existing_barcode)
            except ValueError as error:
                raise ValueError(
                    f"Invalid barcode in Excel row {product['_row_index']}: {error}"
                ) from error

        label_data = build_label_data(
            product,
            profile_config,
            barcode_value
        )

        row_index = product["_row_index"]
        barcode_value = label_data["barcode_value"]

        barcodes_by_row[row_index] = barcode_value

        for _ in range(quantity):
            render_label(
                pdf,
                label_data
            )
            pdf.showPage()

    pdf.save()

    return barcodes_by_row