from pathlib import Path

from src.bootstrap import parse_args
from src.bootstrap import register_fonts
from src.config_loader import load_profile_config
from src.excel_reader import read_products
from src.excel_writer import write_products_with_barcodes
from src.pdf_renderer import render_labels_pdf


def validate_input_file(filepath):
    input_path = Path(filepath)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")


def run():
    args = parse_args()

    input_filepath = args.input
    output_filepath = args.output

    validate_input_file(input_filepath)

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


def main():
    try:
        run()
    except FileNotFoundError as error:
        print(error)

if __name__ == "__main__":
    main()