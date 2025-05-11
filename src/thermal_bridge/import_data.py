from berroutils.crypter import Crypter
from berroutils.plugins.file_handler import CryptoJsonFileHandler

from src import DATA_DIR
from src.thermal_bridge.psi_data import Psi


def main():
    password = "missing"
    mysalt = "missing"

    filepath = DATA_DIR / "psi_data.enc"
    crypter = Crypter.from_password_salt(password=password, salt=mysalt)
    filehandler = CryptoJsonFileHandler(file_path=filepath, crypter=crypter)
    psi = Psi(filehandler=filehandler)

    filepath_new_source = DATA_DIR / "thermal_bridge_44er.csv"
    psi.update_from_file(filepath=filepath_new_source)


if __name__ == '__main__':
    main()
