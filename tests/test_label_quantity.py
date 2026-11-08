from src.pdf_renderer import render_labels_pdf, get_label_quantity


def test_render_labels_pdf_repeats_pages_for_quantity(tmp_path, monkeypatch):
    import src.pdf_renderer as renderer

    class FakeCanvas:
        def __init__(self):
            self.pages = 0

        def setPageSize(self, size):
            pass

        def showPage(self):
            self.pages += 1

        def save(self):
            pass

    class FakeBarcodeStorage:
        def __init__(self):
            self.calls = 0

        def next_barcode(self):
            self.calls += 1
            return f"{self.calls:013d}"

    pdf = FakeCanvas()
    drawn_barcodes = []
    monkeypatch.setattr(renderer.canvas, "Canvas", lambda path: pdf)
    monkeypatch.setattr(
        renderer,
        "render_label_58x40_vertical_price",
        lambda pdf, data: drawn_barcodes.append(data["barcode_value"]),
    )

    products = [
        {"_row_index": 2, "article": "A", "name": "A", "price": 10, "quantity": 2},
        {"_row_index": 3, "article": "B", "name": "B", "price": 10, "quantity": 3},
        {"_row_index": 4, "article": "C", "name": "C", "price": 10, "quantity": 0},
        {"_row_index": 5, "article": "D", "name": "D", "price": 10},
    ]
    config = {"store_name": "Test", "label_item_fields": ["article", "name"]}
    storage = FakeBarcodeStorage()

    result = render_labels_pdf(config, products, tmp_path / "output.xlsx", storage)

    assert pdf.pages == 6
    assert storage.calls == 4
    assert len(result) == 4
    assert drawn_barcodes == [result[2]] * 2 + [result[3]] * 3 + [result[5]]


def test_label_quantity_validation():
    import pytest
    from src.pdf_renderer import get_label_quantity

    assert get_label_quantity({}) == 1
    assert get_label_quantity({"quantity": None}) == 1
    assert get_label_quantity({"quantity": ""}) == 1
    assert get_label_quantity({"quantity": "2"}) == 2
    assert get_label_quantity({"quantity": 2.0}) == 2
    assert get_label_quantity({"quantity": 0}) == 0

    for invalid in [-1, 1.5, "abc", "NaN"]:
        with pytest.raises(ValueError, match="Invalid quantity"):
            get_label_quantity({"quantity": invalid})
