Attempt to run an Excel lookup on streamlit

https://thermalbridge.streamlit.app


#### Import directly from Excel (no Google Sheets needed)

Install dependencies with `uv sync`. Export the `44er Wand` worksheet with:

```sh
uv run python -m src.thermal_bridge.excel_import "data/Stand 29.08.xlsx" "data/Stand 29.08 - 44er Wand.csv"
```

Use `--sheet "40er Wand"` to select another worksheet with the same layout.
The converter combines the headers in rows 2–3 (columns A–J), skips empty
Bezeichnung rows, and adds `row_color`, `text_size`, and `text_color` from
the Bezeichnung cell. Excel dates become `dd.mm.yyyy`; font sizes become
integers and colors become lowercase `#rrggbb` values for the existing importer.
Point `filepath_new_source` in `import_data.py` at this CSV.

Alternatively, skip CSV entirely in `import_data.py`:

```python
filepath_new_source = DATA_DIR / "Stand 29.08.xlsx"
psi.update_from_excel(filepath_new_source, sheet_name="44er Wand")
```

Keep the existing encrypted file handler and supply its key as before.
The direct importer prompts in the terminal for invalid Psi values and repeats
the prompt until a numeric value is entered (use a decimal point). Corrections
are saved in the imported dataset; the original workbook is not edited.
The supplied workbook has two malformed Psi values: B7403 (`0,.0209`) and
B7404 (`0,.0269`). You can correct them at the prompts during direct import. CSV export
preserves these values so they can also be reviewed in the exported file.

Only stored cell formatting is extracted; conditional formatting is not
evaluated. Formula values come from Excel's saved calculation results,
so recalculate and save in Excel if those results are missing or outdated.
Existing font-size rules (12 = category, 11 = subsection, red 10 = extra
information) still apply; unusual formatting should be reviewed in the source.

#### Previous import workflow using Google Sheets:
1) Copy the code from Extensions / Apps Script in file https://docs.google.com/spreadsheets/d/10sybeF1HE_hacJeI9MT6HGqcU8ibvale-aKQlE5g-BM/edit?gid=893176465#gid=893176465
2) Copy columns `K, L, M` from Tab "44er Wand" 
3) Make sure column `Psi-Wert` contains only floats by filtering by condition _is not between -1 and +1_
4) Make sure column `text_size` contains only values 10, 11 and 12
5) Download as .csv
6) In `import_data.py` point `filepath_new_source` to the csv-file
7) Get the key from streamlit before running the import
