from src.barcode_storage import get_or_create_barcode
from src.barcode_storage import load_storage
from src.barcode_storage import save_storage


def test_load_storage_returns_empty_dict_for_missing_file(tmp_path):
    data_file = tmp_path / "barcodes.json"

    result = load_storage(data_file)

    assert result == {}


def test_save_and_load_storage(tmp_path):
    data_file = tmp_path / "barcodes.json"

    data = {
        "227701:40(p)": "2966150061736"
    }

    save_storage(data, data_file)

    result = load_storage(data_file)

    assert result == data


def test_get_or_create_barcode_returns_same_barcode_for_same_product(tmp_path):
    data_file = tmp_path / "barcodes.json"

    first_result = get_or_create_barcode("227701:40(p)", data_file)
    second_result = get_or_create_barcode("227701:40(p)", data_file)
    

    assert first_result == second_result