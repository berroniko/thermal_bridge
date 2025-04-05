from pathlib import Path

from berroutils.plugins.file_handler import JsonFileHandler
from src.thermal_bridge.psi_data import Psi
from src import DATA_DIR


def init_psi():
    filepath = DATA_DIR / "psi_data.json"
    filehandler = JsonFileHandler(file_path=filepath)
    return Psi(filehandler=filehandler)
