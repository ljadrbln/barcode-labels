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
    regular_font_path = Path(
        "assets/fonts/DejaVuSans.ttf"
    )

    bold_font_path = Path(
        "assets/fonts/DejaVuSans-Bold.ttf"
    )

    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            str(regular_font_path)
        )
    )

    pdfmetrics.registerFont(
        TTFont(
            "DejaVu-Bold",
            str(bold_font_path)
        )
    )