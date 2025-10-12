Attempt to run an Excel lookup on streamlit

https://thermalbridge.streamlit.app


#### Import a new dataset from Google Sheets:
1) Copy the code from Extensions / Apps Script in file https://docs.google.com/spreadsheets/d/10sybeF1HE_hacJeI9MT6HGqcU8ibvale-aKQlE5g-BM/edit?gid=893176465#gid=893176465
2) Copy columns `K, L, M` from Tab "44er Wand" 
3) Make sure column `Psi-Wert` contains only floats by filtering by condition _is not between -1 and +1_
4) Make sure column `text_size` contains only values 10, 11 and 12
5) Download as .csv
6) In `import_data.py` point `filepath_new_source` to the csv-file
7) Get the key from streamlit before running the import