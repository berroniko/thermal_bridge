from pathlib import Path

from src.berroutils.plugins.file_handler import JsonFileHandler
from src.thermal_bridge.psi_data import Psi

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def init_psi():
    filepath = DATA_DIR / "psi_data.json"
    filehandler = JsonFileHandler(file_path=filepath)
    return Psi(filehandler=filehandler)
