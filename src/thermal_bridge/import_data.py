from berroutils.crypter import Crypter
from berroutils.plugins.file_handler import CryptoJsonFileHandler

from src import DATA_DIR
from src.thermal_bridge.psi_data import Psi


def main():
    key = 'missing'

    filepath = DATA_DIR / "psi_data.enc"
    crypter = Crypter(key=key)
    filehandler = CryptoJsonFileHandler(file_path=filepath, crypter=crypter)
    psi = Psi(filehandler=filehandler)

    # filepath_new_source = DATA_DIR / "thermal_bridge_44er.csv"
    filepath_new_source = DATA_DIR / "thermal_brige_14May2024_44er.csv"
    psi.update_from_file(filepath=filepath_new_source)


if __name__ == '__main__':
    main()
