
from src.label_data_builder import build_label_data
from src.label_data_builder import remove_brand_prefix
from src.label_layouts import render_label_58x40_bags


def test_remove_brand_prefix():
    assert remove_brand_prefix("Renato Angi Leather Bag", "Renato Angi") == "Leather Bag"
    assert remove_brand_prefix("RENATO ANGI - Leather Bag", "Renato Angi") == "Leather Bag"
    assert remove_brand_prefix("Leather Bag Renato Angi", "Renato Angi") == "Leather Bag Renato Angi"
    assert remove_brand_prefix("Guesswork Bag", "Guess") == "Guesswork Bag"
    assert remove_brand_prefix("Leather Bag", "") == "Leather Bag"


def test_bags_label_data_does_not_change_original_product():
    product = {
        "article": "BG-001", "name": "Renato Angi Leather Bag",
        "brand": "Renato Angi", "price": 149, "currency": "USD",
    }
    profile = {
        "store_name": "COSMO", "layout": "label_58x40_bags",
        "label_item_fields": ["article", "name"],
    }

    result = build_label_data(product, profile, "1234567890123")

    assert result["brand_line"] == "Renato Angi"
    assert result["item_line"] == "BG-001 Leather Bag"
    assert result["logo_path"] is None
    assert product["name"] == "Renato Angi Leather Bag"


def test_shoes_keep_original_name():
    product = {
        "article": "SH-001", "name": "Renato Angi Shoes",
        "brand": "Renato Angi", "price": 149, "currency": "USD",
    }
    profile = {
        "store_name": "COSMO", "layout": "label_58x40_vertical_price",
        "label_item_fields": ["article", "name"],
    }

    result = build_label_data(product, profile, "1234567890123")

    assert result["item_line"] == "SH-001 Renato Angi Shoes"


def test_bags_layout_uses_logo_or_store_fallback(monkeypatch):
    import src.label_layouts as layouts

    calls = []
    monkeypatch.setattr(layouts, "draw_store_line", lambda *args: calls.append("store"))
    monkeypatch.setattr(layouts, "draw_bags_brand", lambda *args: calls.append("brand"))
    monkeypatch.setattr(layouts, "draw_item_line", lambda *args: calls.append("item"))
    monkeypatch.setattr(layouts, "draw_vertical_price", lambda *args: calls.append("price"))
    monkeypatch.setattr(layouts, "draw_vertical_separator", lambda *args: calls.append("separator"))
    monkeypatch.setattr(layouts, "draw_barcode", lambda *args: calls.append("barcode"))

    data = {
        "store_line": "COSMO", "logo_path": None, "brand_line": "Renato Angi",
        "price_line": "149 $", "item_line": "BG-001 Leather Bag", "barcode_value": "1234567890123",
    }
    render_label_58x40_bags(object(), data)

    assert calls == ["separator", "price", "store", "brand", "item", "barcode"]
