import argparse

from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default="input/demo_products.xlsx"
    )

    parser.add_argument(
        "--output",
        default="output/products_with_barcodes.xlsx"
    )

    result = parser.parse_args()

    return result


def register_fonts():
    font_path = Path("assets/fonts/DejaVuSans.ttf")

    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            font_path
        )
    )