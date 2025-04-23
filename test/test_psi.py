from berroutils.plugins.file_handler import JsonFileHandler

from src import TEST_DATA_DIR
from src.thermal_bridge.psi_data import Psi
from test.conftest import fp_psi_data


def test_update_from_csv(fp_psi_data):
    filehandler = JsonFileHandler(file_path=fp_psi_data)
    psi = Psi(filehandler=filehandler)
    filepath_new_source = TEST_DATA_DIR / "test_thermal_bridge.csv"
    psi.update_from_file(filepath=filepath_new_source)

    assert len(psi.data) == 14
