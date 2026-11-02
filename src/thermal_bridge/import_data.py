from berroutils.crypter import Crypter
from berroutils.plugins.file_handler import CryptoJsonFileHandler, JsonFileHandler
from pathlib import Path
import json

from src import DATA_DIR, DEV_DATA_DIR, SRC_ROOT
from src.thermal_bridge.psi_data import Psi


def main():

    with open(SRC_ROOT.parent.parent / Path("credentials.json")) as f:
        credentials = json.load(f)
    key = credentials.get("thermalbridge_encryption_key")

    # alternatively get the key from streamlit.secrets
    # key = 'key_from_streamlit_secrets'

    filepath = DATA_DIR / "psi_data.enc"
    crypter = Crypter(key=key)
    filehandler = CryptoJsonFileHandler(file_path=filepath, crypter=crypter)
    psi = Psi(filehandler=filehandler, crypter=crypter)

    filepath_new_source = DEV_DATA_DIR / "Stand 10-2026.xlsx"
    psi.update_from_excel(filepath_new_source, sheet_name="44er Wand")
    print(f"{len(psi.data)} entries")


def dev_main():
    """
    Import to json file for human readability.

    Result will be stored in dev_data to ensure they are not committed and visible to the public. The dev_data folder is in .gitignore.
    """

    # export OPENAI_API_KEY="api key here"

    filepath = DEV_DATA_DIR / "psi_data_oct26.json"
    filehandler = JsonFileHandler(file_path=filepath)
    psi = Psi(filehandler=filehandler)

    filepath_new_source = DEV_DATA_DIR / "Stand 10-2026.xlsx"
    psi.update_from_excel(filepath=filepath_new_source, sheet_name="44er Wand")
    print(f"{len(psi.data)} entries")


if __name__ == '__main__':
    dev_main()
