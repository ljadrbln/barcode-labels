# Barcode Labels Generator

Generate:

- EAN13 barcodes
- PDF labels
- XLSX files with barcode column

## Install

```bash
pip install reportlab==3.6.13 openpyxl
```

## Input XLSX format

| article | name          | size  | price |
| ------- | ------------- | ----- | ----- |
| 227701  | ICEBERG белый | 40(p) | 290   |

## Run

Default demo:

```bash
python3 main.py
```

Custom files:

```bash
python3 main.py \
    --input input/products.xlsx \
    --output output/products_with_barcodes.xlsx
```

## Output

Generated files:

```text
output/
├── products_with_barcodes.xlsx
└── products_with_barcodes_labels.pdf
```

## Notes

- Barcodes are stored in:
  `data/barcodes.json`
- Same product always gets the same barcode.
- PDF label size:
  `58x40 mm`
