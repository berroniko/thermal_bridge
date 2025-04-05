from berroutils.plugins.file_handler import JsonFileHandler
from src.thermal_bridge.psi_data import Psi
from src import TEST_DATA_DIR


filepath = TEST_DATA_DIR / "test_psi_data.json"
filehandler = JsonFileHandler(file_path=filepath)


def test_update_from_csv():
    psi = Psi(filehandler=filehandler)
    filepath_new_source = TEST_DATA_DIR / "test_thermal_bridge.csv"
    psi.update_from_file(filepath=filepath_new_source)

    assert len(psi.data) == 14
