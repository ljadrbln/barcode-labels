from pathlib import Path

from src.output_paths import build_pdf_path


def test_build_pdf_path():
    output_filepath = "output/products_with_barcodes.xlsx"

    result = build_pdf_path(output_filepath)

    expected = Path(
        "output/products_with_barcodes_labels.pdf"
    )

    assert result == expected