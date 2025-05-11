import streamlit
from berroutils.crypter import Crypter
from berroutils.plugins.file_handler import CryptoJsonFileHandler

from src import DATA_DIR
from src.thermal_bridge.psi_data import Psi


def init_psi():
    filepath = DATA_DIR / "psi_data.enc"
    crypter = Crypter(key=streamlit.secrets.key)
    filehandler = CryptoJsonFileHandler(file_path=filepath, crypter=crypter)
    return Psi(filehandler=filehandler)
