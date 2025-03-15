from src import DATA_DIR
from src.berroutils.plugins.file_handler import JsonFileHandler
from src.thermal_bridge.psi_data import Psi

filepath_storage = DATA_DIR / "psi_data.json"
filehandler = JsonFileHandler(file_path=filepath_storage)
psi = Psi(filehandler=filehandler)

filepath_new_source = DATA_DIR / "thermal_bridge_44er.csv"
psi.update_from_file(filepath=filepath_new_source)
