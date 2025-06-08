from berroutils.crypter import Crypter
from berroutils.plugins.file_handler import CryptoJsonFileHandler, JsonFileHandler

from src import DATA_DIR
from src.thermal_bridge.psi_data import Psi


def main():
    key = 'missing'

    filepath = DATA_DIR / "psi_data.enc"
    crypter = Crypter(key=key)
    filehandler = CryptoJsonFileHandler(file_path=filepath, crypter=crypter)
    psi = Psi(filehandler=filehandler)

    # filepath_new_source = DATA_DIR / "thermal_bridge_44er.csv"
    filepath_new_source = DATA_DIR / "Stand 06Juni25 adapted - 44er Wand.csv"
    psi.update_from_file(filepath=filepath_new_source)
    print("{len(psi.data)} entries")

def new_main():
    filepath = DATA_DIR / "psi_data_from_scratch.json"
    filehandler = JsonFileHandler(file_path=filepath)
    psi = Psi(filehandler=filehandler)

    # filepath_new_source = DATA_DIR / "thermal_bridge_44er.csv"
    filepath_new_source = DATA_DIR / "Stand 06Juni25 adapted - 44er Wand.csv"
    psi.update_from_file(filepath=filepath_new_source)
    print("{len(psi.data)} entries")

if __name__ == '__main__':
    main()
