from berroutils.crypter import Crypter
from berroutils.plugins.file_handler import CryptoJsonFileHandler, JsonFileHandler

from src import DATA_DIR, DEV_DATA_DIR
from src.thermal_bridge.psi_data import Psi


def main():
    # get from streamlit.secrets
    key = 'missing'

    filepath = DATA_DIR / "psi_data.enc"
    crypter = Crypter(key=key)
    filehandler = CryptoJsonFileHandler(file_path=filepath, crypter=crypter)
    psi = Psi(filehandler=filehandler, crypter=crypter)

    filepath_new_source = DEV_DATA_DIR / "Stand Oktober 25 - 44er Wand.csv"
    psi.update_from_file(filepath=filepath_new_source)
    print(f"{len(psi.data)} entries")

def dev_main():
    """
    Import to json file for human readability.

    Result will be stored in dev_data to ensure they are not committed and visible to the public. The dev_data folder is in .gitignore.
    """

    # export OPENAI_API_KEY="api key here"

    filepath = DEV_DATA_DIR / "psi_data.json"
    filehandler = JsonFileHandler(file_path=filepath)
    psi = Psi(filehandler=filehandler)

    filepath_new_source = DEV_DATA_DIR / "Stand Oktober 25 - 44er Wand.csv"
    psi.update_from_file(filepath=filepath_new_source)
    print(f"{len(psi.data)} entries")

if __name__ == '__main__':
    dev_main()
