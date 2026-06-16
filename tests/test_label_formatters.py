from src.label_data_builder import format_currency
from src.label_data_builder import format_price
from src.label_data_builder import format_size


def test_format_currency_maps_uah():
    assert format_currency("UAH") == "грн"


def test_format_currency_maps_usd():
    assert format_currency("USD") == "$"


def test_format_currency_maps_eur():
    assert format_currency("EUR") == "€"


def test_format_currency_maps_rub():
    assert format_currency("RUB") == "₽"


def test_format_currency_keeps_unknown_currency_code():
    assert format_currency("PLN") == "PLN"


def test_format_price_uses_thousands_separator_and_currency_label():
    assert format_price(10990, "UAH") == "10 990.00 грн"


def test_format_price_keeps_unknown_currency_code():
    assert format_price(199, "PLN") == "199.00 PLN"


def test_format_size():
    assert format_size("37") == "37 р."


def test_format_size_returns_empty_string_for_empty_value():
    assert format_size("") == ""