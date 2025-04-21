from berroutils.container.list_of_dict_container import ListOfDictContainer
from math import isnan

from src.utils import is_nan, parse_date


class Psi(ListOfDictContainer):
    required_keys: set[str] = {'Waermebruecke', 'Bezeichnung', 'Psi-Wert', 'Datum'}
    alternative_keys: dict[str] = {'Wärmebrücke'                     : 'Waermebruecke',
                                   'Zusatzinfo W\u00e4rmebr\u00fccke': 'Zusatzinfo Waermebruecke', }

    # format: alternative_keys = {"alt_key": "unique_key"}

    def __str__(self):
        return 'psi'

    def _clean_data(self, data):
        cleaned = [elem for elem in data if not is_nan(elem.get('Bezeichnung'))]
        cleaned = []
        for elem in data:
            if is_nan(elem.get('Bezeichnung')):
                continue
            new_elem = elem.copy()
            datum = elem.get('Datum')
            if is_nan(datum):
                new_elem['Datum'] = None
            else:
                new_elem['Datum'] = parse_date(elem.get('Datum')).strftime("%Y-%m-%d")
            cleaned.append(new_elem)
        return cleaned
