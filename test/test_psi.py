import pytest
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
    assert psi.data[0] == {'Bezeichnung'             : 'AW44-P-15KS(2,0)-160mm035-BP16(19)-060mm035US+FS-035_ohne '
                                                       'Foamglas+ohne SD',
                           'Datum'                   : '20.07.2017',
                           'Farbe'                   : 'light cyan',
                           'Name'                    : None,
                           'Nr.'                     : 1294.0,
                           'Psi-Wert'                : 0.2501,
                           'VHAG'                    : 'X',
                           'W&P'                     : None,
                           'Waermebruecke'           : 'Außenwand auf Bodenplatte (EG)',
                           'Zusatzinfo Waermebruecke': 'Erhöhte Terrasse (140mm028)',
                           'dichte'                  : None,
                           'dicke'                   : 160,
                           'ebz'                     : None,
                           'material'                : 'P',
                           'mit Referenzbauteil'     : None,
                           'staerke'                 : 'AW44',
                           'wlg'                     : '035'}


@pytest.mark.parametrize('bezeichnung, expected',
                         [('AW44-P-15KS(2,0)-160mm035-BP16(19)-060mm035US+FS-035_ohne Foamglas+ohne SD',
                           {'staerke': 'AW44', 'material': 'P', 'dichte': None, 'dicke': 160, 'wlg': '035'}),
                          ('AWEG44-15PPW4-120mm035-stark belüftet-AWKG30-Stb-200mm037-Stb.-D16(19)',
                           {'staerke': 'AWEG44', 'material': None, 'dichte': 'PPW4', 'dicke': 120, 'wlg': '035'}),
                          ('AW44-P-15PPW2-160mm032-Drempel-240mm032',
                           {'staerke': 'AW44', 'material': 'P', 'dichte': 'PPW2', 'dicke': 160, 'wlg': '032'}),
                          ('AW44-V-15PPW2-160mm032_Stb-D18(19)+120mm042_AWEG44V-15PPW2-160mm 032-AWKG an EG',
                           {'staerke': 'AW44', 'material': 'V', 'dichte': 'PPW2', 'dicke': 160, 'wlg': '032'}),
                          ('AW44-P-15PPW2-160mm032_Dach-280mm032(25°)_Ringanker17,5x20cm',
                           {'staerke': 'AW44', 'material': 'P', 'dichte': 'PPW2', 'dicke': 160, 'wlg': '032'}),
                          ('AW44-P-15PPW2-160mm032_Dach-360mm032',
                           {'staerke': 'AW44', 'material': 'P', 'dichte': 'PPW2', 'dicke': 160, 'wlg': '032'}),
                          ('Dach-240mm032+40mm032',
                           {'staerke': None, 'material': None, 'dichte': None, 'dicke': 240, 'wlg': '032'}),
                          ('AW44-V-15KS(2,0)-160mm032-BP18(19)-100mm036US+FS ohne SD_ohne Foamglas',
                           {'staerke': 'AW44', 'material': 'V', 'dichte': None, 'dicke': 160, 'wlg': '032'}),
                          ('KBL-240mm035+40mm032_Dach-220mm035+40mm032',
                           {'staerke': None, 'material': None, 'dichte': None, 'dicke': 240, 'wlg': '035'}),
                          ('KBL-240mm035-Dach-220mm035',
                           {'staerke': None, 'material': None, 'dichte': None, 'dicke': 240, 'wlg': '035'}),
                          ('KBL-280mm032-Dach-360mm032   SPB beheizt',
                           {'staerke': None, 'material': None, 'dichte': None, 'dicke': 280, 'wlg': '032'}),
                          ('Porenbetondecke an Steildach',
                           {'staerke': None, 'material': None, 'dichte': None, 'dicke': None, 'wlg': None}),
                          ('240PPW4-140mm032_Dach-240mm032',
                           {'staerke': None, 'material': None, 'dichte': 'PPW4', 'dicke': 140, 'wlg': '032'})])
def test_parse_bezeichnung(bezeichnung, expected):
    assert Psi._parse_bezeichnung(bezeichnung) == expected

# expression = "^(?P<staerke>[A-Z]+\d+)?(-?(?P<material>[A-Z])-)?(\d+(?P<dichte>[a-zA-Z]+\d))?(-(?P<dicke>\d+)mm(?P<wlg>\d+))?"
# gm
# "^(?P<staerke>[A-Z]+\d+)?(-(?P<material>[A-Z]))?(-?\d+(?P<dichte>[a-zA-Z]+\d))?(-(?P<dicke>\d+)mm(?P<wlg>\d+))?"
# gm
