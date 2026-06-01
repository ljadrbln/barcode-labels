import argparse

from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default="input/demo_products_shoes.xlsx"
    )

    parser.add_argument(
        "--output",
        default="output/shoes_with_barcodes.xlsx"
    )

    parser.add_argument(
        "--profile",
        default="shoes"
    )    

    result = parser.parse_args()

    return result


def register_fonts():
    font_path = Path(
        "assets/fonts/DejaVuSans.ttf"
    )

    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            str(font_path)
        )
    )