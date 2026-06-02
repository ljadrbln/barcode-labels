from src.output_paths import build_pdf_path
from src.pdf_renderer import render_labels_pdf
from src.bootstrap import register_fonts


def test_render_labels_pdf_creates_pdf(tmp_path):
    register_fonts()
    
    output_filepath = tmp_path / "products_with_barcodes.xlsx"

    products = [
        {
            "_row_index": 2,
            "article": "BG-001",
            "name": "Leather Bag",
            "price": 149,
            "currency": "USD"
        }
    ]

    profile_config = {
        "store_name": "Test Store",
        "product_key_fields": [
            "article"
        ],
        "label_item_fields": [
            "article",
            "name"
        ]
    }

    result = render_labels_pdf(
        profile_config,
        products,
        output_filepath
    )

    pdf_path = build_pdf_path(
        output_filepath
    )

    assert 2 in result
    assert len(result[2]) == 13
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0