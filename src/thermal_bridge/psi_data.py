from src.berroutils.container.list_of_dict_container import ListOfDictContainer
from src.utils import is_nan


class Psi(ListOfDictContainer):
    required_keys: set[str] = {'Waermebruecke', 'Bezeichnung', 'Psi-Wert'}
    alternative_keys: dict[str] = {'Wärmebrücke': 'Waermebruecke'}

    # format: alternative_keys = {"alt_key": "unique_key"}

    def __str__(self):
        return 'psi'

    def _clean_data(self, data):
        cleaned = [elem for elem in data if not is_nan(elem.get('Bezeichnung'))]
        return cleaned
