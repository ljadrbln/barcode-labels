from pathlib import Path


def build_pdf_path(output_filepath):
    output_path = Path(output_filepath)

    pdf_name = f"{output_path.stem}_labels.pdf"

    result = output_path.with_name(pdf_name)

    return result