import pytest

from src.barcode_generator import generate_ean13_barcode
from src.barcode_generator import validate_ean13_barcode
from src.pdf_renderer import render_labels_pdf


class FakeBarcodeStorage:
    def __init__(self):
        self.calls = 0

    def next_barcode(self):
        self.calls += 1
        return generate_ean13_barcode(100 + self.calls)


class FakeCanvas:
    instances = []

    def __init__(self, filepath):
        self.pages = 0
        FakeCanvas.instances.append(self)

    def setPageSize(self, size):
        pass

    def showPage(self):
        self.pages += 1

    def save(self):
        pass


def test_validate_existing_ean13():
    barcode = generate_ean13_barcode(123)
    assert validate_ean13_barcode(barcode) == barcode
    assert validate_ean13_barcode(int(barcode)) == barcode
    assert validate_ean13_barcode("  " + barcode + "  ") == barcode


@pytest.mark.parametrize("barcode", [
    "12345", "2900000000125", "abc0000000000", True, 123.5,
])
def test_reject_invalid_existing_ean13(barcode):
    with pytest.raises(ValueError):
        validate_ean13_barcode(barcode)


def test_reuse_existing_and_generate_only_missing(monkeypatch, tmp_path):
    import src.pdf_renderer as renderer

    FakeCanvas.instances.clear()
    monkeypatch.setattr(renderer.canvas, "Canvas", FakeCanvas)
    rendered = []
    monkeypatch.setattr(
        renderer,
        "render_label_58x40_vertical_price",
        lambda pdf, data: rendered.append(data["barcode_value"]),
    )

    existing = generate_ean13_barcode(42)
    products = [
        {"_row_index": 2, "article": "A", "name": "Bag A", "price": 100,
         "currency": "UAH", "barcode": existing},
        {"_row_index": 3, "article": "B", "name": "Bag B", "price": 200,
         "currency": "UAH", "barcode": None},
    ]
    profile = {
        "store_name": "Test", "label_item_fields": ["article", "name"],
    }
    storage = FakeBarcodeStorage()
    result = render_labels_pdf(profile, products, tmp_path / "out.xlsx", storage)

    assert storage.calls == 1
    assert result[2] == existing
    assert result[3] == generate_ean13_barcode(101)
    assert rendered == [existing, result[3]]
    assert FakeCanvas.instances[0].pages == 2


def test_invalid_existing_barcode_does_not_generate_replacement(monkeypatch, tmp_path):
    import src.pdf_renderer as renderer

    monkeypatch.setattr(renderer.canvas, "Canvas", FakeCanvas)
    profile = {"store_name": "Test", "label_item_fields": ["article"]}
    product = {"_row_index": 7, "article": "A", "price": 100,
               "currency": "UAH", "barcode": "123"}
    storage = FakeBarcodeStorage()

    with pytest.raises(ValueError, match="Excel row 7"):
        render_labels_pdf(profile, [product], tmp_path / "out.xlsx", storage)
    assert storage.calls == 0
