import streamlit
from berroutils.crypter import Crypter
from berroutils.plugins.file_handler import CryptoJsonFileHandler, JsonFileHandler

from src import DATA_DIR, DEV_DATA_DIR
from src.thermal_bridge.psi_data import Psi


def init_psi():
    filepath = DATA_DIR / "psi_data.enc"
    crypter = Crypter(key=streamlit.secrets.key)
    filehandler = CryptoJsonFileHandler(file_path=filepath, crypter=crypter)
    return Psi(filehandler=filehandler)

# def init_psi():
#     filepath = DEV_DATA_DIR / "psi_data_oct26.json"
#     filehandler = JsonFileHandler(file_path=filepath)
#     return Psi(filehandler=filehandler)
